import json


# ==================================================
# MANAGER INFORMATION
# ==================================================

manager_id = 1053858


# ==================================================
# GAMEWEEK DATA
# ==================================================

gameweeks = [
    {
        "gameweek": 1,
        "points": 55,
        "total_points": 55,
        "overall_rank": 2935782,
        "transfers": 0,
        "transfer_cost": 0,
        "bench_points": 9,
        "captain": "Haaland",
        "captain_raw_points": 2,
        "captain_contribution": 4,
        "chip": None
    },

    {
        "gameweek": 2,
        "points": 68,
        "total_points": 123,
        "overall_rank": 5574442,
        "transfers": 0,
        "transfer_cost": 0,
        "bench_points": 1,
        "captain": "Haaland",
        "captain_raw_points": 13,
        "captain_contribution": 26,
        "chip": None
    },

    {
        "gameweek": 3,
        "points": 41,
        "total_points": 164,
        "overall_rank": 6693471,
        "transfers": 15,
        "transfer_cost": 0,
        "bench_points": 9,
        "captain": "Haaland",
        "captain_raw_points": 9,
        "captain_contribution": 18,
        "chip": "wildcard"
    }
]


# ==================================================
# COMPLETE DATASET
# ==================================================

fpl_data = {
    "manager_id": manager_id,
    "gameweeks": gameweeks
}


# ==================================================
# SAVE TO JSON
# ==================================================

filename = "fpl_history.json"

with open(filename, "w") as file:

    json.dump(
        fpl_data,
        file,
        indent=4
    )


# ==================================================
# CONFIRMATION
# ==================================================

print()
print("=" * 60)
print("FPL DATA SAVED")
print("=" * 60)

print("Manager ID:", manager_id)
print("Gameweeks saved:", len(gameweeks))
print("File:", filename)

print("=" * 60)