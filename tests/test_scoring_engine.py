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


print("\nBENCH PRIORITY REGRESSION TEST")
print("-" * 60)

def make_player(pid, name, position, minutes, starting, slot):
    return {
        "player_id": pid,
        "player_name": name,
        "position_name": position,
        "minutes": minutes,
        "is_starting": starting,
        "squad_position": slot,
    }

# Original 3-4-3 starting XI
xi = [
    make_player(1, "GK", "Goalkeeper", 90, True, 1),
    make_player(2, "DEF 1", "Defender", 0, True, 2),
    make_player(3, "DEF 2", "Defender", 90, True, 3),
    make_player(4, "DEF 3", "Defender", 90, True, 4),
    make_player(5, "MID 1", "Midfielder", 0, True, 5),
    make_player(6, "MID 2", "Midfielder", 90, True, 6),
    make_player(7, "MID 3", "Midfielder", 90, True, 7),
    make_player(8, "MID 4", "Midfielder", 90, True, 8),
    make_player(9, "FWD 1", "Forward", 90, True, 9),
    make_player(10, "FWD 2", "Forward", 90, True, 10),
    make_player(11, "FWD 3", "Forward", 90, True, 11),
]

bench = [
    make_player(12, "Bench GK", "Goalkeeper", 90, False, 12),
    make_player(13, "Bench MID", "Midfielder", 90, False, 13),
    make_player(14, "Bench DEF", "Defender", 90, False, 14),
    make_player(15, "Bench FWD", "Forward", 90, False, 15),
]

result = engine.apply_auto_substitutions(xi + bench)

for sub in result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

print("Formation valid:", result["formation_valid"])

print("\nCOMPETING SUBSTITUTES TEST")
print("-" * 60)

# Reuse the previous 3-4-3 XI.
# DEF 1 and MID 1 did not play.
#
# Bench MID is first priority.
# Bench DEF is second priority.
# Bench FWD is third priority.
#
# Make the bench defender unavailable.

competing_xi = [player.copy() for player in xi]
competing_bench = [player.copy() for player in bench]

for player in competing_bench:
    if player["player_name"] == "Bench DEF":
        player["minutes"] = 0

competing_result = engine.apply_auto_substitutions(
    competing_xi + competing_bench
)

for sub in competing_result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

print(
    "Number of substitutions:",
    len(competing_result["substitutions"])
)
print(
    "Final XI size:",
    len(competing_result["final_xi"])
)
print(
    "Formation valid:",
    competing_result["formation_valid"]
)


print("\nBENCH PRIORITY CONFLICT TEST")
print("-" * 60)

# Original formation: 4-4-2
# Missing starters: one defender, one midfielder
# First bench player: midfielder
# Second bench player: defender
# Third bench player: forward

conflict_xi = [
    make_player(101, "GK", "Goalkeeper", 90, True, 1),
    make_player(102, "DEF 1", "Defender", 0, True, 2),
    make_player(103, "DEF 2", "Defender", 90, True, 3),
    make_player(104, "DEF 3", "Defender", 90, True, 4),
    make_player(105, "DEF 4", "Defender", 90, True, 5),
    make_player(106, "MID 1", "Midfielder", 0, True, 6),
    make_player(107, "MID 2", "Midfielder", 90, True, 7),
    make_player(108, "MID 3", "Midfielder", 90, True, 8),
    make_player(109, "MID 4", "Midfielder", 90, True, 9),
    make_player(110, "FWD 1", "Forward", 90, True, 10),
    make_player(111, "FWD 2", "Forward", 90, True, 11),
]

conflict_bench = [
    make_player(112, "Bench GK", "Goalkeeper", 90, False, 12),
    make_player(113, "Bench MID", "Midfielder", 90, False, 13),
    make_player(114, "Bench DEF", "Defender", 90, False, 14),
    make_player(115, "Bench FWD", "Forward", 90, False, 15),
]

conflict_result = engine.apply_auto_substitutions(
    conflict_xi + conflict_bench
)

for sub in conflict_result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

print(
    "Formation valid:",
    conflict_result["formation_valid"]
)


print("\nSINGLE-SLOT BENCH PRIORITY TEST")
print("-" * 60)

single_xi = [player.copy() for player in conflict_xi]
single_bench = [player.copy() for player in conflict_bench]

# Only MID 1 did not play.
for player in single_xi:
    if player["player_name"] == "DEF 1":
        player["minutes"] = 90

