import sqlite3
from datetime import datetime
from database.db import get_connection


def save_sync_history(
    season,
    status,
    successful_managers,
    failed_managers,
    started_at,
    finished_at
):
    """
    Save a synchronization run to the database.
    """

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO sync_history (
                season,
                status,
                successful_managers,
                failed_managers,
                started_at,
                finished_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                season,
                status,
                successful_managers,
                failed_managers,
                started_at,
                finished_at
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()

def get_latest_sync():
    """
    Retrieve the most recent synchronization record.
    """

    connection = get_connection()

    try:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute("""
            SELECT
                sync_id,
                season,
                status,
                successful_managers,
                failed_managers,
                started_at,
                finished_at
            FROM sync_history
            ORDER BY sync_id DESC
            LIMIT 1
        """)

        record = cursor.fetchone()

        if record is None:
            return None

        return dict(record)

    finally:
        connection.close()
