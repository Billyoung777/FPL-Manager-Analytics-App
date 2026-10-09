
from tracker.historical_rankings import calculate_historical_rankings

LEAGUE_IDS = [1701837, 1840079]


def calculate_rank_movements(league_id):
    league_name, rankings = calculate_historical_rankings(league_id)

    movements = {}
    previous_ranks = {}

    for gameweek, managers in sorted(rankings.items()):
        gameweek_movements = []

        for manager in managers:
            manager_id = manager["manager_id"]
            current_rank = manager["rank"]
            previous_rank = previous_ranks.get(manager_id)

            if previous_rank is None:
                change = None
            else:
                change = previous_rank - current_rank

            gameweek_movements.append({
                "manager_id": manager_id,
                "team_name": manager["team_name"],
                "rank": current_rank,
                "previous_rank": previous_rank,
                "change": change
            })

            previous_ranks[manager_id] = current_rank

        movements[gameweek] = gameweek_movements

    return league_name, movements


def main():
    print("=" * 70)
    print("FPL MINI-LEAGUE RANK MOVEMENTS")
    print("=" * 70)

    for league_id in LEAGUE_IDS:
        league_name, movements = calculate_rank_movements(league_id)

        print(f"\nLeague: {league_name}")
        print("-" * 70)

        for gameweek, managers in movements.items():
            print(f"\nGAMEWEEK {gameweek}")

            for manager in managers:
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


if __name__ == "__main__":
    main()
