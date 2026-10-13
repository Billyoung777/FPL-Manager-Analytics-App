from tracker.mini_league_tracker import get_mini_league
from database.league_repository import save_league, get_league


LEAGUE_IDS = [1701837, 1840079]


def sync_league(league_id):
    """
    Retrieve a mini-league from the FPL API
    and save its information in SQLite.
    """
    print(f"\nFetching FPL league {league_id}...")

    league_data = get_mini_league(league_id)

    league_info = league_data["league"]
    league_name = league_info["name"]

    save_league(
        league_id=league_id,
        league_name=league_name
    )

    print("League synchronized successfully.")

    return get_league(league_id)


def main():
    print("=" * 55)
    print("FPL MINI-LEAGUE DATABASE SYNCHRONIZATION")
    print("=" * 55)

    for league_id in LEAGUE_IDS:
        league = sync_league(league_id)

        print(f"League ID: {league['league_id']}")
        print(f"League Name: {league['league_name']}")
        print(f"Last Updated: {league['last_updated']}")

    print("\nDATABASE LEAGUE SYNC: COMPLETE")


if __name__ == "__main__":
    main()