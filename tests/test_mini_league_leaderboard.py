
from unittest.mock import patch

from tracker.mini_league_leaderboard import build_leaderboard


def make_history(points, costs):
    history = []

    for gw, (score, cost) in enumerate(zip(points, costs), start=1):
        history.append({
            "event": gw,
            "points": score,
            "event_transfers_cost": cost
        })

    return history


mock_league = {
    "league": {"name": "Test League"},
    "standings": {
        "results": [
            {
                "entry": 101,
                "entry_name": "Team A",
                "player_name": "Manager A"
            },
            {
                "entry": 102,
                "entry_name": "Team B",
                "player_name": "Manager B"
            }
        ]
    }
}

mock_histories = {
    101: make_history([50, 60, 70], [0, 4, 0]),
    102: make_history([55, 65, 75], [0, 0, 0])
}


with patch(
    "tracker.mini_league_leaderboard.get_mini_league",
    return_value=mock_league
), patch(
    "tracker.mini_league_leaderboard.get_manager_history",
    side_effect=lambda manager_id: mock_histories[manager_id]
):
    league_name, leaderboard = build_leaderboard(123456)


assert league_name == "Test League"
assert len(leaderboard) == 2

# Team B: 55 + 65 + 75 = 195
assert leaderboard[0]["team_name"] == "Team B"
assert leaderboard[0]["total_points"] == 195
assert leaderboard[0]["average_points"] == 65.0

# Team A: 50 + (60 - 4) + 70 = 176
assert leaderboard[1]["team_name"] == "Team A"
assert leaderboard[1]["total_points"] == 176
assert leaderboard[1]["average_points"] == round(176 / 3, 2)

print("=" * 60)
print("MINI-LEAGUE LEADERBOARD VALIDATION")
print("=" * 60)
print("Ranking order: PASS")
print("Transfer deductions: PASS")
print("Total points: PASS")
print("Average points: PASS")
print("LEADERBOARD VALIDATION: PASS")
