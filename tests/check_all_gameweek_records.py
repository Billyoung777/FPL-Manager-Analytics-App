
from database.db import get_connection


SEASON = "2026/27"


def check_gameweek_records():
    connection = get_connection()

    try:
        print("=" * 65)
        print("FPL HISTORICAL GAMEWEEK DATABASE VERIFICATION")
        print("=" * 65)

        cursor = connection.execute("""
            SELECT
                m.manager_id,
                m.team_name,
                COUNT(DISTINCT g.gameweek) AS gameweeks
            FROM managers AS m

            JOIN league_memberships AS lm
                ON m.manager_id = lm.manager_id

            LEFT JOIN gameweek_performances AS g
                ON m.manager_id = g.manager_id
                AND g.season = ?

            GROUP BY m.manager_id, m.team_name
            ORDER BY m.manager_id
        """, (SEASON,))

        rows = cursor.fetchall()

        expected_gameweeks = 6

        for manager_id, team_name, count in rows:
            status = (
                "OK" if count == expected_gameweeks
                else "CHECK"
            )

            print(
                f"{manager_id} | "
                f"{team_name} | "
                f"Gameweeks: {count} | "
                f"{status}"
            )

        total_records = connection.execute("""
            SELECT COUNT(*)
            FROM gameweek_performances
            WHERE season = ?
        """, (SEASON,)).fetchone()[0]

        print("-" * 65)
        print(f"Managers checked: {len(rows)}")
        print(f"Total gameweek records: {total_records}")

        if (
            len(rows) == 12
            and all(count == expected_gameweeks for _, _, count in rows)
            and total_records == 72
        ):
            print("DATABASE VERIFICATION: PASSED")
        else:
            print("DATABASE VERIFICATION: CHECK REQUIRED")

    finally:
        connection.close()


if __name__ == "__main__":
    check_gameweek_records()
