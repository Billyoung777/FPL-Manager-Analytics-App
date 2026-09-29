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