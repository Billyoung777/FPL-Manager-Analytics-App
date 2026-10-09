
from tracker.mini_league_tracker import get_mini_league

LEAGUE_IDS = [1701837, 1840079]
MY_MANAGER_ID = 1053858

print("=" * 60)
print("MINI-LEAGUE TRACKER VALIDATION")
print("=" * 60)

for league_id in LEAGUE_IDS:
    data = get_mini_league(league_id)

    league_name = data["league"]["name"]
    managers = data["standings"]["results"]

    print(f"\nLeague: {league_name}")
    print(f"Managers retrieved: {len(managers)}")

    assert len(managers) > 0, (
        f"League {league_id}: No managers found"
    )

    manager_ids = [manager["entry"] for manager in managers]

    assert len(manager_ids) == len(set(manager_ids)), (
        f"League {league_id}: Duplicate manager IDs detected"
    )

    assert MY_MANAGER_ID in manager_ids, (
        f"League {league_id}: My manager ID not found"
    )

    for manager in managers:
        assert manager["entry"] > 0
        assert manager["rank"] > 0
        assert isinstance(manager["total"], int)

    print("Validation: PASS")

print("\nALL MINI-LEAGUE VALIDATIONS: PASS")
