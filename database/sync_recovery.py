
def build_recovery_plan(audit_report):
    """
    Build a recovery plan from a completeness audit.

    This function does not modify the database
    or make FPL API requests.
    """

    recovery_queue = []
    deferred = []
    skipped = []

    for manager in audit_report["managers"]:
        status = manager["status"]

        if status in ("incomplete", "not_synchronized"):
            recovery_queue.append({
                "manager_id": manager["manager_id"],
                "status": status,
                "missing_gameweeks": manager["missing_gameweeks"]
            })

        elif status == "unknown":
            deferred.append(manager["manager_id"])

        elif status == "complete":
            skipped.append(manager["manager_id"])

        else:
            raise ValueError(
                f"Unsupported completeness status: {status}"
            )

    return {
        "season": audit_report["season"],
        "recovery_required": len(recovery_queue),
        "deferred": len(deferred),
        "skipped": len(skipped),
        "recovery_queue": recovery_queue,
        "deferred_manager_ids": deferred,
        "skipped_manager_ids": skipped
    }
