
import unittest
from unittest.mock import patch

from database.sync_recovery_executor import (
    recover_verified_gameweeks
)


class TestVerifiedRecoveryIntegration(unittest.TestCase):

    def setUp(self):
        self.recovery_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1053858,
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

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_verified_snapshot_passed_to_executor(
        self,
        mock_verified,
        mock_recover
    ):
        mock_verified.return_value = [1, 2, 8, 9]
        mock_recover.return_value = {
            "successful": 2,
            "failed": 0
        }

        result = recover_verified_gameweeks(
            self.recovery_plan,
            allow_live="CONFIRM_LIVE_RECOVERY"
        )

        mock_verified.assert_called_once_with()

        mock_recover.assert_called_once_with(
            self.recovery_plan,
            verified_gameweeks=[1, 2, 8, 9]
        )

        self.assertEqual(
            result,
            {"successful": 2, "failed": 0}
        )

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_verification_api_failure_blocks_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        mock_verified.side_effect = RuntimeError(
            "FPL verification API unavailable"
        )

        with self.assertRaises(RuntimeError):
            recover_verified_gameweeks(
                self.recovery_plan,
                allow_live="CONFIRM_LIVE_RECOVERY"
            )

        mock_verified.assert_called_once_with()
        mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_verification_fetched_once_for_multiple_managers(
        self,
        mock_verified,
        mock_recover
    ):
        mock_verified.return_value = [1, 2, 8, 9]

        recover_verified_gameweeks(
            self.recovery_plan,
            allow_live="CONFIRM_LIVE_RECOVERY"
        )

        mock_verified.assert_called_once_with()
        mock_recover.assert_called_once_with(
            self.recovery_plan,
            verified_gameweeks=[1, 2, 8, 9]
        )


    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_empty_verification_snapshot_blocks_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        mock_verified.return_value = []

        with self.assertRaises(ValueError) as context:
            recover_verified_gameweeks(
                self.recovery_plan,
                allow_live="CONFIRM_LIVE_RECOVERY"
            )

        self.assertEqual(
            str(context.exception),
            "No verified gameweeks available for recovery"
        )

        mock_verified.assert_called_once_with()
        mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_malformed_verification_snapshot_blocks_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        invalid_snapshots = [
            ["8", 9],
            [None, 8],
            [True, 8],
            [0, 8],
            [39],
            "8,9",
            {"gameweek": 8},
            [8, 8]
        ]

        for snapshot in invalid_snapshots:
            with self.subTest(snapshot=snapshot):
                mock_verified.reset_mock()
                mock_recover.reset_mock()
                mock_verified.return_value = snapshot

                with self.assertRaises(ValueError) as context:
                    recover_verified_gameweeks(
                        self.recovery_plan,
                        allow_live="CONFIRM_LIVE_RECOVERY"
                    )

                self.assertEqual(
                    str(context.exception),
                    "Invalid verified gameweek snapshot"
                )

                mock_verified.assert_called_once_with()
                mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_live_recovery_requires_explicit_authorization(
        self,
        mock_verified,
        mock_recover
    ):
        for authorization in (None, False, True, 1, "yes"):
            with self.subTest(authorization=authorization):
                mock_verified.reset_mock()
                mock_recover.reset_mock()

                kwargs = (
                    {}
                    if authorization is None
                    else {"allow_live": authorization}
                )

                with self.assertRaises(PermissionError) as context:
                    recover_verified_gameweeks(
                        self.recovery_plan,
                        **kwargs
                    )

                self.assertEqual(
                    str(context.exception),
                    "Live recovery requires explicit authorization"
                )

                mock_verified.assert_not_called()
                mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_invalid_season_blocks_live_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        invalid_plan = {
            "season": "invalid-season",
            "recovery_queue": [
                {
                    "manager_id": 1053858,
                    "missing_gameweeks": [8, 9]
                }
            ]
        }

        with self.assertRaises(ValueError) as context:
            recover_verified_gameweeks(
                invalid_plan,
                allow_live="CONFIRM_LIVE_RECOVERY"
            )

        self.assertEqual(
            str(context.exception),
            "Invalid recovery season"
        )

        mock_verified.assert_not_called()
        mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_invalid_recovery_queue_blocks_live_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        invalid_queues = [
            None,
            "invalid",
            {},
            [None],
            ["invalid"],
            [{"manager_id": 1053858}],
            [{"missing_gameweeks": [8, 9]}]
        ]

        for queue in invalid_queues:
            with self.subTest(queue=queue):
                mock_verified.reset_mock()
                mock_recover.reset_mock()

                invalid_plan = {
                    "season": "2026/27",
                    "recovery_queue": queue
                }

                with self.assertRaises(ValueError) as context:
                    recover_verified_gameweeks(
                        invalid_plan,
                        allow_live="CONFIRM_LIVE_RECOVERY"
                    )

                self.assertEqual(
                    str(context.exception),
                    "Invalid recovery queue"
                )

                mock_verified.assert_not_called()
                mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_invalid_manager_ids_block_live_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        invalid_manager_ids = [
            None,
            0,
            -1,
            "1053858",
            True,
            1.5
        ]

        for manager_id in invalid_manager_ids:
            with self.subTest(manager_id=manager_id):
                mock_verified.reset_mock()
                mock_recover.reset_mock()

                invalid_plan = {
                    "season": "2026/27",
                    "recovery_queue": [
                        {
                            "manager_id": manager_id,
                            "missing_gameweeks": [8, 9]
                        }
                    ]
                }

                with self.assertRaises(ValueError) as context:
                    recover_verified_gameweeks(
                        invalid_plan,
                        allow_live="CONFIRM_LIVE_RECOVERY"
                    )

                self.assertEqual(
                    str(context.exception),
                    "Invalid recovery manager ID"
                )

                mock_verified.assert_not_called()
                mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_duplicate_manager_ids_block_live_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        duplicate_plan = {
            "season": "2026/27",
            "recovery_queue": [
                {
                    "manager_id": 1053858,
                    "missing_gameweeks": [8]
                },
                {
                    "manager_id": 1053858,
                    "missing_gameweeks": [9]
                }
            ]
        }

        with self.assertRaises(ValueError) as context:
            recover_verified_gameweeks(
                duplicate_plan,
                allow_live="CONFIRM_LIVE_RECOVERY"
            )

        self.assertEqual(
            str(context.exception),
            "Duplicate manager ID in recovery queue"
        )

        mock_verified.assert_not_called()
        mock_recover.assert_not_called()

    @patch(
        "database.sync_recovery_executor.recover_missing_gameweeks"
    )
    @patch(
        "database.sync_recovery_executor.get_verified_gameweek_ids"
    )
    def test_invalid_gameweeks_block_live_recovery(
        self,
        mock_verified,
        mock_recover
    ):
        invalid_gameweeks = [
            None,
            [],
            "8,9",
            {},
            [0],
            [39],
            [-1],
            ["8"],
            [None],
            [True],
            [8.5],
            [8, 8]
        ]

        for gameweeks in invalid_gameweeks:
            with self.subTest(gameweeks=gameweeks):
                mock_verified.reset_mock()
                mock_recover.reset_mock()

                invalid_plan = {
                    "season": "2026/27",
                    "recovery_queue": [
                        {
                            "manager_id": 1053858,
                            "missing_gameweeks": gameweeks
                        }
                    ]
                }

                with self.assertRaises(ValueError) as context:
                    recover_verified_gameweeks(
                        invalid_plan,
                        allow_live="CONFIRM_LIVE_RECOVERY"
                    )

                self.assertEqual(
                    str(context.exception),
                    "Invalid recovery gameweeks"
                )

                mock_verified.assert_not_called()
                mock_recover.assert_not_called()

if __name__ == "__main__":
    unittest.main()
