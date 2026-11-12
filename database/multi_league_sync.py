import time
from database.league_repository import get_league
from database.membership_repository import get_league_members
from database.sync_gameweeks import sync_gameweeks
from database.gameweek_status import get_finished_gameweek_ids


SEASON = "2026/27"

SYNC_LEAGUE_IDS = [
    1701837,
    1840079
]


def sync_selected_leagues(
    league_ids=None,
    season=SEASON,
    request_delay=0.5,
    sleep_func=None
): 
    """
    Synchronize unique managers across selected leagues.

    Each manager is synchronized once, even if
    they belong to multiple selected leagues.
    """

    if request_delay < 0:
        raise ValueError("request_delay cannot be negative")

    if sleep_func is None:
        sleep_func = time.sleep

    if league_ids is None:
        league_ids = SYNC_LEAGUE_IDS

    unique_managers = set()
    selected_leagues = []

    for league_id in league_ids:

        league = get_league(league_id)

        if league is None:
            raise ValueError(
                f"League {league_id} is not registered."
            )

        members = get_league_members(league_id)

        selected_leagues.append({
            "league_id": league_id,
            "league_name": league["league_name"],
            "member_count": len(members)
        })

        for member in members:
            unique_managers.add(
                member["manager_id"]
            )

    results = {
        "season": season,
        "leagues": selected_leagues,
        "total_leagues": len(selected_leagues),
        "total_unique_managers": len(unique_managers),
        "successful": 0,
        "failed": 0,
        "managers": []
    }


    manager_ids = sorted(unique_managers)

    # Retrieve completed gameweeks once for this sync run.
    completed_gameweeks = (
        get_finished_gameweek_ids()
        if manager_ids
        else []
    )

    for index, manager_id in enumerate(manager_ids):


        try:

            history = sync_gameweeks(
                manager_id,
                season,
                completed_gameweeks=completed_gameweeks
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

        if index < len(manager_ids) - 1:
            sleep_func(request_delay)

    return results
