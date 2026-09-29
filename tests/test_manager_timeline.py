from tracker.manager_timeline import ManagerTimeline


MANAGER_ID = 1053858

timeline_tracker = ManagerTimeline()

timeline = timeline_tracker.build_timeline(
    MANAGER_ID
)
summary = timeline_tracker.get_timeline_summary(
    timeline
)

#The following section prints the manager's timeline, including gameweek scores, official points, chips used, and squad changes for each gameweek.
print("=" * 70)
print("FPL MANAGER TIMELINE")
print("=" * 70)

print(f"Manager ID: {MANAGER_ID}")
print(f"Gameweeks Found: {len(timeline)}")

#The following section prints a summary of the manager's season, including total gameweeks, total points, average points, highest and lowest gameweek scores, total players in and out, and chips used.
print("\n" + "-" * 70)
print("SEASON TIMELINE")
print("-" * 70)

for snapshot in timeline:
    gameweek = snapshot["gameweek"]
    analysis = snapshot["analysis"]
    official = snapshot["official"]
    official_metrics = snapshot["official_metrics"]
    chip = snapshot["chip"]
    squad_changes = snapshot["squad_changes"]

    if chip:
        chip_name = chip["name"]
    else:
        chip_name = "None"

    transfer_cost = official_metrics["event_transfers_cost"]
    bench_points = official_metrics["points_on_bench"]

    print(
        f"GW{gameweek} | "
        f"Score: {analysis['manager_score']} | "
        f"Official: {official['points']} | "
        f"Transfer Cost: {transfer_cost} | "
        f"Bench: {bench_points} | "
        f"Chip: {chip_name} | "
        f"IN: {len(squad_changes['players_in'])} | "
        f"OUT: {len(squad_changes['players_out'])}"
    )

#The following section prints a summary of the manager's season, including total gameweeks, total points, average points, highest and lowest gameweek scores, total players in and out, and chips used.
print("\n" + "-" * 70)
print("SEASON SUMMARY")
print("-" * 70)

print("Gameweeks:", summary["gameweeks"])
print("Total Points:", summary["total_points"])
print("Average Points:", summary["average_points"])

print(
    "Highest Gameweek:",
    f"GW{summary['highest_gameweek']['gameweek']} "
    f"({summary['highest_gameweek']['points']} pts)"
)

print(
    "Lowest Gameweek:",
    f"GW{summary['lowest_gameweek']['gameweek']} "
    f"({summary['lowest_gameweek']['points']} pts)"
)

print("Total Players In:", summary["total_players_in"])
print("Total Players Out:", summary["total_players_out"])

print("Chips Used:")

if summary["chips_used"]:
    for chip in summary["chips_used"]:
        print(
            f"- {chip['name']} | "
            f"GW{chip['gameweek']}"
        )
else:
    print("- None")


print("=" * 70)
print("TIMELINE COMPLETE")
print("=" * 70)