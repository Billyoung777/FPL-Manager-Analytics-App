import requests

BASE_URL = "https://fantasy.premierleague.com/api"

response = requests.get(
    f"{BASE_URL}/bootstrap-static/",
    timeout=30
)
response.raise_for_status()

data = response.json()

for event in data["events"]:
    if event["id"] == 6:
        print("=" * 60)
        print("GW6 OFFICIAL STATUS")
        print("=" * 60)

        print("Gameweek:", event["id"])
        print("Finished:", event["finished"])
        print("Data checked:", event["data_checked"])
        print("Deadline:", event["deadline_time"])

        break
else:
    print("GW6 not found")
