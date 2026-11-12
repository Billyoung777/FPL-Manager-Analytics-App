from database.sync_gameweeks import sync_gameweeks
from database.gameweek_repository import get_manager_gameweeks
from database.gameweek_status import get_verified_gameweek_ids

def execute_recovery_plan(
    recovery_plan,
    dry_run=True
):
    """
    Execute or preview a synchronization recovery plan.

    Dry-run mode does not modify the database
    or make FPL API requests.
    """

    if not dry_run:
        raise NotImplementedError(
            "Live recovery execution is not enabled yet."
        )

    results = {
        "season": recovery_plan["season"],
        "dry_run": True,
        "total_queued": len(
            recovery_plan["recovery_queue"]
        ),
        "managers": []
    }

    for manager in recovery_plan["recovery_queue"]:
        results["managers"].append({
            "manager_id": manager["manager_id"],
            "status": "planned",
            "missing_gameweeks": list(
                manager["missing_gameweeks"]
            )
        })

    return results

def recover_missing_gameweeks(
    recovery_plan,
    verified_gameweeks=None
):
    """
    Synchronize missing gameweeks for queued managers.

    Each manager is processed independently.
    Successful recovery requires all requested
    gameweeks to be present in the returned history.
    """

    season = recovery_plan["season"]
    recovery_queue = recovery_plan["recovery_queue"]

    results = {
        "season": season,
        "total_queued": len(recovery_queue),
        "successful": 0,
        "failed": 0,
        "managers": []
    }

    processed_managers = set()

    for manager in recovery_queue:
        manager_id = manager["manager_id"]

        # Reject invalid manager IDs before synchronization.
        if type(manager_id) is not int or manager_id <= 0:
            results["failed"] += 1
            results["managers"].append({
                "manager_id": manager_id,
                "status": "invalid",
                "error": "Manager ID must be a positive integer"
            })
            continue

        # Reject duplicate manager recovery requests.
        if manager_id in processed_managers:
            results["failed"] += 1
            results["managers"].append({
                "manager_id": manager_id,
                "status": "invalid",
                "error": "Duplicate manager in recovery queue"
            })
            continue

        processed_managers.add(manager_id)

        # Extract and normalize requested gameweeks.
        # Read the requested gameweeks.
        # Read the requested gameweeks.
        requested_gameweeks = manager["missing_gameweeks"]

        # Reject empty recovery requests.
        if not requested_gameweeks:
            results["failed"] += 1
            results["managers"].append({
                "manager_id": manager_id,
                "status": "invalid",
                "error": "No missing gameweeks specified"
            })
            continue

        # Reject invalid gameweek numbers.
        if (
            not isinstance(requested_gameweeks, (list, tuple))
            or any(
                type(gw) is not int or not 1 <= gw <= 38
                for gw in requested_gameweeks
            )
        ):
            results["failed"] += 1
            results["managers"].append({
                "manager_id": manager_id,
                "status": "invalid",
                "error": "Gameweeks must be integers between 1 and 38"
            })
            continue

        # Normalize valid gameweeks.
        missing_gameweeks = sorted(
            set(requested_gameweeks)
        )

        # Reject recovery when verification is unavailable.
        if verified_gameweeks is None:
            results["failed"] += 1
            results["managers"].append({
                "manager_id": manager_id,
                "status": "invalid",
                "error": "Verified gameweek data is required"
            })
            continue

        # Reject gameweeks that are not verified.
        unverified_gameweeks = sorted(
            set(missing_gameweeks) - set(verified_gameweeks)
        )

        if unverified_gameweeks:
            results["failed"] += 1
            results["managers"].append({
                "manager_id": manager_id,
                "status": "invalid",
                "error": "Unverified gameweeks cannot be recovered",
                "unverified_gameweeks": unverified_gameweeks
            })
            continue

        try:
            sync_gameweeks(
                manager_id,
                season,
                completed_gameweeks=missing_gameweeks
            )

            # Independently verify the stored SQLite records.
            history = get_manager_gameweeks(
                manager_id,
                season
            )

            stored_gameweeks = {
                record["gameweek"]
                for record in history
            }

            still_missing = sorted(
                set(missing_gameweeks) - stored_gameweeks
            )

            if still_missing:
                results["failed"] += 1

                results["managers"].append({
                    "manager_id": manager_id,
                    "status": "incomplete",
                    "missing_gameweeks": still_missing
                })

            else:
                results["successful"] += 1

                results["managers"].append({
                    "manager_id": manager_id,
                    "status": "recovered",
                    "missing_gameweeks": []
                })

        except (
            RuntimeError,
            ValueError,
            KeyError,
            TypeError,
            OSError
        ) as error:
            results["failed"] += 1

            results["managers"].append({
                "manager_id": manager_id,
                "status": "failed",
                "error": str(error)
            })

    
    return results



def recover_verified_gameweeks(recovery_plan):
    """
    Recover missing gameweeks using the current
    FPL verification snapshot.

    Verification is retrieved once per batch.
    Reject empty verification snapshots.
    """

    verified_gameweeks = get_verified_gameweek_ids()

    if not verified_gameweeks:
        raise ValueError(
            "No verified gameweeks available for recovery"
        )

    return recover_missing_gameweeks(
        recovery_plan,
        verified_gameweeks=verified_gameweeks
    )

    """
    Recover missing gameweeks using the current
    FPL verification snapshot.

    Verification is retrieved once per batch.
    """

    verified_gameweeks = get_verified_gameweek_ids()

    return recover_missing_gameweeks(
        recovery_plan,
        verified_gameweeks=verified_gameweeks
    )
