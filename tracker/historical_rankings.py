
from tracker.mini_league_tracker import get_mini_league
from tracker.manager_comparison import get_manager_history

LEAGUE_IDS = [1701837, 1840079]


def calculate_historical_rankings(league_id):
    league_data = get_mini_league(league_id)

    league_name = league_data["league"]["name"]
    managers = league_data["standings"]["results"]

    gameweek_data = {}

    for manager in managers:
        history = get_manager_history(manager["entry"])

        cumulative_points = 0

        for gw in sorted(history, key=lambda item: item["event"]):
            net_points = (
                gw["points"] - gw["event_transfers_cost"]
            )

            cumulative_points += net_points

            gameweek_data.setdefault(gw["event"], []).append({
                "manager_id": manager["entry"],
                "team_name": manager["entry_name"],
                "cumulative_points": cumulative_points
            })

    rankings = {}

    for gameweek, results in sorted(gameweek_data.items()):
        results.sort(
            key=lambda manager: manager["cumulative_points"],
            reverse=True
        )

        for rank, manager in enumerate(results, start=1):
            manager["rank"] = rank

        rankings[gameweek] = results

    return league_name, rankings


def main():
    print("=" * 75)
    print("FPL MINI-LEAGUE HISTORICAL RANKINGS")
    print("=" * 75)

    for league_id in LEAGUE_IDS:
        league_name, rankings = calculate_historical_rankings(league_id)

        print(f"\nLeague: {league_name}")
        print("-" * 75)

        for gameweek, managers in rankings.items():
            print(f"\nGAMEWEEK {gameweek}")
            print(
                f"{'Rank':<6}"
                f"{'Team':<30}"
                f"{'Total Points':<15}"
            )
            print("-" * 55)

            for manager in managers:
                print(
                    f"{manager['rank']:<6}"
                    f"{manager['team_name'][:29]:<30}"
                    f"{manager['cumulative_points']:<15}"
                )


if __name__ == "__main__":
    main()
