import requests

manager_id = 1053858

# Get manager history
history_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/history/"

history_response = requests.get(history_url)
history_data = history_response.json()

# Get manager chips
chips = history_data["chips"]

# Get manager transfers
transfers_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/transfers/"

transfers_response = requests.get(transfers_url)
transfers = transfers_response.json()


print("FPL MANAGER TIMELINE")
print("======================")

for gameweek in range(1, 4):

    # Find GW history
    gw_data = None

    for record in history_data["current"]:
        if record["event"] == gameweek:
            gw_data = record
            break

    # Find chip
    chip_used = None

    for chip in chips:
        if chip["event"] == gameweek:
            chip_used = chip["name"]
            break

    # Count transfers
    transfer_count = 0

    for transfer in transfers:
        if transfer["event"] == gameweek:
            transfer_count += 1

    print()
    print(f"GW{gameweek}")
    print("----------------------")

    if gw_data:
        print("Points:", gw_data["points"])
        print("Total Points:", gw_data["total_points"])
        print("Overall Rank:", gw_data["overall_rank"])
    else:
        print("Points: Not available")

    print("Transfers:", transfer_count)

    if chip_used:
        print("Chip:", chip_used)
    else:
        print("Chip: None")