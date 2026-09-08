import requests

manager_id = 1053858


def get_official_score(gameweek):

    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/history/"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    for record in data["current"]:
        if record["event"] == gameweek:
            return record["points"]

    return None


def get_calculated_score(gameweek):

    picks_url = (
        f"https://fantasy.premierleague.com/api/"
        f"entry/{manager_id}/event/{gameweek}/picks/"
    )

    picks_response = requests.get(picks_url, timeout=10)
    picks_response.raise_for_status()

    picks_data = picks_response.json()

    total_points = 0

    for pick in picks_data["picks"]:

        player_id = pick["element"]
        multiplier = pick["multiplier"]

        player_url = (
            f"https://fantasy.premierleague.com/api/"
            f"element-summary/{player_id}/"
        )

        player_response = requests.get(player_url, timeout=10)
        player_response.raise_for_status()

        player_data = player_response.json()

        for record in player_data["history"]:

            if record["round"] == gameweek:

                points = record["total_points"]

                total_points += points * multiplier

                break

    return total_points


print()
print("FPL SCORE VALIDATION")
print("=" * 50)

for gameweek in range(1, 4):

    calculated = get_calculated_score(gameweek)
    official = get_official_score(gameweek)

    difference = calculated - official

    print()
    print(f"GW{gameweek}")
    print("-" * 50)
    print("Calculated:", calculated)
    print("Official:  ", official)
    print("Difference:", difference)

    if calculated == official:
        print("Status:     MATCH ✓")
    else:
        print("Status:     MISMATCH ✗")

print()
print("=" * 50)
print("VALIDATION COMPLETE")