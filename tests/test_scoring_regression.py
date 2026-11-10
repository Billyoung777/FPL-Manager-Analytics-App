import contextlib
import io
import unittest

from tests.test_scoring_engine import main


class TestScoringRegression(unittest.TestCase):

    def test_scoring_engine_regressions(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            main()

        report = output.getvalue()

        self.assertIn(
            "Full gameweek scoring: PASS",
            report
        )

        self.assertIn(
            "Invalid formations: 0",
            report
        )

        self.assertIn(
            "Different final XIs: 0",
            report
        )


if __name__ == "__main__":
    unittest.main()
