import json


# ==================================================
# READ SAVED DATA
# ==================================================

filename = "fpl_history.json"

with open(filename, "r") as file:
    fpl_data = json.load(file)


manager_id = fpl_data["manager_id"]
gameweeks = fpl_data["gameweeks"]


# ==================================================
# BASIC CALCULATIONS
# ==================================================

total_points = gameweeks[-1]["total_points"]

points_list = [
    gameweek["points"]
    for gameweek in gameweeks
]

average_points = sum(points_list) / len(points_list)

highest_gameweek = max(
    gameweeks,
    key=lambda gameweek: gameweek["points"]
)

lowest_gameweek = min(
    gameweeks,
    key=lambda gameweek: gameweek["points"]
)


# ==================================================
# DISPLAY ANALYTICS
# ==================================================

print()
print("=" * 60)
print("FPL MANAGER ANALYTICS")
print("=" * 60)

print("Manager ID:", manager_id)
print()

print("TOTAL POINTS:", total_points)

print(
    "AVERAGE POINTS:",
    round(average_points, 2)
)

print(
    "HIGHEST GW:",
    f'GW{highest_gameweek["gameweek"]}',
    "-",
    highest_gameweek["points"],
    "points"
)

print(
    "LOWEST GW:",
    f'GW{lowest_gameweek["gameweek"]}',
    "-",
    lowest_gameweek["points"],
    "points"
)


# ==================================================
# GAMEWEEK-TO-GAMEWEEK CHANGE
# ==================================================

print()
print("-" * 60)
print("GAMEWEEK POINT CHANGES")
print("-" * 60)

previous_points = None

for gameweek in gameweeks:

    current_points = gameweek["points"]

    if previous_points is None:

        print(
            f'GW{gameweek["gameweek"]}: '
            f'{current_points} points '
            f'(FIRST GAMEWEEK)'
        )

    else:

        change = current_points - previous_points

        if change > 0:
            result = f"+{change}"

        else:
            result = str(change)

        print(
            f'GW{gameweek["gameweek"]}: '
            f'{current_points} points '
            f'({result} vs previous GW)'
        )

    previous_points = current_points


# ==================================================
# COMPLETE
# ==================================================

print()
print("=" * 60)
print("ANALYTICS COMPLETE")
print("=" * 60)