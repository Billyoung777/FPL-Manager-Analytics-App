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


# Get player names
bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url, timeout=10)
bootstrap_response.raise_for_status()

bootstrap_data = bootstrap_response.json()

players = {
    player["id"]: player["web_name"]
    for player in bootstrap_data["elements"]
}


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

            player_out = players.get(
                transfer["element_out"],
                f"Unknown ({transfer['element_out']})"
            )

            player_in = players.get(
                transfer["element_in"],
                f"Unknown ({transfer['element_in']})"
            )

            print(
                f"{player_out:<18} → {player_in}"
            )


print()
print("=" * 60)
print("TRANSFER TIMELINE COMPLETE")