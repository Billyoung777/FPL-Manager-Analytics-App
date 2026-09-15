from api.fpl_client import FPLClient


class PlayerPerformanceTracker:
    def __init__(self, client=None):
        self.client = client or FPLClient()

    def get_player_gameweek_performance(self, player_id, gameweek):
        player_data = self.client.get_player_history(player_id)

        history = player_data["history"]

        for gameweek_data in history:
            if gameweek_data["round"] == gameweek:
                return {
                    "player_id": gameweek_data["element"],
                    "gameweek": gameweek_data["round"],
                    "minutes": gameweek_data["minutes"],
                    "points": gameweek_data["total_points"],
                    "goals": gameweek_data["goals_scored"],
                    "assists": gameweek_data["assists"],
                    "clean_sheets": gameweek_data["clean_sheets"],
                    "bonus": gameweek_data["bonus"],
                    "bps": gameweek_data["bps"],
                    "yellow_cards": gameweek_data["yellow_cards"],
                    "red_cards": gameweek_data["red_cards"],
                    "saves": gameweek_data["saves"],
                }

        return None
    
    def get_squad_performance(self, squad, gameweek):
        performances = []

        all_players = squad["starting_xi"] + squad["bench"]

        for player in all_players:
            performance = self.get_player_gameweek_performance(
                player["element"],
                gameweek
            )

            if performance:
                performance["player_name"] = player["player_name"]
                performance["position_name"] = player["position_name"]
                performance["is_starting"] = player["multiplier"] > 0

                performances.append(performance)

        return performances
    
    def calculate_squad_points(self, performances):
        total_points = 0

        for performance in performances:
            total_points += performance["points"]

        return total_points
    
    def calculate_starting_points(self, performances):  
        starting_points = 0

        for performance in performances:
            if performance["is_starting"]:
                starting_points += performance["points"]

        return starting_points

    def calculate_captain_points(self, performances, squad):
        captain = squad["captain"]

        if captain is None:
            return 0

        for performance in performances:
            if performance["player_id"] == captain["element"]:
                return performance["points"]

        return 0
    
    def calculate_captain_bonus(self, captain_points):
        return captain_points

    def calculate_bench_points(self, performances):
        bench_points = 0

        for performance in performances:
            if not performance["is_starting"]:
                bench_points += performance["points"]

        return bench_points
    
    def calculate_manager_score(self, starting_points, captain_bonus):
        return starting_points + captain_bonus

    def analyze_gameweek(self, squad, gameweek):
        performances = self.get_squad_performance(
            squad,
            gameweek
        )

        total_squad_points = self.calculate_squad_points(
            performances
        )

        starting_points = self.calculate_starting_points(
            performances
        )

        bench_points = self.calculate_bench_points(
            performances
        )

        captain_points = self.calculate_captain_points(
            performances,
            squad
        )

        captain_bonus = self.calculate_captain_bonus(
            captain_points
        )

        manager_score = self.calculate_manager_score(
            starting_points,
            captain_bonus
        )

        return {
            "gameweek": gameweek,
            "total_squad_points": total_squad_points,
            "starting_points": starting_points,
            "bench_points": bench_points,
            "captain_points": captain_points,
            "captain_bonus": captain_bonus,
            "manager_score": manager_score,
        }