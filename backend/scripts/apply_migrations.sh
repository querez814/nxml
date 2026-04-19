#!/usr/bin/env bash
# Apply SQL migrations to DATABASE_URL (Railway Postgres, etc.).
#
# Run with:  bash scripts/apply_migrations.sh
# Or:        ./scripts/apply_migrations.sh
# Or Python:  python scripts/apply_migrations.py
# Do NOT run this .sh file with `python` (it is not Python).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "DATABASE_URL is not set" >&2
  exit 1
fi
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$ROOT/migrations/001_valuation_snapshot.sql"
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$ROOT/migrations/002_financial_and_ai_cache.sql"
echo "Migrations applied."
