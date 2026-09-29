from api.fpl_client import FPLClient


client = FPLClient()

try:
    manager = client.get_manager(999999999)

    print("Manager retrieved successfully!")
    print("Manager ID:", manager["id"])

except RuntimeError as error:
    print("API error handled successfully!")
    print(error)