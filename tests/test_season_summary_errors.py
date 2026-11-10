import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import requests

from tracker import season_summary


def mock_generate_summary(league_id):
    if league_id == 1701837:
        raise requests.exceptions.Timeout("Connection timed out")

    return {
        "league_id": league_id,
        "league_name": "Kasi Football League",
        "leaderboard": [],
        "gameweek_winners": {},
        "rank_movements": {},
        "consistency": []
    }


class TestSeasonSummaryErrors(unittest.TestCase):

    def test_api_timeout_does_not_stop_reporting(self):
        output = io.StringIO()

        with patch(
            "tracker.season_summary.generate_season_summary",
            side_effect=mock_generate_summary
        ):
            with redirect_stdout(output):
                season_summary.main()

        result = output.getvalue()

        # Confirm the failed league is reported.
        self.assertIn("League 1701837:", result)
        self.assertIn("Connection timed out", result)

        # Confirm the next league is processed.
        self.assertIn("League: Kasi Football League", result)

        # Confirm reporting continues after the timeout.
        self.assertIn("CURRENT LEADERBOARD", result)
        self.assertIn(
            "MANAGER CONSISTENCY ANALYTICS",
            result
        )


if __name__ == "__main__":
    unittest.main()
