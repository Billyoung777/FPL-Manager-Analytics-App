from database.db import get_connection


def check_tables():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = ?
            ORDER BY name
        """, ("table",))

        tables = [row[0] for row in cursor.fetchall()]

        print("=" * 50)
        print("FPL DATABASE TABLE VERIFICATION")
        print("=" * 50)

        for table in tables:
            print(f"[OK] {table}")

        expected_tables = {
            "managers",
            "leagues",
            "league_memberships",
            "gameweek_performances"
        }

        missing_tables = expected_tables - set(tables)

        if missing_tables:
            print(f"\nMissing tables: {sorted(missing_tables)}")
            print("DATABASE VERIFICATION: FAILED")
        else:
            print("\nDATABASE VERIFICATION: PASSED")
            print(f"Required tables found: {len(expected_tables)}")

    finally:
        connection.close()


if __name__ == "__main__":
    check_tables()
