
import unittest

from dashboard.app import app


class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_manager_dashboard_loads(self):
        response = self.client.get("/manager?id=1053858")

        self.assertEqual(response.status_code, 200)
    def test_manager_selection(self):
        response = self.client.get("/manager?id=6979233")

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Ctrl Alt Defeat Ai",
            response.data
        )

    def test_invalid_manager_id(self):
        response = self.client.get("/manager?id=-1")

        self.assertEqual(response.status_code, 400)

        self.assertIn(
            b"Invalid manager ID",
            response.data
        )

    def test_manager_not_found(self):
        response = self.client.get(
            "/manager?id=999999999999"
        )

        self.assertEqual(response.status_code, 404)

        self.assertIn(
            b"Manager analytics not available",
            response.data
        )

        
if __name__ == "__main__":
    unittest.main()
