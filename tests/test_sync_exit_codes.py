
import unittest

from database.sync_all import get_exit_code


class TestSyncExitCodes(unittest.TestCase):

    def test_success_exit_code(self):
        result = {"status": "success"}
        self.assertEqual(get_exit_code(result), 0)

    def test_failed_exit_code(self):
        result = {"status": "failed"}
        self.assertEqual(get_exit_code(result), 1)

    def test_partial_exit_code(self):
        result = {"status": "partial"}
        self.assertEqual(get_exit_code(result), 2)


if __name__ == "__main__":
    unittest.main()
