import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from velo_watch.db import (
    add_or_update_candidate,
    delete_candidate,
    get_candidate,
    init_db,
    list_candidates,
)


class DbTests(unittest.TestCase):
    def test_add_and_list_candidate(self) -> None:
        with TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            init_db(tmp_path)
            row_id, created = add_or_update_candidate(
                tmp_path,
                {
                    "source": "craigslist",
                    "url": "https://sfbay.craigslist.org/example",
                    "title": "Cannondale bike",
                    "score": 33,
                    "score_reasons": ["make match"],
                },
            )

            self.assertTrue(created)
            candidate = get_candidate(tmp_path, row_id)
            self.assertIsNotNone(candidate)
            self.assertEqual(candidate["title"], "Cannondale bike")
            self.assertEqual(list_candidates(tmp_path)[0]["score"], 33)

    def test_delete_candidate(self) -> None:
        with TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            init_db(tmp_path)
            row_id, _ = add_or_update_candidate(
                tmp_path,
                {
                    "source": "manual",
                    "url": "https://example.com/delete-me",
                    "title": "delete me",
                },
            )

            deleted = delete_candidate(tmp_path, row_id)

            self.assertIsNotNone(deleted)
            self.assertIsNone(get_candidate(tmp_path, row_id))


if __name__ == "__main__":
    unittest.main()
