import requests


manager_id = 1053858


url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/history/"

response = requests.get(url)

data = response.json()


print("MANAGER CHIPS")
print("----------------------")


for chip in data["chips"]:

    print(chip)