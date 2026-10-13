
from database.db import get_connection


def save_league(league_id, league_name):
    """
    Insert a new league or update an existing league.
    """
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO leagues (
                league_id,
                league_name
            )
            VALUES (?, ?)

            ON CONFLICT(league_id)
            DO UPDATE SET
                league_name = excluded.league_name,
                last_updated = CURRENT_TIMESTAMP
        """, (league_id, league_name))

        connection.commit()

    finally:
        connection.close()


def get_league(league_id):
    """
    Retrieve a league from the local database.
    """
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT
                league_id,
                league_name,
                last_updated
            FROM leagues
            WHERE league_id = ?
        """, (league_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "league_id": row[0],
            "league_name": row[1],
            "last_updated": row[2]
        }

    finally:
        connection.close()
