import requests


def get_player_gameweek(player_id, gameweek):

    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

    response = requests.get(url)

    data = response.json()

    for record in data["history"]:

        if record["round"] == gameweek:
            return record

    return None


# Manager and gameweek
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


# Create player ID → player name lookup
player_lookup = {
    player["id"]: player["web_name"]
    for player in bootstrap_data["elements"]
}


print("MY GW1 SQUAD")
print("----------------------")


for pick in picks_data["picks"]:

    player_id = pick["element"]

    player_name = player_lookup[player_id]

    stats = get_player_gameweek(player_id, gameweek)

    if stats:

        points = stats["total_points"]

        if pick["position"] <= 11:
            squad_status = "STARTER"
        else:
            squad_status = "BENCH"

        if pick["is_captain"]:
            captain_status = "CAPTAIN"
        elif pick["is_vice_captain"]:
            captain_status = "VICE-CAPTAIN"
        else:
            captain_status = ""

        print(
            player_name,
            "|",
            squad_status,
            "|",
            captain_status,
            "| Points:", points,
            "| Position:", pick["position"]
        )

    else:

        print(player_name, "| No GW1 data")