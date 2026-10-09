
from tracker.mini_league_tracker import get_mini_league
from tracker.manager_comparison import get_manager_history

LEAGUE_IDS = [1701837, 1840079]


def build_leaderboard(league_id):
    league_data = get_mini_league(league_id)

    league_name = league_data["league"]["name"]
    managers = league_data["standings"]["results"]

    leaderboard = []

    for manager in managers:
        history = get_manager_history(manager["entry"])

        net_points = [
            gw["points"] - gw["event_transfers_cost"]
            for gw in history
        ]

        total_points = sum(net_points)
        gameweeks = len(net_points)

        average_points = (
            total_points / gameweeks
            if gameweeks else 0
        )

        leaderboard.append({
            "manager_id": manager["entry"],
            "team_name": manager["entry_name"],
            "manager_name": manager["player_name"],
            "total_points": total_points,
            "average_points": round(average_points, 2),
            "gameweeks": gameweeks
        })

    leaderboard.sort(
        key=lambda manager: manager["total_points"],
        reverse=True
    )

    return league_name, leaderboard


def main():
    print("=" * 75)
    print("FPL MINI-LEAGUE LEADERBOARD")
    print("=" * 75)

    for league_id in LEAGUE_IDS:
        league_name, leaderboard = build_leaderboard(league_id)

        print(f"\nLeague: {league_name}")
        print("-" * 75)

        print(
            f"{'Rank':<6}"
            f"{'Team':<30}"
            f"{'Total':<10}"
            f"{'Avg/GW':<10}"
        )

        print("-" * 75)

        for rank, manager in enumerate(leaderboard, start=1):
            print(
                f"{rank:<6}"
                f"{manager['team_name'][:29]:<30}"
                f"{manager['total_points']:<10}"
                f"{manager['average_points']:<10.2f}"
            )


if __name__ == "__main__":
    main()
