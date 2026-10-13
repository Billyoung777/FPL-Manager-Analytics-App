
import subprocess
import sys

TEST_MODULES = [
    "tests.test_head_to_head",
    "tests.test_gameweek_winners",
    "tests.test_historical_rankings",
    "tests.test_league_insights",
    "tests.test_manager_consistency",
    "tests.test_mini_league_errors",
    "tests.test_mini_league_leaderboard",
    "tests.test_mini_league_pagination",
    "tests.test_performance_trends",
    "tests.test_rank_movements",
    "tests.test_season_summary",
    "tests.test_season_summary_errors",
]

print("=" * 60, flush=True)
print("FPL MANAGER ANALYTICS - UNIT TEST RUNNER", flush=True)
print("=" * 60, flush=True)

passed = 0
failed = []

for module in TEST_MODULES:
    print(f"\nRunning {module}...", flush=True)

    result = subprocess.run(
        [sys.executable, "-m", module],
        check=False
    )

    if result.returncode == 0:
        print(f"PASS: {module}", flush=True)
        passed += 1
    else:
        print(f"FAIL: {module}", flush=True)
        failed.append(module)

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {len(failed)}")
print(f"Total: {len(TEST_MODULES)}")

if failed:
    print("\nFailed modules:")
    for module in failed:
        print(f"- {module}")

sys.exit(1 if failed else 0)
