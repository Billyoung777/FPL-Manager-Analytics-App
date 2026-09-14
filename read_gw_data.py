import json


# ==================================================
# READ JSON FILE
# ==================================================

filename = "fpl_history.json"

with open(filename, "r") as file:

    fpl_data = json.load(file)


# ==================================================
# GET MANAGER INFORMATION
# ==================================================

manager_id = fpl_data["manager_id"]

gameweeks = fpl_data["gameweeks"]


# ==================================================
# DISPLAY DATA
# ==================================================

print()
print("=" * 60)
print("FPL MANAGER HISTORY")
print("=" * 60)

print("Manager ID:", manager_id)
print("Gameweeks:", len(gameweeks))

print()


# ==================================================
# DISPLAY EACH GAMEWEEK
# ==================================================

for gameweek in gameweeks:

    print(
        f'GW{gameweek["gameweek"]} | '
        f'Points: {gameweek["points"]} | '
        f'Total: {gameweek["total_points"]} | '
        f'Rank: {gameweek["overall_rank"]}'
    )


print()
print("=" * 60)
print("DATA READ COMPLETE")
print("=" * 60)