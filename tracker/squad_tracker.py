from api.fpl_client import FPLClient


class SquadTracker:
    def __init__(self, client=None):
        self.client = client or FPLClient()

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

    def get_historical_squads(self, manager_id, last_gameweek):
        historical_squads = []

        for gameweek in range(1, last_gameweek + 1):
            squad = self.get_gameweek_squad(
                manager_id,
                gameweek
            )

            historical_squads.append(squad)

        return historical_squads