import requests

manager_id = 1053858

# Get transfer data
transfers_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/transfers/"
)

transfers_response = requests.get(transfers_url, timeout=10)
transfers_response.raise_for_status()

transfers = transfers_response.json()


print()
print("FPL TRANSFER TIMELINE")
print("=" * 60)


# Check GW1 to GW3
for gameweek in range(1, 4):

    gameweek_transfers = []

    for transfer in transfers:

        if transfer["event"] == gameweek:
            gameweek_transfers.append(transfer)

    print()
    print(f"GW{gameweek}")
    print("-" * 60)

    if not gameweek_transfers:
        print("No transfers")

    else:

        print(
            "Number of transfer records:",
            len(gameweek_transfers)
        )

        for transfer in gameweek_transfers:

            print(
                f'OUT ID: {transfer["element_out"]:<5} '
                f'→ IN ID: {transfer["element_in"]:<5}'
            )


print()
print("=" * 60)
print("TRANSFER TIMELINE COMPLETE")