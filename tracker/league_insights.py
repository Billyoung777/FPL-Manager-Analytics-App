
from tracker.rank_movements import calculate_rank_movements

LEAGUE_IDS = [1701837, 1840079]


def calculate_league_insights(league_id):
    league_name, movements = calculate_rank_movements(league_id)

    insights = {}

    for gameweek, managers in sorted(movements.items()):
        climbers = [
            manager for manager in managers
            if manager["change"] is not None
            and manager["change"] > 0
        ]

        fallers = [
            manager for manager in managers
            if manager["change"] is not None
            and manager["change"] < 0
        ]

        biggest_climb = max(
            (manager["change"] for manager in climbers),
            default=0
        )

        biggest_drop = min(
            (manager["change"] for manager in fallers),
            default=0
        )

        insights[gameweek] = {
            "biggest_climbers": [
                manager for manager in climbers
                if manager["change"] == biggest_climb
            ],
            "biggest_fallers": [
                manager for manager in fallers
                if manager["change"] == biggest_drop
            ]
        }

    return league_name, insights


def main():
    print("=" * 70)
    print("FPL MINI-LEAGUE INSIGHTS")
    print("=" * 70)

    for league_id in LEAGUE_IDS:
        league_name, insights = calculate_league_insights(league_id)

        print(f"\nLeague: {league_name}")
        print("-" * 70)

        for gameweek, result in insights.items():
            print(f"\nGAMEWEEK {gameweek}")

            if gameweek == min(insights):
                print("First gameweek - no previous rankings")
                continue

            if result["biggest_climbers"]:
                print("BIGGEST CLIMBER(S):")
                for manager in result["biggest_climbers"]:
                    print(
                        f"  {manager['team_name']} "
                        f"(UP {manager['change']})"
                    )
            else:
                print("No upward movements")

            if result["biggest_fallers"]:
                print("BIGGEST FALLER(S):")
                for manager in result["biggest_fallers"]:
                    print(
                        f"  {manager['team_name']} "
                        f"(DOWN {abs(manager['change'])})"
                    )
            else:
                print("No downward movements")


if __name__ == "__main__":
    main()
