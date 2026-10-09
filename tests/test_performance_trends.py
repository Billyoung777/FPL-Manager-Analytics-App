
from unittest.mock import patch

from tracker.performance_trends import calculate_performance_trend


mock_history = [
    {"event": 3, "points": 45, "event_transfers_cost": 4},
    {"event": 1, "points": 50, "event_transfers_cost": 0},
    {"event": 2, "points": 70, "event_transfers_cost": 4},
]


with patch(
    "tracker.performance_trends.get_manager_history",
    return_value=mock_history
):
    trend = calculate_performance_trend(123456)


assert len(trend) == 3

# Confirm gameweeks are ordered correctly.
assert [gw["gameweek"] for gw in trend] == [1, 2, 3]

# Net points: 50, 66, 41
assert [gw["net_points"] for gw in trend] == [50, 66, 41]

# Cumulative points: 50, 116, 157
assert [gw["cumulative_points"] for gw in trend] == [
    50, 116, 157
]

print("=" * 60)
print("PERFORMANCE TRENDS VALIDATION")
print("=" * 60)
print("Gameweek ordering: PASS")
print("Transfer deductions: PASS")
print("Cumulative points: PASS")
print("PERFORMANCE TRENDS VALIDATION: PASS")
