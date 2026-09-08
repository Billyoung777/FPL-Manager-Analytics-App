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


players = {
    player["id"]: player
    for player in bootstrap_data["elements"]
}


# ==============================
# GET GAMEWEEK PLAYER STATS
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
# BUILD SQUAD DATA
# ==============================

starting_xi = []
bench = []


for pick in picks_data["picks"]:

    player_id = pick["element"]

    player = players[player_id]

    stats = get_player_gameweek(
        player_id,
        gameweek
    )

    if stats:
        minutes = stats["minutes"]
        points = stats["total_points"]
    else:
        minutes = None
        points = None

    player_data = {
        "id": player_id,
        "name": player["web_name"],
        "position": pick["position"],
        "element_type": player["element_type"],
        "minutes": minutes,
        "points": points
    }

    if pick["position"] <= 11:
        starting_xi.append(player_data)
    else:
        bench.append(player_data)


# ==============================
# SHOW STARTING XI
# ==============================

print()
print(f"GW{gameweek} AUTO-SUBSTITUTION CHECK")
print("=" * 60)

print()
print("STARTING XI")
print("-" * 60)

for player in starting_xi:

    status = "PLAYED"

    if player["minutes"] == 0:
        status = "DID NOT PLAY"

    print(
        f'{player["name"]:<18} '
        f'Minutes: {str(player["minutes"]):<3} '
        f'Points: {str(player["points"]):<3} '
        f'{status}'
    )


# ==============================
# FIND PLAYERS WHO DID NOT PLAY
# ==============================

did_not_play = [
    player
    for player in starting_xi
    if player["minutes"] == 0
]


print()
print("STARTERS WHO DID NOT PLAY")
print("-" * 60)

if did_not_play:

    for player in did_not_play:
        print(
            f'{player["name"]} '
            f'(Position Type: {player["element_type"]})'
        )

else:

    print("None")


# ==============================
# SHOW BENCH
# ==============================

print()
print("BENCH ORDER")
print("-" * 60)

for player in bench:

    print(
        f'Bench {player["position"] - 11}: '
        f'{player["name"]:<18} '
        f'Minutes: {str(player["minutes"]):<3} '
        f'Points: {str(player["points"]):<3}'
    )


# ==============================
# BASIC AUTO-SUB CHECK
# ==============================

print()
print("AUTO-SUBSTITUTION ANALYSIS")
print("-" * 60)

if not did_not_play:

    print("No automatic substitutions required.")

else:

    for missing_player in did_not_play:

        replacement_found = False

        for bench_player in bench:

            # Bench player must have played
            if bench_player["minutes"] == 0:
                continue

            # Check formation after replacement
            test_team = [
                player
                for player in starting_xi
                if player["id"] != missing_player["id"]
            ]

            test_team.append(bench_player)

            goalkeeper_count = sum(
                player["element_type"] == 1
                for player in test_team
            )

            defender_count = sum(
                player["element_type"] == 2
                for player in test_team
            )

            midfielder_count = sum(
                player["element_type"] == 3
                for player in test_team
            )

            forward_count = sum(
                player["element_type"] == 4
                for player in test_team
            )

            valid_formation = (
                goalkeeper_count == 1
                and defender_count >= 3
                and midfielder_count >= 2
                and forward_count >= 1
            )

            if valid_formation:

                print(
                    f'{missing_player["name"]} '
                    f'-> '
                    f'{bench_player["name"]}'
                )

                replacement_found = True
                break

        if not replacement_found:

            print(
                f'{missing_player["name"]} '
                f'-> No valid replacement found'
            )


print()
print("=" * 60)
print("AUTO-SUB CHECK COMPLETE")