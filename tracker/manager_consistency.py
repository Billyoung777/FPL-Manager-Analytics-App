
import statistics

from tracker.mini_league_tracker import get_mini_league
from tracker.manager_comparison import get_manager_history


LEAGUE_IDS = [1701837, 1840079]


def calculate_manager_consistency(league_id):
    league_data = get_mini_league(league_id)

    league_name = league_data["league"]["name"]
    managers = league_data["standings"]["results"]

    results = []

    for manager in managers:
        history = get_manager_history(manager["entry"])

        net_points = [
            gw["points"] - gw["event_transfers_cost"]
            for gw in history
        ]

        if not net_points:
            continue

        results.append({
            "manager_id": manager["entry"],
            "team_name": manager["entry_name"],
            "gameweeks": len(net_points),
            "average_points": statistics.mean(net_points),
            "best_gw": max(net_points),
            "worst_gw": min(net_points),
            "standard_deviation": statistics.pstdev(net_points)
        })

    # Lower standard deviation = more consistent scoring.
    results.sort(
        key=lambda manager: manager["standard_deviation"]
    )

    return league_name, results


def main():
    print("=" * 85)
    print("FPL MINI-LEAGUE MANAGER CONSISTENCY ANALYTICS")
    print("=" * 85)

    for league_id in LEAGUE_IDS:
        league_name, managers = calculate_manager_consistency(
            league_id
        )

        print(f"\nLeague: {league_name}")
        print("-" * 85)

        print(
            f"{'Team':<30}"
            f"{'Average':<12}"
            f"{'Best GW':<12}"
            f"{'Worst GW':<12}"
            f"{'Std Dev':<12}"
        )

        print("-" * 85)

        for manager in managers:
            print(
                f"{manager['team_name'][:29]:<30}"
                f"{manager['average_points']:<12.2f}"
                f"{manager['best_gw']:<12}"
                f"{manager['worst_gw']:<12}"
                f"{manager['standard_deviation']:<12.2f}"
            )


if __name__ == "__main__":
    main()
