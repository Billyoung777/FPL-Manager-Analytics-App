import requests

manager_id = 1053858

url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/"

response = requests.get(url)

print(response.status_code)
manager = response.json()

print("FPL MANAGER")
print("----------------------")
print("Entry ID:", manager["id"])
print("Team:", manager["name"])
print("Manager:", manager["player_first_name"], manager["player_last_name"])
print("Overall Points:", manager["summary_overall_points"])
print("Overall Rank:", manager["summary_overall_rank"])