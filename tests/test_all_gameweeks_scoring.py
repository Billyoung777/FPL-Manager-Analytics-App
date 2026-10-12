
import requests
from tracker.scoring_engine import ScoringEngine

MANAGER_ID = 1053858

BASE_URL = "https://fantasy.premierleague.com/api"

print("=" * 60)
print("AUTOMATED FPL GAMEWEEK VALIDATION")
print("=" * 60)

# Fetch manager history.
history_url = f"{BASE_URL}/entry/{MANAGER_ID}/history/"

response = requests.get(history_url, timeout=30)
response.raise_for_status()

history_data = response.json()

gameweeks = history_data["current"]

# Fetch official gameweek completion statuses.
events_response = requests.get(
    f"{BASE_URL}/bootstrap-static/",
    timeout=30
)
events_response.raise_for_status()

events = {
    event["id"]: event
    for event in events_response.json()["events"]
}

# Validate only finalized gameweeks.
completed_gameweeks = [
    gw for gw in gameweeks
    if events.get(gw["event"], {}).get("finished") is True
    and events.get(gw["event"], {}).get("data_checked") is True
]

print(
    f"\nFinalized gameweeks available: "
    f"{len(completed_gameweeks)}"
)

skipped = [
    gw["event"] for gw in gameweeks
    if gw not in completed_gameweeks
]

if skipped:
    print(f"Unfinished gameweeks skipped: {skipped}")

gameweeks = completed_gameweeks


print(f"\nManager ID: {MANAGER_ID}")
print(f"Gameweeks found: {len(gameweeks)}")

print("\nOFFICIAL GAMEWEEK HISTORY")
print("-" * 60)

for gw in gameweeks:
    print(
        f"GW{gw['event']} | "
        f"Points: {gw['points']} | "
        f"Total: {gw['total_points']} | "
        f"Transfer cost: {gw['event_transfers_cost']}"
    )


print("\nGAMEWEEK SQUAD VALIDATION")
print("-" * 60)

for gw in gameweeks:
    gw_number = gw["event"]

    picks_url = (
        f"{BASE_URL}/entry/{MANAGER_ID}/"
        f"event/{gw_number}/picks/"
    )

    picks_response = requests.get(
        picks_url,
        timeout=30
    )
    picks_response.raise_for_status()

    picks_data = picks_response.json()

    picks = picks_data["picks"]
    active_chip = picks_data.get("active_chip")

    print(
        f"GW{gw_number} | "
        f"Players: {len(picks)} | "
        f"Chip: {active_chip}"
    )

    assert len(picks) == 15, (
        f"GW{gw_number}: Expected 15 players, "
        f"found {len(picks)}"
    )

print("\nALL GAMEWEEK SQUADS: PASS")

print("\nGAMEWEEK HISTORY RETRIEVAL: PASS")

print("\nAUTOMATED GAMEWEEK SCORING")
print("-" * 60)

engine = ScoringEngine()

# Fetch player and position information once.
bootstrap_response = requests.get(
    f"{BASE_URL}/bootstrap-static/",
    timeout=30
)
bootstrap_response.raise_for_status()

bootstrap = bootstrap_response.json()

players_by_id = {
    player["id"]: player
    for player in bootstrap["elements"]
}

position_names = {
    position["id"]: position["singular_name"]
    for position in bootstrap["element_types"]
}

passed = 0
failed = 0

for gw in gameweeks:
    gw_number = gw["event"]

    # Fetch finalized squad picks.
    picks_response = requests.get(
        f"{BASE_URL}/entry/{MANAGER_ID}/event/{gw_number}/picks/",
        timeout=30
    )
    picks_response.raise_for_status()

    picks_data = picks_response.json()

    # Fetch actual player performance for the gameweek.
    live_response = requests.get(
        f"{BASE_URL}/event/{gw_number}/live/",
        timeout=30
    )
    live_response.raise_for_status()

    live_data = live_response.json()

    live_by_id = {
        player["id"]: player
        for player in live_data["elements"]
    }

    performances = []

    for pick in picks_data["picks"]:
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
        active_chip=picks_data.get("active_chip"),
        transfer_cost=gw["event_transfers_cost"]
    )


    if gw_number == 6:
        print("\n" + "=" * 60)
        print("GW6 SCORING DEBUG")
        print("=" * 60)

        for pick, performance in zip(
            picks_data["picks"], performances
        ):
            print(
                f"{performance['player_name']:<20} "
                f"Position: {pick['position']:<2} "
                f"Multiplier: {pick['multiplier']} "
                f"Minutes: {performance['minutes']:<3} "
                f"Points: {performance['points']:<3} "
                f"Captain: {performance['is_captain']} "
                f"Vice: {performance['is_vice_captain']}"
            )

        print("\nOFFICIAL AUTO SUBSTITUTIONS:")
        print(picks_data.get("automatic_subs", []))

        print("\nACTIVE CHIP:")
        print(picks_data.get("active_chip"))

        print("\nSCORING ENGINE RESULT:")
        print(result)

        print("\nOFFICIAL ENTRY HISTORY:")
        print(picks_data.get("entry_history"))

    official_points = gw["points"]
    calculated_points = result["total_points"]

    status = (
        "PASS"
        if calculated_points == official_points
        and result["formation_valid"]
        else "FAIL"
    )

    print(
        f"GW{gw_number} | "
        f"Official: {official_points} | "
        f"Engine: {calculated_points} | "
        f"{status}"
    )

    if status == "PASS":
        passed += 1
    else:
        failed += 1

print("-" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total checked: {len(gameweeks)}")

assert failed == 0, (
    f"{failed} gameweeks failed scoring validation"
)

print("\nALL GAMEWEEK SCORING VALIDATIONS: PASS")
