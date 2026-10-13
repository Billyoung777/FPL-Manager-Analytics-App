
from api.fpl_client import FPLClient
from database.manager_repository import save_manager, get_manager


def sync_manager(manager_id):
    """
    Retrieve a manager from the FPL API
    and save their information in SQLite.
    """
    client = FPLClient()

    print(f"Fetching FPL manager {manager_id}...")

    manager_data = client.get(f"entry/{manager_id}/")

    first_name = manager_data.get("player_first_name", "")
    last_name = manager_data.get("player_last_name", "")

    manager_name = f"{first_name} {last_name}".strip()
    team_name = manager_data["name"]

    save_manager(
        manager_id=manager_id,
        manager_name=manager_name,
        team_name=team_name
    )

    print("Manager synchronized successfully.")

    return get_manager(manager_id)


def main():
    manager_id = 1053858

    print("=" * 55)
    print("FPL MANAGER DATABASE SYNCHRONIZATION")
    print("=" * 55)

    manager = sync_manager(manager_id)

    print(f"Manager ID: {manager['manager_id']}")
    print(f"Manager Name: {manager['manager_name']}")
    print(f"Team Name: {manager['team_name']}")
    print(f"Last Updated: {manager['last_updated']}")

    print("\nDATABASE SYNC: COMPLETE")


if __name__ == "__main__":
    main()
