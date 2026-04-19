#!/usr/bin/env python3
"""Apply SQL migrations using psql. Same as apply_migrations.sh — use when you prefer `python` over bash.

Usage (from backend/):
  python scripts/apply_migrations.py

Requires: DATABASE_URL, and `psql` on PATH.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[misc, assignment]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    if load_dotenv:
        load_dotenv(root / ".env")

    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        print("DATABASE_URL is not set. Export it or add it to backend/.env", file=sys.stderr)
        return 1

    migrations = [
        root / "migrations" / "001_valuation_snapshot.sql",
        root / "migrations" / "002_financial_and_ai_cache.sql",
    ]
    for path in migrations:
        if not path.is_file():
            print(f"Missing migration file: {path}", file=sys.stderr)
            return 1
        print(f"Applying {path.name}...")
        subprocess.run(
            ["psql", dsn, "-v", "ON_ERROR_STOP=1", "-f", str(path)],
            check=True,
        )
    print("Migrations applied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
