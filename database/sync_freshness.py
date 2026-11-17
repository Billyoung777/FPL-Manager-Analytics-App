
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def calculate_sync_freshness(finished_at, now=None):
    """
    Classify the age of the latest synchronization.

    Fresh: less than 24 hours
    Aging: 24 to 48 hours
    Stale: more than 48 hours
    """

    if not finished_at:
        return {
            "freshness": "unknown",
            "age_hours": None
        }

    sync_time = datetime.fromisoformat(finished_at)

    if sync_time.tzinfo is None:
        sync_time = sync_time.replace(
            tzinfo=ZoneInfo("Africa/Johannesburg")
        )

    if now is None:
        now = datetime.now(timezone.utc)

    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    age_hours = max(
        0,
        (now - sync_time).total_seconds() / 3600
    )

    if age_hours < 24:
        freshness = "fresh"
    elif age_hours <= 48:
        freshness = "aging"
    else:
        freshness = "stale"

    return {
        "freshness": freshness,
        "age_hours": round(age_hours, 2)
    }
