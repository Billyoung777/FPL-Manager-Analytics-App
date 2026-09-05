import requests

manager_id = 1053858
gameweek = 1

# -------------------------
# 1. Get GW1 squad
# -------------------------

picks_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/"

picks_response = requests.get(picks_url)
picks_data = picks_response.json()


# -------------------------
# 2. Get all player data
# -------------------------

bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url)
bootstrap_data = bootstrap_response.json()

players = bootstrap_data["elements"]


# -------------------------
# 3. Create player lookup
# -------------------------

player_lookup = {
    player["id"]: player
    for player in players
}


# -------------------------
# 4. Display our GW1 squad
# -------------------------

print("MY GW1 SQUAD")
print("=" * 50)

for pick in picks_data["picks"]:

    player_id = pick["element"]

    player = player_lookup[player_id]

    print(
        player["web_name"],
        "-",
        "GW Points:",
        player["event_points"]
    )