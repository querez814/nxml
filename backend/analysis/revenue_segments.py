"""
Revenue Segments from MD&A
Extracts MD&A from latest 10-Q via sec-api.io, sends to OpenRouter, returns structured segment data.
Uses OPENROUTER_API_KEY_GEMINI and SEC_API_KEY.
"""

import json
import os
import re
from fastapi import APIRouter, HTTPException
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL_GEMINI", "google/gemini-2.0-flash-001")
SEC_QUERY_URL = "https://api.sec-api.io"
SEC_EXTRACTOR_URL = "https://api.sec-api.io/extractor"
MAX_SECTION_CHARS = 80_000

SYSTEM_PROMPT = """You are an equity analyst focused on **revenue segmentation**.

The backend has already used the sec-api.io Content Extraction API to pull the company's latest Form 10-Q section:

- Item 2: "Management's Discussion and Analysis of Financial Condition and Results of Operations" (MD&A).

You will receive:

- `ticker`: the company ticker (string).
- `filing_date`: the 10-Q filing date (string).
- `mdna_text`: the full plain-text MD&A section (Item 2). Segment discussion and trends are often here.
- `financial_statements_text`: the Financial Statements section (Item 1), including Notes. Segment revenue tables (e.g., "Note X: Segment Information") with dollar amounts and percentages are often here.

Your task is to examine BOTH `mdna_text` AND `financial_statements_text` to find **revenue by segment**. This may be by:
- business line / product category,
- geography / region,
- customer type or channel,
- or other clearly defined operating segments.

If segment information is present, you should **extract and normalize it**. If it is not present in MD&A, you must explicitly say that there are **no revenue segments disclosed in the MD&A text provided**.

OUTPUT FORMAT

Always respond with a single JSON object only, in this exact schema:

{
  "ticker": "<ticker>",
  "filing_date": "<filing_date>",
  "has_segment_disclosure": true | false,
  "segment_basis": "<\"business_line\" | \"geography\" | \"mixed\" | \"other\" | null>",
  "segments": [
    {
      "name": "<segment name>",
      "description": "<short description or null>",
      "period": "<period reference if mentioned, e.g., \"Q1 2026\" or \"six months ended Jan 31, 2026\" or null>",
      "revenue_amount": "<revenue figure as a string exactly as stated, e.g., \"$523.4 million\" or null>",
      "revenue_percentage_of_total": "<percentage of total revenue as a string, e.g., \"42%\" or null>",
      "trend_comment": "<one short sentence summarizing direction vs prior period, if disclosed, otherwise null>"
    }
  ],
  "no_segment_reason": "<if has_segment_disclosure is false, brief explanation such as \"MD&A only discusses consolidated revenue, no segment breakdown\"; otherwise null>"
}

DETAILED INSTRUCTIONS

1. Carefully scan BOTH `mdna_text` and `financial_statements_text` for any tables or paragraphs that:
   - list multiple revenue lines with labels and amounts, or
   - explicitly discuss revenue "by segment", "by reportable segment", "by geography", "by region", "by product category", etc.

2. If you find such disclosure:
   - Set `has_segment_disclosure` to true.
   - Set `segment_basis` to the main segmentation basis:
     - "business_line" – segments are product lines, business units, or services.
     - "geography" – segments are regions/countries.
     - "mixed" – both types are clearly present.
     - "other" – some other basis (e.g., customer type).
   - For each clearly defined segment, create one entry under `segments` with:
     - `name`: the segment label exactly or close to how the filing names it.
     - `revenue_amount`: CRITICAL – extract the dollar revenue for this segment. Look for:
       * Tables with segment names and dollar amounts (e.g., "$523.4 million", "$1.2 billion")
       * Prose like "revenue from [segment] was $X" or "[segment] revenue of $X"
       * Rows in tabular text where a segment name is followed by a dollar figure
       Copy the figure exactly as stated (e.g., "$523.4 million"). If no dollar amount is disclosed for this segment, use null.
     - `revenue_percentage_of_total`: CRITICAL – extract the share of total revenue (NOT the YoY growth rate). Look for:
       * Tables with segment names and percentage columns (e.g., "42%", "35% of total")
       * Prose like "[segment] represented X% of revenue" or "X% of total revenue"
       Copy the percentage as stated. Do NOT use growth rates like "increased 38%" here; those go in trend_comment. If no share-of-total percentage is disclosed, use null.
     - `trend_comment`: short one-sentence summary of the trend if the text explicitly compares this segment to a prior period (e.g., "Revenue in Europe increased 10% year over year due to higher demand"). Do not infer trends not stated.

3. If you do NOT find any segment breakdown:
   - Set `has_segment_disclosure` to false.
   - Set `segments` to an empty array.
   - Set `segment_basis` to null.
   - Set `no_segment_reason` to a short explanation, such as:
     - "MD&A discusses revenue only on a consolidated basis."
     - "MD&A references segments but provides no quantitative breakdown."

GUARDRAILS

- Use ONLY information in `mdna_text` and `financial_statements_text`. Do not invent segment names or amounts.
- If numbers are ambiguous, prefer leaving `revenue_amount` or `revenue_percentage_of_total` as null rather than guessing.
- Do not provide any narrative or markdown outside the JSON object.
- Do not give investment advice or qualitative ratings; your job here is purely extraction of segment information."""

