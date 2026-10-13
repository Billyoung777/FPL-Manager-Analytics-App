
from api.fpl_client import FPLClient


def get_gameweek_statuses():
    """
    Retrieve gameweek completion and verification
    statuses from the FPL API.
    """

    client = FPLClient()

    data = client.get("bootstrap-static/")

    statuses = []

    for event in data["events"]:
        finished = event["finished"]
        data_checked = event["data_checked"]

        statuses.append({
            "gameweek": event["id"],
            "finished": finished,
            "data_checked": data_checked,
            "verified": finished and data_checked
        })

    return statuses


def main():
    print("=" * 60)
    print("FPL GAMEWEEK VERIFICATION STATUS")
    print("=" * 60)

    statuses = get_gameweek_statuses()

    for status in statuses:
        if status["verified"]:
            label = "VERIFIED"
        elif status["finished"]:
            label = "AWAITING DATA CHECK"
        else:
            label = "NOT VERIFIED"

        print(
            f"GW{status['gameweek']:02d} | "
            f"Finished: {status['finished']} | "
            f"Data Checked: {status['data_checked']} | "
            f"{label}"
        )

    verified_count = sum(
        1 for status in statuses if status["verified"]
    )

    print("-" * 60)
    print(f"Verified gameweeks: {verified_count}")
    print("GAMEWEEK STATUS CHECK: COMPLETE")


if __name__ == "__main__":
    main()
