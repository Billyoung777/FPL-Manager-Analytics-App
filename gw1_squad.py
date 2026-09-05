import requests

manager_id = 1053858
gameweek = 1

# Get manager's GW1 squad
picks_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/"

picks_response = requests.get(picks_url)
picks_data = picks_response.json()

# Get all FPL players
bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url)
bootstrap_data = bootstrap_response.json()

players = bootstrap_data["elements"]

# Create a player ID -> player name lookup
player_lookup = {
    player["id"]: player["web_name"]
    for player in players
}

# Display our squad
print("MY GW1 SQUAD")
print("----------------------")

for pick in picks_data["picks"]:
    player_id = pick["element"]
    player_name = player_lookup[player_id]

    print(player_id, "-", player_name)