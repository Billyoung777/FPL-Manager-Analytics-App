import requests


# ==============================
# SETTINGS
# ==============================

manager_id = 1053858

gameweek = int(input("Enter gameweek: "))


# ==============================
# GET MANAGER PICKS
# ==============================

picks_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/event/{gameweek}/picks/"
)

picks_response = requests.get(picks_url, timeout=10)
picks_response.raise_for_status()

picks_data = picks_response.json()


# ==============================
# GET PLAYER DATA
# ==============================

bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url, timeout=10)
bootstrap_response.raise_for_status()

bootstrap_data = bootstrap_response.json()


player_lookup = {
    player["id"]: player["web_name"]
    for player in bootstrap_data["elements"]
}


# ==============================
# GET PLAYER GAMEWEEK POINTS
# ==============================

def get_player_gameweek(player_id, gameweek):

    url = (
        f"https://fantasy.premierleague.com/api/"
        f"element-summary/{player_id}/"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    for record in data["history"]:

        if record["round"] == gameweek:
            return record

    return None


# ==============================
# REPORT
# ==============================

print()
print(f"GW{gameweek} SQUAD REPORT")
print("=" * 50)


starting_xi = []
bench = []


for pick in picks_data["picks"]:

    player_id = pick["element"]

    player_name = player_lookup.get(
        player_id,
        f"Unknown Player ({player_id})"
    )

    stats = get_player_gameweek(
        player_id,
        gameweek
    )

    if stats:
        points = stats["total_points"]
    else:
        points = None


    # Captain / Vice-Captain

    if pick["is_captain"]:
        role = "CAPTAIN"

    elif pick["is_vice_captain"]:
        role = "VICE-CAPTAIN"

    else:
        role = ""


    player_info = {
        "name": player_name,
        "points": points,
        "position": pick["position"],
        "role": role
    }


    # Starting XI / Bench

    if pick["position"] <= 11:
        starting_xi.append(player_info)

    else:
        bench.append(player_info)


# ==============================
# STARTING XI
# ==============================

print()
print("STARTING XI")
print("-" * 50)

for player in starting_xi:

    if player["points"] is None:
        points_text = "N/A"
    else:
        points_text = str(player["points"])

    role_text = player["role"]

    print(
        f'{player["name"]:<18} '
        f'Points: {points_text:<3} '
        f'{role_text}'
    )


# ==============================
# BENCH
# ==============================

print()
print("BENCH")
print("-" * 50)

for player in bench:

    if player["points"] is None:
        points_text = "N/A"
    else:
        points_text = str(player["points"])

    print(
        f'{player["name"]:<18} '
        f'Points: {points_text}'
    )


print()
print("=" * 50)
print("REPORT COMPLETE")