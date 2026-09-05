import requests

player_id = 411

url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

response = requests.get(url)

print(response.status_code)

data = response.json()

print("Available data:", data.keys())

print("Number of history records:", len(data["history"]))

print("First history record:")
for gameweek in data["history"]:
    if gameweek["round"] == 1:
        print("GW1 FOUND")
        print("Points:", gameweek["total_points"])
        print("Minutes:", gameweek["minutes"])
        print("Goals:", gameweek["goals_scored"])
        print("Assists:", gameweek["assists"])
        print("Clean Sheets:", gameweek["clean_sheets"])
        print("Bonus:", gameweek["bonus"])
        print("BPS:", gameweek["bps"])