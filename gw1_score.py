import requests


def get_player_gameweek(player_id, gameweek):

    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

    response = requests.get(url)

    data = response.json()

    for record in data["history"]:

        if record["round"] == gameweek:
            return record

    return None


manager_id = 1053858

gameweek = int(input("Enter gameweek: "))


# Get manager picks
picks_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/"

picks_response = requests.get(picks_url)

picks_data = picks_response.json()


# Get player information
bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url)

bootstrap_data = bootstrap_response.json()


player_lookup = {
    player["id"]: player["web_name"]
    for player in bootstrap_data["elements"]
}


total_points = 0


print(f"GW{gameweek} MANAGER SCORE")
print("----------------------")


for pick in picks_data["picks"]:

    player_id = pick["element"]

    player_name = player_lookup[player_id]

    stats = get_player_gameweek(player_id, gameweek)

    if stats:

        points = stats["total_points"]

        multiplier = pick["multiplier"]

        contributed_points = points * multiplier

        if multiplier > 0:

            total_points += contributed_points

            print(
                player_name,
                "| Raw:", points,
                "| Multiplier:", multiplier,
                "| Contributed:", contributed_points
            )


print()
print(f"Calculated GW{gameweek} Points:", total_points)
# Get official manager history
history_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/history/"

history_response = requests.get(history_url)

history_data = history_response.json()


official_points = None

for record in history_data["current"]:

    if record["event"] == gameweek:
        official_points = record["points"]
        break


print()
print("VALIDATION")
print("----------------------")
print("Calculated:", total_points)
print("Official:  ", official_points)

if total_points == official_points:
    print("Difference: 0")
    print("Status:     MATCH ✓")
else:
    difference = total_points - official_points
    print("Difference:", difference)
    print("Status:     MISMATCH ✗")