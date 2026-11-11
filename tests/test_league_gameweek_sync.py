
import unittest
from unittest.mock import patch

from database.league_gameweek_sync import (
    sync_league_gameweeks
)


class TestLeagueGameweekSync(unittest.TestCase):

    @patch("database.league_gameweek_sync.sync_gameweeks")
    @patch("database.league_gameweek_sync.get_league_members")
    def test_sync_all_members(
        self,
        mock_members,
        mock_sync
    ):
        mock_members.return_value = [
            {"manager_id": 1},
            {"manager_id": 2}
        ]

        mock_sync.return_value = [
            {"gameweek": 1},
            {"gameweek": 2}
        ]

        result = sync_league_gameweeks(
            100,
            "2026/27"
        )

        self.assertEqual(result["total_managers"], 2)
        self.assertEqual(result["successful"], 2)
        self.assertEqual(result["failed"], 0)

        self.assertEqual(mock_sync.call_count, 2)

    @patch("database.league_gameweek_sync.sync_gameweeks")
    @patch("database.league_gameweek_sync.get_league_members")
    def test_sync_continues_after_failure(
        self,
        mock_members,
        mock_sync
    ):
        mock_members.return_value = [
            {"manager_id": 1},
            {"manager_id": 2}
        ]

        mock_sync.side_effect = [
            RuntimeError("FPL API unavailable"),
            [{"gameweek": 1}]
        ]

        result = sync_league_gameweeks(
            100,
            "2026/27"
        )

        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(mock_sync.call_count, 2)


if __name__ == "__main__":
    unittest.main()
