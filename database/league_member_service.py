from tracker.mini_league_tracker import get_mini_league
from database.manager_repository import save_manager
from database.league_repository import save_league
from database.membership_repository import save_membership


def synchronize_league_members(league_id, fetch_league=None):
    """
    Synchronize managers belonging to a selected FPL league.
    """
    if not isinstance(league_id, int) or league_id <= 0:
        raise ValueError("Invalid league ID")

    if fetch_league is None:
        fetch_league = lambda league_id: get_mini_league(
            league_id,
            max_pages=2
        )

    data = fetch_league(league_id)

    league_name = data["league"]["name"]
    members = data["standings"]["results"]

    save_league(league_id, league_name)

    for member in members:
        manager_id = member["entry"]

        save_manager(
            manager_id=manager_id,
            manager_name=member["player_name"],
            team_name=member["entry_name"]
        )

        save_membership(
            league_id=league_id,
            manager_id=manager_id
        )

    return {
        "league_id": league_id,
        "league_name": league_name,
        "members_synchronized": len(members)
    }