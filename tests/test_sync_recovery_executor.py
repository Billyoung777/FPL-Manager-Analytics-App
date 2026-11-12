from unittest.mock import patch
import unittest

from database.sync_recovery_executor import (
    execute_recovery_plan,
    recover_missing_gameweeks
)


class TestSyncRecoveryExecutor(unittest.TestCase):

    def test_dry_run_previews_recovery_queue(self):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                },
                {
                    "manager_id": 2000001,
                    "status": "not_synchronized",
                    "missing_gameweeks": [1, 2, 3]
                }
            ]
        }

        result = execute_recovery_plan(
            recovery_plan,
            dry_run=True
        )

        self.assertTrue(result["dry_run"])
        self.assertEqual(result["season"], "2026/27")
        self.assertEqual(result["total_queued"], 2)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1234567,
                    "status": "planned",
                    "missing_gameweeks": [8, 9, 10]
                },
                {
                    "manager_id": 2000001,
                    "status": "planned",
                    "missing_gameweeks": [1, 2, 3]
                }
            ]
        )


    def test_live_execution_is_disabled(self):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                }
            ]
        }

        with self.assertRaisesRegex(
            NotImplementedError,
            "Live recovery execution is not enabled yet"
        ):
            execute_recovery_plan(
                recovery_plan,
                dry_run=False
            )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_successful_gameweek_recovery(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                }
            ]
        }

        mock_get_gameweeks.return_value = [
            {"gameweek": 1},
            {"gameweek": 2},
            {"gameweek": 8},
            {"gameweek": 9},
            {"gameweek": 10}
        ]

        result = recover_missing_gameweeks(
            recovery_plan,
            verified_gameweeks=[8, 9, 10]
        )

        mock_sync.assert_called_once_with(
            1234567,
            "2026/27",
            completed_gameweeks=[8, 9, 10]
        )
        mock_get_gameweeks.assert_called_once_with(
            1234567,
            "2026/27"
        )

        self.assertEqual(result["total_queued"], 1)
        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 0)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1234567,
                    "status": "recovered",
                    "missing_gameweeks": []
                }
            ]
        )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_partial_gameweek_recovery(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                }
            ]
        }

        # Simulate a synchronization that returns
        # GW8 and GW9 but not GW10.
        mock_get_gameweeks.return_value = [
            {"gameweek": 1},
            {"gameweek": 2},
            {"gameweek": 8},
            {"gameweek": 9}
        ]

        result = recover_missing_gameweeks(
            recovery_plan,
            verified_gameweeks=[8, 9, 10]
        )

        mock_sync.assert_called_once_with(
            1234567,
            "2026/27",
            completed_gameweeks=[8, 9, 10]
        )
        mock_get_gameweeks.assert_called_once_with(
            1234567,
            "2026/27"
        )

        self.assertEqual(result["total_queued"], 1)
        self.assertEqual(result["successful"], 0)
        self.assertEqual(result["failed"], 1)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [10]
                }
            ]
        )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_api_failure_does_not_stop_other_managers(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9]
                },
                {
                    "manager_id": 2000001,
                    "status": "not_synchronized",
                    "missing_gameweeks": [1, 2]
                }
            ]
        }

        mock_sync.side_effect = [
            RuntimeError("FPL API unavailable"),
            None
        ]

        mock_get_gameweeks.return_value = [
            {"gameweek": 1},
            {"gameweek": 2}
        ]

        result = recover_missing_gameweeks(
            recovery_plan,
            verified_gameweeks=[1, 2, 8, 9]
        )

        self.assertEqual(mock_sync.call_count, 2)
        mock_get_gameweeks.assert_called_once_with(
            2000001,
            "2026/27"
        )
        self.assertEqual(result["total_queued"], 2)
        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 1)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1234567,
                    "status": "failed",
                    "error": "FPL API unavailable"
                },
                {
                    "manager_id": 2000001,
                    "status": "recovered",
                    "missing_gameweeks": []
                }
            ]
        )

    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_empty_missing_gameweeks_rejected(self, mock_sync):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1053858,
                    "status": "incomplete",
                    "missing_gameweeks": []
                }
            ]
        }

        result = recover_missing_gameweeks(
            recovery_plan
        )

        # No synchronization should be attempted.
        mock_sync.assert_not_called()

        self.assertEqual(result["total_queued"], 1)
        self.assertEqual(result["successful"], 0)
        self.assertEqual(result["failed"], 1)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1053858,
                    "status": "invalid",
                    "error": "No missing gameweeks specified"
                }
            ]
        )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_sqlite_verification_detects_missing_records(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                }
            ]
        }

        # Synchronization completes without raising an error.
        mock_sync.return_value = [
            {"gameweek": 8},
            {"gameweek": 9},
            {"gameweek": 10}
        ]

        # But SQLite only contains GW8 and GW9.
        mock_get_gameweeks.return_value = [
            {"gameweek": 1},
            {"gameweek": 2},
            {"gameweek": 8},
            {"gameweek": 9}
        ]

        result = recover_missing_gameweeks(
            recovery_plan,
            verified_gameweeks=[8, 9, 10]
        )

        mock_sync.assert_called_once_with(
            1234567,
            "2026/27",
            completed_gameweeks=[8, 9, 10]
        )

        mock_get_gameweeks.assert_called_once_with(
            1234567,
            "2026/27"
        )

        self.assertEqual(result["total_queued"], 1)
        self.assertEqual(result["successful"], 0)
        self.assertEqual(result["failed"], 1)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [10]
                }
            ]
        )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_duplicate_manager_recovery_rejected(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1053858,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9]
                },
                {
                    "manager_id": 1053858,
                    "status": "incomplete",
                    "missing_gameweeks": [10]
                }
            ]
        }

        # SQLite confirms the first recovery succeeded.
        mock_get_gameweeks.return_value = [
            {"gameweek": 8},
            {"gameweek": 9}
        ]

        result = recover_missing_gameweeks(
            recovery_plan,
            verified_gameweeks=[8, 9, 10]
        )

        # Only the first occurrence should synchronize.
        mock_sync.assert_called_once_with(
            1053858,
            "2026/27",
            completed_gameweeks=[8, 9]
        )

        mock_get_gameweeks.assert_called_once_with(
            1053858,
            "2026/27"
        )

        self.assertEqual(result["total_queued"], 2)
        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 1)

        self.assertEqual(
            result["managers"],
            [
                {
                    "manager_id": 1053858,
                    "status": "recovered",
                    "missing_gameweeks": []
                },
                {
                    "manager_id": 1053858,
                    "status": "invalid",
                    "error": "Duplicate manager in recovery queue"
                }
            ]
        )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_invalid_manager_ids_rejected(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        invalid_ids = [
            0,
            -10,
            "abc",
            None,
            True
        ]

        for invalid_id in invalid_ids:
            with self.subTest(manager_id=invalid_id):
                mock_sync.reset_mock()
                mock_get_gameweeks.reset_mock()

                recovery_plan = {
                    "season": "2026/27",
                    "recovery_queue": [
                        {
                            "manager_id": invalid_id,
                            "status": "incomplete",
                            "missing_gameweeks": [8, 9]
                        }
                    ]
                }

                result = recover_missing_gameweeks(
                    recovery_plan
                )

                # Invalid IDs must never trigger synchronization.
                mock_sync.assert_not_called()

                # Invalid IDs must never query SQLite.
                mock_get_gameweeks.assert_not_called()

                self.assertEqual(
                    result["total_queued"],
                    1
                )

                self.assertEqual(
                    result["successful"],
                    0
                )

                self.assertEqual(
                    result["failed"],
                    1
                )

                self.assertEqual(
                    result["managers"],
                    [
                        {
                            "manager_id": invalid_id,
                            "status": "invalid",
                            "error": (
                                "Manager ID must be a positive integer"
                            )
                        }
                    ]
                )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_invalid_gameweek_numbers_rejected(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        invalid_gameweeks = [
            [0],
            [39],
            [-1],
            ["10"],
            [None],
            [True],
            [8, "9"]
        ]

        for gameweeks in invalid_gameweeks:
            with self.subTest(gameweeks=gameweeks):
                mock_sync.reset_mock()
                mock_get_gameweeks.reset_mock()

                recovery_plan = {
                    "season": "2026/27",
                    "recovery_queue": [
                        {
                            "manager_id": 1053858,
                            "status": "incomplete",
                            "missing_gameweeks": gameweeks
                        }
                    ]
                }

                result = recover_missing_gameweeks(
                    recovery_plan,
                    verified_gameweeks=list(range(1, 39))
                )

                mock_sync.assert_not_called()
                mock_get_gameweeks.assert_not_called()

                self.assertEqual(
                    result["total_queued"],
                    1
                )
                self.assertEqual(
                    result["successful"],
                    0
                )
                self.assertEqual(
                    result["failed"],
                    1
                )
                self.assertEqual(
                    result["managers"],
                    [{
                        "manager_id": 1053858,
                        "status": "invalid",
                        "error": (
                            "Gameweeks must be integers "
                            "between 1 and 38"
                        )
                    }]
                )

    @patch("database.sync_recovery_executor.get_manager_gameweeks")
    @patch("database.sync_recovery_executor.sync_gameweeks")
    def test_unverified_gameweeks_rejected(
        self,
        mock_sync,
        mock_get_gameweeks
    ):
        scenarios = [
            {
                "name": "verification_unavailable",
                "requested": [8, 9],
                "verified": None,
                "expected": {
                    "manager_id": 1053858,
                    "status": "invalid",
                    "error": "Verified gameweek data is required"
                }
            },
            {
                "name": "unverified_gameweek",
                "requested": [11],
                "verified": [1, 2, 8, 9, 10],
                "expected": {
                    "manager_id": 1053858,
                    "status": "invalid",
                    "error": "Unverified gameweeks cannot be recovered",
                    "unverified_gameweeks": [11]
                }
            },
            {
                "name": "mixed_verification",
                "requested": [8, 9, 11],
                "verified": [8, 9, 10],
                "expected": {
                    "manager_id": 1053858,
                    "status": "invalid",
                    "error": "Unverified gameweeks cannot be recovered",
                    "unverified_gameweeks": [11]
                }
            }
        ]

        for scenario in scenarios:
            with self.subTest(name=scenario["name"]):
                mock_sync.reset_mock()
                mock_get_gameweeks.reset_mock()

                recovery_plan = {
                    "season": "2026/27",
                    "recovery_queue": [
                        {
                            "manager_id": 1053858,
                            "status": "incomplete",
                            "missing_gameweeks": scenario["requested"]
                        }
                    ]
                }

                result = recover_missing_gameweeks(
                    recovery_plan,
                    verified_gameweeks=scenario["verified"]
                )

                mock_sync.assert_not_called()
                mock_get_gameweeks.assert_not_called()

                self.assertEqual(result["total_queued"], 1)
                self.assertEqual(result["successful"], 0)
                self.assertEqual(result["failed"], 1)
                self.assertEqual(
                    result["managers"],
                    [scenario["expected"]]
                )

if __name__ == "__main__":
    unittest.main()
