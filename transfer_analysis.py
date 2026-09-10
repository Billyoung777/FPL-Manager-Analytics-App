import requests

manager_id = 1053858
gameweek = int(input("Enter gameweek: "))


# Get manager transfers
transfers_url = (
    f"https://fantasy.premierleague.com/api/"
    f"entry/{manager_id}/transfers/"
)

response = requests.get(transfers_url, timeout=10)
response.raise_for_status()

transfers = response.json()


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
print(f"GW{gameweek} TRANSFER ANALYSIS")
print("=" * 60)


transfer_count = 0

for transfer in transfers:

    if transfer["event"] == gameweek:

        transfer_count += 1

        player_out = players.get(
            transfer["element_out"],
            f"Unknown ({transfer['element_out']})"
        )

        player_in = players.get(
            transfer["element_in"],
            f"Unknown ({transfer['element_in']})"
        )

        print(
            f"OUT: {player_out:<18} "
            f"IN: {player_in:<18}"
        )

        print(
            f"    OUT Cost: {transfer['element_out_cost']} "
            f"| IN Cost: {transfer['element_in_cost']}"
        )

        print()


print("-" * 60)
print("Total Transfers:", transfer_count)
print("=" * 60)