USER_PROMPT_TEMPLATE = """Extract revenue segments from the following 10-Q sections.

ticker: {ticker}
filing_date: {filing_date}

=== MD&A (Item 2) ===

{mdna_text}

=== Financial Statements (Item 1, including Notes) ===

{financial_statements_text}

Respond with ONLY a single JSON object in the schema you were given. You MUST extract revenue_amount and revenue_percentage_of_total when they appear in tables or prose. No other text."""


def _get_latest_10q_url(ticker: str, sec_key: str) -> tuple[str, str]:
    """Query sec-api for latest 10-Q, return (filing_url, filing_date)."""
    payload = {
        "query": f'ticker:{ticker.upper()} AND formType:"10-Q"',
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}],
    }
    resp = requests.post(
        f"{SEC_QUERY_URL}?token={sec_key}",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"sec-api Query error: {resp.status_code} - {resp.text[:300]}",
        )
    data = resp.json()
    filings = data.get("filings") or data.get("hits") or []
    if not filings:
        raise HTTPException(
            status_code=404,
            detail=f"No 10-Q found for ticker {ticker}",
        )
    filing = filings[0]
    link = filing.get("linkToFilingDetails") or filing.get("linkToTxt") or ""
    if not link:
        acc = filing.get("accessionNo", "").replace("-", "")
        cik = filing.get("cik", "")
        if acc and cik:
            link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/index.htm"
        else:
            raise HTTPException(status_code=502, detail="Could not resolve 10-Q URL")
    if link.startswith("sec.gov"):
        link = "https://www." + link
    elif not link.startswith("http"):
        link = "https://www.sec.gov/Archives/edgar/" + link.lstrip("/")
    filed_at = filing.get("filedAt") or filing.get("filedAtHuman") or ""
    filing_date = ""
    if filed_at:
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", str(filed_at))
        if m:
            filing_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    period = filing.get("periodOfReport") or ""
    if not filing_date and period:
        filing_date = str(period)
    return link, filing_date or "unknown"


def _extract_section(url: str, item: str, sec_key: str, max_chars: int = MAX_SECTION_CHARS) -> str:
    """Extract a 10-Q item via sec-api Extractor API."""
    params = {"url": url, "item": item, "type": "text", "token": sec_key}
    resp = requests.get(SEC_EXTRACTOR_URL, params=params, timeout=90)
    if resp.status_code != 200:
        return ""
    text = (resp.text or "").strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[Content truncated due to length.]"
    return text


def _parse_json_response(text: str) -> dict | None:
    """Extract JSON from LLM response (may be wrapped in ```json ... ```)."""
    text = text.strip()
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


@router.post("/revenue-segments/{ticker}")
async def get_revenue_segments(ticker: str):
    """Fetch latest 10-Q MD&A, extract revenue segments via LLM, return structured JSON."""
    api_key = os.getenv("OPENROUTER_API_KEY_GEMINI")
    sec_key = os.getenv("SEC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY_GEMINI is not configured",
        )
    if not sec_key:
        raise HTTPException(
            status_code=500,
            detail="SEC_API_KEY is not configured (sec-api.io)",
        )

    try:
        ticker_upper = ticker.upper()
        filing_url, filing_date = _get_latest_10q_url(ticker_upper, sec_key)
        mdna_text = _extract_section(filing_url, "part1item2", sec_key, max_chars=60_000)
        financial_statements_text = _extract_section(
            filing_url, "part1item1", sec_key, max_chars=60_000
        )

        if not mdna_text or len(mdna_text.strip()) < 100:
            return {
                "ticker": ticker_upper,
                "filing_date": filing_date,
                "has_segment_disclosure": False,
                "segment_basis": None,
                "segments": [],
                "no_segment_reason": "MD&A section could not be extracted or is empty.",
            }

        user_content = USER_PROMPT_TEMPLATE.format(
            ticker=ticker_upper,
            filing_date=filing_date,
            mdna_text=mdna_text,
            financial_statements_text=financial_statements_text or "(not available)",
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
                "max_tokens": 8192,
                "temperature": 0.0,
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

        content = choices[0].get("message", {}).get("content", "").strip()
        result = _parse_json_response(content)
        if not result:
            raise HTTPException(
                status_code=502,
                detail="Could not parse LLM response as JSON",
            )

        result["ticker"] = result.get("ticker") or ticker_upper
        result["filing_date"] = result.get("filing_date") or filing_date
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
