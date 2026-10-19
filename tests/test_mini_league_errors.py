
import unittest
from unittest.mock import patch

from tracker.mini_league_tracker import get_mini_league


class TestMiniLeagueErrors(unittest.TestCase):

    @patch("tracker.mini_league_tracker.FPLClient")
    def test_invalid_league_id(self, mock_client):
        mock_client.return_value.get_league_standings.side_effect = (
            RuntimeError("FPL API returned an HTTP error: 404 Not Found")
        )

        with self.assertRaisesRegex(RuntimeError, "404 Not Found"):
            get_mini_league(999999999)

        mock_client.return_value.get_league_standings.assert_called_once_with(
            999999999, 1
        )

    @patch("tracker.mini_league_tracker.FPLClient")
    def test_api_connection_failure(self, mock_client):
        mock_client.return_value.get_league_standings.side_effect = (
            RuntimeError("FPL API request failed: Unable to connect")
        )

        with self.assertRaisesRegex(RuntimeError, "Unable to connect"):
            get_mini_league(1701837)

    @patch("tracker.mini_league_tracker.FPLClient")
    def test_api_timeout(self, mock_client):
        mock_client.return_value.get_league_standings.side_effect = (
            RuntimeError("FPL API request timed out")
        )

        with self.assertRaisesRegex(RuntimeError, "timed out"):
            get_mini_league(1701837)


if __name__ == "__main__":
    unittest.main()
