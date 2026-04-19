#!/usr/bin/env python3
"""Clear or inspect Postgres statement caches (same ``DATABASE_URL`` as ``db.py``).

Loads ``backend/.env`` when present.

Examples (run from ``backend/``)::

  python scripts/clear_financial_cache.py --list
  python scripts/clear_financial_cache.py --symbol NVDA
  python scripts/clear_financial_cache.py --symbol NVDA --datasets cashflow_quarterly cashflow_annual
  python scripts/clear_financial_cache.py --symbol NVDA --valuation
  python scripts/clear_financial_cache.py --symbol NVDA --valuation-only
  python scripts/clear_financial_cache.py --all-financial
  python scripts/clear_financial_cache.py --symbol NVDA --dry-run

Requires: ``asyncpg`` (backend requirements).
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.is_file():
        load_dotenv(env_file)


def _dsn() -> str:
    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        print(
            "DATABASE_URL is not set. Add it to backend/.env or export it (see db.py).",
            file=sys.stderr,
        )
        sys.exit(1)
    return dsn


DATASETS = frozenset(
    {
        "income_quarterly",
        "income_annual",
        "balance_quarterly",
        "balance_annual",
        "cashflow_quarterly",
        "cashflow_annual",
    }
)


async def cmd_list(conn) -> None:
    rows = await conn.fetch(
        """
        SELECT symbol, dataset, fetched_at, latest_fiscal_date
        FROM financial_statement_cache
        ORDER BY symbol, dataset
        """
    )
    if not rows:
        print("financial_statement_cache: (empty)")
        return
    print(f"{'symbol':<12} {'dataset':<22} {'fetched_at':<28} latest_fiscal_date")
    for r in rows:
        print(f"{r['symbol']:<12} {r['dataset']:<22} {str(r['fetched_at']):<28} {r['latest_fiscal_date']}")


async def cmd_clear_financial(
    conn,
    symbol: str,
    datasets: list[str] | None,
    dry_run: bool,
) -> int:
    sym = symbol.strip().upper()
    if datasets:
        unknown = set(datasets) - DATASETS
        if unknown:
            print(f"Unknown dataset(s): {sorted(unknown)}", file=sys.stderr)
            print(f"Valid: {sorted(DATASETS)}", file=sys.stderr)
            return 1

    if not datasets:
        if dry_run:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM financial_statement_cache WHERE symbol = $1",
                sym,
            )
            print(f"[dry-run] would delete {count} row(s) for symbol={sym} (all datasets)")
            return 0
        result = await conn.execute(
            "DELETE FROM financial_statement_cache WHERE symbol = $1",
            sym,
        )
        print(f"Deleted all financial cache for {sym}: {result}")
        return 0

    if dry_run:
        count = await conn.fetchval(
            """
            SELECT COUNT(*) FROM financial_statement_cache
            WHERE symbol = $1 AND dataset = ANY($2::text[])
            """,
            sym,
            datasets,
        )
        print(f"[dry-run] would delete {count} row(s) for {sym} datasets={datasets}")
        return 0

    result = await conn.execute(
        """
        DELETE FROM financial_statement_cache
        WHERE symbol = $1 AND dataset = ANY($2::text[])
        """,
        sym,
        datasets,
    )
    print(f"Deleted for {sym} datasets={datasets}: {result}")
    return 0


async def cmd_truncate_financial(conn, dry_run: bool) -> int:
    if dry_run:
        n = await conn.fetchval("SELECT COUNT(*) FROM financial_statement_cache")
        print(f"[dry-run] would TRUNCATE financial_statement_cache ({n} rows)")
        return 0
    await conn.execute("TRUNCATE financial_statement_cache")
    print("TRUNCATE financial_statement_cache — done.")
    return 0


async def cmd_clear_valuation(conn, symbol: str, dry_run: bool) -> None:
    sym = symbol.strip().upper()
    if dry_run:
        n = await conn.fetchval("SELECT COUNT(*) FROM valuation_snapshot WHERE symbol = $1", sym)
        print(f"[dry-run] would delete {n} valuation_snapshot row(s) for {sym}")
        return
    result = await conn.execute("DELETE FROM valuation_snapshot WHERE symbol = $1", sym)
    print(f"valuation_snapshot for {sym}: {result}")


async def _run(args: argparse.Namespace) -> int:
    import asyncpg

    conn = await asyncpg.connect(dsn=_dsn())
    try:
        if args.list:
            await cmd_list(conn)
            return 0

        if args.all_financial:
            return await cmd_truncate_financial(conn, args.dry_run)

        if not args.symbol:
            print("Pass --symbol TICKER, or --all-financial, or --list.", file=sys.stderr)
            return 1

        if args.valuation_only:
            await cmd_clear_valuation(conn, args.symbol, args.dry_run)
            return 0

        err = await cmd_clear_financial(conn, args.symbol, args.datasets, args.dry_run)
        if err:
            return err

        if args.valuation:
            await cmd_clear_valuation(conn, args.symbol, args.dry_run)

        return 0
    finally:
        await conn.close()


def main() -> int:
    _load_env()
    p = argparse.ArgumentParser(
        description="Clear financial_statement_cache rows (same DB config as db.py)."
    )
    p.add_argument("--symbol", "-s", help="Ticker symbol, e.g. NVDA")
    p.add_argument(
        "--datasets",
        "-d",
        nargs="+",
        metavar="NAME",
        help=f"Limit delete to these datasets (default: all for symbol). Choices: {sorted(DATASETS)}",
    )
    p.add_argument(
        "--all-financial",
        action="store_true",
        help="TRUNCATE financial_statement_cache (all tickers).",
    )
    p.add_argument(
        "--valuation",
        action="store_true",
        help="Also DELETE valuation_snapshot rows for --symbol (after financial delete unless --valuation-only).",
    )
    p.add_argument(
        "--valuation-only",
        action="store_true",
        dest="valuation_only",
        help="Only DELETE valuation_snapshot for --symbol (skip financial_statement_cache).",
    )
    p.add_argument("--list", action="store_true", help="List financial_statement_cache rows and exit.")
    p.add_argument("--dry-run", action="store_true", help="Show what would be deleted, do not DELETE/TRUNCATE.")
    args = p.parse_args()

    if args.list and (args.symbol or args.all_financial or args.datasets or args.valuation):
        print("--list cannot be combined with delete options.", file=sys.stderr)
        return 1

    if args.all_financial and (args.symbol or args.datasets or args.valuation):
        print("--all-financial only truncates the financial cache table (no --symbol/--valuation).", file=sys.stderr)
        return 1

    if args.valuation_only and not args.symbol:
        print("--valuation-only requires --symbol.", file=sys.stderr)
        return 1

    return asyncio.run(_run(args))


if __name__ == "__main__":
    sys.exit(main())