# Bench DEF is first choice, Bench MID second.
for player in single_bench:
    if player["player_name"] == "Bench DEF":
        player["squad_position"] = 13
    elif player["player_name"] == "Bench MID":
        player["squad_position"] = 14

result = engine.apply_auto_substitutions(
    single_xi + single_bench
)

substitutions = result["substitutions"]

for sub in substitutions:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

print("Formation valid:", result["formation_valid"])

assert len(substitutions) == 1
assert substitutions[0]["player_in"]["player_name"] == "Bench DEF"

print("Bench priority test: PASS")


print("\nGW5 FORMATION CHANGE TEST")
print("-" * 60)

# Use our existing 3-4-3 starting XI.
gw5_xi = [player.copy() for player in xi]

# The non-playing forward represents João Pedro.
# All other starters played.
for player in gw5_xi:
    player["minutes"] = (
        0 if player["player_name"] == "FWD 3" else 90
    )

# Use the existing bench and put the midfielder first.
gw5_bench = [player.copy() for player in bench]

for player in gw5_bench:
    if player["player_name"] == "Bench MID":
        player["squad_position"] = 13
    elif player["player_name"] == "Bench DEF":
        player["squad_position"] = 14
    elif player["player_name"] == "Bench FWD":
        player["squad_position"] = 15

gw5_result = engine.apply_auto_substitutions(
    gw5_xi + gw5_bench
)

for sub in gw5_result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

formation = gw5_result["formation"]

print(
    "Final formation:",
    f"{formation['Defender']}-"
    f"{formation['Midfielder']}-"
    f"{formation['Forward']}"
)

assert len(gw5_result["substitutions"]) == 1
assert gw5_result["formation_valid"]
assert (
    formation["Defender"],
    formation["Midfielder"],
    formation["Forward"]
) == (3, 5, 2)

print("GW5 formation change test: PASS")


print("\nBENCH PRIORITY FALLBACK TEST")
print("-" * 60)

# Reuse the 4-4-2 starting XI from earlier.
fallback_xi = [player.copy() for player in conflict_xi]
fallback_bench = [player.copy() for player in conflict_bench]

# Only MID 1 is unavailable.
for player in fallback_xi:
    player["minutes"] = (
        0 if player["player_name"] == "MID 1" else 90
    )

# Bench MID has first priority but did not play.
# Bench DEF has second priority and played.
for player in fallback_bench:
    if player["player_name"] == "Bench MID":
        player["minutes"] = 0
    elif player["player_name"] == "Bench DEF":
        player["minutes"] = 90

fallback_result = engine.apply_auto_substitutions(
    fallback_xi + fallback_bench
)

for sub in fallback_result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

assert len(fallback_result["substitutions"]) == 1
assert (
    fallback_result["substitutions"][0]["player_in"]["player_name"]
    == "Bench DEF"
)
assert fallback_result["formation_valid"]

print("Bench priority fallback test: PASS")


print("\nMULTIPLE STARTERS PRIORITY TEST")
print("-" * 60)

# Original 4-4-2:
# DEF 1 and MID 1 did not play.
# Only Bench MID played among the outfield substitutes.

priority_xi = [player.copy() for player in conflict_xi]
priority_bench = [player.copy() for player in conflict_bench]

for player in priority_bench:
    if player["player_name"] in ("Bench DEF", "Bench FWD"):
        player["minutes"] = 0

priority_result = engine.apply_auto_substitutions(
    priority_xi + priority_bench
)

for sub in priority_result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

print(
    "Number of substitutions:",
    len(priority_result["substitutions"])
)
print(
    "Final formation:",
    priority_result["formation"]
)
print(
    "Formation valid:",
    priority_result["formation_valid"]
)

assert len(priority_result["substitutions"]) == 1
assert (
    priority_result["substitutions"][0]["player_in"]["player_name"]
    == "Bench MID"
)

print("Multiple starters priority test: PASS")


print("\nSTARTER-FIRST VS BENCH-FIRST REGRESSION")
print("-" * 60)

# Original formation: 4-4-2
# Missing starters: DEF 1 and MID 1
# Bench priority:
# 1. Bench MID (played)
# 2. Bench DEF (played)
# 3. Bench FWD (did not play)

