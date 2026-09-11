import requests

manager_id = 1053858


# Get manager history
history_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/history/"
)

history_response = requests.get(history_url, timeout=10)
history_response.raise_for_status()

history_data = history_response.json()


# Get transfers
transfers_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/transfers/"
)

transfers_response = requests.get(transfers_url, timeout=10)
transfers_response.raise_for_status()

transfers = transfers_response.json()


# Get chips
chips = history_data["chips"]


print()
print("FPL CHIP & TRANSFER TIMELINE")
print("=" * 60)


# Check GW1 to GW3
for gameweek in range(1, 4):

    # Find chip used
    chip_used = None

    for chip in chips:

        if chip["event"] == gameweek:
            chip_used = chip["name"]
            break


    # Count transfer records
    transfer_count = 0

    for transfer in transfers:

        if transfer["event"] == gameweek:
            transfer_count += 1


    print()
    print(f"GW{gameweek}")
    print("-" * 60)

    if chip_used:
        print("Chip:", chip_used)
    else:
        print("Chip: None")

    print("Transfer Records:", transfer_count)


print()
print("=" * 60)
print("CHIP & TRANSFER TIMELINE COMPLETE")