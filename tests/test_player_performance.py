from api.fpl_client import FPLClient
from tracker.player_performance import PlayerPerformanceTracker


MANAGER_ID = 1053858

client = FPLClient()
tracker = PlayerPerformanceTracker(client)


# Find the latest completed gameweek
latest_finished_gameweek = client.get_latest_finished_gameweek()

print("=" * 60)
print("FPL PLAYER PERFORMANCE TRACKER")
print("=" * 60)

print(f"Manager ID: {MANAGER_ID}")
print(f"Latest Finished Gameweek: GW{latest_finished_gameweek}")

# Analyze every completed gameweek
multi_gameweek_analysis = tracker.analyze_gameweeks(
    MANAGER_ID,
    1,
    latest_finished_gameweek
)

print("\n" + "-" * 60)
print("GAMEWEEK PERFORMANCE")
print("-" * 60)

for analysis in multi_gameweek_analysis:
    print(
        f"GW{analysis['gameweek']} | "
        f"Raw: {analysis['total_squad_points']} | "
        f"Starting: {analysis['starting_points']} | "
        f"Bench: {analysis['bench_points']} | "
        f"Captain: {analysis['captain_points']} | "
        f"Score: {analysis['manager_score']} | "
        f"Multiplier Score: {analysis['multiplier_score']}"
    )
print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)