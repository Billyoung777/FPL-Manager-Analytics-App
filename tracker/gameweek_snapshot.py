from api.fpl_client import FPLClient
from tracker.squad_tracker import SquadTracker
from tracker.player_performance import PlayerPerformanceTracker

# This class is responsible for retrieving a snapshot of a manager's squad, performances, analysis, official gameweek data, and chip usage for a specific gameweek. It uses the FPLClient to interact with the FPL API and the SquadTracker and PlayerPerformanceTracker to gather relevant data.
class GameweekSnapshot:
    def __init__(self, client=None):
        self.client = client or FPLClient()

        self.squad_tracker = SquadTracker(
            self.client
        )

        self.performance_tracker = PlayerPerformanceTracker(
            self.client
        )

# This method retrieves a snapshot of a manager's squad, performances, analysis, official gameweek data, and chip usage for a specific gameweek. It uses the SquadTracker to get the squad, the PlayerPerformanceTracker to get performances and analysis, and the FPLClient to get official gameweek history and chip information.
    def get_snapshot(self, manager_id, gameweek):
        squad = self.squad_tracker.get_gameweek_squad(
            manager_id,
            gameweek
        )
#this method retrieves the performances of the squad for a specific gameweek using the PlayerPerformanceTracker. It also analyzes the gameweek using the same tracker. Additionally, it retrieves the manager's history and chip usage for the specified gameweek using the FPLClient. Finally, it returns a dictionary containing all the relevant data.
        performances = self.performance_tracker.get_squad_performance(
            squad,
            gameweek
        )

        analysis = self.performance_tracker.analyze_gameweek(
            squad,
            gameweek
        )
        manager_history = self.client.get_manager_history(
            manager_id
        )

#This method retrieves the official gameweek history for a specific manager and gameweek using the FPLClient. It iterates through the manager's history to find the relevant gameweek data and also checks for any chip usage during that gameweek. Finally, it returns a dictionary containing the manager ID, gameweek, squad, performances, analysis, official gameweek data, and chip information.
        gameweek_history = None

        for history in manager_history["current"]:
            if history["event"] == gameweek:
                gameweek_history = history
                break
#This method retrieves the chip used by a manager for a specific gameweek by iterating through the manager's history and checking for any chip usage during that gameweek. If a chip is found, it is stored in the `gameweek_chip` variable. Finally, the method returns a dictionary containing the manager ID, gameweek, squad, performances, analysis, official gameweek data, and chip information.
        chips = manager_history["chips"]

        gameweek_chip = None

        for chip in chips:
            if chip["event"] == gameweek:
                gameweek_chip = chip
                break

#This method retrieves the transfers made by a manager for a specific gameweek using the FPLClient. It iterates through the manager's transfers and filters them based on the specified gameweek. Finally, it returns a dictionary containing the manager ID, gameweek, squad, performances, analysis, official gameweek data, and chip information.
        transfers = self.client.get_manager_transfers(
            manager_id
        )

        gameweek_transfers = []

        for transfer in transfers:
            if transfer["event"] == gameweek:
                gameweek_transfers.append(transfer)

#This method retrieves the player data from the FPL API using the FPLClient. It creates a lookup dictionary that maps player IDs to their web names. Then, it iterates through the gameweek transfers and constructs a list of transfer details, including player IDs, names, and costs for both players involved in each transfer. Finally, it returns a dictionary containing the manager ID, gameweek, squad, performances, analysis, official gameweek data, chip information, and transfer details.
        players_data = self.client.get_players()

        player_lookup = {
            player["id"]: player["web_name"]
            for player in players_data["elements"]
        }

        transfer_details = []

        for transfer in gameweek_transfers:
            transfer_details.append({
                "player_out_id": transfer["element_out"],
                "player_out": player_lookup.get(
                    transfer["element_out"],
                    "Unknown Player"
                ),
                "player_in_id": transfer["element_in"],
                "player_in": player_lookup.get(
                    transfer["element_in"],
                    "Unknown Player"
                ),
                "player_out_cost": transfer["element_out_cost"],
                "player_in_cost": transfer["element_in_cost"],
            })

#This method returns a dictionary containing the manager ID, gameweek, squad, performances, analysis, official gameweek data, and chip information. It provides a comprehensive snapshot of a manager's performance and squad for a specific gameweek.
        return {
            "manager_id": manager_id,
            "gameweek": gameweek,
            "squad": squad,
            "performances": performances,
            "analysis": analysis,
            "official": gameweek_history,
            "chip": gameweek_chip,
            "transfers": transfer_details,
        }

