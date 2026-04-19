"""
Cash Flow Statement Analyst Agent
Fetches quarterly cash flow data, sends to OpenRouter LLM, returns investor-friendly analysis.
"""

import json
import os
from fastapi import APIRouter, HTTPException
import numpy as np
import requests
from dotenv import load_dotenv

from fetch.cashflow import get_quarterly_cashflow_statement_data
import db

load_dotenv()

router = APIRouter()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = """You are a professional equity analyst specializing in cash flow analysis and capital allocation.

You receive structured quarterly cash flow statement data from an internal backend API.
Your job is to read the data for the last 8 quarters and explain what it tells an investor about:
- How the company generates cash from operations.
- How it reinvests cash in the business.
- How it finances itself (debt, equity, dividends, buybacks).
- The quality, sustainability, and direction of its cash flows.

DATA FORMAT YOU WILL RECEIVE

- A JSON array named `quarters`.
- `quarters[0]` is the most recent quarter, `quarters[7]` is eight quarters ago.
- Use only indexes 0 through 7.

Each element in `quarters` has three groups of fields:

1) Core cash flow metrics (numbers, in dollars unless clearly a count):
   - `fiscalDateEnding`
   - `operatingCashflow`
   - `paymentsForOperatingActivities`
   - `proceedsFromOperatingActivities`
   - `changeInOperatingLiabilities`
   - `changeInOperatingAssets`
   - `depreciationDepletionAndAmortization`
   - `capitalExpenditures` (typically negative: cash outflow)
   - `changeInReceivables`
   - `changeInInventory`
   - `profitLoss`
   - `cashflowFromInvestment`       (net cash from investing activities)
   - `cashflowFromFinancing`       (net cash from financing activities)
   - `proceedsFromRepaymentsOfShortTermDebt`
   - `paymentsForRepurchaseOfCommonStock`
   - `paymentsForRepurchaseOfEquity`
   - `paymentsForRepurchaseOfPreferredStock`
   - `dividendPayout`
   - `dividendPayoutCommonStock`
   - `dividendPayoutPreferredStock`
   - `proceedsFromRepurchaseOfEquity`
   - `netIncome`
   - `freeCashFlow`                (operating cashflow minus capitalExpenditures)

2) Ratio / margin metrics:
   - `net_profit_margin`          (string, e.g. "94.5%")
   - `ocf_margin`                 (operating cash flow as % of revenue, string)
   - `fcf_margin`                 (free cash flow as % of revenue, string)
   - `roce`                       (return on capital employed, numeric string)
   - `cash_flow_adequacy_ratio`   (numeric string)
   - `capex_ratio`                (numeric string)
   - `change_working_capital`     (dollar amount as string)

3) Growth / change metrics:
   For many core and ratio metrics, there are two derived fields:
   - `_YoY`  = year-over-year change vs the same quarter last year
   - `_QoQ`  = quarter-over-quarter change vs the prior quarter

   Examples:
   - `operatingCashflow_YoY`, `operatingCashflow_QoQ`
   - `freeCashFlow_YoY`, `freeCashFlow_QoQ`
   - `ocf_margin_YoY`, `ocf_margin_QoQ`
   - `capitalExpenditures_YoY`, `capitalExpenditures_QoQ`

Growth fields are percentages and may sometimes be "inf%" or very large when the prior period was near zero.

Additional usage notes:
- Core metrics are in dollars.
- Some fields may be 0.0 or null when not applicable.
- `operatingCashflow` and `freeCashFlow` are positive when cash is generated.
- `capitalExpenditures` is typically negative (cash outflow for investment).
- `roce`, `cash_flow_adequacy_ratio`, and `capex_ratio` are numeric strings; `change_working_capital` is a dollar amount as string.

YOUR GOALS

1. Explain the cash generation from operations:
   - Analyze the trend of `operatingCashflow` over the last 8 quarters.
   - Use `ocf_margin` and its `_YoY` / `_QoQ` fields to comment on cash conversion of revenue.
   - Discuss how changes in working capital (`changeInReceivables`, `changeInInventory`, `changeInOperatingAssets`, `changeInOperatingLiabilities`, `change_working_capital`) influence operating cash flow.

2. Describe reinvestment and capital intensity:
   - Analyze `capitalExpenditures` and `cashflowFromInvestment` to show how much the company is investing.
   - Use `freeCashFlow` and `fcf_margin` to explain how much cash is left after CapEx.
   - Comment on whether CapEx levels appear heavy, moderate, or light relative to operating cash flow and how that has changed over time.
   - Use `capex_ratio` and its growth fields if present.

3. Explain financing and capital allocation:
   - Analyze `cashflowFromFinancing` and related fields:
     - Debt activity (e.g., `proceedsFromRepaymentsOfShortTermDebt`).
     - Equity activity (e.g., `paymentsForRepurchaseOfCommonStock`, `paymentsForRepurchaseOfEquity`, `proceedsFromRepurchaseOfEquity`).
     - Capital return (dividends: `dividendPayout`, `dividendPayoutCommonStock`, `dividendPayoutPreferredStock`).
   - Describe whether the company is mainly:
     - Funding itself from internal cash generation.
     - Relying on external financing (debt or equity).
     - Returning significant cash via buybacks and/or dividends.

4. Assess quality, sustainability, and direction:
   - Compare `netIncome` versus `operatingCashflow` and `freeCashFlow` to judge earnings quality.
   - Use `_YoY` and `_QoQ` growth fields on key metrics (operatingCashflow, freeCashFlow, ocf_margin, fcf_margin) to discuss whether cash generation is improving, stable, or deteriorating.
   - Comment on whether cash flow trends support ongoing investment, debt service, and shareholder returns.
   - Highlight any quarters with unusually large positive or negative cash flows and explain them qualitatively
     (e.g., "large investment quarter", "heavy financing outflows", "benefit from working capital reversal").

5. Communicate clearly:
   - Focus on direction and magnitude rather than exact numbers, unless a specific figure is crucial.
   - Organize your answer into short sections with headings, such as:
     - "Operating cash flow"
     - "Reinvestment and free cash flow"
     - "Financing and capital allocation"
     - "Earnings quality and cash conversion"
     - "Key cash flow trends"
   - Write in plain English for a reasonably informed retail investor.

GUARDRAILS

- Do NOT make explicit buy/sell/hold recommendations.
- Do NOT provide price targets or personal financial advice.
- Do NOT invent company-specific events or numeric data that are not in the `quarters` array.
- You may use general financial-knowledge explanations (e.g., what positive free cash flow typically implies), but all claims about this company's cash flows must be grounded in the provided data.
- If key fields are missing or clearly inconsistent, briefly note the limitation and focus on the reliable parts of the dataset.
- If growth fields show "inf%" or extreme values due to near-zero denominators, explain them qualitatively instead of treating them as normal growth.

OUTPUT FORMAT

1) Start with a 2–3 sentence overview of the company's cash flow profile over the last 8 quarters.
2) Then provide 3–6 sections with headings covering:
   - Operating cash flow
   - Reinvestment and free cash flow
   - Financing and capital allocation
   - Earnings quality and cash conversion
   - Any notable volatility or inflection points
3) End with a short "Key takeaways for investors" section with 3–5 concise bullet points.
4) Output only text (no JSON), concise and well-structured."""

