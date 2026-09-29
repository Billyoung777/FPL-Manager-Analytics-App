from tracker.gameweek_snapshot import GameweekSnapshot


MANAGER_ID = 1053858
GAMEWEEK = 5

snapshot_tracker = GameweekSnapshot()

snapshot = snapshot_tracker.get_snapshot(
    MANAGER_ID,
    GAMEWEEK
)

analysis = snapshot["analysis"]
performances = snapshot["performances"]
official = snapshot["official"]
chip = snapshot["chip"]
transfers = snapshot["transfers"]
squad_changes = snapshot["squad_changes"]


print("=" * 60)
print("MANAGER GAMEWEEK SNAPSHOT")
print("=" * 60)

print(f"Manager ID: {MANAGER_ID}")
print(f"Gameweek: {GAMEWEEK}")


# Chip
print("\nChip:")
if chip:
    print(chip["name"])
else:
    print("None")


# Transfers
print("\nTransfers:")
print(f"Transfers Found: {len(transfers)}")

if transfers:
    for transfer in transfers:
        print(
            f"{transfer['player_out']} -> "
            f"{transfer['player_in']}"
        )
else:
    print("None")

# Squad Changes
print("\nNet Squad Changes:")

print("Players Out:")
if squad_changes["players_out"]:
    for player in squad_changes["players_out"]:
        print(
            f"- {player['player_name']} | "
            f"{player['position']}"
        )
else:
    print("- None")

print("\nPlayers In:")
if squad_changes["players_in"]:
    for player in squad_changes["players_in"]:
        print(
            f"- {player['player_name']} | "
            f"{player['position']}"
        )
else:
    print("- None")


# Starting XI
print("\nStarting XI:")

for player in performances:
    if player["is_starting"]:
        print(
            f"{player['player_name']} | "
            f"{player['position_name']} | "
            f"{player['points']} pts"
        )


# Bench
print("\nBench:")

for player in performances:
    if not player["is_starting"]:
        print(
            f"{player['player_name']} | "
            f"{player['position_name']} | "
            f"{player['points']} pts"
        )


# Calculated analysis
print("\n" + "-" * 60)
print("GAMEWEEK ANALYSIS")
print("-" * 60)

print("Raw Squad Points:", analysis["total_squad_points"])
print("Starting XI Points:", analysis["starting_points"])
print("Bench Points:", analysis["bench_points"])
print("Captain Points:", analysis["captain_points"])
print("Captain Bonus:", analysis["captain_bonus"])
print("Calculated Manager Score:", analysis["manager_score"])


# Official FPL data
print("\n" + "-" * 60)
print("OFFICIAL FPL DATA")
print("-" * 60)

if official:
    print("Official GW Points:", official["points"])
    print("Total Points:", official["total_points"])
    print("Overall Rank:", official["overall_rank"])

    if analysis["manager_score"] == official["points"]:
        print("Score Validation: PASS")
    else:
        print("Score Validation: FAIL")
else:
    print("No official gameweek data found.")

# Additional Official FPL data
print(
    f"Transfer Cost: "
    f"{snapshot['official_metrics']['event_transfers_cost']}"
)

print(
    f"Official Bench Points: "
    f"{snapshot['official_metrics']['points_on_bench']}"
)
print(
    f"Official Transfers: "
    f"{snapshot['official_metrics']['event_transfers']}"
)


print("=" * 60)
print("SNAPSHOT COMPLETE")
print("=" * 60)