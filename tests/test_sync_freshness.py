
import unittest
from datetime import datetime, timedelta, timezone

from database.sync_freshness import calculate_sync_freshness


class TestSyncFreshness(unittest.TestCase):

    def setUp(self):
        self.now = datetime(
            2026, 11, 16, 12, 0, 0,
            tzinfo=timezone.utc
        )

    def test_fresh_sync(self):
        timestamp = (
            self.now - timedelta(hours=3)
        ).isoformat()

        result = calculate_sync_freshness(timestamp, self.now)

        self.assertEqual(result["freshness"], "fresh")
        self.assertEqual(result["age_hours"], 3.0)

    def test_aging_sync(self):
        timestamp = (
            self.now - timedelta(hours=30)
        ).isoformat()

        result = calculate_sync_freshness(timestamp, self.now)

        self.assertEqual(result["freshness"], "aging")

    def test_stale_sync(self):
        timestamp = (
            self.now - timedelta(hours=72)
        ).isoformat()

        result = calculate_sync_freshness(timestamp, self.now)

        self.assertEqual(result["freshness"], "stale")

    def test_missing_timestamp(self):
        result = calculate_sync_freshness(None, self.now)

        self.assertEqual(result["freshness"], "unknown")
        self.assertIsNone(result["age_hours"])

    def test_exactly_24_hours_is_aging(self):
        timestamp = (
            self.now - timedelta(hours=24)
        ).isoformat()

        result = calculate_sync_freshness(timestamp, self.now)

        self.assertEqual(result["freshness"], "aging")

    def test_exactly_48_hours_is_aging(self):
        timestamp = (
            self.now - timedelta(hours=48)
        ).isoformat()

        result = calculate_sync_freshness(timestamp, self.now)

        self.assertEqual(result["freshness"], "aging")

    def test_more_than_48_hours_is_stale(self):
        timestamp = (
            self.now - timedelta(hours=48, seconds=1)
        ).isoformat()

        result = calculate_sync_freshness(timestamp, self.now)

        self.assertEqual(result["freshness"], "stale")

    def test_naive_south_african_timestamp(self):
        timestamp = "2026-11-16 14:00:00"

        now = datetime(
            2026, 11, 16, 12, 0, 0,
            tzinfo=timezone.utc
        )

        result = calculate_sync_freshness(timestamp, now)

        self.assertEqual(result["freshness"], "fresh")
        self.assertEqual(result["age_hours"], 0.0)

if __name__ == "__main__":
    unittest.main()
