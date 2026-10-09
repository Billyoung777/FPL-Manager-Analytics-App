
import requests

from tracker.mini_league_tracker import get_mini_league

BASE_URL = "https://fantasy.premierleague.com/api"

LEAGUE_IDS = [1701837, 1840079]


def get_manager_history(manager_id):
    url = f"{BASE_URL}/entry/{manager_id}/history/"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()["current"]


def main():
    print("=" * 60)
    print("FPL MANAGER GAMEWEEK COMPARISON")
    print("=" * 60)

    for league_id in LEAGUE_IDS:
        league_data = get_mini_league(league_id)

        league_name = league_data["league"]["name"]
        managers = league_data["standings"]["results"]

        print(f"\nLeague: {league_name}")
        print("-" * 60)

        for manager in managers:
            manager_id = manager["entry"]
            team_name = manager["entry_name"]

            try:
                history = get_manager_history(manager_id)

                gw_points = {
                    gw["event"]: gw["points"]- gw["event_transfers_cost"]
                    for gw in history
                }

                # Validate the manager's recorded cumulative total.
                if history:
                    calculated_total = sum(
                        gw["points"] - gw["event_transfers_cost"]
                        for gw in history
                    )

                    official_total = history[-1]["total_points"]

                    assert calculated_total == official_total, (
                        f"Scoring mismatch for {team_name}: "
                        f"Calculated {calculated_total}, "
                        f"Official {official_total}"
                    )

                points_display = " | ".join(
                    f"GW{gw}: {points}"
                    for gw, points in sorted(gw_points.items())
                )


                print(f"\n{team_name}")
                print(f"Entry ID: {manager_id}")
                print(f"Net points: {points_display}")
                print(f"Total: {calculated_total} | Validation: PASS")


            except requests.RequestException as error:
                print(
                    f"\n{team_name}: "
                    f"Could not retrieve history - {error}"
                )


if __name__ == "__main__":
    main()