comparison_xi = [
    make_player(201, "GK", "Goalkeeper", 90, True, 1),
    make_player(202, "DEF 1", "Defender", 0, True, 2),
    make_player(203, "DEF 2", "Defender", 90, True, 3),
    make_player(204, "DEF 3", "Defender", 90, True, 4),
    make_player(205, "DEF 4", "Defender", 90, True, 5),
    make_player(206, "MID 1", "Midfielder", 0, True, 6),
    make_player(207, "MID 2", "Midfielder", 90, True, 7),
    make_player(208, "MID 3", "Midfielder", 90, True, 8),
    make_player(209, "MID 4", "Midfielder", 90, True, 9),
    make_player(210, "FWD 1", "Forward", 90, True, 10),
    make_player(211, "FWD 2", "Forward", 90, True, 11),
]

comparison_bench = [
    make_player(212, "Bench GK", "Goalkeeper", 90, False, 12),
    make_player(213, "Bench MID", "Midfielder", 90, False, 13),
    make_player(214, "Bench DEF", "Defender", 90, False, 14),
    make_player(215, "Bench FWD", "Forward", 0, False, 15),
]

# Algorithm A: Current production engine
starter_first_xi, starter_first_subs = (
    engine.apply_outfield_substitutions(
        comparison_xi,
        comparison_bench[1:]
    )
)

# Algorithm B: Experimental bench-first algorithm
# This exists only inside the test file.
def experimental_bench_first(starters, bench_players):
    current_xi = starters.copy()
    substitutions = []

    for player_in in sorted(
        bench_players,
        key=lambda p: p["squad_position"]
    ):
        if not engine.player_played(player_in):
            continue

        for player_out in current_xi:
            if player_out["position_name"] == "Goalkeeper":
                continue

            if engine.player_played(player_out):
                continue

            if not engine.can_make_substitution(
                current_xi,
                player_out,
                player_in
            ):
                continue

            current_xi = engine.apply_substitution(
                current_xi,
                player_out,
                player_in
            )

            substitutions.append({
                "player_out": player_out,
                "player_in": player_in,
            })
            break

    return current_xi, substitutions


bench_first_xi, bench_first_subs = (
    experimental_bench_first(
        comparison_xi,
        comparison_bench[1:]
    )
)

def show_comparison(label, final_xi, substitutions):
    print(f"\n{label}")

    for sub in substitutions:
        print(
            sub["player_out"]["player_name"],
            "->",
            sub["player_in"]["player_name"]
        )

    print(
        "Formation:",
        engine.get_formation(final_xi)
    )
    print(
        "Valid:",
        engine.is_valid_formation(final_xi)
    )

    return {
        player["player_id"]
        for player in final_xi
    }


starter_ids = show_comparison(
    "STARTER-FIRST",
    starter_first_xi,
    starter_first_subs
)

bench_ids = show_comparison(
    "BENCH-FIRST",
    bench_first_xi,
    bench_first_subs
)

print("\nSame final XI:", starter_ids == bench_ids)

assert engine.is_valid_formation(starter_first_xi)
assert engine.is_valid_formation(bench_first_xi)

print("Algorithm comparison test: PASS")


print("\nAUTOMATED FORMATION COVERAGE TEST")
print("-" * 60)

valid_formations = [
    (3, 4, 3),
    (3, 5, 2),
    (4, 3, 3),
    (4, 4, 2),
    (4, 5, 1),
    (5, 3, 2),
    (5, 4, 1),
]

for defenders, midfielders, forwards in valid_formations:
    test_xi = [
        make_player(
            1000, "GK", "Goalkeeper", 90, True, 1
        )
    ]

    player_id = 1001

    for position, count in [
        ("Defender", defenders),
        ("Midfielder", midfielders),
        ("Forward", forwards),
    ]:
        for number in range(count):
            test_xi.append(
                make_player(
                    player_id,
                    f"{position} {number + 1}",
                    position,
                    90,
                    True,
                    len(test_xi) + 1
                )
            )
            player_id += 1

    assert engine.is_valid_formation(test_xi)

    print(
        f"{defenders}-{midfielders}-{forwards}: PASS"
    )

print("Formation coverage test: PASS")


from itertools import combinations, product

print("\nAUTOMATED SUBSTITUTION COMPARISON")
print("-" * 60)

scenarios_checked = 0
different_final_xi = 0
first_difference = None

