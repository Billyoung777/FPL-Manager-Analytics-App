
import unittest
from unittest.mock import patch, MagicMock
from flask import template_rendered

from dashboard.app import app


class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def mock_dashboard_data(self, manager_name, team_name):
        """Configure deterministic database and analytics fixtures."""

        connection = MagicMock()

        connection.execute.side_effect = [
            MagicMock(fetchall=MagicMock(return_value=[
                (1053858, manager_name, team_name)
            ])),
            MagicMock(fetchone=MagicMock(return_value=(
                manager_name, team_name, 3, 150
            ))),
            MagicMock(fetchone=MagicMock(return_value=(
                50, 60, 40
            ))),
            MagicMock(fetchall=MagicMock(return_value=[
                (1, 50),
                (2, 60),
                (3, 40)
            ]))
        ]

        analytics = {
            "total_net_points": 150,
            "average_points": 50,
            "best_gameweek": {
                "gameweek": 2,
                "points": 60
            },
            "worst_gameweek": {
                "gameweek": 3,
                "points": 40
            },
            "performance_trends": []
        }

        return connection, analytics

    def test_manager_dashboard_loads(self):
        connection, analytics = self.mock_dashboard_data(
            "Test Manager", "Test FC"
        )

        with patch("dashboard.app.sync_gameweeks") as mock_sync, \
             patch(
                 "dashboard.app.calculate_manager_analytics",
                 return_value=analytics
             ), \
             patch(
                 "dashboard.app.get_connection",
                 return_value=connection
             ), \
             patch(
                 "dashboard.app.get_latest_gameweek_update",
                 return_value="2026-10-26 10:00:00"
             ):

            response = self.client.get("/manager?id=1053858")

        self.assertEqual(response.status_code, 200)
        mock_sync.assert_called_once_with(1053858, "2026/27")
        connection.close.assert_called_once()

    def test_manager_selection(self):
        connection, analytics = self.mock_dashboard_data(
            "Selected Manager", "Ctrl Alt Defeat Ai"
        )

        with patch("dashboard.app.sync_gameweeks"), \
             patch(
                 "dashboard.app.calculate_manager_analytics",
                 return_value=analytics
             ), \
             patch(
                 "dashboard.app.get_connection",
                 return_value=connection
             ), \
             patch(
                 "dashboard.app.get_latest_gameweek_update",
                 return_value=None
             ):

            response = self.client.get("/manager?id=6979233")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ctrl Alt Defeat Ai", response.data)
        connection.close.assert_called_once()

    def test_invalid_manager_id(self):
        with patch("dashboard.app.sync_gameweeks") as mock_sync:
            response = self.client.get("/manager?id=-1")

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid manager ID", response.data)
        mock_sync.assert_not_called()

    def test_manager_not_found(self):
        with patch(
            "dashboard.app.sync_gameweeks",
            side_effect=ValueError("Manager unavailable")
        ), patch(
            "dashboard.app.get_manager",
            return_value=None
        ) as mock_manager:

            response = self.client.get(
                "/manager?id=999999999999"
            )

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Manager not found", response.data)
        mock_manager.assert_called_once_with(999999999999)

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
            ) as mock_latest_update, patch(
                "dashboard.app.get_connection"
            ) as mock_get_connection:

                mock_connection = MagicMock()

                mock_connection.execute.side_effect = [
                    MagicMock(fetchall=MagicMock(return_value=[
                        (6940780, "Test Manager", "Test FC")
                    ])),
                    MagicMock(fetchone=MagicMock(return_value=(
                        "Test Manager", "Test FC", 6, 315
                    ))),
                    MagicMock(fetchone=MagicMock(return_value=(
                        52.5, 84, 26
                    ))),
                    MagicMock(fetchall=MagicMock(return_value=[
                        (1, 66),
                        (2, 84),
                        (3, 26),
                        (4, 63),
                        (5, 40),
                        (6, 36)
                    ]))
                ]

                mock_get_connection.return_value = mock_connection

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

        mock_latest_update.assert_called_once_with(
            6940780,
            "2026/27"
        )

        mock_connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
