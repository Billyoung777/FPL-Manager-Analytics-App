from tracker.mini_league_tracker import get_mini_league
from tracker.manager_comparison import get_manager_history
from api.fpl_client import FPLClient
import statistics
import sys
import argparse


def get_head_to_head_histories(manager_a_id, manager_b_id):
    """
    Retrieve gameweek histories for two FPL managers.
    """

    history_a = get_manager_history(manager_a_id)
    history_b = get_manager_history(manager_b_id)

    return {
        "manager_a_id": manager_a_id,
        "manager_b_id": manager_b_id,
        "history_a": history_a,
        "history_b": history_b,
    }


def compare_gameweeks(history_a, history_b):
    """
    Compare gameweeks shared by two managers.
    Uses net points after transfer deductions.
    """

    scores_a = {
        gw["event"]: gw["points"] - gw["event_transfers_cost"]
        for gw in history_a
    }

    scores_b = {
        gw["event"]: gw["points"] - gw["event_transfers_cost"]
        for gw in history_b
    }

    shared_gameweeks = sorted(
        set(scores_a) & set(scores_b)
    )

    results = []

    for gw in shared_gameweeks:
        points_a = scores_a[gw]
        points_b = scores_b[gw]

        if points_a > points_b:
            winner = "A"
        elif points_b > points_a:
            winner = "B"
        else:
            winner = "TIE"

        results.append({
            "gameweek": gw,
            "manager_a_points": points_a,
            "manager_b_points": points_b,
            "winner": winner,
        })

    return results

def calculate_h2h_record(results):
    """
    Count gameweek wins, losses and ties
    for two FPL managers.
    """

    manager_a_wins = 0
    manager_b_wins = 0
    ties = 0

    for result in results:
        if result["winner"] == "A":
            manager_a_wins += 1

        elif result["winner"] == "B":
            manager_b_wins += 1

        else:
            ties += 1

    return {
        "manager_a_wins": manager_a_wins,
        "manager_b_wins": manager_b_wins,
        "ties": ties,
        "gameweeks_compared": len(results),
    }


def calculate_manager_statistics(history):
    """
    Calculate performance statistics from FPL
    manager gameweek history.
    """

    scores = [
        {
            "gameweek": gw["event"],
            "points": gw["points"] - gw["event_transfers_cost"]
        }
        for gw in history
    ]

    if not scores:
        return None

    total_points = sum(gw["points"] for gw in scores)
    average_points = total_points / len(scores)

    best_gw = max(scores, key=lambda gw: gw["points"])
    worst_gw = min(scores, key=lambda gw: gw["points"])

    standard_deviation = statistics.pstdev(
        gw["points"] for gw in scores
    )

    return {
        "total_points": total_points,
        "average_points": round(average_points, 2),
        "best_gw": best_gw,
        "worst_gw": worst_gw,
        "standard_deviation": round(standard_deviation, 2),
        "gameweeks": len(scores),
    }



def filter_completed_gameweeks(
    history_a,
    history_b,
    include_provisional=False
):
    """
    Filter manager histories by gameweek status.

    include_provisional=False:
        Only verified gameweeks.

    include_provisional=True:
        Include all available gameweek histories.
    """

    if include_provisional:
        return history_a, history_b

    client = FPLClient()
    bootstrap = client.get("bootstrap-static/")

    completed_gws = {
        event["id"]
        for event in bootstrap["events"]
        if event["finished"] is True
        and event["data_checked"] is True
    }

    filtered_a = [
        gw for gw in history_a
        if gw["event"] in completed_gws
    ]

    filtered_b = [
        gw for gw in history_b
        if gw["event"] in completed_gws
    ]

    return filtered_a, filtered_b


