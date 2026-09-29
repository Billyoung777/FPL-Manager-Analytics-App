from api.fpl_client import FPLClient


class SquadTracker:
    def __init__(self, client=None):
        self.client = client or FPLClient()

# This method retrieves the squad of a manager for a specific gameweek using the FPLClient. It fetches the manager's picks and player data, constructs a lookup for player names and positions, and categorizes players into starting XI and bench. It also identifies the captain and vice-captain. Finally, it returns a dictionary containing the gameweek, starting XI, bench, captain, and vice-captain information.
    def get_gameweek_squad(self, manager_id, gameweek):
        picks_data = self.client.get_manager_picks(manager_id, gameweek)
        players_data = self.client.get_players()

        picks = picks_data["picks"]
        players = players_data["elements"]

        player_lookup = {
            player["id"]: {
                "name": player["web_name"],
                "position": player["element_type"],
            }
            for player in players
        }

        position_lookup = {
            1: "Goalkeeper",
            2: "Defender",
            3: "Midfielder",
            4: "Forward",
        }

        starting_xi = []
        bench = []
        captain = None
        vice_captain = None

        for player in picks:
            player_info = player_lookup.get(
                player["element"],
                {}
            )

            player["player_name"] = player_info.get(
                "name",
                "Unknown Player"
            )

            player["position_name"] = position_lookup.get(
                player_info.get("position"),
                "Unknown Position"
            )

            if player["multiplier"] > 0:
                starting_xi.append(player)
            else:
                bench.append(player)

            if player["is_captain"]:
                captain = player

            if player["is_vice_captain"]:
                vice_captain = player

        return {
            "gameweek": gameweek,
            "starting_xi": starting_xi,
            "bench": bench,
            "captain": captain,
            "vice_captain": vice_captain,
        }
#This method retrieves the squad of a manager for a specific gameweek using the FPLClient. It fetches the manager's picks and player data, constructs a lookup for player names and positions, and categorizes players into starting XI and bench. It also identifies the captain and vice-captain. Finally, it returns a dictionary containing the gameweek, starting XI, bench, captain, and vice-captain information.
    def get_historical_squads(self, manager_id, last_gameweek):
        historical_squads = []

        for gameweek in range(1, last_gameweek + 1):
            squad = self.get_gameweek_squad(
                manager_id,
                gameweek
            )

            historical_squads.append(squad)

        return historical_squads

# This method retrieves the squad changes for a manager between two consecutive gameweeks. It compares the previous gameweek's squad with the current gameweek's squad to identify players who were transferred out and players who were transferred in. It returns a dictionary containing lists of players out and players in, along with their IDs, names, and positions.
    def get_squad_changes(self, manager_id, gameweek):
        if gameweek <= 1:
            return {
                "players_out": [],
                "players_in": [],
            }

        previous_squad = self.get_gameweek_squad(
            manager_id,
            gameweek - 1
        )

        current_squad = self.get_gameweek_squad(
            manager_id,
            gameweek
        )

        previous_players = (
            previous_squad["starting_xi"]
            + previous_squad["bench"]
        )

        current_players = (
            current_squad["starting_xi"]
            + current_squad["bench"]
        )

        previous_ids = {
            player["element"]
            for player in previous_players
        }

        current_ids = {
            player["element"]
            for player in current_players
        }

        players_out_ids = previous_ids - current_ids
        players_in_ids = current_ids - previous_ids

        players_out = [
            {
                "player_id": player["element"],
                "player_name": player["player_name"],
                "position": player["position_name"],
            }
            for player in previous_players
            if player["element"] in players_out_ids
        ]

        players_in = [
            {
                "player_id": player["element"],
                "player_name": player["player_name"],
                "position": player["position_name"],
            }
            for player in current_players
            if player["element"] in players_in_ids
        ]

        return {
            "players_out": players_out,
            "players_in": players_in,
        }