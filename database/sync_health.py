
from database.sync_history_repository import get_latest_sync


def show_sync_health():
    """Display the latest database synchronization status."""

    print("=" * 55)
    print("FPL MANAGER ANALYTICS - SYNC HEALTH")
    print("=" * 55)

    latest_sync = get_latest_sync()

    if latest_sync is None:
        print("No synchronization history found.")
        print("Database Status: NOT YET SYNCHRONIZED")
        print("=" * 55)
        return

    status = latest_sync["status"]

    print(f"Season: {latest_sync['season']}")
    print(f"Last Sync: {latest_sync['finished_at']}")
    print(f"Status: {status.upper()}")
    print()
    print(f"Successful Managers: {latest_sync['successful_managers']}")
    print(f"Failed Managers: {latest_sync['failed_managers']}")
    print()

    if status == "success":
        health = "HEALTHY"
    elif status == "partial":
        health = "PARTIAL - ATTENTION REQUIRED"
    else:
        health = "FAILED - ATTENTION REQUIRED"

    print(f"Database Status: {health}")
    print("=" * 55)


if __name__ == "__main__":
    show_sync_health()
