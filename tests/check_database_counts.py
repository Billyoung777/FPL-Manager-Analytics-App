
from database.db import get_connection


def check_database_counts():
    connection = get_connection()

    try:
        manager_count = connection.execute(
            "SELECT COUNT(*) FROM managers"
        ).fetchone()[0]

        league_count = connection.execute(
            "SELECT COUNT(*) FROM leagues"
        ).fetchone()[0]

        membership_count = connection.execute(
            "SELECT COUNT(*) FROM league_memberships"
        ).fetchone()[0]

        unique_members = connection.execute("""
            SELECT COUNT(DISTINCT manager_id)
            FROM league_memberships
        """).fetchone()[0]

        print("=" * 55)
        print("FPL DATABASE RECORD VERIFICATION")
        print("=" * 55)

        print(f"Total managers: {manager_count}")
        print(f"Total leagues: {league_count}")
        print(f"Total memberships: {membership_count}")
        print(f"Unique league members: {unique_members}")

        print("\nDATABASE RECORD VERIFICATION: COMPLETE")

    finally:
        connection.close()


if __name__ == "__main__":
    check_database_counts()
