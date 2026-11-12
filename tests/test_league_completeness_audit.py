
import unittest
from unittest.mock import patch

from database.league_completeness_audit import audit_selected_leagues


class TestLeagueCompletenessAudit(unittest.TestCase):

    @patch(
        "database.league_completeness_audit.get_manager_completeness"
    )
    @patch(
        "database.league_completeness_audit.get_league_members"
    )
    def test_shared_manager_audited_once(
        self,
        mock_members,
        mock_completeness
    ):
        mock_members.side_effect = [
            [
                {"manager_id": 1, "team_name": "Team A"},
                {"manager_id": 2, "team_name": "Team B"}
            ],
            [
                {"manager_id": 2, "team_name": "Team B"},
                {"manager_id": 3, "team_name": "Team C"}
            ]
        ]

        def completeness_result(manager_id, season, expected):
            return {
                "manager_id": manager_id,
                "status": "complete",
                "stored_count": 3,
                "expected_count": 3,
                "missing_gameweeks": []
            }

        mock_completeness.side_effect = completeness_result

        result = audit_selected_leagues(
            league_ids=[100, 200],
            season="2026/27",
            expected_gameweeks=[1, 2, 3]
        )

        self.assertEqual(result["total_unique_managers"], 3)
        self.assertEqual(result["summary"]["complete"], 3)
        self.assertEqual(len(result["managers"]), 3)

        self.assertEqual(mock_members.call_count, 2)
        self.assertEqual(mock_completeness.call_count, 3)


    @patch(
        "database.league_completeness_audit.get_manager_completeness"
    )
    @patch(
        "database.league_completeness_audit.get_league_members"
    )
    def test_incomplete_manager_detected(
        self,
        mock_members,
        mock_completeness
    ):
        mock_members.return_value = [
            {"manager_id": 1, "team_name": "Team A"},
            {"manager_id": 2, "team_name": "Team B"}
        ]

        mock_completeness.side_effect = [
            {
                "manager_id": 1,
                "status": "complete",
                "stored_count": 3,
                "expected_count": 3,
                "missing_gameweeks": []
            },
            {
                "manager_id": 2,
                "status": "incomplete",
                "stored_count": 2,
                "expected_count": 3,
                "missing_gameweeks": [2]
            }
        ]

        result = audit_selected_leagues(
            league_ids=[100],
            season="2026/27",
            expected_gameweeks=[1, 2, 3]
        )

        self.assertEqual(result["total_unique_managers"], 2)
        self.assertEqual(result["summary"]["complete"], 1)
        self.assertEqual(result["summary"]["incomplete"], 1)

        incomplete = [
            manager
            for manager in result["managers"]
            if manager["status"] == "incomplete"
        ]

        self.assertEqual(len(incomplete), 1)
        self.assertEqual(incomplete[0]["manager_id"], 2)
        self.assertEqual(incomplete[0]["missing_gameweeks"], [2])

    @patch(
        "database.league_completeness_audit.get_manager_completeness"
    )
    @patch(
        "database.league_completeness_audit.get_league_members"
    )
    def test_unsynchronized_manager_detected(
        self,
        mock_members,
        mock_completeness
    ):
        mock_members.return_value = [
            {
                "manager_id": 10,
                "team_name": "New Manager FC"
            }
        ]

        mock_completeness.return_value = {
            "manager_id": 10,
            "status": "not_synchronized",
            "stored_count": 0,
            "expected_count": 10,
            "missing_gameweeks": list(range(1, 11))
        }

        result = audit_selected_leagues(
            league_ids=[100],
            season="2026/27",
            expected_gameweeks=list(range(1, 11))
        )

        self.assertEqual(
            result["total_unique_managers"], 1
        )

        self.assertEqual(
            result["summary"]["not_synchronized"], 1
        )

        self.assertEqual(
            result["summary"]["complete"], 0
        )

        manager = result["managers"][0]

        self.assertEqual(
            manager["status"], "not_synchronized"
        )

        self.assertEqual(
            manager["stored_count"], 0
        )

        self.assertEqual(
            manager["missing_gameweeks"],
            list(range(1, 11))
        )

        mock_completeness.assert_called_once_with(
            10,
            "2026/27",
            list(range(1, 11))
        )

if __name__ == "__main__":
    unittest.main()
