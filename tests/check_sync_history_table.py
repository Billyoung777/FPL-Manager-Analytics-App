
from database.db import get_connection

connection = get_connection()

try:
    result = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?
        """,
        ("sync_history",)
    ).fetchone()

    if result:
        print("SUCCESS: sync_history table exists.")
    else:
        print("ERROR: sync_history table not found.")

finally:
    connection.close()
