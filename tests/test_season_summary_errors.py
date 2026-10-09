
import io
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


output = io.StringIO()

with patch(
    "tracker.season_summary.generate_season_summary",
    side_effect=mock_generate_summary
):
    with redirect_stdout(output):
        season_summary.main()


result = output.getvalue()

assert "League 1701837:" in result
assert "Connection timed out" in result
assert "League: Kasi Football League" in result
assert "CURRENT LEADERBOARD" in result
assert "MANAGER CONSISTENCY ANALYTICS" in result

print("=" * 60)
print("SEASON SUMMARY ERROR HANDLING TEST")
print("=" * 60)
print("API timeout detected: PASS")
print("Error message displayed: PASS")
print("Second league processed: PASS")
print("Report continues after failure: PASS")
print("SEASON SUMMARY ERROR HANDLING: PASS")
