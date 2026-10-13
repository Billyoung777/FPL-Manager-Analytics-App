
from api.fpl_client import FPLClient

from database.manager_repository import get_manager
from database.gameweek_repository import (
    save_gameweek_performance,
    get_manager_gameweeks
)


MANAGER_ID = 1053858
SEASON = "2026/27"


def sync_gameweeks(manager_id, season):
    """
    Fetch and store available FPL gameweek history.
    """

    client = FPLClient()

    print(f"Fetching gameweek history for {manager_id}...")

    # The manager must already exist because of
    # the database foreign-key constraint.
    if get_manager(manager_id) is None:
        raise ValueError(
            f"Manager {manager_id} is not in the database. "
            "Synchronize the manager first."
        )

    history_data = client.get(
        f"entry/{manager_id}/history/"
    )

    gameweeks = history_data["current"]

    for gw in gameweeks:
        save_gameweek_performance(
            manager_id=manager_id,
            season=season,
            gameweek=gw["event"],
            points=gw["points"],
            transfer_cost=gw["event_transfers_cost"],
            total_points=gw["total_points"]
        )

    return get_manager_gameweeks(manager_id, season)


def main():
    print("=" * 60)
    print("FPL GAMEWEEK DATABASE SYNCHRONIZATION")
    print("=" * 60)

    history = sync_gameweeks(MANAGER_ID, SEASON)

    for gw in history:
        net_points = gw["points"] - gw["transfer_cost"]

        print(
            f"GW{gw['gameweek']} | "
            f"Points: {gw['points']} | "
            f"Transfer Cost: {gw['transfer_cost']} | "
            f"Net: {net_points} | "
            f"Total: {gw['total_points']}"
        )

    print(f"\nStored gameweeks: {len(history)}")
    print("GAMEWEEK DATABASE SYNC: COMPLETE")


if __name__ == "__main__":
    main()
