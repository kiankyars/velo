import unittest

from velo_watch.__main__ import looks_like_url


class CliTests(unittest.TestCase):
    def test_looks_like_url(self) -> None:
        self.assertTrue(looks_like_url("https://offerup.com/search?q=cannondale"))
        self.assertTrue(looks_like_url("http://example.com"))
        self.assertFalse(looks_like_url("bike.jpg"))


if __name__ == "__main__":
    unittest.main()
