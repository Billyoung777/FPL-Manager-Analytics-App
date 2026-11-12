
import unittest

from database.sync_recovery import build_recovery_plan


class TestSyncRecovery(unittest.TestCase):

    def test_incomplete_manager_queued_for_recovery(self):
        audit_report = {
            "season": "2026/27",
            "managers": [
                {
                    "manager_id": 1053858,
                    "status": "complete",
                    "missing_gameweeks": []
                },
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                }
            ]
        }

        result = build_recovery_plan(audit_report)

        self.assertEqual(result["season"], "2026/27")
        self.assertEqual(result["recovery_required"], 1)
        self.assertEqual(result["skipped"], 1)
        self.assertEqual(result["deferred"], 0)

        self.assertEqual(
            result["recovery_queue"],
            [
                {
                    "manager_id": 1234567,
                    "status": "incomplete",
                    "missing_gameweeks": [8, 9, 10]
                }
            ]
        )

        self.assertEqual(
            result["skipped_manager_ids"],
            [1053858]
        )


    def test_unsynchronized_manager_queued_for_recovery(self):
        audit_report = {
            "season": "2026/27",
            "managers": [
                {
                    "manager_id": 2000001,
                    "status": "not_synchronized",
                    "missing_gameweeks": [1, 2, 3, 4]
                }
            ]
        }

        result = build_recovery_plan(audit_report)

        self.assertEqual(result["recovery_required"], 1)
        self.assertEqual(result["skipped"], 0)
        self.assertEqual(result["deferred"], 0)

        self.assertEqual(
            result["recovery_queue"],
            [
                {
                    "manager_id": 2000001,
                    "status": "not_synchronized",
                    "missing_gameweeks": [1, 2, 3, 4]
                }
            ]
        )

        self.assertEqual(
            result["deferred_manager_ids"], []
        )

        self.assertEqual(
            result["skipped_manager_ids"], []
        )

    def test_unknown_manager_deferred(self):
        audit_report = {
            "season": "2026/27",
            "managers": [
                {
                    "manager_id": 3000001,
                    "status": "unknown",
                    "missing_gameweeks": []
                }
            ]
        }

        result = build_recovery_plan(audit_report)

        self.assertEqual(result["recovery_required"], 0)
        self.assertEqual(result["deferred"], 1)
        self.assertEqual(result["skipped"], 0)

        self.assertEqual(
            result["deferred_manager_ids"],
            [3000001]
        )

        self.assertEqual(
            result["recovery_queue"],
            []
        )

        self.assertEqual(
            result["skipped_manager_ids"],
            []
        )

if __name__ == "__main__":
    unittest.main()
