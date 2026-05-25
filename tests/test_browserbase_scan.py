import unittest
from datetime import date

from velo_watch.browserbase_scan import (
    is_listing_url,
    normalize_listing_url,
    parse_posted_date,
    price_from_text,
)


class BrowserbaseScanTests(unittest.TestCase):
    def test_listing_url_filters(self) -> None:
        self.assertTrue(
            is_listing_url(
                "https://sfbay.craigslist.org/sfc/bik/d/san-francisco-cannondale/123.html",
                "craigslist",
            )
        )
        self.assertFalse(
            is_listing_url(
                "https://sfbay.craigslist.org/search/bia?query=cannondale",
                "craigslist",
            )
        )
        self.assertTrue(
            is_listing_url("https://offerup.com/item/detail/abc123", "offerup")
        )
        self.assertTrue(
            is_listing_url("https://www.facebook.com/marketplace/item/123456", "facebook")
        )

    def test_normalize_listing_url_strips_fragment_and_utm(self) -> None:
        self.assertEqual(
            normalize_listing_url("https://offerup.com/item/detail/abc?utm_source=x&cid=1#frag"),
            "https://offerup.com/item/detail/abc?cid=1",
        )

    def test_price_from_text(self) -> None:
        self.assertEqual(price_from_text("Cannondale bike $600 nearby"), "$600")
        self.assertIsNone(price_from_text("Cannondale bike nearby"))

    def test_parse_posted_date(self) -> None:
        today = date(2026, 5, 8)
        self.assertEqual(parse_posted_date("Listed 3 days ago", today), date(2026, 5, 5))
        self.assertEqual(parse_posted_date("yesterday", today), date(2026, 5, 7))
        self.assertEqual(parse_posted_date("May 05", today), date(2026, 5, 5))
        self.assertEqual(parse_posted_date("05/06/2026", today), date(2026, 5, 6))
        self.assertIsNone(parse_posted_date("no date here", today))


if __name__ == "__main__":
    unittest.main()
