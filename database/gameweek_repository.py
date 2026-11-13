
from database.db import get_connection



def save_gameweek_performance(
    manager_id,
    season,
    gameweek,
    points,
    transfer_cost,
    total_points,
    connection=None
):
    """
    Insert or update a manager's gameweek performance.

    If a connection is provided, the caller controls
    the transaction.

    Otherwise, this function manages its own transaction.
    """

    owns_connection = connection is None

    if owns_connection:
        connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO gameweek_performances (
                manager_id,
                season,
                gameweek,
                points,
                transfer_cost,
                total_points
            )
            VALUES (?, ?, ?, ?, ?, ?)

            ON CONFLICT(manager_id, season, gameweek)
            DO UPDATE SET
                points = excluded.points,
                transfer_cost = excluded.transfer_cost,
                total_points = excluded.total_points,
                last_updated = CURRENT_TIMESTAMP
        """, (
            manager_id,
            season,
            gameweek,
            points,
            transfer_cost,
            total_points
        ))

        if owns_connection:
            connection.commit()

    except Exception:
        if owns_connection:
            connection.rollback()
        raise

    finally:
        if owns_connection:
            connection.close()


def get_manager_gameweeks(manager_id, season):
    """
    Retrieve a manager's stored gameweek history.
    """

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT
                gameweek,
                points,
                transfer_cost,
                total_points
            FROM gameweek_performances
            WHERE manager_id = ?
              AND season = ?
            ORDER BY gameweek ASC
        """, (manager_id, season))

        return [
            {
                "gameweek": row[0],
                "points": row[1],
                "transfer_cost": row[2],
                "total_points": row[3]
            }
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()

def get_latest_gameweek_update(manager_id, season):
    """
    Return the latest saved gameweek update timestamp.
    """

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT MAX(last_updated)
            FROM gameweek_performances
            WHERE manager_id = ?
              AND season = ?
        """, (manager_id, season))

        row = cursor.fetchone()
        return row[0] if row else None

    finally:
        connection.close()