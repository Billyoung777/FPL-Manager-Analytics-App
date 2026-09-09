import requests

manager_id = 1053858
gameweek = int(input("Enter gameweek: "))


# Get manager's GW squad
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


# Calculate bench points
bench_points = 0

print()
print(f"GW{gameweek} BENCH POINTS")
print("=" * 50)

for pick in picks_data["picks"]:

    if pick["position"] > 11:

        player_id = pick["element"]

        player = players[player_id]

        stats = get_player_gameweek(player_id, gameweek)

        if stats:
            points = stats["total_points"]
        else:
            points = 0

        bench_points += points

        print(
            f'{player["web_name"]:<18} '
            f'Points: {points}'
        )


print()
print("-" * 50)
print("Total Bench Points:", bench_points)
print("=" * 50)