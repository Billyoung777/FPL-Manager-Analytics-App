
import requests

BASE_URL = "https://fantasy.premierleague.com/api"

LEAGUE_IDS = [1701837, 1840079]



def get_mini_league(league_id):
    all_managers = []
    page = 1
    league_info = None

    while True:
        url = (
            f"{BASE_URL}/leagues-classic/"
            f"{league_id}/standings/"
        )

        response = requests.get(
            url,
            params={"page_standings": page},
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        if league_info is None:
            league_info = data["league"]

        standings = data["standings"]
        all_managers.extend(standings["results"])

        if not standings.get("has_next", False):
            break

        page += 1

    return {
        "league": league_info,
        "standings": {
            "results": all_managers
        }
    }



def main():
    print("=" * 60)
    print("FPL MINI-LEAGUE TRACKER")
    print("=" * 60)

    for league_id in LEAGUE_IDS:
        try:
            data = get_mini_league(league_id)

            league = data["league"]
            standings = data["standings"]["results"]

            print(f"\nLeague: {league['name']}")
            print(f"League ID: {league_id}")
            print(f"Managers retrieved: {len(standings)}")
            print("-" * 60)

            for manager in standings:
                print(
                    f"Rank: {manager['rank']} | "
                    f"Manager: {manager['player_name']} | "
                    f"Team: {manager['entry_name']} | "
                    f"Entry ID: {manager['entry']} | "
                    f"Points: {manager['total']}"
                )

        except requests.RequestException as error:
            print(f"\nLeague {league_id}: API error - {error}")
        except (KeyError, TypeError) as error:
            print(f"\nLeague {league_id}: Unexpected data - {error}")


if __name__ == "__main__":
    main()
