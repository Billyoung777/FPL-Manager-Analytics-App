import requests


def get_player_gameweek(player_id, gameweek):

    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

    response = requests.get(url)

    data = response.json()

    for record in data["history"]:

        if record["round"] == gameweek:
            return record

    return None


# Test Haaland GW1
stats = get_player_gameweek(411, 1)

print("Haaland GW1")
print("----------------------")

if stats:
    print("Points:", stats["total_points"])
    print("Minutes:", stats["minutes"])
    print("Goals:", stats["goals_scored"])
    print("Assists:", stats["assists"])
    print("Clean Sheets:", stats["clean_sheets"])
    print("Bonus:", stats["bonus"])
    print("BPS:", stats["bps"])
else:
    print("No data found")