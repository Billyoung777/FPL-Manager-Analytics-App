from database.db import get_connection


def save_membership(league_id, manager_id):
    """
    Add a manager to a league without creating
    duplicate memberships.
    """
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO league_memberships (
                league_id,
                manager_id
            )
            VALUES (?, ?)

            ON CONFLICT(league_id, manager_id)
            DO NOTHING
        """, (league_id, manager_id))

        connection.commit()

    finally:
        connection.close()


def get_league_members(league_id):
    """
    Retrieve all managers belonging to a league.
    """
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT
                m.manager_id,
                m.manager_name,
                m.team_name
            FROM league_memberships AS lm
            JOIN managers AS m
                ON lm.manager_id = m.manager_id
            WHERE lm.league_id = ?
            ORDER BY m.team_name
        """, (league_id,))

        return [
            {
                "manager_id": row[0],
                "manager_name": row[1],
                "team_name": row[2]
            }
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()
