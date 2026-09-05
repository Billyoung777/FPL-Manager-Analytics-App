import requests

manager_id = 1053858
gameweek = 1

url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/"

response = requests.get(url)

print(response.status_code)

data = response.json()

print("Keys:", data.keys())
print("Number of picks:", len(data["picks"]))
print("First pick:", data["picks"][0])