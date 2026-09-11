import requests

manager_id = 1053858


# --------------------------------------------------
# GET MANAGER HISTORY
# --------------------------------------------------

history_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/history/"
)

history_response = requests.get(history_url, timeout=10)
history_response.raise_for_status()

history_data = history_response.json()


# --------------------------------------------------
# GET TRANSFERS
# --------------------------------------------------

transfers_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/transfers/"
)

transfers_response = requests.get(transfers_url, timeout=10)
transfers_response.raise_for_status()

transfers = transfers_response.json()


# --------------------------------------------------
# GET CHIPS
# --------------------------------------------------

chips = history_data["chips"]


# --------------------------------------------------
# REPORT
# --------------------------------------------------

print()
print("FPL MANAGER DECISION TIMELINE")
print("=" * 70)


for gameweek in range(1, 4):

    # Find manager history
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
    print("-" * 70)


    # Manager performance
    if gw_data:

        print("Points:", gw_data["points"])
        print("Total Points:", gw_data["total_points"])
        print("Overall Rank:", gw_data["overall_rank"])
        print("Transfers:", transfer_count)
        print("Transfer Cost:", gw_data["event_transfers_cost"])
        print("Bench Points:", gw_data["points_on_bench"])

    else:

        print("Manager data not available")


    # Chip
    if chip_used:

        print("Chip:", chip_used)

    else:

        print("Chip: None")


print()
print("=" * 70)
print("MANAGER DECISION TIMELINE COMPLETE")