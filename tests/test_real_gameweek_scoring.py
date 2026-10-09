
import requests

MANAGER_ID = 1053858
GAMEWEEK = 5
url = (
    "https://fantasy.premierleague.com/api/"
    f"entry/{MANAGER_ID}/event/{GAMEWEEK}/picks/"
)

print("=" * 60)
print("REAL FPL GAMEWEEK DATA INSPECTION")
print("=" * 60)

response = requests.get(url, timeout=20)
response.raise_for_status()

data = response.json()

print("Manager ID:", MANAGER_ID)
print("Gameweek:", GAMEWEEK)

print("\nENTRY HISTORY")
print(data.get("entry_history"))

print("\nAUTOMATIC SUBSTITUTIONS")
print(data.get("automatic_subs"))

print("\nSQUAD PICKS")
for pick in data.get("picks", []):
    print(
        "Player ID:", pick["element"],
        "| Position:", pick["position"],
        "| Multiplier:", pick["multiplier"],
        "| Captain:", pick["is_captain"],
        "| Vice:", pick["is_vice_captain"],
    )

print("\nTotal picks:", len(data.get("picks", [])))
print("=" * 60)


print(f"\nGW{GAMEWEEK} PLAYER PERFORMANCE")
print("-" * 60)

base_url = "https://fantasy.premierleague.com/api/"

bootstrap_response = requests.get(
    base_url + "bootstrap-static/",
    timeout=20
)
bootstrap_response.raise_for_status()

live_response = requests.get(
    base_url + f"event/{GAMEWEEK}/live/",
    timeout=20
)
live_response.raise_for_status()

bootstrap = bootstrap_response.json()
live_data = live_response.json()

players_by_id = {
    player["id"]: player
    for player in bootstrap["elements"]
}

live_by_id = {
    player["id"]: player
    for player in live_data["elements"]
}

for pick in data["picks"]:
    player_id = pick["element"]

    player = players_by_id[player_id]
    live_player = live_by_id[player_id]

    minutes = live_player["stats"]["minutes"]
    points = live_player["stats"]["total_points"]

    print(
        f"{player['web_name']:<18}"
        f" | Minutes: {minutes:>3}"
        f" | Points: {points:>3}"
        f" | Multiplier: {pick['multiplier']}"
    )



from tracker.scoring_engine import ScoringEngine

print(f"\nREAL GW{GAMEWEEK} SCORING VALIDATION")
print("-" * 60)

engine = ScoringEngine()

position_names = {
    position["id"]: position["singular_name"]
    for position in bootstrap["element_types"]
}

performances = []

for pick in data["picks"]:
    player_id = pick["element"]
    player = players_by_id[player_id]
    stats = live_by_id[player_id]["stats"]

    performances.append({
        "player_id": player_id,
        "player_name": player["web_name"],
        "position_name": position_names[
            player["element_type"]
        ],
        "minutes": stats["minutes"],
        "points": stats["total_points"],
        "is_starting": pick["position"] <= 11,
        "squad_position": pick["position"],
        "is_captain": pick["is_captain"],
        "is_vice_captain": pick["is_vice_captain"],
    })

result = engine.calculate_gameweek_points(performances)

official_points = data["entry_history"]["points"]
calculated_points = result["total_points"]

print("Official FPL points:", official_points)
print("ScoringEngine points:", calculated_points)
print("Base points:", result["base_points"])
print("Captain bonus:", result["captain_bonus"])

official_subs = data.get("automatic_subs", [])
engine_subs = result["substitutions"]

print("Official automatic substitutions:", len(official_subs))
print("Engine automatic substitutions:", len(engine_subs))

for sub in official_subs:
    player_out = players_by_id[sub["element_out"]]["web_name"]
    player_in = players_by_id[sub["element_in"]]["web_name"]

    print(f"Official substitution: {player_out} -> {player_in}")

if official_subs:
    print(
        "Note: API picks are already finalized; "
        "independent substitution replay not yet validated."
    )

print("Formation valid:", result["formation_valid"])

assert len(performances) == 15
assert result["formation_valid"]
assert calculated_points == official_points

print(f"REAL GW{GAMEWEEK} SCORING VALIDATION: PASS")


print(f"\nGW{GAMEWEEK} AUTO-SUB REPLAY")
print("-" * 60)

if official_subs:
    original_performances = [
        player.copy() for player in performances
    ]

    for sub in official_subs:
        player_out = next(
            player for player in original_performances
            if player["player_id"] == sub["element_out"]
        )

        player_in = next(
            player for player in original_performances
            if player["player_id"] == sub["element_in"]
        )

        player_out["is_starting"] = True
        player_in["is_starting"] = False

        player_out["squad_position"], player_in["squad_position"] = (
            player_in["squad_position"],
            player_out["squad_position"],
        )

    replay = engine.calculate_gameweek_points(
        original_performances
    )

    print("Official substitutions:", official_subs)
    print("Engine substitutions:", replay["substitutions"])
    print("Official points:", official_points)
    print("Replay points:", replay["total_points"])
    print("Formation valid:", replay["formation_valid"])
else:
    print("No official automatic substitutions to replay.")
