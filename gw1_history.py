import requests


manager_id = 1053858
gameweek = 1


url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/history/"

response = requests.get(url)

print(response.status_code)

data = response.json()

print("Available data:")
print(data.keys())

print()
print("GW1 MANAGER HISTORY")
print("----------------------")


for gameweek_data in data["current"]:

    if gameweek_data["event"] == gameweek:

        print(gameweek_data)