from __future__ import annotations

import os
from pathlib import Path


def load_home_env(path: str | Path | None = None) -> Path:
    env_path = Path(path).expanduser() if path else Path.home() / ".env"
    if not env_path.exists():
        return env_path

    for raw_line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = strip_inline_comment(value.strip())
        if not key or not key.replace("_", "").isalnum():
            continue
        os.environ.setdefault(key, strip_quotes(value))

    return env_path


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def strip_inline_comment(value: str) -> str:
    quote: str | None = None
    for index, char in enumerate(value):
        if char in {"'", '"'}:
            quote = None if quote == char else char
        if char == "#" and quote is None:
            if index == 0 or value[index - 1].isspace():
                return value[:index].rstrip()
    return value
