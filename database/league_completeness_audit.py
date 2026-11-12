
from database.membership_repository import get_league_members
from database.league_completeness import get_manager_completeness


def audit_selected_leagues(league_ids, season, expected_gameweeks):
    """
    Audit gameweek coverage across selected mini-leagues.

    Managers appearing in multiple leagues are checked once.
    This function only reads existing database records.
    """

    unique_managers = {}

    for league_id in league_ids:
        members = get_league_members(league_id)

        for member in members:
            unique_managers[member["manager_id"]] = member

    summary = {
        "complete": 0,
        "incomplete": 0,
        "not_synchronized": 0,
        "unknown": 0
    }

    manager_results = []

    for manager_id in sorted(unique_managers):
        member = unique_managers[manager_id]

        result = get_manager_completeness(
            manager_id,
            season,
            expected_gameweeks
        )

        summary[result["status"]] += 1

        manager_results.append({
            "manager_id": manager_id,
            "team_name": member["team_name"],
            **result
        })

    return {
        "season": season,
        "league_ids": list(league_ids),
        "total_unique_managers": len(unique_managers),
        "summary": summary,
        "managers": manager_results
    }
