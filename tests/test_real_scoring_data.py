from api.fpl_client import FPLClient
from tracker.squad_tracker import SquadTracker
from tracker.player_performance import PlayerPerformanceTracker


MANAGER_ID = 1053858
START_GAMEWEEK = 1
END_GAMEWEEK = 5


client = FPLClient()
squad_tracker = SquadTracker(client)
performance_tracker = PlayerPerformanceTracker(client)


print("=" * 90)
print("REAL FPL AUTO-SUB INSPECTION")
print("=" * 90)

for gameweek in range(
    START_GAMEWEEK,
    END_GAMEWEEK + 1
):
    squad = squad_tracker.get_gameweek_squad(
        MANAGER_ID,
        gameweek
    )

    performances = (
        performance_tracker.get_squad_performance(
            squad,
            gameweek
        )
    )

    print(f"\nGAMEWEEK {gameweek}")
    print("-" * 90)

    print(
        f"{'Player':<20}"
        f"{'Position':<15}"
        f"{'Slot':<8}"
        f"{'Minutes':<10}"
        f"{'Multiplier':<12}"
        f"{'Status':<10}"
    )

    print("-" * 90)

    for player in sorted(
        performances,
        key=lambda item: item["squad_position"]
    ):
        status = (
            "START"
            if player["is_starting"]
            else "BENCH"
        )

        marker = ""

        if player["minutes"] == 0:
            marker = " <-- DID NOT PLAY"

        print(
            f"{player['player_name']:<20}"
            f"{player['position_name']:<15}"
            f"{player['squad_position']:<8}"
            f"{player['minutes']:<10}"
            f"{player['multiplier']:<12}"
            f"{status:<10}"
            f"{marker}"
        )

print("\n" + "=" * 90)
print("INSPECTION COMPLETE")
print("=" * 90)

raw_picks = client.get_manager_picks(
    MANAGER_ID,
    5
)

players_data = client.get_players()

player_lookup = {
    player["id"]: player["web_name"]
    for player in players_data["elements"]
}

print("\nRAW GW5 PICKS")
print("-" * 90)

for pick in raw_picks["picks"]:
    player_name = player_lookup.get(
        pick["element"],
        "Unknown"
    )

    print(
        f"{player_name:<20} | "
        f"position={pick['position']} | "
        f"multiplier={pick['multiplier']} | "
        f"captain={pick['is_captain']} | "
        f"vice={pick['is_vice_captain']}"
    )

print("\nAUTOMATIC SUBSTITUTIONS")
print("-" * 90)

print(
    raw_picks.get(
        "automatic_subs",
        "automatic_subs field not found"
    )
)
print("\nGW5 AUTO-SUB DETAILS")
print("-" * 90)

for auto_sub in raw_picks["automatic_subs"]:
    player_in = player_lookup.get(
        auto_sub["element_in"],
        "Unknown"
    )

    player_out = player_lookup.get(
        auto_sub["element_out"],
        "Unknown"
    )

    print(
        f"OUT: {player_out} "
        f"(ID {auto_sub['element_out']})"
    )

    print(
        f"IN:  {player_in} "
        f"(ID {auto_sub['element_in']})"
    )