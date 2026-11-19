
import unittest
from unittest.mock import Mock, patch

from database.sync_squads import sync_manager_squad


class TestSquadSynchronization(unittest.TestCase):

    def setUp(self):
        self.manager_id = 1053858
        self.gameweek = 10
        self.season = "2026/27"

        self.picks = [
            {
                "element": 1000 + position,
                "position": position,
                "multiplier": (
                    2 if position == 1
                    else 1 if position <= 11
                    else 0
                ),
                "is_captain": position == 1,
                "is_vice_captain": position == 2,
            }
            for position in range(1, 16)
        ]

        self.client = Mock()
        self.client.get_players.return_value = {
            "events": [
                {
                    "id": 10,
                    "is_previous": True,
                    "is_current": False,
                    "data_checked": True,
                }
            ]
        }
        self.client.get_manager_picks.return_value = {
            "picks": self.picks
        }

    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_new_squad_is_saved(self, mock_get, mock_save):
        mock_get.return_value = []

        result = sync_manager_squad(
            self.manager_id,
            self.gameweek,
            client=self.client,
        )

        self.assertEqual(result["status"], "updated")
        self.assertTrue(result["is_final"])
        self.assertEqual(len(result["picks"]), 15)

        self.client.get_manager_picks.assert_called_once_with(
            self.manager_id, self.gameweek
        )
        mock_save.assert_called_once_with(
            self.manager_id,
            self.season,
            self.gameweek,
            self.picks,
        )


    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_force_refreshes_cached_squad(self, mock_get, mock_save):
        mock_get.return_value = self.picks

        result = sync_manager_squad(
            self.manager_id,
            self.gameweek,
            force=True,
            client=self.client,
        )

        self.assertEqual(result["status"], "updated")
        self.client.get_manager_picks.assert_called_once()
        mock_save.assert_called_once()

    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_provisional_squad_refreshes(self, mock_get, mock_save):
        mock_get.return_value = self.picks
        self.client.get_players.return_value["events"][0].update({
            "data_checked": False,
            "is_previous": False,
            "is_current": True,
        })

        result = sync_manager_squad(
            self.manager_id,
            self.gameweek,
            client=self.client,
        )

        self.assertEqual(result["status"], "updated")
        self.assertFalse(result["is_final"])
        mock_save.assert_called_once()

    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_future_gameweek_is_rejected(self, mock_get, mock_save):
        mock_get.return_value = []
        self.client.get_players.return_value["events"][0].update({
            "data_checked": False,
            "is_previous": False,
            "is_current": False,
        })

        with self.assertRaises(ValueError):
            sync_manager_squad(
                self.manager_id,
                self.gameweek,
                client=self.client,
            )

        self.client.get_manager_picks.assert_not_called()
        mock_save.assert_not_called()

    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_api_failure_does_not_save(self, mock_get, mock_save):
        mock_get.return_value = []
        self.client.get_manager_picks.side_effect = RuntimeError(
            "FPL API temporarily unavailable"
        )

        with self.assertRaises(RuntimeError):
            sync_manager_squad(
                self.manager_id,
                self.gameweek,
                client=self.client,
            )

        mock_save.assert_not_called()

    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_incomplete_picks_are_rejected(self, mock_get, mock_save):
        mock_get.return_value = []
        self.client.get_manager_picks.return_value = {
            "picks": self.picks[:14]
        }

        with self.assertRaises(ValueError):
            sync_manager_squad(
                self.manager_id,
                self.gameweek,
                client=self.client,
            )

        mock_save.assert_not_called()

    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks")
    def test_unknown_gameweek_is_rejected(self, mock_get, mock_save):
        self.client.get_players.return_value = {"events": []}

        with self.assertRaises(ValueError):
            sync_manager_squad(
                self.manager_id,
                self.gameweek,
                client=self.client,
            )

        mock_get.assert_not_called()
        mock_save.assert_not_called()

    def test_invalid_manager_id_is_rejected(self):
        with self.assertRaises(ValueError):
            sync_manager_squad(
                -1,
                self.gameweek,
                client=self.client,
            )

        self.client.get_players.assert_not_called()

    def test_invalid_gameweek_is_rejected(self):
        with self.assertRaises(ValueError):
            sync_manager_squad(
                self.manager_id,
                39,
                client=self.client,
            )

        self.client.get_players.assert_not_called()


    @patch("database.sync_squads.save_manager_picks")
    @patch("database.sync_squads.get_manager_picks", create=True)
    def test_finalized_squad_refreshes_without_cache_metadata(
        self, mock_get, mock_save
    ):
        result = sync_manager_squad(
            self.manager_id,
            self.gameweek,
            client=self.client,
        )

        self.assertEqual(result["status"], "updated")
        self.assertTrue(result["is_final"])
        self.client.get_manager_picks.assert_called_once_with(
            self.manager_id, self.gameweek
        )
        mock_save.assert_called_once()
        mock_get.assert_not_called()

if __name__ == "__main__":
    unittest.main()
