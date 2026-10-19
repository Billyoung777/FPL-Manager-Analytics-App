
import unittest
from unittest.mock import patch, call

from tracker.mini_league_tracker import get_mini_league


class TestMiniLeaguePagination(unittest.TestCase):

    @patch("tracker.mini_league_tracker.FPLClient")
    def test_multiple_pages(self, mock_client):

        page_1 = {
            "league": {"name": "Test Mini-League"},
            "standings": {
                "results": [
                    {"entry": 101, "rank": 1},
                    {"entry": 102, "rank": 2}
                ],
                "has_next": True
            }
        }

        page_2 = {
            "league": {"name": "Test Mini-League"},
            "standings": {
                "results": [
                    {"entry": 103, "rank": 3}
                ],
                "has_next": False
            }
        }

        mock_client.return_value.get_league_standings.side_effect = [
            page_1,
            page_2
        ]

        result = get_mini_league(123456)

        managers = result["standings"]["results"]
        manager_ids = [manager["entry"] for manager in managers]

        self.assertEqual(manager_ids, [101, 102, 103])
        self.assertEqual(
            result["league"]["name"],
            "Test Mini-League"
        )

        self.assertEqual(
            mock_client.return_value.get_league_standings.call_args_list,
            [
                call(123456, 1),
                call(123456, 2)
            ]
        )


if __name__ == "__main__":
    unittest.main()
