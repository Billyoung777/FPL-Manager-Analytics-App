import requests
from tracker.mini_league_leaderboard import build_leaderboard
from tracker.gameweek_winners import find_gameweek_winners
from tracker.rank_movements import calculate_rank_movements
from tracker.manager_consistency import calculate_manager_consistency


LEAGUE_IDS = [1701837, 1840079]




def generate_season_summary(league_id):
    league_name, leaderboard = build_leaderboard(league_id)
    _, winners = find_gameweek_winners(league_id)
    _, rank_movements = calculate_rank_movements(league_id)
    _, consistency = calculate_manager_consistency(league_id)

    return {
        "league_id": league_id,
        "league_name": league_name,
        "leaderboard": leaderboard,
        "gameweek_winners": winners,
        "rank_movements": rank_movements,
        "consistency": consistency
    }



def main():
    print("=" * 75)
    print("FPL MINI-LEAGUE SEASON SUMMARY")
    print("=" * 75)


    for league_id in LEAGUE_IDS:
        try:
            summary = generate_season_summary(league_id)
        except requests.RequestException as error:
            print(
                f"\nLeague {league_id}: "
                f"Unable to retrieve season summary - {error}"
            )
            continue

        print(f"\nLeague: {summary['league_name']}")
        print("-" * 75)

        print("\nCURRENT LEADERBOARD")
        print("-" * 75)

        print(
            f"{'Rank':<6}"
            f"{'Team':<30}"
            f"{'Total':<12}"
            f"{'Average':<12}"
        )

        print("-" * 75)

        for rank, manager in enumerate(
            summary["leaderboard"], start=1
        ):
            print(
                f"{rank:<6}"
                f"{manager['team_name'][:29]:<30}"
                f"{manager['total_points']:<12}"
                f"{manager['average_points']:<12.2f}"
            )


        print("\nGAMEWEEK WINNERS")

        for gameweek, winners in summary["gameweek_winners"].items():
            for winner in winners:
                print(
                    f"GW{gameweek}: "
                    f"{winner['team_name']} "
                    f"({winner['points']} points)"
                )


        print("\nLATEST GAMEWEEK RANK MOVEMENTS")
        print("-" * 75)

        movements = summary["rank_movements"]

        if movements:
            latest_gw = max(movements)

            print(f"Gameweek {latest_gw}")

            for manager in movements[latest_gw]:
                change = manager["change"]

                if change is None:
                    movement = "FIRST GW"
                elif change > 0:
                    movement = f"UP {change}"
                elif change < 0:
                    movement = f"DOWN {abs(change)}"
                else:
                    movement = "UNCHANGED"

                print(
                    f"{manager['rank']:>2}. "
                    f"{manager['team_name']:<28} "
                    f"{movement}"
                )
        else:
            print("No completed gameweeks available.")


        print("\nMANAGER CONSISTENCY ANALYTICS")
        print("-" * 75)

        print(
            f"{'Team':<30}"
            f"{'Average':<12}"
            f"{'Best GW':<12}"
            f"{'Worst GW':<12}"
            f"{'Std Dev':<12}"
        )

        print("-" * 75)

        for manager in summary["consistency"]:
            print(
                f"{manager['team_name'][:29]:<30}"
                f"{manager['average_points']:<12.2f}"
                f"{manager['best_gw']:<12}"
                f"{manager['worst_gw']:<12}"
                f"{manager['standard_deviation']:<12.2f}"
            )


if __name__ == "__main__":
    main()
