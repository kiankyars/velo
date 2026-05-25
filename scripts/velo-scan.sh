#!/bin/zsh
set -euo pipefail

cd /Users/kian/Developer/vélo
mkdir -p data/logs
export UV_CACHE_DIR=/Users/kian/Developer/vélo/.uv-cache
export VELO_MAX_LISTINGS_PER_SEARCH="${VELO_MAX_LISTINGS_PER_SEARCH:-8}"
export VELO_DETAIL_WAIT_MS="${VELO_DETAIL_WAIT_MS:-1000}"
export VELO_DETAIL_TIMEOUT_MS="${VELO_DETAIL_TIMEOUT_MS:-12000}"
export VELO_POSTED_AFTER_DATE="${VELO_POSTED_AFTER_DATE:-2026-05-04}"

{
  echo "=== velo-watch scan $(date -Iseconds) ==="
  /Users/kian/.local/bin/uv run python3 -m velo_watch scan
  echo
} >> data/logs/scan.log 2>&1
