import requests


manager_id = 1053858


# Get player information
bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

bootstrap_response = requests.get(bootstrap_url)

bootstrap_data = bootstrap_response.json()


player_lookup = {
    player["id"]: player["web_name"]
    for player in bootstrap_data["elements"]
}


# Get transfers
transfers_url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/transfers/"

transfers_response = requests.get(transfers_url)

transfers = transfers_response.json()


print("MANAGER TRANSFERS")
print("----------------------")


for transfer in transfers:

    player_out = player_lookup.get(transfer["element_out"], "Unknown")
    player_in = player_lookup.get(transfer["element_in"], "Unknown")

    print(
        "GW", transfer["event"],
        "| OUT:", player_out,
        "| IN:", player_in,
        "| OUT Cost:", transfer["element_out_cost"],
        "| IN Cost:", transfer["element_in_cost"]
    )