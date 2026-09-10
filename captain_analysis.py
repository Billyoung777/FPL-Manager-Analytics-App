import requests

manager_id = 1053858
gameweek = int(input("Enter gameweek: "))


# Get manager picks
picks_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/event/{gameweek}/picks/"
)

picks_response = requests.get(picks_url, timeout=10)
picks_response.raise_for_status()

picks_data = picks_response.json()


# Get player information
bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url, timeout=10)
bootstrap_response.raise_for_status()

bootstrap_data = bootstrap_response.json()

players = {
    player["id"]: player
    for player in bootstrap_data["elements"]
}


# Get historical player stats
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


# Find captain
captain = None

for pick in picks_data["picks"]:

    if pick["is_captain"]:

        player_id = pick["element"]
        captain = pick

        break


print()
print(f"GW{gameweek} CAPTAIN ANALYSIS")
print("=" * 50)


if captain:

    player_id = captain["element"]
    player = players[player_id]

    stats = get_player_gameweek(player_id, gameweek)

    if stats:

        raw_points = stats["total_points"]
        multiplier = captain["multiplier"]
        captain_points = raw_points * multiplier

        print("Captain:", player["web_name"])
        print("Raw Points:", raw_points)
        print("Multiplier:", multiplier)
        print("Captain Contribution:", captain_points)

    else:

        print("Captain gameweek data not found.")

else:

    print("Captain not found.")


print("=" * 50)