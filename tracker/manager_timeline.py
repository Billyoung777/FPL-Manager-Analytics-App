from api.fpl_client import FPLClient
from tracker.gameweek_snapshot import GameweekSnapshot


class ManagerTimeline:
    def __init__(self, client=None):
        self.client = client or FPLClient()
        self.snapshot_tracker = GameweekSnapshot(self.client)

#The following method calculates a summary of the manager's timeline, including total points, average points, highest and lowest gameweek scores, total transfers in and out, and chips used.
    def get_timeline_summary(self, timeline):
        if not timeline:
            return None

        total_points = 0
        total_transfers_in = 0
        total_transfers_out = 0
        chips_used = []

        highest_gameweek = None
        lowest_gameweek = None

        for snapshot in timeline:
            gameweek = snapshot["gameweek"]
            analysis = snapshot["analysis"]
            chip = snapshot["chip"]
            squad_changes = snapshot["squad_changes"]

            score = analysis["manager_score"]

            total_points += score

            total_transfers_in += len(
                squad_changes["players_in"]
            )

            total_transfers_out += len(
                squad_changes["players_out"]
            )

            if chip:
                chips_used.append({
                    "name": chip["name"],
                    "gameweek": gameweek,
                })

            if (
                highest_gameweek is None
                or score > highest_gameweek["points"]
            ):
                highest_gameweek = {
                    "gameweek": gameweek,
                    "points": score,
                }

            if (
                lowest_gameweek is None
                or score < lowest_gameweek["points"]
            ):
                lowest_gameweek = {
                    "gameweek": gameweek,
                    "points": score,
                }

        average_points = total_points / len(timeline)

        return {
            "gameweeks": len(timeline),
            "total_points": total_points,
            "average_points": round(average_points, 2),
            "highest_gameweek": highest_gameweek,
            "lowest_gameweek": lowest_gameweek,
            "total_players_in": total_transfers_in,
            "total_players_out": total_transfers_out,
            "chips_used": chips_used,
        }

#The following method builds a timeline of the manager's performance across all gameweeks, retrieving snapshots for each gameweek and compiling them into a list.
    def build_timeline(self, manager_id):
        latest_gameweek = self.client.get_latest_finished_gameweek()

        if latest_gameweek is None:
            return []

        timeline = []

        for gameweek in range(1, latest_gameweek + 1):
            snapshot = self.snapshot_tracker.get_snapshot(
                manager_id,
                gameweek
            )

            timeline.append(snapshot)

        return timeline