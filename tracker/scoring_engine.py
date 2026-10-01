class ScoringEngine:
    def __init__(self):
        pass

    def player_played(self, performance):
        return performance["minutes"] > 0

    def get_non_playing_starters(self, performances):
        non_playing_starters = []

        for performance in performances:
            if (
                performance["is_starting"]
                and not self.player_played(performance)
            ):
                non_playing_starters.append(performance)

        return non_playing_starters

#the following section tests the get_non_playing_starters method of the ScoringEngine class, which identifies players who were in the starting lineup but did not play any minutes in a gameweek. It creates a list of player performances and checks for non-playing starters.
    def get_ordered_bench(self, performances):
        bench = []

        for performance in performances:
            if not performance["is_starting"]:
                bench.append(performance)

        bench.sort(
            key=lambda player: player["squad_position"]
        )

        return bench
#This split the bench into two categories: the goalkeeper and the outfield players.
    def split_bench(self, performances):
        ordered_bench = self.get_ordered_bench(
            performances
        )

        bench_goalkeeper = None
        outfield_bench = []

        for player in ordered_bench:
            if player["position_name"] == "Goalkeeper":
                bench_goalkeeper = player
            else:
                outfield_bench.append(player)

        return {
            "goalkeeper": bench_goalkeeper,
            "outfield": outfield_bench,
        }
#formation is a dictionary that counts the number of players in each position (Goalkeeper, Defender, Midfielder, Forward) based on the provided list of players. It initializes the counts to zero and then iterates through the players, incrementing the count for each player's position. Finally, it returns the formation dictionary with the counts of players in each position.
    def get_formation(self, players):
        formation = {
            "Goalkeeper": 0,
            "Defender": 0,
            "Midfielder": 0,
            "Forward": 0,
        }

        for player in players:
            position = player["position_name"]

            if position in formation:
                formation[position] += 1

        return formation

#formation validation checks
    def is_valid_formation(self, players):
        if len(players) != 11:
            return False

        formation = self.get_formation(players)

        if formation["Goalkeeper"] != 1:
            return False

        if formation["Defender"] < 3:
            return False

        if formation["Defender"] > 5:
            return False

        if formation["Midfielder"] < 2:
            return False

        if formation["Midfielder"] > 5:
            return False

        if formation["Forward"] < 1:
            return False

        if formation["Forward"] > 3:
            return False

        return True

    def can_make_substitution(
        self,
        starting_players,
        player_out,
        player_in
    ):
        new_starting_players = []

        for player in starting_players:
            if player is not player_out:
                new_starting_players.append(player)

        new_starting_players.append(player_in)

        return self.is_valid_formation(
            new_starting_players
        )

    def find_eligible_substitute(
        self,
        starting_players,
        player_out,
        outfield_bench
    ):
        for player_in in outfield_bench:

            if not self.player_played(player_in):
                continue

            if self.can_make_substitution(
                starting_players,
                player_out,
                player_in
            ):
                return player_in

        return None

#the apply_substitution method takes a list of starting players, a player to be substituted out, and a player to be substituted in. It creates a new list of starting players by replacing the player_out with the player_in while keeping the other players unchanged. The method returns the updated list of starting players after the substitution.
    def apply_substitution(
        self,
        starting_players,
        player_out,
        player_in
    ):
        updated_starting_players = []

        for player in starting_players:
            if player is player_out:
                updated_starting_players.append(player_in)
            else:
                updated_starting_players.append(player)

        return updated_starting_players

    def apply_goalkeeper_substitution(
        self,
        starting_players,
        bench_goalkeeper
    ):
        starting_goalkeeper = None

        for player in starting_players:
            if player["position_name"] == "Goalkeeper":
                starting_goalkeeper = player
                break

        if starting_goalkeeper is None:
            return starting_players, None

        if self.player_played(starting_goalkeeper):
            return starting_players, None

        if bench_goalkeeper is None:
            return starting_players, None

        if not self.player_played(bench_goalkeeper):
            return starting_players, None

        updated_players = self.apply_substitution(
            starting_players,
            starting_goalkeeper,
            bench_goalkeeper
        )

        substitution = {
            "player_out": starting_goalkeeper,
            "player_in": bench_goalkeeper,
        }

        return updated_players, substitution

#the apply_outfield_substitutions method takes a list of starting players and a list of outfield bench players. It identifies non-playing starters and attempts to substitute them with eligible outfield bench players. The method returns the updated list of starting players after substitutions and a list of substitutions made.
    def apply_outfield_substitutions(
        self,
        starting_players,
        outfield_bench
    ):
        updated_starting_players = starting_players.copy()
        substitutions = []
        used_substitutes = set()

        non_playing_starters = (
            self.get_non_playing_starters(
                updated_starting_players
            )
        )

        for player_out in non_playing_starters:

            if player_out["position_name"] == "Goalkeeper":
                continue

            for player_in in outfield_bench:

                player_key = id(player_in)

                if player_key in used_substitutes:
                    continue

                if not self.player_played(player_in):
                    continue

                if not self.can_make_substitution(
                    updated_starting_players,
                    player_out,
                    player_in
                ):
                    continue

                updated_starting_players = (
                    self.apply_substitution(
                        updated_starting_players,
                        player_out,
                        player_in
                    )
                )

                used_substitutes.add(player_key)

                substitutions.append({
                    "player_out": player_out,
                    "player_in": player_in,
                })

                break

        return updated_starting_players, substitutions

#Apply auto substitutions method takes a list of player performances and applies automatic substitutions based on the rules of the game. It identifies starting players, splits the bench into goalkeeper and outfield players, and applies goalkeeper and outfield substitutions as needed. The method returns a dictionary containing the original starting lineup, the final starting lineup after substitutions, the list of substitutions made, the formation of the final lineup, and whether the formation is valid.
    def apply_auto_substitutions(self, performances):
        starting_players = [
            player
            for player in performances
            if player["is_starting"]
        ]

        bench = self.split_bench(performances)

        updated_starting_players, goalkeeper_sub = (
            self.apply_goalkeeper_substitution(
                starting_players,
                bench["goalkeeper"]
            )
        )

        updated_starting_players, outfield_subs = (
            self.apply_outfield_substitutions(
                updated_starting_players,
                bench["outfield"]
            )
        )

        substitutions = []

        if goalkeeper_sub:
            substitutions.append(goalkeeper_sub)

        substitutions.extend(outfield_subs)

        return {
            "original_xi": starting_players,
            "final_xi": updated_starting_players,
            "substitutions": substitutions,
            "formation": self.get_formation(
                updated_starting_players
            ),
            "formation_valid": self.is_valid_formation(
                updated_starting_players
            ),
        }