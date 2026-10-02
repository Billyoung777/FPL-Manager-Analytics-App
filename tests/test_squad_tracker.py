from tracker.squad_tracker import SquadTracker


tracker = SquadTracker()

squad = tracker.get_gameweek_squad(1053858, 5)

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
    5
)

for squad in historical_squads:
    print(
        f"GW{squad['gameweek']} | "
        f"Starting XI: {len(squad['starting_xi'])} | "
        f"Bench: {len(squad['bench'])} | "
        f"Captain: {squad['captain']['player_name']} | "
        f"Vice: {squad['vice_captain']['player_name']}"
    )

#this section tests the get_gameweek_squad method of the SquadTracker class, which retrieves the squad of a manager for a specific gameweek. It prints out the details of the starting XI, bench, captain, and vice-captain. It also tests the get_historical_squads method to retrieve and print historical squad information for the last 5 gameweeks.
gw5_squad = tracker.get_gameweek_squad(
    1053858,
    5
)

print("\nGW5 OFFICIAL AUTO-SUBS")
print("-" * 60)

for auto_sub in gw5_squad["automatic_subs"]:
    print(
        f"OUT ID: {auto_sub['element_out']} | "
        f"IN ID: {auto_sub['element_in']}"
    )

original_gw5 = tracker.reconstruct_pre_auto_sub_squad(
    gw5_squad
)

print("\nGW5 RECONSTRUCTED PRE-AUTO-SUB SQUAD")
print("-" * 60)

print("Starting XI:")

for player in original_gw5["starting_xi"]:
    print(
        f"- {player['player_name']} "
        f"(ID {player['element']})"
    )

print("\nBench:")

for player in original_gw5["bench"]:
    print(
        f"- {player['player_name']} "
        f"(ID {player['element']})"
        
    )