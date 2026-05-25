import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from velo_watch.matching import parse_price, score_candidate


class MatchingTests(unittest.TestCase):
    def test_parse_price(self) -> None:
        self.assertEqual(parse_price("$1,200"), 1200)
        self.assertEqual(parse_price("600"), 600)
        self.assertIsNone(parse_price("no price"))

    def test_score_candidate_keyword_price_location(self) -> None:
        with TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            profile = {
                "make": "Cannondale",
                "model": "",
                "color": "green",
                "serial": "",
                "distinctive_terms": ["pannier", "aero"],
                "components": [],
                "reference_photos": [],
                "low_price_threshold": 1200,
            }
            candidate = {
                "title": "Green Cannondale road bike with pannier",
                "price": "$600",
                "location": "San Francisco",
                "raw_text": "",
            }

            score, reasons = score_candidate(tmp_path, candidate, profile)

            self.assertGreaterEqual(score, 50)
            self.assertTrue(any("make match" in reason for reason in reasons))
            self.assertTrue(any("price" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
