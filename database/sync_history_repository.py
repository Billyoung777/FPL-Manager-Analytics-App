import sqlite3
from datetime import datetime
from database.db import get_connection


def save_sync_history(
    season,
    status,
    successful_managers,
    failed_managers,
    started_at,
    finished_at,
    stage=None,
    error_message=None,
    failed_manager_ids=None
):
    """
    Save synchronization history with optional failure details.

    Requires the sync_history schema migration.
    """
    import json

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
                finished_at,
                stage,
                error_message,
                failed_manager_ids
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                season,
                status,
                successful_managers,
                failed_managers,
                started_at,
                finished_at,
                stage,
                error_message,
                (
                    json.dumps(failed_manager_ids)
                    if failed_manager_ids is not None
                    else None
                )
            )
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()

def get_latest_sync():
    """
    Retrieve the latest synchronization record,
    including optional failure details.
    """
    import json

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
                finished_at,
                stage,
                error_message,
                failed_manager_ids
            FROM sync_history
            ORDER BY sync_id DESC
            LIMIT 1
        """)

        record = cursor.fetchone()

        if record is None:
            return None

        result = dict(record)

        if result["failed_manager_ids"] is not None:
            result["failed_manager_ids"] = json.loads(
                result["failed_manager_ids"]
            )

        return result

    finally:
        connection.close()
