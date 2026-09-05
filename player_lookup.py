import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)

print(response.status_code)

data = response.json()

print(data.keys())
players = data["elements"]

for player in players:
    if player["id"] == 496:
        print(player)