for defenders, midfielders, forwards in valid_formations:

    # Build a fresh starting XI for each formation.
    starters = [
        make_player(1000, "GK", "Goalkeeper", 90, True, 1)
    ]

    next_id = 1001

    for position, count in [
        ("Defender", defenders),
        ("Midfielder", midfielders),
        ("Forward", forwards),
    ]:
        for number in range(count):
            starters.append(
                make_player(
                    next_id,
                    f"{position} {number + 1}",
                    position,
                    90,
                    True,
                    len(starters) + 1
                )
            )
            next_id += 1

    bench = [
        make_player(2000, "Bench DEF", "Defender", 90, False, 13),
        make_player(2001, "Bench MID", "Midfielder", 90, False, 14),
        make_player(2002, "Bench FWD", "Forward", 90, False, 15),
    ]

    # Test every pair of unavailable outfield starters.
    for missing in combinations(range(1, 11), 2):

        # Test all combinations of bench availability.
        for availability in product((0, 90), repeat=3):

            test_starters = [p.copy() for p in starters]
            test_bench = [p.copy() for p in bench]

            for index in missing:
                test_starters[index]["minutes"] = 0

            for player, minutes in zip(
                test_bench, availability
            ):
                player["minutes"] = minutes

            starter_xi, starter_subs = (
                engine.apply_outfield_substitutions(
                    test_starters,
                    test_bench
                )
            )

            bench_xi, bench_subs = (
                experimental_bench_first(
                    test_starters,
                    test_bench
                )
            )

            starter_ids = {
                p["player_id"] for p in starter_xi
            }
            bench_ids = {
                p["player_id"] for p in bench_xi
            }

            scenarios_checked += 1

            assert engine.is_valid_formation(starter_xi)
            assert engine.is_valid_formation(bench_xi)

            if starter_ids != bench_ids:
                different_final_xi += 1

                if first_difference is None:
                    first_difference = {
                        "formation": (
                            defenders, midfielders, forwards
                        ),
                        "missing": [
                            test_starters[i]["player_name"]
                            for i in missing
                        ],
                        "bench_minutes": availability,
                        "starter_subs": [
                            (
                                s["player_out"]["player_name"],
                                s["player_in"]["player_name"]
                            )
                            for s in starter_subs
                        ],
                        "bench_subs": [
                            (
                                s["player_out"]["player_name"],
                                s["player_in"]["player_name"]
                            )
                            for s in bench_subs
                        ],
                    }

print("Scenarios checked:", scenarios_checked)
print("Different final XIs:", different_final_xi)

if first_difference:
    print("\nFIRST DIFFERENCE FOUND")
    print("Formation:", first_difference["formation"])
    print("Missing starters:", first_difference["missing"])
    print("Bench minutes:", first_difference["bench_minutes"])
    print("Starter-first:", first_difference["starter_subs"])
    print("Bench-first:", first_difference["bench_subs"])
else:
    print("No differences found in tested scenarios.")

print("Automated comparison complete.")



from itertools import combinations, permutations, product

print("\nEXPANDED AUTO-SUBSTITUTION REGRESSION")
print("-" * 60)

total_scenarios = 0
different_final_xis = 0
invalid_formations = 0
first_difference = None

bench_positions = ("Defender", "Midfielder", "Forward")

for defenders, midfielders, forwards in valid_formations:

    starters = [
        make_player(1000, "GK", "Goalkeeper", 90, True, 1)
    ]

    next_id = 1001

    for position, count in [
        ("Defender", defenders),
        ("Midfielder", midfielders),
        ("Forward", forwards),
    ]:
        for number in range(count):
            starters.append(
                make_player(
                    next_id,
                    f"{position} {number + 1}",
                    position,
                    90,
                    True,
                    len(starters) + 1
                )
            )
            next_id += 1

    assert engine.is_valid_formation(starters)

    for bench_order in permutations(bench_positions):

        bench = [
            make_player(
                2000 + index,
                f"Bench {position}",
                position,
                90,
                False,
                13 + index
            )
            for index, position in enumerate(bench_order)
        ]

        for missing_count in (1, 2, 3):

            for missing in combinations(
                range(1, 11),
                missing_count
            ):

                for availability in product(
                    (0, 90),
                    repeat=3
                ):

                    test_starters = [
                        player.copy()
                        for player in starters
                    ]

                    test_bench = [
                        player.copy()
                        for player in bench
                    ]

                    for index in missing:
                        test_starters[index]["minutes"] = 0

                    for player, minutes in zip(
                        test_bench,
                        availability
                    ):
                        player["minutes"] = minutes

                    starter_xi, starter_subs = (
                        engine.apply_outfield_substitutions(
                            test_starters,
                            test_bench
                        )
                    )

                    bench_xi, bench_subs = (
                        experimental_bench_first(
                            test_starters,
                            test_bench
                        )
                    )

                    starter_ids = {
                        p["player_id"]
                        for p in starter_xi
                    }

                    bench_ids = {
                        p["player_id"]
                        for p in bench_xi
                    }

                    total_scenarios += 1

                    if (
                        not engine.is_valid_formation(starter_xi)
                        or not engine.is_valid_formation(bench_xi)
                    ):
                        invalid_formations += 1

                    if starter_ids != bench_ids:
                        different_final_xis += 1

                        if first_difference is None:
                            first_difference = {
                                "formation": (
                                    defenders,
                                    midfielders,
                                    forwards
                                ),
                                "bench_order": bench_order,
                                "missing": [
                                    test_starters[i]["player_name"]
                                    for i in missing
                                ],
                                "availability": availability,
                                "starter_subs": [
                                    (
                                        s["player_out"]["player_name"],
                                        s["player_in"]["player_name"]
                                    )
                                    for s in starter_subs
                                ],
                                "bench_subs": [
                                    (
                                        s["player_out"]["player_name"],
                                        s["player_in"]["player_name"]
                                    )
                                    for s in bench_subs
                                ],
                            }

