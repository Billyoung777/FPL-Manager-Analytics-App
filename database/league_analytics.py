from database.gameweek_status import get_gameweek_statuses
from database.db import get_connection
import json


SEASON = "2026/27"
LEAGUE_IDS = [1701837, 1840079]


def get_database_leaderboard(league_id, season, mode="provisional"):
    """
    Build a mini-league leaderboard using
    locally stored SQLite gameweek data.
    """

    if mode not in ("verified", "provisional"):
        raise ValueError(
            "Mode must be 'verified' or 'provisional'."
        )

    verified_ids = None

    if mode == "verified":
        statuses = get_gameweek_statuses()

        verified_ids = {
            status["gameweek"]
            for status in statuses
            if status["verified"]
        }

    connection = get_connection()

    try:
        league = connection.execute("""
            SELECT league_name
            FROM leagues
            WHERE league_id = ?
        """, (league_id,)).fetchone()

        if league is None:
            raise ValueError(f"League {league_id} not found.")

        cursor = connection.execute("""
            SELECT
                m.manager_id,
                m.manager_name,
                m.team_name,
                COUNT(g.gameweek) AS gameweeks,
                COALESCE(
                    SUM(g.points - g.transfer_cost), 0
                ) AS total_points

            FROM league_memberships AS lm

            JOIN managers AS m
                ON lm.manager_id = m.manager_id

            LEFT JOIN gameweek_performances AS g
                ON m.manager_id = g.manager_id
                AND g.season = ?
                AND (
                    ? = 'provisional'
                    OR g.gameweek IN (
                        SELECT CAST(value AS INTEGER)
                        FROM json_each(?)
                    )
                )

            WHERE lm.league_id = ?

            GROUP BY
                m.manager_id,
                m.manager_name,
                m.team_name

            ORDER BY
                total_points DESC,
                m.manager_id ASC
        """, (
git status

        leaderboard = []

        for rank, row in enumerate(cursor.fetchall(), start=1):
            manager_id, manager_name, team_name, gameweeks, points = row

            average = (
                round(points / gameweeks, 2)
                if gameweeks else 0
            )

            leaderboard.append({
                "rank": rank,
                "manager_id": manager_id,
                "manager_name": manager_name,
                "team_name": team_name,
                "gameweeks": gameweeks,
                "total_points": points,
                "average_points": average
            })

        return league[0], leaderboard

    finally:
        connection.close()


def main():
    print("=" * 65)
    print("FPL DATABASE-POWERED MINI-LEAGUE LEADERBOARD")
    print("=" * 65)

    for league_id in LEAGUE_IDS:
        league_name, leaderboard = get_database_leaderboard(
            league_id,
            SEASON
        )

        print(f"\nLEAGUE: {league_name}")

        for manager in leaderboard:
            print(
                f"{manager['rank']:>2}. "
                f"{manager['team_name']:<25} "
                f"{manager['total_points']:>4} pts | "
                f"AVG: {manager['average_points']}"
            )

    print("\nDATABASE LEADERBOARD: COMPLETE")


if __name__ == "__main__":
    main()
