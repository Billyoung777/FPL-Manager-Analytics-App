from tracker.scoring_engine import ScoringEngine


engine = ScoringEngine()


played_player = {
    "player_name": "Test Player A",
    "minutes": 90,
}

non_playing_player = {
    "player_name": "Test Player B",
    "minutes": 0,
}


print("=" * 60)
print("FPL SCORING ENGINE")
print("=" * 60)

print(
    f"{played_player['player_name']} played: "
    f"{engine.player_played(played_player)}"
)

print(
    f"{non_playing_player['player_name']} played: "
    f"{engine.player_played(non_playing_player)}"
)

#The following section tests the get_non_playing_starters method of the ScoringEngine class, which identifies players who were in the starting lineup but did not play any minutes in a gameweek. It creates a list of player performances and checks for non-playing starters.
performances = [
    {
        "player_name": "Starting Defender",
        "position_name": "Defender",
        "minutes": 90,
        "is_starting": True,
    },
    {
        "player_name": "Starting Midfielder",
        "position_name": "Midfielder",
        "minutes": 0,
        "is_starting": True,
    },
    {
        "player_name": "Bench Forward",
        "position_name": "Forward",
        "minutes": 90,
        "is_starting": False,
    },
]

non_playing_starters = engine.get_non_playing_starters(
    performances
)

print("\nNon-playing starters:")

for player in non_playing_starters:
    print(
        f"- {player['player_name']} | "
        f"{player['position_name']} | "
        f"{player['minutes']} mins"
    )

print("=" * 60)
print("SCORING ENGINE TEST COMPLETE")
print("=" * 60)