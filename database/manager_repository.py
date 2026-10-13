from database.db import get_connection


def save_manager(manager_id, manager_name, team_name):
    """
    Insert a new FPL manager or update an existing manager.
    """
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO managers (
                manager_id,
                manager_name,
                team_name
            )
            VALUES (?, ?, ?)

            ON CONFLICT(manager_id)
            DO UPDATE SET
                manager_name = excluded.manager_name,
                team_name = excluded.team_name,
                last_updated = CURRENT_TIMESTAMP
        """, (manager_id, manager_name, team_name))

        connection.commit()

    finally:
        connection.close()


def get_manager(manager_id):
    """
    Retrieve a manager by their FPL entry ID.
    """
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT
                manager_id,
                manager_name,
                team_name,
                last_updated
            FROM managers
            WHERE manager_id = ?
        """, (manager_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "manager_id": row[0],
            "manager_name": row[1],
            "team_name": row[2],
            "last_updated": row[3]
        }

    finally:
        connection.close()
