import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from velo_watch.env import load_home_env, strip_inline_comment, strip_quotes


class EnvTests(unittest.TestCase):
    def test_strip_quotes(self) -> None:
        self.assertEqual(strip_quotes('"abc"'), "abc")
        self.assertEqual(strip_quotes("'abc'"), "abc")
        self.assertEqual(strip_quotes("abc"), "abc")

    def test_strip_inline_comment(self) -> None:
        self.assertEqual(strip_inline_comment("abc # comment"), "abc")
        self.assertEqual(strip_inline_comment('"abc # kept"'), '"abc # kept"')

    def test_load_home_env_does_not_override_existing(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text(
                """
export BROWSERBASE_API_KEY=from_file
VELO_SCAN_WAIT_MS="9000"
""".strip(),
                encoding="utf-8",
            )
            old_key = os.environ.get("BROWSERBASE_API_KEY")
            old_wait = os.environ.get("VELO_SCAN_WAIT_MS")
            try:
                os.environ["BROWSERBASE_API_KEY"] = "existing"
                os.environ.pop("VELO_SCAN_WAIT_MS", None)
                load_home_env(path)

                self.assertEqual(os.environ["BROWSERBASE_API_KEY"], "existing")
                self.assertEqual(os.environ["VELO_SCAN_WAIT_MS"], "9000")
            finally:
                restore_env("BROWSERBASE_API_KEY", old_key)
                restore_env("VELO_SCAN_WAIT_MS", old_wait)


def restore_env(key: str, value: str | None) -> None:
    if value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
