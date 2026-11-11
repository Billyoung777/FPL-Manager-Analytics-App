
from database.membership_repository import get_league_members
from database.sync_gameweeks import sync_gameweeks


def sync_league_gameweeks(league_id, season):
    """
    Synchronize available gameweek history for
    every manager belonging to a mini-league.

    Continue processing if an individual manager fails.
    """

    members = get_league_members(league_id)

    results = {
        "league_id": league_id,
        "season": season,
        "total_managers": len(members),
        "successful": 0,
        "failed": 0,
        "managers": []
    }

    for member in members:
        manager_id = member["manager_id"]

        try:
            history = sync_gameweeks(
                manager_id,
                season
            )

            results["successful"] += 1

            results["managers"].append({
                "manager_id": manager_id,
                "status": "success",
                "stored_gameweeks": len(history)
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
