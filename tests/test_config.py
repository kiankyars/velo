import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from velo_watch.config import load_simple_yaml


class ConfigTests(unittest.TestCase):
    def test_load_simple_yaml_list_of_mappings(self) -> None:
        with TemporaryDirectory() as directory:
            config = Path(directory) / "watchlist.yml"
            config.write_text(
                """
cadence: "twice_daily"
searches:
  - name: "OfferUp Cannondale"
    marketplace: "offerup"
    url: "https://offerup.com/search?q=cannondale"
""".strip(),
                encoding="utf-8",
            )

            parsed = load_simple_yaml(config)

            self.assertEqual(parsed["cadence"], "twice_daily")
            self.assertEqual(parsed["searches"][0]["marketplace"], "offerup")


if __name__ == "__main__":
    unittest.main()
