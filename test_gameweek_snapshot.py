from tracker.gameweek_snapshot import GameweekSnapshot


MANAGER_ID = 1053858
GAMEWEEK = 3

snapshot_tracker = GameweekSnapshot()

snapshot = snapshot_tracker.get_snapshot(
    MANAGER_ID,
    GAMEWEEK
)

print("=" * 60)
print("MANAGER GAMEWEEK SNAPSHOT")
print("=" * 60)

print("Manager ID:", snapshot["manager_id"])
print("Gameweek:", snapshot["gameweek"])

analysis = snapshot["analysis"]
performances = snapshot["performances"]
official = snapshot["official"]
chip = snapshot["chip"]
transfers = snapshot["transfers"]

print("\nOfficial FPL Data:")

#This section prints the official FPL data for the specified gameweek, including points scored, total points, and overall rank. If no official gameweek data is found, it prints a message indicating that.
if official:
    print("Official Points:", official["points"])
    print("Total Points:", official["total_points"])
    print("Overall Rank:", official["overall_rank"])
else:
    print("No official gameweek data found.")

if official:
    if analysis["manager_score"] == official["points"]:
        print("Score Validation: PASS")
    else:
        print("Score Validation: FAIL")

print("\nChip:")

#This section prints the chip used by a manager for the specified gameweek. If a chip was used, it prints the name of the chip; otherwise, it prints "None" to indicate that no chip was used during that gameweek.
if chip:
    print(chip["name"])
else:
    print("None")

#This section prints the starting XI and bench players along with their positions and points scored in the specified gameweek. It also prints the total points for the starting XI, bench, captain, and the manager's overall score for that gameweek.
print("\nStarting XI:")
print("\nTransfers:")
print("\nTransfers:")
print("Transfers Found:", len(transfers))

for transfer in transfers:
    print(
        f"{transfer['player_out']} -> "
        f"{transfer['player_in']}"
    )

#This section prints the starting XI and bench players along with their positions and points scored in the specified gameweek. It also prints the total points for the starting XI, bench, captain, and the manager's overall score for that gameweek.
for player in performances:
    if player["is_starting"]:
        print(
            f"{player['player_name']} | "
            f"{player['position_name']} | "
            f"{player['points']} pts"
        )

print("\n")
print("\nBench:")

#This section prints the bench players along with their positions and points scored in the specified gameweek. It also prints the total points for the starting XI, bench, captain, and the manager's overall score for that gameweek.
for player in performances:
    if not player["is_starting"]:
        print(
            f"{player['player_name']} | "
            f"{player['position_name']} | "
            f"{player['points']} pts"
        )

print("Starting XI Points:", analysis["starting_points"])
print("Bench Points:", analysis["bench_points"])
print("Captain Points:", analysis["captain_points"])
print("Manager Score:", analysis["manager_score"])

print("=" * 60)