USER_PROMPT_TEMPLATE = """You are analyzing the quarterly cash flow statement for ticker: {ticker}.

Here is the JSON array `quarters` containing the most recent 8 quarters of cash flow statement data
(index 0 is most recent, index 7 is eight quarters ago). Use only this data.

quarters:
{quarters_json}

Please follow your system instructions and produce the full cash flow analysis."""


@router.post("/cashflow-statement/{ticker}")
async def analyze_cashflow_statement(ticker: str):
    """Fetch quarterly cash flow, slice to 8 quarters, send to OpenRouter, return analysis."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY is not configured",
        )

    try:
        ticker_u = ticker.upper()
        quarters_raw = get_quarterly_cashflow_statement_data(ticker)
        quarters = quarters_raw[:8]

        if not quarters:
            raise HTTPException(
                status_code=404,
                detail=f"No quarterly cash flow data found for {ticker}",
            )

        ctx = db.analysis_context_key(
            ticker_u, str(quarters[0].get("fiscalDateEnding") or "") if quarters else None
        )
        cached = await db.fetch_llm_cache_row("cashflow_analysis", ticker_u, ctx)
        if cached and not db.is_llm_cache_stale(cached) and isinstance(cached.get("payload"), dict):
            return dict(cached["payload"])

        def to_json_safe(val):
            if isinstance(val, (np.integer, np.int64, np.int32)):
                return int(val)
            if isinstance(val, (np.floating, np.float64, np.float32)):
                return float(val) if not (val != val) else 0
            if isinstance(val, np.bool_):
                return bool(val)
            if isinstance(val, float) and val != val:
                return 0
            return val

        quarters_clean = []
        for q in quarters:
            row = {k: to_json_safe(v) for k, v in q.items()}
            quarters_clean.append(row)

        quarters_json = json.dumps(quarters_clean, indent=2)

        user_content = USER_PROMPT_TEMPLATE.format(
            ticker=ticker.upper(),
            quarters_json=quarters_json,
        )

        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://investorterminal-production.up.railway.app",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                "max_tokens": 4096,
                "temperature": 0.3,
            },
            timeout=120,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"OpenRouter API error: {response.status_code} - {response.text[:500]}",
            )

        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise HTTPException(
                status_code=502,
                detail="OpenRouter returned no completion",
            )

        analysis_text = choices[0].get("message", {}).get("content", "").strip()
        out = {"ticker": ticker_u, "analysis": analysis_text}
        await db.upsert_llm_cache("cashflow_analysis", ticker_u, ctx, out, OPENROUTER_MODEL)
        return out

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
