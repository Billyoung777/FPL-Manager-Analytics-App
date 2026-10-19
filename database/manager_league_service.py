from api.fpl_client import FPLClient
from database.manager_repository import save_manager
from database.league_repository import save_league
from database.membership_repository import save_membership


def register_manager_leagues(manager_id, client=None):
    """
    Retrieve a public FPL manager profile and save
    the manager's classic league memberships.
    """
    if not isinstance(manager_id, int) or manager_id <= 0:
        raise ValueError("Invalid FPL Manager ID")

    client = client or FPLClient()

    profile = client.get_manager(manager_id)

    save_manager(
        manager_id=manager_id,
        manager_name=(
            f"{profile['player_first_name']} "
            f"{profile['player_last_name']}"
        ).strip(),
        team_name=profile["name"]
    )

    leagues = profile.get("leagues", {}).get("classic", [])

    for league in leagues:
        save_league(
            league_id=league["id"],
            league_name=league["name"]
        )

        save_membership(
            league_id=league["id"],
            manager_id=manager_id
        )

    return {
        "manager_id": manager_id,
        "team_name": profile["name"],
        "leagues": [
            {
                "league_id": league["id"],
                "league_name": league["name"]
            }
            for league in leagues
        ]
    }