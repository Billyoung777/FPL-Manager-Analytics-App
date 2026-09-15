from tracker.squad_tracker import SquadTracker


tracker = SquadTracker()

squad = tracker.get_gameweek_squad(1053858, 4)

print("Squad retrieved successfully!")
print("Gameweek:", squad["gameweek"])
print("Starting XI:", len(squad["starting_xi"]))
print("Bench:", len(squad["bench"]))

print(
    "Captain:",
    squad["captain"]["element"]
)

print(
    "Vice-captain:",
    squad["vice_captain"]["element"]
)

print("\nStarting XI:")
for player in squad["starting_xi"]:
    print(
        f"Player ID: {player['element']} | "
        f"Player: {player['player_name']} | "
        f"Position: {player['position_name']} | "
        f"Multiplier: {player['multiplier']}"
    )

print("\nBench:")
for player in squad["bench"]:
    print(
        f"Player ID: {player['element']} | "
        f"Player: {player['player_name']} | "
        f"Position: {player['position_name']}"
    )

print("\nHistorical Squad Test:")

historical_squads = tracker.get_historical_squads(
    1053858,
    4
)

for squad in historical_squads:
    print(
        f"GW{squad['gameweek']} | "
        f"Starting XI: {len(squad['starting_xi'])} | "
        f"Bench: {len(squad['bench'])} | "
        f"Captain: {squad['captain']['player_name']} | "
        f"Vice: {squad['vice_captain']['player_name']}"
    )