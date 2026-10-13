
from database.gameweek_repository import get_manager_gameweeks
from database.gameweek_status import get_gameweek_statuses


MANAGER_ID = 1053858
SEASON = "2026/27"


def get_filtered_gameweeks(manager_id, season, mode="verified"):
    """
    Retrieve stored gameweeks.

    verified:
        Only officially verified gameweeks.

    provisional:
        All available stored gameweeks.
    """

    if mode not in ("verified", "provisional"):
        raise ValueError(
            "Mode must be 'verified' or 'provisional'."
        )

    history = get_manager_gameweeks(manager_id, season)

    if mode == "provisional":
        return history

    statuses = get_gameweek_statuses()

    verified_ids = {
        status["gameweek"]
        for status in statuses
        if status["verified"]
    }

    return [
        gw for gw in history
        if gw["gameweek"] in verified_ids
    ]


def main():
    print("=" * 60)
    print("FPL VERIFIED GAMEWEEK DATABASE ANALYTICS")
    print("=" * 60)

    for mode in ("verified", "provisional"):
        history = get_filtered_gameweeks(
            MANAGER_ID,
            SEASON,
            mode
        )

        print(f"\nMODE: {mode.upper()}")

        total = 0

        for gw in history:
            net_points = gw["points"] - gw["transfer_cost"]
            total += net_points

            print(
                f"GW{gw['gameweek']} | "
                f"Net Points: {net_points}"
            )

        print(f"Gameweeks included: {len(history)}")
        print(f"Total net points: {total}")

    print("\nGAMEWEEK FILTERING: COMPLETE")


if __name__ == "__main__":
    main()
