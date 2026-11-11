
from database.gameweek_repository import get_manager_gameweeks
from database.gameweek_completeness import check_gameweek_completeness


def get_manager_completeness(
    manager_id,
    season,
    expected_gameweeks
):
    """
    Check stored gameweek coverage for a manager.

    Missing records indicate a coverage gap, not necessarily
    a failed synchronization.
    """

    history = get_manager_gameweeks(manager_id, season)

    stored_gameweeks = [
        record["gameweek"]
        for record in history
    ]

    result = check_gameweek_completeness(
        stored_gameweeks,
        expected_gameweeks
    )

    return {
        "manager_id": manager_id,
        **result
    }
