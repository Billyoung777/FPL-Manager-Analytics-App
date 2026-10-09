
from tracker.manager_comparison import get_manager_history


def calculate_performance_trend(manager_id):
    history = get_manager_history(manager_id)

    trend = []
    cumulative_points = 0

    for gw in sorted(history, key=lambda item: item["event"]):
        net_points = (
            gw["points"] - gw["event_transfers_cost"]
        )

        cumulative_points += net_points

        trend.append({
            "gameweek": gw["event"],
            "net_points": net_points,
            "cumulative_points": cumulative_points
        })

    return trend


def main():
    manager_id = 1053858

    trend = calculate_performance_trend(manager_id)

    print("=" * 65)
    print("FPL MANAGER PERFORMANCE TRENDS")
    print("=" * 65)

    print(f"Manager ID: {manager_id}")
    print("-" * 65)

    print(
        f"{'GW':<8}"
        f"{'Net Points':<15}"
        f"{'Cumulative Points':<20}"
    )

    print("-" * 65)

    for result in trend:
        print(
            f"{result['gameweek']:<8}"
            f"{result['net_points']:<15}"
            f"{result['cumulative_points']:<20}"
        )


if __name__ == "__main__":
    main()
