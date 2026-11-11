
def check_gameweek_completeness(stored_gameweeks, expected_gameweeks):
    """
    Compare locally stored gameweek IDs against expected
    finalized gameweek IDs.

    expected_gameweeks=None means verification is unavailable.
    """

    stored = set(stored_gameweeks)

    if expected_gameweeks is None:
        return {
            "status": "unknown",
            "stored_count": len(stored),
            "expected_count": None,
            "missing_gameweeks": []
        }

    expected = set(expected_gameweeks)
    missing = sorted(expected - stored)

    if not stored:
        status = "not_synchronized"
    elif missing:
        status = "incomplete"
    else:
        status = "complete"

    return {
        "status": status,
        "stored_count": len(stored),
        "expected_count": len(expected),
        "missing_gameweeks": missing
    }
