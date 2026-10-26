import unittest
from unittest.mock import patch
from flask import template_rendered
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
            b"Manager not found",
            response.data
        )

    def test_dashboard_charts_use_net_points(self):
        captured = []

        def record_template(sender, template, context, **extra):
            captured.append(context)


        template_rendered.connect(record_template, app)
        try:
            with patch(
                "dashboard.app.calculate_manager_analytics"
            ) as mock_analytics, patch(
                "dashboard.app.sync_gameweeks"
            ), patch(
                "dashboard.app.get_latest_gameweek_update",
                return_value="2026-10-26 10:00:00"
            ):

                mock_analytics.return_value = {
                    "total_net_points": 315,
                    "average_points": 52.5,
                    "best_gameweek": {
                        "gameweek": 2,
                        "points": 84
                    },
                    "worst_gameweek": {
                        "gameweek": 3,
                        "points": 26
                    },
                    "performance_trends": []
                }

                response = self.client.get(
                    "/manager?id=6940780"
                )
                print("RESPONSE STATUS:", response.status_code)
                print("RESPONSE BODY:", response.get_data(as_text=True)[:500])
        finally:
            template_rendered.disconnect(record_template, app)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(captured), 1)

        context = captured[0]

        self.assertEqual(
            context["gameweek_points"],
            [66, 84, 26, 63, 40, 36]
        )

        self.assertEqual(
            context["cumulative_points"],
            [66, 150, 176, 239, 279, 315]
        )

        self.assertEqual(context["total_points"], 315)      
if __name__ == "__main__":
    unittest.main()