print("Total scenarios:", total_scenarios)
print("Different final XIs:", different_final_xis)
print("Invalid formations:", invalid_formations)

if first_difference:
    print("\nFIRST DIFFERENCE")
    for key, value in first_difference.items():
        print(f"{key}: {value}")
else:
    print("No final-XI differences found.")

print("Expanded regression complete.")



print("\nCAPTAINCY FALLBACK TEST")
print("-" * 60)

captain = {
    "player_id": 301,
    "player_name": "Captain",
    "minutes": 90,
    "is_captain": True,
    "is_vice_captain": False,
}

vice = {
    "player_id": 302,
    "player_name": "Vice-Captain",
    "minutes": 90,
    "is_captain": False,
    "is_vice_captain": True,
}

# Scenario 1: Captain plays
result = engine.calculate_captaincy([captain, vice])

assert result["effective_captain"]["player_id"] == 301
assert result["multiplier"] == 2
assert result["vice_captain_activated"] is False

print("Captain plays: PASS")

# Scenario 2: Captain doesn't play
captain["minutes"] = 0

result = engine.calculate_captaincy([captain, vice])

assert result["effective_captain"]["player_id"] == 302
assert result["multiplier"] == 2
assert result["vice_captain_activated"] is True

print("Vice-captain fallback: PASS")

# Scenario 3: Neither plays
vice["minutes"] = 0

result = engine.calculate_captaincy([captain, vice])

assert result["effective_captain"] is None
assert result["multiplier"] == 1
assert result["vice_captain_activated"] is False

print("Neither plays: PASS")

print("CAPTAINCY FALLBACK TEST COMPLETE")


print("\nCAPTAINCY AND AUTO-SUB INTEGRATION TEST")
print("-" * 60)

# Reuse our earlier 3-4-3 starting XI and bench.
integration_xi = [p.copy() for p in xi]

integration_bench = [
    make_player(12, "Bench GK", "Goalkeeper", 90, False, 12),
    make_player(13, "Bench MID", "Midfielder", 90, False, 13),
    make_player(14, "Bench DEF", "Defender", 90, False, 14),
    make_player(15, "Bench FWD", "Forward", 90, False, 15),
]


# All players initially played.
for player in integration_xi + integration_bench:
    player["minutes"] = 90
    player["is_captain"] = False
    player["is_vice_captain"] = False

# Captain: FWD 3, who did not play.
# Vice-captain: MID 2, who played.
for player in integration_xi:
    if player["player_name"] == "FWD 3":
        player["is_captain"] = True
        player["minutes"] = 0
    elif player["player_name"] == "MID 2":
        player["is_vice_captain"] = True

# Make Bench MID first in substitution priority.

# Assign unique bench positions.

# Assign unique bench positions.
bench_order = {
    "Bench GK": 12,
    "Bench MID": 13,
    "Bench Midfielder": 13,
    "Bench DEF": 14,
    "Bench Defender": 14,
    "Bench FWD": 15,
    "Bench Forward": 15,
}

for player in integration_bench:
    player["squad_position"] = bench_order[
        player["player_name"]
    ]



performances = integration_xi + integration_bench
assert len(integration_xi) == 11
assert len(integration_bench) == 4
assert len(performances) == 15

auto_sub_result = engine.apply_auto_substitutions(
    performances
)


print("\nActual substitutions:")

for sub in auto_sub_result["substitutions"]:
    print(
        sub["player_out"]["player_name"],
        "->",
        sub["player_in"]["player_name"]
    )

