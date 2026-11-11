
import unittest

from database.gameweek_status import (
    get_finished_gameweek_ids,
    get_verified_gameweek_ids
)


class TestGameweekStatusHelpers(unittest.TestCase):

    def setUp(self):
        self.statuses = [
            {"gameweek": 1, "finished": True, "verified": True},
            {"gameweek": 2, "finished": True, "verified": True},
            {"gameweek": 3, "finished": True, "verified": False},
            {"gameweek": 4, "finished": False, "verified": False}
        ]

    def test_finished_gameweeks(self):
        result = get_finished_gameweek_ids(self.statuses)
        self.assertEqual(result, [1, 2, 3])

    def test_verified_gameweeks(self):
        result = get_verified_gameweek_ids(self.statuses)
        self.assertEqual(result, [1, 2])

    def test_no_finished_gameweeks(self):
        statuses = [
            {"gameweek": 1, "finished": False, "verified": False}
        ]
        self.assertEqual(
            get_finished_gameweek_ids(statuses),
            []
        )


if __name__ == "__main__":
    unittest.main()

