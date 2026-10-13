
from tracker.mini_league_tracker import get_mini_league

from database.manager_repository import save_manager
from database.league_repository import save_league
from database.membership_repository import (
    save_membership,
    get_league_members
)


LEAGUE_IDS = [1701837, 1840079]


def sync_league_memberships(league_id):
    """
    Synchronize a mini-league and its managers
    into the local SQLite database.
    """
    print(f"\nFetching league {league_id}...")

    league_data = get_mini_league(league_id)

    league_info = league_data["league"]
    standings = league_data["standings"]["results"]

    save_league(
        league_id,
        league_info["name"]
    )

    for entry in standings:
        manager_id = entry["entry"]
        manager_name = entry["player_name"]
        team_name = entry["entry_name"]

        save_manager(
            manager_id,
            manager_name,
            team_name
        )

        save_membership(
            league_id,
            manager_id
        )

    members = get_league_members(league_id)

    print(f"League: {league_info['name']}")
    print(f"API members: {len(standings)}")
    print(f"Database members: {len(members)}")

    return members


def main():
    print("=" * 60)
    print("FPL LEAGUE MEMBERSHIP SYNCHRONIZATION")
    print("=" * 60)

    for league_id in LEAGUE_IDS:
        sync_league_memberships(league_id)

    print("\nMEMBERSHIP SYNCHRONIZATION: COMPLETE")


if __name__ == "__main__":
    main()
