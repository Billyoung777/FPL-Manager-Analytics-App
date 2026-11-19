
from api.fpl_client import FPLClient
from database.squad_repository import save_manager_picks
from database.squad_repository import (
    get_manager_picks,
    save_manager_picks,
)


SEASON = "2026/27"


def sync_manager_squad(
    manager_id,
    gameweek,
    season=SEASON,
    force=False,
    client=None,
):
    """
    Fetch and store one manager's gameweek squad.

    Returns a dictionary describing the synchronization result.
    """

    if type(manager_id) is not int or manager_id <= 0:
        raise ValueError("Invalid manager ID")

    if type(gameweek) is not int or not 1 <= gameweek <= 38:
        raise ValueError("Invalid gameweek")

    if not isinstance(season, str) or not season.strip():
        raise ValueError("Invalid season")

    if type(force) is not bool:
        raise ValueError("force must be a boolean")

    client = client if client is not None else FPLClient()

    # Determine whether the gameweek has been finalized.
    bootstrap = client.get_players()
    events = bootstrap.get("events", [])

    event = next(
        (
            item for item in events
            if item.get("id") == gameweek
        ),
        None,
    )

    if event is None:
        raise ValueError("Gameweek not found in FPL data")

    is_final = event.get("data_checked") is True


    # Never request picks before the gameweek deadline.
    if not event.get("is_previous", False) and not event.get(
        "is_current", False
    ) and not is_final:
        raise ValueError(
            "Squad picks are not available before the gameweek deadline"
        )

    response = client.get_manager_picks(
        manager_id,
        gameweek,
    )

    if not isinstance(response, dict):
        raise ValueError("Invalid FPL picks response")

    picks = response.get("picks")

    if not isinstance(picks, list) or len(picks) != 15:
        raise ValueError(
            "FPL response must contain exactly 15 squad picks"
        )

    save_manager_picks(
        manager_id,
        season,
        gameweek,
        picks,
    )

    return {
        "manager_id": manager_id,
        "season": season,
        "gameweek": gameweek,
        "status": "updated",
        "is_final": is_final,
        "picks": picks,
    }
