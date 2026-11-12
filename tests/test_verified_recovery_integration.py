
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
            self.recovery_plan
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
                self.recovery_plan
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
            self.recovery_plan
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
                self.recovery_plan
            )

        self.assertEqual(
            str(context.exception),
            "No verified gameweeks available for recovery"
        )

        mock_verified.assert_called_once_with()
        mock_recover.assert_not_called()

if __name__ == "__main__":
    unittest.main()
