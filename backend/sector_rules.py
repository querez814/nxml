"""Sector-aware ratio display rules.

Maps Alpha Vantage `Sector` strings (uppercase, e.g. "TECHNOLOGY") to the
ordered list of valuation-ratio column names that are most meaningful for
that sector. Unknown sectors fall back to `DEFAULT_ORDER`.
"""
from __future__ import annotations

from typing import List

DEFAULT_ORDER: List[str] = [
    "pe_ratio", "pe_fwd", "pe_fwd_nongaap",
    "peg_ratio", "peg_nongaap_fwd",
    "ps_ttm", "ps_fwd",
    "ev_to_revenue", "ev_to_sales_fwd",
    "ev_to_ebitda", "ev_to_ebit", "ev_to_gross_profit",
    "pb_ratio",
    "price_to_cash_flow_ttm", "price_to_fcf_ttm", "ev_to_fcf_ttm",
    "ev_to_net_income",
    "dividend_yield", "dividend_yield_ttm",
]

SECTOR_ORDERS: dict[str, List[str]] = {
    "TECHNOLOGY": [
        "ps_fwd", "ps_ttm",
        "ev_to_sales_fwd", "ev_to_revenue",
        "ev_to_gross_profit",
        "pe_fwd_nongaap", "pe_fwd", "pe_ratio",
        "ev_to_ebitda",
        "peg_nongaap_fwd", "peg_ratio",
        "price_to_fcf_ttm", "ev_to_fcf_ttm",
        "pb_ratio",
    ],
    "COMMUNICATION SERVICES": [
        "pe_fwd", "pe_ratio",
        "ev_to_ebitda", "ev_to_ebit",
        "ps_ttm", "ev_to_revenue",
        "price_to_fcf_ttm", "ev_to_fcf_ttm",
        "pb_ratio",
        "dividend_yield",
    ],
    "FINANCE": [
        "pe_ratio", "pe_fwd",
        "pb_ratio",
        "roe_ttm",
        "dividend_yield", "dividend_yield_ttm",
        "peg_ratio",
    ],
    "FINANCIAL SERVICES": [
        "pe_ratio", "pe_fwd",
        "pb_ratio",
        "roe_ttm",
        "dividend_yield", "dividend_yield_ttm",
        "peg_ratio",
    ],
    "REAL ESTATE": [
        "pb_ratio",
        "dividend_yield", "dividend_yield_ttm",
        "ev_to_ebitda",
        "ps_ttm",
        "price_to_fcf_ttm",
        "pe_ratio",
    ],
    "ENERGY": [
        "ev_to_ebitda",
        "price_to_cash_flow_ttm", "price_to_fcf_ttm", "ev_to_fcf_ttm",
        "pe_ratio", "pe_fwd",
        "pb_ratio",
        "dividend_yield",
    ],
    "BASIC MATERIALS": [
        "ev_to_ebitda",
        "price_to_cash_flow_ttm", "price_to_fcf_ttm",
        "pe_ratio", "pe_fwd",
        "pb_ratio",
        "dividend_yield",
    ],
    "UTILITIES": [
        "pe_ratio", "pe_fwd",
        "dividend_yield", "dividend_yield_ttm",
        "pb_ratio",
        "ev_to_ebitda",
        "price_to_fcf_ttm",
    ],
    "CONSUMER DEFENSIVE": [
        "pe_fwd", "pe_ratio",
        "ev_to_ebitda", "ev_to_ebit",
        "ps_ttm", "ev_to_revenue",
        "dividend_yield",
        "peg_ratio",
    ],
    "CONSUMER CYCLICAL": [
        "pe_fwd", "pe_ratio",
        "ev_to_ebitda", "ev_to_ebit",
        "ps_ttm", "ev_to_revenue",
        "price_to_fcf_ttm",
        "peg_ratio",
    ],
    "HEALTHCARE": [
        "pe_fwd", "pe_ratio",
        "ev_to_ebitda",
        "ps_ttm", "ps_fwd", "ev_to_revenue",
        "price_to_fcf_ttm",
        "peg_ratio",
    ],
    "HEALTH CARE": [
        "pe_fwd", "pe_ratio",
        "ev_to_ebitda",
        "ps_ttm", "ps_fwd", "ev_to_revenue",
        "price_to_fcf_ttm",
        "peg_ratio",
    ],
    "INDUSTRIALS": [
        "pe_fwd", "pe_ratio",
        "ev_to_ebitda", "ev_to_ebit",
        "pb_ratio",
        "price_to_fcf_ttm",
        "ps_ttm",
        "dividend_yield",
    ],
}


DISPLAY_LABELS: dict[str, str] = {
    "pe_ratio":               "P/E (TTM)",
    "pe_fwd":                 "P/E (FWD)",
    "pe_fwd_nongaap":         "P/E Non-GAAP (FWD)",
    "peg_ratio":              "PEG (TTM)",
    "peg_nongaap_fwd":        "PEG Non-GAAP (FWD)",
    "ps_ttm":                 "P/S (TTM)",
    "ps_fwd":                 "P/S (FWD)",
    "pb_ratio":               "P/B",
    "price_to_cash_flow_ttm": "P/CF (TTM)",
    "price_to_fcf_ttm":       "P/FCF (TTM)",
    "ev_to_revenue":          "EV/Sales (TTM)",
    "ev_to_sales_fwd":        "EV/Sales (FWD)",
    "ev_to_ebitda":           "EV/EBITDA (TTM)",
    "ev_to_ebit":             "EV/EBIT (TTM)",
    "ev_to_gross_profit":     "EV/Gross Profit (TTM)",
    "ev_to_fcf_ttm":          "EV/FCF (TTM)",
    "ev_to_net_income":       "EV/Net Income (TTM)",
    "dividend_yield":         "Dividend Yield",
    "dividend_yield_ttm":     "Dividend Yield (TTM)",
    "roe_ttm":                "ROE (TTM)",
    "roa_ttm":                "ROA (TTM)",
    "profit_margin":          "Profit Margin",
    "operating_margin_ttm":   "Operating Margin (TTM)",
    "book_value_per_share":   "Book Value / Share",
}


def get_ratio_priority(sector: str | None) -> List[str]:
    """Return the ordered ratio column names to display for `sector`."""
    if not sector:
        return DEFAULT_ORDER
    key = sector.strip().upper()
    return SECTOR_ORDERS.get(key, DEFAULT_ORDER)


def label_for(column: str) -> str:
    return DISPLAY_LABELS.get(column, column.replace("_", " ").title())