def main():

    parser = argparse.ArgumentParser(
        description="FPL Head-to-Head Manager Comparison"
    )

    parser.add_argument(
        "--mode",
        choices=["verified", "provisional"],
        default="verified",
        help="Choose verified or provisional gameweek results"
    )

    args = parser.parse_args()

    include_provisional = args.mode == "provisional"
    
    manager_a_id = 1053858

    # Retrieve managers from our existing mini-league.
    league_data = get_mini_league(1701837)

    managers = league_data["standings"]["results"]

    # Select another manager from the league.
    opponent = next(
        manager
        for manager in managers
        if manager["entry"] != manager_a_id
    )

    manager_b_id = opponent["entry"]

    print(f"\nOpponent selected: {opponent['entry_name']}")
    print(f"Opponent Manager ID: {manager_b_id}")


    comparison = get_head_to_head_histories(
        manager_a_id,
        manager_b_id
    )


    filtered_a, filtered_b = filter_completed_gameweeks(
        comparison["history_a"],
        comparison["history_b"],
        include_provisional=include_provisional
    )


    comparison["history_a"] = filtered_a
    comparison["history_b"] = filtered_b

    print(
        "\nReporting mode:",
        "PROVISIONAL" if include_provisional else "VERIFIED"
    )


    print("=" * 60)
    print("FPL HEAD-TO-HEAD MANAGER COMPARISON")
    print("=" * 60)

    print(f"Manager A: {comparison['manager_a_id']}")
    print(f"Manager B: {comparison['manager_b_id']}")

    print(
        f"Manager A gameweeks: "
        f"{len(comparison['history_a'])}"
    )

    print(
        f"Manager B gameweeks: "
        f"{len(comparison['history_b'])}"
    )

    print("\nHISTORY RETRIEVAL: PASS")
    
    results = compare_gameweeks(
        comparison["history_a"],
        comparison["history_b"]
    )

    print("\n" + "-" * 60)
    print("GAMEWEEK HEAD-TO-HEAD RESULTS")
    print("-" * 60)

    for result in results:
        print(
            f"GW{result['gameweek']} | "
            f"A: {result['manager_a_points']} | "
            f"B: {result['manager_b_points']} | "
            f"Winner: {result['winner']}"
        )

    print("\nGAMEWEEK COMPARISON: COMPLETE")

    record = calculate_h2h_record(results)

    print("\n" + "-" * 60)
    print("HEAD-TO-HEAD RECORD")
    print("-" * 60)

    print(f"Manager A wins: {record['manager_a_wins']}")
    print(f"Manager B wins: {record['manager_b_wins']}")
    print(f"Ties: {record['ties']}")
    print(f"Gameweeks compared: {record['gameweeks_compared']}")

    print("\nH2H RECORD CALCULATION: COMPLETE")


    stats_a = calculate_manager_statistics(
        comparison["history_a"]
    )

    stats_b = calculate_manager_statistics(
        comparison["history_b"]
    )

    print("\n" + "-" * 60)
    print("MANAGER PERFORMANCE STATISTICS")
    print("-" * 60)

    for label, stats in [
        ("MANAGER A", stats_a),
        ("MANAGER B", stats_b),
    ]:
        print(f"\n{label}")
        print(f"Total points: {stats['total_points']}")
        print(f"Average points: {stats['average_points']}")
        print(
            f"Best GW: GW{stats['best_gw']['gameweek']} "
            f"({stats['best_gw']['points']} points)"
        )
        print(
            f"Worst GW: GW{stats['worst_gw']['gameweek']} "
            f"({stats['worst_gw']['points']} points)"
        )
        print(
            f"Standard deviation: "
            f"{stats['standard_deviation']}"
        )

    print("\nMANAGER STATISTICS: COMPLETE")

if __name__ == "__main__":
    try:
        main()

    except (RuntimeError, ValueError, KeyError, StopIteration) as error:
        print("\n" + "=" * 60)
        print("FPL HEAD-TO-HEAD ERROR")
        print("=" * 60)
        print(f"Error: {error}")
        print("\nPlease check the manager IDs, league data,")
        print("and FPL API connection before trying again.")

        sys.exit(1)

