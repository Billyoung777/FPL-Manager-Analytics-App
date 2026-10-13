
from database.db import get_connection
from database.sync_gameweeks import sync_gameweeks


SEASON = "2026/27"


def get_all_manager_ids():
    """
    Retrieve unique managers belonging to
    our tracked mini-leagues.
    """
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT DISTINCT manager_id
            FROM league_memberships
            ORDER BY manager_id
        """)

        return [row[0] for row in cursor.fetchall()]

    finally:
        connection.close()


def sync_all_gameweeks(season):
    """
    Synchronize historical gameweek performances
    for every tracked manager.
    """
    manager_ids = get_all_manager_ids()

    print(f"Managers found: {len(manager_ids)}")

    successful = 0
    failed = []

    for index, manager_id in enumerate(manager_ids, start=1):
        print(f"\n[{index}/{len(manager_ids)}] Manager {manager_id}")

        try:
            history = sync_gameweeks(manager_id, season)

            print(f"Stored gameweeks: {len(history)}")
            successful += 1

        except (RuntimeError, ValueError, KeyError) as error:
            print(f"Synchronization failed: {error}")
            failed.append(manager_id)

    print("\n" + "=" * 60)
    print("SYNCHRONIZATION SUMMARY")
    print("=" * 60)

    print(f"Managers processed: {len(manager_ids)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(failed)}")

    if failed:
        print(f"Failed manager IDs: {failed}")

    return successful, failed


def main():
    print("=" * 60)
    print("FPL ALL-MANAGER GAMEWEEK SYNCHRONIZATION")
    print("=" * 60)

    sync_all_gameweeks(SEASON)


if __name__ == "__main__":
    main()
