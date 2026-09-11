import requests


# ==================================================
# SETTINGS
# ==================================================

manager_id = 1053858
gameweek = int(input("Enter gameweek: "))


# ==================================================
# GET MANAGER HISTORY
# ==================================================

history_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/history/"
)

history_response = requests.get(history_url, timeout=10)
history_response.raise_for_status()

history_data = history_response.json()


# Find selected gameweek
manager_data = None

for record in history_data["current"]:

    if record["event"] == gameweek:
        manager_data = record
        break


# ==================================================
# GET MANAGER PICKS
# ==================================================

picks_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/event/{gameweek}/picks/"
)

picks_response = requests.get(picks_url, timeout=10)
picks_response.raise_for_status()

picks_data = picks_response.json()


# ==================================================
# GET PLAYER DATA
# ==================================================

bootstrap_url = (
    "https://fantasy.premierleague.com/api/"
    "bootstrap-static/"
)

bootstrap_response = requests.get(
    bootstrap_url,
    timeout=10
)

bootstrap_response.raise_for_status()

bootstrap_data = bootstrap_response.json()

players = {
    player["id"]: player
    for player in bootstrap_data["elements"]
}


# ==================================================
# PLAYER GAMEWEEK HISTORY
# ==================================================

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


# ==================================================
# FIND CAPTAIN
# ==================================================

captain = None

for pick in picks_data["picks"]:

    if pick["is_captain"]:
        captain = pick
        break


# ==================================================
# CALCULATE BENCH POINTS
# ==================================================

bench_points = 0

for pick in picks_data["picks"]:

    if pick["position"] > 11:

        stats = get_player_gameweek(
            pick["element"],
            gameweek
        )

        if stats:
            bench_points += stats["total_points"]


# ==================================================
# GET CHIP
# ==================================================

chip_used = None

for chip in history_data["chips"]:

    if chip["event"] == gameweek:

        chip_used = chip["name"]
        break


# ==================================================
# COUNT TRANSFERS
# ==================================================

transfers_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/transfers/"
)

transfers_response = requests.get(
    transfers_url,
    timeout=10
)

transfers_response.raise_for_status()

transfers = transfers_response.json()


transfer_count = 0

for transfer in transfers:

    if transfer["event"] == gameweek:
        transfer_count += 1


# ==================================================
# DISPLAY REPORT
# ==================================================

print()
print("=" * 70)
print(f"FPL MANAGER — GAMEWEEK {gameweek}")
print("=" * 70)


# --------------------------------------------------
# PERFORMANCE
# --------------------------------------------------

print()
print("PERFORMANCE")
print("-" * 70)

if manager_data:

    print("Gameweek Points:", manager_data["points"])
    print("Total Points:", manager_data["total_points"])
    print("Overall Rank:", manager_data["overall_rank"])
    print("Transfers:", transfer_count)
    print("Transfer Cost:", manager_data["event_transfers_cost"])
    print("Bench Points:", manager_data["points_on_bench"])

else:

    print("Manager data not available")


# --------------------------------------------------
# CAPTAIN
# --------------------------------------------------

print()
print("CAPTAIN")
print("-" * 70)

if captain:

    player_id = captain["element"]

    player = players[player_id]

    stats = get_player_gameweek(
        player_id,
        gameweek
    )

    if stats:

        raw_points = stats["total_points"]
        multiplier = captain["multiplier"]
        captain_points = raw_points * multiplier

        print("Captain:", player["web_name"])
        print("Raw Points:", raw_points)
        print("Multiplier:", multiplier)
        print("Captain Contribution:", captain_points)

else:

    print("Captain not found")


# --------------------------------------------------
# CHIP
# --------------------------------------------------

print()
print("CHIP")
print("-" * 70)

if chip_used:

    print("Chip:", chip_used)

else:

    print("Chip: None")


# --------------------------------------------------
# TRANSFERS
# --------------------------------------------------

print()
print("TRANSFERS")
print("-" * 70)

print("Transfer Records:", transfer_count)


# --------------------------------------------------
# BENCH
# --------------------------------------------------

print()
print("BENCH")
print("-" * 70)

for pick in picks_data["picks"]:

    if pick["position"] > 11:

        player_id = pick["element"]

        player = players[player_id]

        stats = get_player_gameweek(
            player_id,
            gameweek
        )

        if stats:
            points = stats["total_points"]
        else:
            points = 0

        print(
            f'{player["web_name"]:<18} '
            f'Points: {points}'
        )


print()
print("BENCH POINTS:", bench_points)


# ==================================================
# COMPLETE
# ==================================================

print()
print("=" * 70)
print("GAMEWEEK REPORT COMPLETE")
print("=" * 70)