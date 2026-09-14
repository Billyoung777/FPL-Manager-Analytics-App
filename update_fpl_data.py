import json
import requests


# ==================================================
# SETTINGS
# ==================================================

manager_id = 1053858
filename = "fpl_history.json"


# ==================================================
# GET FPL GAMEWEEK STATUS
# ==================================================

bootstrap_url = (
    "https://fantasy.premierleague.com/api/"
    "bootstrap-static/"
)

response = requests.get(
    bootstrap_url,
    timeout=10
)

response.raise_for_status()

data = response.json()


# ==================================================
# FIND COMPLETED GAMEWEEKS
# ==================================================

completed_gameweeks = []

for event in data["events"]:

    if event["finished"]:
        completed_gameweeks.append(event["id"])


# ==================================================
# LOAD EXISTING DATA
# ==================================================

try:

    with open(filename, "r") as file:
        fpl_data = json.load(file)

except FileNotFoundError:

    fpl_data = {
        "manager_id": manager_id,
        "gameweeks": []
    }


# ==================================================
# EXISTING GAMEWEEKS
# ==================================================

existing_gameweeks = {
    gameweek["gameweek"]
    for gameweek in fpl_data["gameweeks"]
}


# ==================================================
# FIND NEW GAMEWEEKS
# ==================================================

new_gameweeks = [
    gameweek
    for gameweek in completed_gameweeks
    if gameweek not in existing_gameweeks
]


# ==================================================
# DISPLAY STATUS
# ==================================================

print()
print("=" * 60)
print("FPL DATA UPDATE")
print("=" * 60)

print("Manager ID:", manager_id)

print(
    "Completed gameweeks:",
    completed_gameweeks
)

print(
    "Already stored:",
    sorted(existing_gameweeks)
)

print(
    "New gameweeks:",
    new_gameweeks
)


# ==================================================
# FETCH MANAGER HISTORY
# ==================================================

history_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/history/"
)

history_response = requests.get(
    history_url,
    timeout=10
)

history_response.raise_for_status()

history_data = history_response.json()


# ==================================================
# ADD NEW GAMEWEEKS
# ==================================================

for gameweek in new_gameweeks:

    manager_record = None

    for record in history_data["current"]:

        if record["event"] == gameweek:
            manager_record = record
            break

    if manager_record:

        gameweek_data = {
            "gameweek": gameweek,
            "points": manager_record["points"],
            "total_points": manager_record["total_points"],
            "overall_rank": manager_record["overall_rank"],
            "transfers": manager_record["event_transfers"],
            "transfer_cost": manager_record["event_transfers_cost"],
            "bench_points": manager_record["points_on_bench"]
        }

        fpl_data["gameweeks"].append(
            gameweek_data
        )

        print(
            f"Added GW{gameweek}"
        )


# ==================================================
# SORT GAMEWEEKS
# ==================================================

fpl_data["gameweeks"].sort(
    key=lambda gameweek: gameweek["gameweek"]
)


# ==================================================
# SAVE DATA
# ==================================================

with open(filename, "w") as file:

    json.dump(
        fpl_data,
        file,
        indent=4
    )


# ==================================================
# FINAL STATUS
# ==================================================

print()
print("-" * 60)

if new_gameweeks:

    print(
        "Added:",
        len(new_gameweeks),
        "new gameweek(s)"
    )

else:

    print(
        "No new completed gameweeks."
    )

print(
    "Total stored:",
    len(fpl_data["gameweeks"])
)

print(
    "Saved to:",
    filename
)

print("=" * 60)
print("UPDATE COMPLETE")
print("=" * 60)