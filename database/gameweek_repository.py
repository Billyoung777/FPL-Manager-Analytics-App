
from database.db import get_connection


def save_gameweek_performance(
    manager_id,
    season,
    gameweek,
    points,
    transfer_cost,
    total_points
):
    """
    Insert or update a manager's gameweek performance.
    """

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

        connection.commit()

    finally:
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
