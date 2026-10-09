
from tracker.mini_league_tracker import get_mini_league
from tracker.manager_comparison import get_manager_history

LEAGUE_IDS = [1701837, 1840079]


def find_gameweek_winners(league_id):
    league_data = get_mini_league(league_id)

    league_name = league_data["league"]["name"]
    managers = league_data["standings"]["results"]

    gameweek_results = {}

    for manager in managers:
        history = get_manager_history(manager["entry"])

        for gw in history:
            gameweek = gw["event"]

            net_points = (
                gw["points"] - gw["event_transfers_cost"]
            )

            result = {
                "team_name": manager["entry_name"],
                "manager_id": manager["entry"],
                "points": net_points
            }

            gameweek_results.setdefault(gameweek, []).append(result)

    winners = {}

    for gameweek, results in sorted(gameweek_results.items()):
        highest_points = max(
            result["points"] for result in results
        )

        # Preserve ties: multiple managers can win the same GW.
        winners[gameweek] = [
            result
            for result in results
            if result["points"] == highest_points
        ]

    return league_name, winners


def main():
    print("=" * 70)
    print("FPL MINI-LEAGUE GAMEWEEK WINNERS")
    print("=" * 70)

    for league_id in LEAGUE_IDS:
        league_name, winners = find_gameweek_winners(league_id)

        print(f"\nLeague: {league_name}")
        print("-" * 70)

        for gameweek, winning_managers in winners.items():
            for manager in winning_managers:
                print(
                    f"GW{gameweek}: "
                    f"{manager['team_name']} | "
                    f"{manager['points']} points"
                )


if __name__ == "__main__":
    main()
