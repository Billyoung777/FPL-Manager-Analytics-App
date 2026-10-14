
from datetime import datetime

from database.schema import create_tables
from database.sync_memberships import sync_league_memberships
from database.sync_all_gameweeks import sync_all_gameweeks


SEASON = "2026/27"

LEAGUE_IDS = [
    1701837,  # FPL Manager Commission Inquiry
    1840079   # Kasi Football League
]


def sync_all():
    print("=" * 65)
    print("FPL MANAGER ANALYTICS - DATABASE SYNCHRONIZATION")
    print("=" * 65)

    print(f"Season: {SEASON}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # STEP 1: Initialize database tables.
    print("\n[1/3] INITIALIZING DATABASE")
    create_tables()

    # STEP 2: Synchronize leagues and memberships.
    print("\n[2/3] SYNCHRONIZING LEAGUES AND MEMBERS")

    successful_leagues = 0
    failed_leagues = []

    for league_id in LEAGUE_IDS:
        try:
            print(f"\nSynchronizing league {league_id}...")

            sync_league_memberships(league_id)

            successful_leagues += 1

        except Exception as error:
            print(f"ERROR: League {league_id}: {error}")
            failed_leagues.append(league_id)

    # Avoid incomplete gameweek synchronization if a league failed.

    if failed_leagues:
        print("\nSynchronization incomplete.")
        print(f"Successful leagues: {successful_leagues}")
        print(f"Failed leagues: {failed_leagues}")
        print("Fix league errors before synchronizing gameweeks.")

        return {
            "status": "failed",
            "season": SEASON,
            "stage": "leagues",
            "successful_leagues": successful_leagues,
            "failed_leagues": failed_leagues
        }


    # STEP 3: Synchronize gameweek performances.
    print("\n[3/3] SYNCHRONIZING GAMEWEEK PERFORMANCES")


    try:
        successful_managers, failed_managers = (
            sync_all_gameweeks(SEASON)
        )

        
        if failed_managers:
            print("\nWARNING: PARTIAL SYNCHRONIZATION")
            print(f"Successful managers: {successful_managers}")
            print(f"Failed managers: {len(failed_managers)}")
            print(f"Failed manager IDs: {failed_managers}")

            return {
                "status": "partial",
                "season": SEASON,
                "successful_managers": successful_managers,
                "failed_managers": failed_managers
            }


        print("\nAll tracked managers synchronized successfully.")

    
    except Exception as error:
        print(f"ERROR: Gameweek synchronization failed: {error}")

        return {
            "status": "failed",
            "season": SEASON,
            "stage": "gameweeks",
            "error": str(error)
        }



    print("\n" + "=" * 65)
    print("SYNCHRONIZATION PROCESS FINISHED")
    print("=" * 65)

    print(f"Leagues processed: {successful_leagues}")
    print(f"Season: {SEASON}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {
        "status": "success",
        "season": SEASON,
        "successful_leagues": successful_leagues,
        "successful_managers": successful_managers,
        "failed_managers": []
    }


def get_exit_code(result):
    """Convert synchronization status into a process exit code."""

    status = result.get("status")

    if status == "success":
        return 0

    if status == "partial":
        return 2

    return 1



if __name__ == "__main__":
    import sys

    result = sync_all()
    sys.exit(get_exit_code(result))

