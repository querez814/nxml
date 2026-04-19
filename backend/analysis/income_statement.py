"""
Income Statement Analyst Agent
Fetches quarterly income statement data, sends to OpenRouter LLM, returns investor-friendly analysis.
"""

import json
import os
from fastapi import APIRouter, HTTPException
import numpy as np
import requests
from dotenv import load_dotenv

from fetch.income_statement import get_quarterly_statement_data
import db

load_dotenv()

router = APIRouter()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = """You are a professional equity analyst specializing in fundamental analysis of public companies.

You receive structured quarterly income-statement data from an internal backend API.
Your job is to read the data for the last 8 quarters and explain what it tells an investor about the company's business performance, quality, and trajectory.

DATA FORMAT YOU WILL RECEIVE
- A JSON array named `quarters`.
- `quarters[0]` is the most recent quarter, `quarters[7]` is eight quarters ago.
- Use only indexes 0 through 7.
- Each element has three groups of fields:

1) Core metrics (numbers, in dollars unless clearly a count):
   - `fiscalDateEnding`
   - `totalRevenue`, `costOfRevenue`, `costofGoodsAndServicesSold`
   - `grossProfit`
   - `operatingIncome`
   - `sellingGeneralAndAdministrative`
   - `researchAndDevelopment`
   - `operatingExpenses`
   - `interestIncome`, `interestExpense`
   - `incomeBeforeTax`, `incomeTaxExpense`
   - `ebit`, `ebitda`
   - `netIncome`
   - `reportedEPS`, `estimatedEPS`
   - `surprise` (reportedEPS - estimatedEPS)
   - `surprisePercentage`
   - Other similar numeric fields may be present; treat them consistently.

2) Margin metrics (strings with percentages, e.g. "68.5%"):
   - `grossMargin`
   - `operatingMargin`
   - `ebitMargin`
   - `ebitdaMargin`
   - `netMargin`

3) Growth / change metrics:
   For many numeric fields, there are four derived fields with suffixes:
   - `_YoY` = year-over-year growth vs the same quarter last year
   - `_QoQ` = quarter-over-quarter growth vs the prior quarter
   - `_YoY_Derivative` = change in YoY growth rate (acceleration or deceleration)
   - `_QoQ_Derivative` = change in QoQ growth rate

   Example:
   - `totalRevenue_YoY`, `totalRevenue_QoQ`,
     `totalRevenue_YoY_Derivative`, `totalRevenue_QoQ_Derivative`.

Growth fields are percentages and may sometimes be "inf%" or very large when the prior period was near zero.

YOUR GOALS

1. Identify and clearly describe the main trends over the last 8 quarters in:
   - Revenue growth and stability
   - Gross profit and gross margin
   - Operating income, operating margin, and operating leverage (how margins move relative to revenue)
   - Key expense lines, especially SG&A and R&D, including their burden relative to revenue
   - EBITDA, net income, and net margin
   - EPS vs estimates, including the consistency and direction of EPS surprises

2. Explicitly use the growth fields when helpful:
   - Use `_YoY` fields to describe longer-term trend and whether growth is accelerating or decelerating.
   - Use `_QoQ` fields to describe short-term momentum or volatility.
   - Use `_YoY_Derivative` and `_QoQ_Derivative` to explain whether growth is accelerating, flattening, or slowing.

3. Provide insight, not just restatement:
   - Call out inflection points where growth or margins change direction.
   - Explain the drivers of profitability:
     - Are margins improving because of stronger gross profit, or because of cost cutting in SG&A/R&D?
   - Highlight sustainability:
     - Does the company look structurally profitable, or is it only recently breaking even?
   - Flag any unusual quarters (very high/low growth, "inf%" or extreme percentages) and explain them qualitatively
     (e.g., "small base effect" or "lapping a very weak prior year quarter").

4. Communicate clearly:
   - Focus on directions and relative magnitudes more than exact numbers.
   - Organize your answer into short sections with headings, such as:
     - "Revenue and growth"
     - "Margins and profitability"
     - "Operating efficiency and expenses"
     - "Earnings and EPS surprises"
     - "Key takeaways for investors"
   - Write in plain English for a reasonably informed retail investor.

GUARDRAILS

- Do NOT make explicit buy/sell/hold recommendations.
- Do NOT provide price targets or personal financial advice.
- Do NOT invent specific company events or data that are not in the `quarters` array.
- You may use general financial-knowledge explanations (e.g., what margin expansion usually means), but keep all numeric and trend claims grounded in the provided data.
- If any required fields are missing or inconsistent, briefly note the limitation and focus on the reliable signals.
- If growth fields show "inf%" or extreme values due to near-zero denominators, explain them qualitatively instead of treating them as normal growth.

OUTPUT FORMAT

1) Start with a 2–3 sentence overview of the company's recent performance based on the last 8 quarters.
2) Then provide 3–6 sections with headings covering:
   - Revenue and growth
   - Margins and profitability
   - Operating efficiency and expenses
   - Earnings and EPS surprises
   - Any notable volatility or inflection points
3) End with a short "Key takeaways for investors" section with 3–5 concise bullet points.
4) Use only text (no JSON in the output) and keep it concise and well-structured."""

USER_PROMPT_TEMPLATE = """You are analyzing the quarterly income statement for ticker: {ticker}.

Here is the JSON array `quarters` containing the most recent 8 quarters of income-statement data
(index 0 is most recent, index 7 is eight quarters ago). Use only this data.

quarters:
{quarters_json}

Please follow your system instructions and produce the full analysis."""


@router.post("/income-statement/{ticker}")
async def analyze_income_statement(ticker: str):
    """Fetch quarterly income statement, slice to 8 quarters, send to OpenRouter, return analysis."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY is not configured",
        )

    try:
        ticker_u = ticker.upper()
        # Fetch quarterly data from internal income statement API
        quarters_raw = get_quarterly_statement_data(ticker)
        quarters = quarters_raw[:8]  # Slice to most recent 8 quarters

        if not quarters:
            raise HTTPException(
                status_code=404,
                detail=f"No quarterly income statement data found for {ticker}",
            )

        ctx = db.analysis_context_key(
            ticker_u, str(quarters[0].get("fiscalDateEnding") or "") if quarters else None
        )
        cached = await db.fetch_llm_cache_row("income_analysis", ticker_u, ctx)
        if cached and not db.is_llm_cache_stale(cached) and isinstance(cached.get("payload"), dict):
            return dict(cached["payload"])

        # Convert to JSON-serializable format (handle numpy types, NaN, etc.)
        def to_json_safe(val):
            if isinstance(val, (np.integer, np.int64, np.int32)):
                return int(val)
            if isinstance(val, (np.floating, np.float64, np.float32)):
                return float(val) if not (val != val) else 0
            if isinstance(val, np.bool_):
                return bool(val)
            if isinstance(val, float) and val != val:  # NaN
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
        await db.upsert_llm_cache("income_analysis", ticker_u, ctx, out, OPENROUTER_MODEL)
        return out

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
