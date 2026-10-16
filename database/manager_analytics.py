import statistics
from database.manager_repository import get_manager
from database.gameweek_repository import get_manager_gameweeks


MANAGER_ID = 1053858
SEASON = "2026/27"


def calculate_manager_analytics(manager_id, season):
    """
    Calculate manager performance using SQLite data.
    No FPL API requests are required.
    """

    manager = get_manager(manager_id)

    if manager is None:
        raise ValueError(f"Manager {manager_id} not found.")

    history = get_manager_gameweeks(manager_id, season)

    if not history:
        raise ValueError(
            f"No gameweek history for manager {manager_id}."
        )

    net_scores = [
        {
            "gameweek": gw["gameweek"],
            "points": gw["points"] - gw["transfer_cost"]
        }
        for gw in history
    ]

    total_points = sum(gw["points"] for gw in net_scores)
    average_points = total_points / len(net_scores)

    points_list = [gw["points"] for gw in net_scores]

    consistency_std = round(
        statistics.pstdev(points_list), 2
    )

    best_gw = max(net_scores, key=lambda gw: gw["points"])
    worst_gw = min(net_scores, key=lambda gw: gw["points"])

    # Calculate gameweek-to-gameweek performance changes
    performance_trends = []

    for index, gw in enumerate(net_scores):
        previous_points = (
            net_scores[index - 1]["points"]
            if index > 0
            else None
        )

        change = (
            gw["points"] - previous_points
            if previous_points is not None
            else None
        )

        performance_trends.append({
            "gameweek": gw["gameweek"],
            "points": gw["points"],
            "change": change
        })

    return {
        "manager_id": manager_id,
        "team_name": manager["team_name"],
        "season": season,
        "gameweeks": len(net_scores),
        "total_net_points": total_points,
        "average_points": round(average_points, 2),
        "consistency_std": consistency_std,
        "best_gameweek": best_gw,
        "worst_gameweek": worst_gw,
        "performance_trends": performance_trends
    }


def main():
    print("=" * 60)
    print("FPL DATABASE-POWERED MANAGER ANALYTICS")
    print("=" * 60)

    result = calculate_manager_analytics(MANAGER_ID, SEASON)

    print(f"Team: {result['team_name']}")
    print(f"Season: {result['season']}")
    print(f"Gameweeks: {result['gameweeks']}")
    print(f"Total Net Points: {result['total_net_points']}")
    print(f"Average Points: {result['average_points']}")

    best = result["best_gameweek"]
    worst = result["worst_gameweek"]

    print(
        f"Best Gameweek: GW{best['gameweek']} "
        f"({best['points']} points)"
    )

    print(
        f"Worst Gameweek: GW{worst['gameweek']} "
        f"({worst['points']} points)"
    )

    print("\nDATABASE ANALYTICS: COMPLETE")


if __name__ == "__main__":
    main()
