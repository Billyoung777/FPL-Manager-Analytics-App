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
        "squad_position": 2,
    },
    {
        "player_name": "Starting Midfielder",
        "position_name": "Midfielder",
        "minutes": 0,
        "is_starting": True,
        "squad_position": 6,
    },
    {
        "player_name": "Bench Defender",
        "position_name": "Defender",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 14,
    },
    {
        "player_name": "Bench Goalkeeper",
        "position_name": "Goalkeeper",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 12,
    },
    {
        "player_name": "Bench Forward",
        "position_name": "Forward",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 13,
    },
    {
        "player_name": "Bench Midfielder",
        "position_name": "Midfielder",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 15,
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
#bench ordering test
ordered_bench = engine.get_ordered_bench(
    performances
)

print("\nOrdered bench:")

for player in ordered_bench:
    print(
        f"- Position {player['squad_position']} | "
        f"{player['player_name']} | "
        f"{player['position_name']}"
    )

#this split the bench into two categories: the goalkeeper and the outfield players.
bench = engine.split_bench(
    performances
)

print("\nBench goalkeeper:")

if bench["goalkeeper"]:
    print(
        f"- {bench['goalkeeper']['player_name']}"
    )

print("\nOutfield bench order:")

for player in bench["outfield"]:
    print(
        f"- {player['player_name']} | "
        f"{player['position_name']}"
    )

starting_players = [
    {
        "player_name": "GK",
        "position_name": "Goalkeeper",
    },
    {
        "player_name": "DEF 1",
        "position_name": "Defender",
    },
    {
        "player_name": "DEF 2",
        "position_name": "Defender",
    },
    {
        "player_name": "DEF 3",
        "position_name": "Defender",
    },
    {
        "player_name": "MID 1",
        "position_name": "Midfielder",
    },
    {
        "player_name": "MID 2",
        "position_name": "Midfielder",
    },
    {
        "player_name": "MID 3",
        "position_name": "Midfielder",
    },
    {
        "player_name": "MID 4",
        "position_name": "Midfielder",
    },
    {
        "player_name": "FWD 1",
        "position_name": "Forward",
    },
    {
        "player_name": "FWD 2",
        "position_name": "Forward",
    },
    {
        "player_name": "FWD 3",
        "position_name": "Forward",
    },
]


formation = engine.get_formation(
    starting_players
)

print("\nStarting formation:")

print(
    f"GK: {formation['Goalkeeper']} | "
    f"DEF: {formation['Defender']} | "
    f"MID: {formation['Midfielder']} | "
    f"FWD: {formation['Forward']}"
)

valid_formation = engine.is_valid_formation(
    starting_players
)
print(
    f"Formation valid: {valid_formation}"
)

invalid_players = [
    player.copy()
    for player in starting_players
]

invalid_players[1]["position_name"] = "Midfielder"

invalid_formation = engine.get_formation(
    invalid_players
)

print("\nInvalid formation:")

print(
    f"GK: {invalid_formation['Goalkeeper']} | "
    f"DEF: {invalid_formation['Defender']} | "
    f"MID: {invalid_formation['Midfielder']} | "
    f"FWD: {invalid_formation['Forward']}"
)

print(
    f"Formation valid: "
    f"{engine.is_valid_formation(invalid_players)}"
)

player_out = starting_players[1]

bench_forward = {
    "player_name": "Bench Forward",
    "position_name": "Forward",
}

bench_defender = {
    "player_name": "Bench Defender",
    "position_name": "Defender",
}

print("\nSubstitution validation:")

forward_allowed = engine.can_make_substitution(
    starting_players,
    player_out,
    bench_forward
)

defender_allowed = engine.can_make_substitution(
    starting_players,
    player_out,
    bench_defender
)

print(
    f"{player_out['player_name']} -> "
    f"{bench_forward['player_name']}: "
    f"{forward_allowed}"
)

print(
    f"{player_out['player_name']} -> "
    f"{bench_defender['player_name']}: "
    f"{defender_allowed}"
)

outfield_bench_test = [
    {
        "player_name": "Bench Forward",
        "position_name": "Forward",
        "minutes": 90,
    },
    {
        "player_name": "Bench Defender",
        "position_name": "Defender",
        "minutes": 90,
    },
    {
        "player_name": "Bench Midfielder",
        "position_name": "Midfielder",
        "minutes": 90,
    },
]

eligible_substitute = engine.find_eligible_substitute(
    starting_players,
    player_out,
    outfield_bench_test
)

print("\nEligible substitute:")

if eligible_substitute:
    print(
        f"{player_out['player_name']} -> "
        f"{eligible_substitute['player_name']}"
    )
else:
    print("No eligible substitute found")

outfield_bench_no_show_test = [
    {
        "player_name": "Bench Defender 1",
        "position_name": "Defender",
        "minutes": 0,
    },
    {
        "player_name": "Bench Defender 2",
        "position_name": "Defender",
        "minutes": 45,
    },
    {
        "player_name": "Bench Midfielder",
        "position_name": "Midfielder",
        "minutes": 90,
    },
]

eligible_after_no_show = engine.find_eligible_substitute(
    starting_players,
    player_out,
    outfield_bench_no_show_test
)

print("\nBench no-show test:")

if eligible_after_no_show:
    print(
        f"{player_out['player_name']} -> "
        f"{eligible_after_no_show['player_name']}"
    )
else:
    print("No eligible substitute found")

updated_starting_players = engine.apply_substitution(
    starting_players,
    player_out,
    eligible_substitute
)

updated_formation = engine.get_formation(
    updated_starting_players
)

print("\nApplied substitution:")

print(
    f"OUT: {player_out['player_name']} | "
    f"IN: {eligible_substitute['player_name']}"
)

print(
    f"Updated XI players: "
    f"{len(updated_starting_players)}"
)

print(
    f"Updated formation: "
    f"GK {updated_formation['Goalkeeper']} | "
    f"DEF {updated_formation['Defender']} | "
    f"MID {updated_formation['Midfielder']} | "
    f"FWD {updated_formation['Forward']}"
)

print(
    f"Updated formation valid: "
    f"{engine.is_valid_formation(updated_starting_players)}"
)

#the following section tests the apply_goalkeeper_substitution method of the ScoringEngine class, which automatically substitutes a bench goalkeeper into the starting lineup if the starting goalkeeper did not play any minutes. It creates a test starting XI with a non-playing goalkeeper and a bench goalkeeper, and checks if the substitution is applied correctly.
goalkeeper_test_xi = [
    {
        "player_name": "Starting GK",
        "position_name": "Goalkeeper",
        "minutes": 0,
    }
]

for player in starting_players:
    if player["position_name"] != "Goalkeeper":
        goalkeeper_test_xi.append(player)

bench_goalkeeper_test = {
    "player_name": "Bench GK",
    "position_name": "Goalkeeper",
    "minutes": 90,
}

goalkeeper_updated_xi, goalkeeper_sub = (
    engine.apply_goalkeeper_substitution(
        goalkeeper_test_xi,
        bench_goalkeeper_test
    )
)

print("\nGoalkeeper auto-sub:")

if goalkeeper_sub:
    print(
        f"{goalkeeper_sub['player_out']['player_name']} -> "
        f"{goalkeeper_sub['player_in']['player_name']}"
    )
else:
    print("No goalkeeper substitution")

# Test: starting goalkeeper played
starting_gk_played_xi = [
    {
        "player_name": "Starting GK Played",
        "position_name": "Goalkeeper",
        "minutes": 90,
    }
]

for player in starting_players:
    if player["position_name"] != "Goalkeeper":
        starting_gk_played_xi.append(player)

_, goalkeeper_sub_played = (
    engine.apply_goalkeeper_substitution(
        starting_gk_played_xi,
        bench_goalkeeper_test
    )
)

print("\nStarting goalkeeper played:")

if goalkeeper_sub_played:
    print("Unexpected goalkeeper substitution")
else:
    print("No goalkeeper substitution")


# Test: bench goalkeeper did not play
bench_gk_no_show = {
    "player_name": "Bench GK No Show",
    "position_name": "Goalkeeper",
    "minutes": 0,
}

_, goalkeeper_sub_no_show = (
    engine.apply_goalkeeper_substitution(
        goalkeeper_test_xi,
        bench_gk_no_show
    )
)

print("\nBench goalkeeper no-show:")

if goalkeeper_sub_no_show:
    print("Unexpected goalkeeper substitution")
else:
    print("No goalkeeper substitution")

multi_sub_xi = []

for player in starting_players:
    player_copy = player.copy()
    player_copy["is_starting"] = True

    if player_copy["player_name"] in [
        "DEF 1",
        "MID 1",
    ]:
        player_copy["minutes"] = 0
    else:
        player_copy["minutes"] = 90

    multi_sub_xi.append(player_copy)

multi_sub_bench = [
    {
        "player_name": "Bench Forward",
        "position_name": "Forward",
        "minutes": 90,
    },
    {
        "player_name": "Bench Defender",
        "position_name": "Defender",
        "minutes": 90,
    },
    {
        "player_name": "Bench Midfielder",
        "position_name": "Midfielder",
        "minutes": 90,
    },
]

multi_sub_updated_xi, multi_substitutions = (
    engine.apply_outfield_substitutions(
        multi_sub_xi,
        multi_sub_bench
    )
)

print("\nMultiple outfield auto-subs:")

for substitution in multi_substitutions:
    print(
        f"{substitution['player_out']['player_name']} -> "
        f"{substitution['player_in']['player_name']}"
    )

multi_sub_formation = engine.get_formation(
    multi_sub_updated_xi
)

print(
    f"Final formation: "
    f"GK {multi_sub_formation['Goalkeeper']} | "
    f"DEF {multi_sub_formation['Defender']} | "
    f"MID {multi_sub_formation['Midfielder']} | "
    f"FWD {multi_sub_formation['Forward']}"
)

print(
    f"Formation valid: "
    f"{engine.is_valid_formation(multi_sub_updated_xi)}"
)

full_squad_test = []

# Starting XI
for player in starting_players:
    player_copy = player.copy()

    player_copy["is_starting"] = True
    player_copy["squad_position"] = (
        len(full_squad_test) + 1
    )

    # Starting GK and DEF 1 do not play
    if player_copy["player_name"] in [
        "GK",
        "DEF 1",
    ]:
        player_copy["minutes"] = 0
    else:
        player_copy["minutes"] = 90

    full_squad_test.append(player_copy)


# Bench
full_squad_test.extend([
    {
        "player_name": "Bench GK",
        "position_name": "Goalkeeper",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 12,
    },
    {
        "player_name": "Bench Forward",
        "position_name": "Forward",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 13,
    },
    {
        "player_name": "Bench Defender",
        "position_name": "Defender",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 14,
    },
    {
        "player_name": "Bench Midfielder",
        "position_name": "Midfielder",
        "minutes": 90,
        "is_starting": False,
        "squad_position": 15,
    },
])


auto_sub_result = engine.apply_auto_substitutions(
    full_squad_test
)

print("\nCombined auto-sub engine:")

for substitution in auto_sub_result["substitutions"]:
    print(
        f"{substitution['player_out']['player_name']} -> "
        f"{substitution['player_in']['player_name']}"
    )

formation = auto_sub_result["formation"]

print(
    f"Final formation: "
    f"GK {formation['Goalkeeper']} | "
    f"DEF {formation['Defender']} | "
    f"MID {formation['Midfielder']} | "
    f"FWD {formation['Forward']}"
)

print(
    f"Formation valid: "
    f"{auto_sub_result['formation_valid']}"
)

print(
    f"Original XI: "
    f"{len(auto_sub_result['original_xi'])}"
)

print(
    f"Final XI: "
    f"{len(auto_sub_result['final_xi'])}"
)

print("\nOFFICIAL AUTO-SUB COMPARISON TEST")
print("-" * 60)

predicted_substitutions = [
    {
        "player_out": {
            "player_id": 165,
            "player_name": "João Pedro",
        },
        "player_in": {
            "player_id": 124,
            "player_name": "Groß",
        },
    }
]

official_substitutions = [
    {
        "entry": 1053858,
        "element_in": 124,
        "element_out": 165,
        "event": 5,
    }
]

comparison = engine.compare_auto_substitutions(
    predicted_substitutions,
    official_substitutions
)

print(f"Predicted: {comparison['predicted']}")
print(f"Official:  {comparison['official']}")
print(f"Match:     {comparison['matches']}")

print("=" * 60)
print("SCORING ENGINE TEST COMPLETE")
print("=" * 60)
