
import requests

MANAGER_ID = 1053858
GAMEWEEK = 3
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

print("\nCHIP INFORMATION")
print("-" * 60)
print("Active chip:", data.get("active_chip"))
print("Transfer cost:", data["entry_history"]["event_transfers_cost"])


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


result = engine.calculate_gameweek_points(
    performances,
    active_chip=data.get("active_chip"),
    transfer_cost=data["entry_history"]["event_transfers_cost"]
)


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
    
    assert replay["total_points"] == official_points
    assert replay["formation_valid"]

    actual_subs = {
        (
            sub["player_out"]["player_id"],
            sub["player_in"]["player_id"],
        )
        for sub in replay["substitutions"]
    }

    expected_subs = {
        (sub["element_out"], sub["element_in"])
        for sub in official_subs
    }

    assert actual_subs == expected_subs, (
        f"Auto-sub mismatch: {actual_subs} != {expected_subs}"
    )

    print(f"REAL GW{GAMEWEEK} AUTO-SUB REPLAY: PASS")

else:
    print("No official automatic substitutions to replay.")



print("\nTRANSFER COST REGRESSION TEST")
print("-" * 60)

normal_result = engine.calculate_gameweek_points(
    performances,
    active_chip=None,
    transfer_cost=4
)

wildcard_result = engine.calculate_gameweek_points(
    performances,
    active_chip="wildcard",
    transfer_cost=4
)

freehit_result = engine.calculate_gameweek_points(
    performances,
    active_chip="freehit",
    transfer_cost=4
)

print("Normal gameweek:", normal_result["total_points"])
print("Wildcard:", wildcard_result["total_points"])
print("Free Hit:", freehit_result["total_points"])

assert normal_result["total_points"] == 37
assert wildcard_result["total_points"] == 41
assert freehit_result["total_points"] == 41

assert normal_result["transfer_cost"] == 4
assert wildcard_result["transfer_cost"] == 0
assert freehit_result["transfer_cost"] == 0

print("TRANSFER COST REGRESSION TEST: PASS")




print("\nTRIPLE CAPTAIN REGRESSION TEST")
print("-" * 60)

normal_result = engine.calculate_gameweek_points(
    performances,
    active_chip=None,
    transfer_cost=0
)

triple_result = engine.calculate_gameweek_points(
    performances,
    active_chip="3xc",
    transfer_cost=0
)

print("Normal captain points:", normal_result["total_points"])
print("Triple Captain points:", triple_result["total_points"])
print("Normal captain bonus:", normal_result["captain_bonus"])
print("Triple Captain bonus:", triple_result["captain_bonus"])

assert normal_result["total_points"] == 41
assert triple_result["total_points"] == 50

assert normal_result["captain_bonus"] == 9
assert triple_result["captain_bonus"] == 18

print("TRIPLE CAPTAIN REGRESSION TEST: PASS")


print("\nBENCH BOOST REGRESSION TEST")
print("-" * 60)

normal_result = engine.calculate_gameweek_points(
    performances,
    active_chip=None,
    transfer_cost=0
)

bench_boost_result = engine.calculate_gameweek_points(
    performances,
    active_chip="bboost",
    transfer_cost=0
)

print("Normal GW points:", normal_result["total_points"])
print("Bench Boost points:", bench_boost_result["total_points"])

print("Normal base points:", normal_result["base_points"])
print("Bench Boost base points:", bench_boost_result["base_points"])

assert normal_result["total_points"] == 41
assert bench_boost_result["total_points"] == 50

assert normal_result["base_points"] == 32
assert bench_boost_result["base_points"] == 41

print("BENCH BOOST REGRESSION TEST: PASS")


print("\nTRIPLE CAPTAIN TO VICE-CAPTAIN TEST")
print("-" * 60)

# Copy GW3 performances without modifying the original data.
tc_vc_performances = [
    player.copy() for player in performances
]

# Simulate the captain not playing.
captain = next(
    player for player in tc_vc_performances
    if player["is_captain"]
)

captain["minutes"] = 0
captain["points"] = 0

# Give the vice-captain 6 points.
vice_captain = next(
    player for player in tc_vc_performances
    if player["is_vice_captain"]
)

vice_captain["minutes"] = 90
vice_captain["points"] = 6

# Calculate normal and Triple Captain results.
normal_result = engine.calculate_gameweek_points(
    tc_vc_performances,
    active_chip=None
)

tc_result = engine.calculate_gameweek_points(
    tc_vc_performances,
    active_chip="3xc"
)

print("Original captain:", captain["player_name"])
print("Vice-captain:", vice_captain["player_name"])
print("Effective captain:", tc_result["effective_captain"]["player_name"])
print("Normal captain bonus:", normal_result["captain_bonus"])
print("Triple Captain bonus:", tc_result["captain_bonus"])

assert tc_result["effective_captain"]["player_id"] == vice_captain["player_id"]
assert normal_result["captain_bonus"] == 6
assert tc_result["captain_bonus"] == 12

assert tc_result["total_points"] - normal_result["total_points"] == 6

print("TRIPLE CAPTAIN TO VICE-CAPTAIN: PASS")


print("\nBENCH BOOST NO DOUBLE-COUNT TEST")
print("-" * 60)

bb_performances = [
    player.copy() for player in performances
]

# Simulate one starting outfield player not playing.
absent_starter = next(
    player for player in bb_performances
    if player["is_starting"]
    and player["position_name"] == "Forward"
    and not player["is_captain"]
)

absent_starter["minutes"] = 0
absent_starter["points"] = 0

bb_result = engine.calculate_gameweek_points(
    bb_performances,
    active_chip="bboost"
)

expected_base = sum(
    player["points"] for player in bb_performances
)

print("Absent starter:", absent_starter["player_name"])
print("Expected base points:", expected_base)
print("Engine base points:", bb_result["base_points"])
print("Number of substitutions:", len(bb_result["substitutions"]))

assert bb_result["substitutions"] == []
assert bb_result["base_points"] == expected_base
assert bb_result["total_points"] == (
    expected_base + bb_result["captain_bonus"]
)

print("BENCH BOOST NO DOUBLE-COUNT: PASS")
