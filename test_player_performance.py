from tracker.player_performance import PlayerPerformanceTracker


tracker = PlayerPerformanceTracker()

performance = tracker.get_player_gameweek_performance(
    154,
    1
)

print("Player performance retrieved successfully!")

print("Player ID:", performance["player_id"])
print("Gameweek:", performance["gameweek"])
print("Points:", performance["points"])
print("Minutes:", performance["minutes"])
print("Goals:", performance["goals"])
print("Assists:", performance["assists"])
print("Clean Sheets:", performance["clean_sheets"])
print("Bonus:", performance["bonus"])
print("BPS:", performance["bps"])
print("Yellow Cards:", performance["yellow_cards"])
print("Red Cards:", performance["red_cards"])
print("Saves:", performance["saves"])

from tracker.squad_tracker import SquadTracker


squad_tracker = SquadTracker()

squad = squad_tracker.get_gameweek_squad(
    1053858,
    2
)

squad_performances = tracker.get_squad_performance(
    squad,
    2
)

print("\nGW1 Squad Performance:")
print("Players found:", len(squad_performances))

print("\nStarting XI:")

for performance in squad_performances:
    if performance["is_starting"]:
        print(
            f"{performance['player_name']} | "
            f"{performance['position_name']} | "
            f"Points: {performance['points']} | "
            f"Minutes: {performance['minutes']} | "
            f"Goals: {performance['goals']} | "
            f"Assists: {performance['assists']}"
        )


print("\nBench:")

for performance in squad_performances:
    if not performance["is_starting"]:
        print(
            f"{performance['player_name']} | "
            f"{performance['position_name']} | "
            f"Points: {performance['points']} | "
            f"Minutes: {performance['minutes']} | "
            f"Goals: {performance['goals']} | "
            f"Assists: {performance['assists']}"
        )

total_squad_points = tracker.calculate_squad_points(
    squad_performances
)

print("\nTotal Squad Player Points:", total_squad_points)

starting_points = tracker.calculate_starting_points(
    squad_performances
)

print("Starting XI Points:", starting_points)

captain_points = tracker.calculate_captain_points(
    squad_performances,
    squad
)
bench_points = tracker.calculate_bench_points(
    squad_performances
)

print("Bench Points:", bench_points)

print("Captain Points:", captain_points)
captain_bonus = tracker.calculate_captain_bonus(
    captain_points
)

print("Captain Bonus:", captain_bonus)

manager_score = tracker.calculate_manager_score(
    starting_points,
    captain_bonus
)

gameweek_analysis = tracker.analyze_gameweek(
    squad,
    2
)

print("\nGameweek Analysis:")
print("Gameweek:", gameweek_analysis["gameweek"])
print("Total Squad Points:", gameweek_analysis["total_squad_points"])
print("Starting XI Points:", gameweek_analysis["starting_points"])
print("Bench Points:", gameweek_analysis["bench_points"])
print("Captain Points:", gameweek_analysis["captain_points"])
print("Captain Bonus:", gameweek_analysis["captain_bonus"])
print("Manager Score:", gameweek_analysis["manager_score"])