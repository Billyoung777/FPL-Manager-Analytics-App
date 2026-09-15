import requests


class FPLClient:
    BASE_URL = "https://fantasy.premierleague.com/api"

    def __init__(self, timeout=10):
        self.timeout = timeout
# This method is used to make a GET request to the FPL API and return the JSON response. It handles exceptions for timeouts, HTTP errors, and other request-related issues.
    def get(self, endpoint):
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            raise RuntimeError(
                f"FPL API request timed out: {endpoint}"
            )

        except requests.exceptions.HTTPError as error:
            raise RuntimeError(
                f"FPL API returned an HTTP error for {endpoint}: {error}"
            )

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"FPL API request failed for {endpoint}: {error}"
            )
        
# Below are the methods that can be added to the FPLClient class to retrieve manager and player data.
# Manager data (Manager ID, Team name, Player name)
    def get_manager(self, manager_id):
        return self.get(f"entry/{manager_id}/")
# Manager gameweek history
    def get_manager_history(self, manager_id):
        return self.get(f"entry/{manager_id}/history/")
# Manager picks for a specific gameweek       
    def get_manager_picks(self, manager_id, gameweek):
        return self.get(f"entry/{manager_id}/event/{gameweek}/picks/")
# Player data (Player ID, Name, Team, Position, Cost, Points, etc.)         
    def get_players(self):
        return self.get("bootstrap-static/")
# Gameweek player stats (Player ID, Gameweek, Points, Goals, Assists, Clean Sheets, etc.)
    def get_player_history(self, player_id):
        return self.get(f"element-summary/{player_id}/")
# Gameweek player stats for a specific gameweek (Player ID, Gameweek, Points, Goals, Assists, Clean Sheets, etc.)
    def get_player_history(self, player_id):
        return self.get(f"element-summary/{player_id}/")