import unittest
from unittest.mock import patch
from tracker.head_to_head import get_head_to_head_histories

from tracker.head_to_head import (
    compare_gameweeks,
    calculate_h2h_record,
    calculate_manager_statistics,
    filter_completed_gameweeks,
)


class TestHeadToHead(unittest.TestCase):

    def setUp(self):
        self.history_a = [
            {"event": 1, "points": 60, "event_transfers_cost": 0},
            {"event": 2, "points": 75, "event_transfers_cost": 4},
            {"event": 3, "points": 50, "event_transfers_cost": 0},
        ]

        self.history_b = [
            {"event": 1, "points": 55, "event_transfers_cost": 0},
            {"event": 2, "points": 80, "event_transfers_cost": 0},
            {"event": 3, "points": 50, "event_transfers_cost": 0},
        ]

    def test_gameweek_comparison(self):
        results = compare_gameweeks(
            self.history_a,
            self.history_b
        )

        self.assertEqual(len(results), 3)

        self.assertEqual(
            [result["winner"] for result in results],
            ["A", "B", "TIE"]
        )

        # GW2 deducts the four-point transfer hit.
        self.assertEqual(results[1]["manager_a_points"], 71)

    def test_h2h_record(self):
        results = compare_gameweeks(
            self.history_a,
            self.history_b
        )

        record = calculate_h2h_record(results)

        self.assertEqual(record["manager_a_wins"], 1)
        self.assertEqual(record["manager_b_wins"], 1)
        self.assertEqual(record["ties"], 1)
        self.assertEqual(record["gameweeks_compared"], 3)

    def test_manager_statistics(self):
        stats = calculate_manager_statistics(
            self.history_a
        )

        self.assertEqual(stats["total_points"], 181)
        self.assertEqual(stats["average_points"], 60.33)
        self.assertEqual(stats["best_gw"]["gameweek"], 2)
        self.assertEqual(stats["worst_gw"]["gameweek"], 3)
        self.assertEqual(stats["gameweeks"], 3)

    def test_completed_gameweek_filter(self):
        mock_bootstrap = {
            "events": [
                {"id": 1, "finished": True, "data_checked": True},
                {"id": 2, "finished": True, "data_checked": True},
                {"id": 3, "finished": True, "data_checked": False},
            ]
        }

        with patch("tracker.head_to_head.FPLClient") as mock_client:
            mock_client.return_value.get.return_value = mock_bootstrap

            filtered_a, filtered_b = filter_completed_gameweeks(
                self.history_a,
                self.history_b
            )

        self.assertEqual(len(filtered_a), 2)
        self.assertEqual(len(filtered_b), 2)
        self.assertEqual(
            [gw["event"] for gw in filtered_a],
            [1, 2]
        )

    def test_empty_history(self):
        self.assertIsNone(
            calculate_manager_statistics([])
        )

        self.assertEqual(
            compare_gameweeks([], self.history_b),
            []
        )

    def test_manager_history_api_failure(self):
        """
        Verify that an API failure is not silently ignored.
        """

        with patch(
            "tracker.head_to_head.get_manager_history"
        ) as mock_history:

            mock_history.side_effect = RuntimeError(
                "FPL API connection failed"
            )

            with self.assertRaisesRegex(
                RuntimeError,
                "FPL API connection failed"
            ):
                get_head_to_head_histories(
                    1053858,
                    953118
                )


    def test_provisional_mode_includes_all_gameweeks(self):
        with patch("tracker.head_to_head.FPLClient") as mock_client:
            filtered_a, filtered_b = filter_completed_gameweeks(
                self.history_a,
                self.history_b,
                include_provisional=True
            )

            mock_client.assert_not_called()

        self.assertEqual(len(filtered_a), 3)
        self.assertEqual(len(filtered_b), 3)

    def test_verified_mode_excludes_unchecked_gameweeks(self):
        mock_bootstrap = {
            "events": [
                {"id": 1, "finished": True, "data_checked": True},
                {"id": 2, "finished": True, "data_checked": True},
                {"id": 3, "finished": False, "data_checked": False},
            ]
        }

        with patch("tracker.head_to_head.FPLClient") as mock_client:
            mock_client.return_value.get.return_value = mock_bootstrap

            filtered_a, filtered_b = filter_completed_gameweeks(
                self.history_a,
                self.history_b,
                include_provisional=False
            )

        self.assertEqual(
            [gw["event"] for gw in filtered_a],
            [1, 2]
        )
        self.assertEqual(
            [gw["event"] for gw in filtered_b],
            [1, 2]
        )


if __name__ == "__main__":
    unittest.main()