print(
    "Final formation:",
    auto_sub_result["formation"]
)


captaincy_result = engine.calculate_captaincy(
    performances
)

print(
    "Effective captain:",
    captaincy_result["effective_captain"]["player_name"]
)

print(
    "Vice-captain activated:",
    captaincy_result["vice_captain_activated"]
)

print(
    "Final formation:",
    auto_sub_result["formation"]
)

assert (
    captaincy_result["effective_captain"]["player_name"]
    == "MID 2"
)
assert captaincy_result["vice_captain_activated"] is True
assert captaincy_result["multiplier"] == 2
assert auto_sub_result["formation_valid"]



assert len(auto_sub_result["substitutions"]) == 1


assert (
    auto_sub_result["substitutions"][0]["player_in"]["player_name"]
     == "Bench MID"
)

integration_bench = [
    make_player(12, "Bench GK", "Goalkeeper", 90, False, 12),
    make_player(13, "Bench MID", "Midfielder", 90, False, 13),
    make_player(14, "Bench DEF", "Defender", 90, False, 14),
    make_player(15, "Bench FWD", "Forward", 90, False, 15),
]

assert auto_sub_result["formation"] == {
    "Goalkeeper": 1,
    "Defender": 3,
    "Midfielder": 5,
    "Forward": 2,
}

print("Captaincy and auto-sub integration: PASS")


print("\nSCORING ENGINE CAPTAINCY POINTS TEST")
print("-" * 60)


points_test = [
    {
        "player_name": "Captain",
        "minutes": 0,
        "points": 0,
        "is_captain": True,
        "is_vice_captain": False,
    },
    {
        "player_name": "Vice-Captain",
        "minutes": 90,
        "points": 8,
        "is_captain": False,
        "is_vice_captain": True,
    },
    {
        "player_name": "Other Starter",
        "minutes": 90,
        "points": 5,
        "is_captain": False,
        "is_vice_captain": False,
    },
]

result = engine.calculate_captaincy_points(points_test)

assert result["total_points"] == 21
assert result["captaincy_multiplier"] == 2
assert result["vice_captain_activated"] is True

print("Calculated points:", result["total_points"])
print("Captaincy multiplier:", result["captaincy_multiplier"])
print("ScoringEngine captaincy points: PASS")


print("\nFINAL XI POINTS INTEGRATION TEST")
print("-" * 60)

# Reuse the successful captaincy + auto-sub scenario.
scoring_players = [
    player.copy() for player in performances
]

# Give every player 2 points initially.
for player in scoring_players:
    player["points"] = 2

    # Players who did not play earn zero points.
    if player["minutes"] == 0:
        player["points"] = 0

# Vice-captain MID 2 scored 8 points.
for player in scoring_players:
    if player["player_name"] == "MID 2":
        player["points"] = 8

# An unused bench forward scored 10 points.
# Those points must NOT count.
for player in scoring_players:
    if player["player_name"] == "Bench FWD":
        player["points"] = 10

auto_subs = engine.apply_auto_substitutions(
    scoring_players
)

final_xi = auto_subs["final_xi"]

# Captain FWD 3 was substituted out.
# Preserve the original captaincy information
# when determining the effective captain.
captaincy = engine.calculate_captaincy(
    scoring_players
)

# Apply the effective captain's multiplier to
# the final XI.
for player in final_xi:
    player["is_captain"] = (
        player is captaincy["effective_captain"]
    )
    player["is_vice_captain"] = False

result = engine.calculate_captaincy_points(
    final_xi
)

print("Final XI size:", len(final_xi))
print("Calculated points:", result["total_points"])
print("Unused bench forward excluded:",
      all(p["player_name"] != "Bench Forward"
          for p in final_xi))

assert len(final_xi) == 11
assert result["total_points"] == 36
assert all(
    p["player_name"] != "Bench Forward"
    for p in final_xi
)

print("Final XI points integration: PASS")



print("\nFULL GAMEWEEK SCORING TEST")
print("-" * 60)

result = engine.calculate_gameweek_points(
    scoring_players
)

print("Base points:", result["base_points"])
print("Captain bonus:", result["captain_bonus"])
print("Total points:", result["total_points"])
print("Final XI size:", len(result["final_xi"]))

assert result["base_points"] == 28
assert result["captain_bonus"] == 8
assert result["total_points"] == 36
assert len(result["final_xi"]) == 11
assert result["formation_valid"] is True

print("Full gameweek scoring: PASS")
