"""
Financing Risk Analyst Agent
Fetches latest 10-Q via sec-api.io, extracts financing sections, sends to OpenRouter (Gemini), returns analysis.
Uses OPENROUTER_API_KEY_GEMINI and SEC_API_KEY.
"""

import json
import os
import re
from fastapi import APIRouter, HTTPException
import requests
from dotenv import load_dotenv

import db

load_dotenv()

router = APIRouter()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL_GEMINI", "google/gemini-2.0-flash-001")
SEC_QUERY_URL = "https://api.sec-api.io"
SEC_EXTRACTOR_URL = "https://api.sec-api.io/extractor"

# Max chars per extracted section to avoid token overflow (part1item1 can be very long)
MAX_SECTION_CHARS = 80_000

SYSTEM_PROMPT = """You are a professional credit and financing-risk analyst.

You receive text excerpts from a company's most recent Form 10-Q that were already extracted by our backend using the sec-api.io Content Extraction API. These excerpts typically come from sections such as:
- "Liquidity and Capital Resources"
- "Purchase Obligations, Lease Commitments and Other Obligations"
- "Debt", "Indebtedness", "Credit Facilities", "Convertible Senior Notes"
- Other related notes that discuss borrowings, covenants, and contractual obligations.

INPUT FORMAT
You will receive a JSON object with this shape (field names may be present or empty depending on the filing):

{
  "ticker": "<TICKER>",
  "filing_date": "<YYYY-MM-DD>",
  "sections": {
    "liquidity_and_capital_resources": "<plain text or empty string>",
    "purchase_obligations_and_commitments": "<plain text or empty string>",
    "debt_and_credit_facilities": "<plain text or empty string>",
    "other_financing_notes": "<plain text or empty string>"
  }
}

Each field is raw text taken directly from the 10-Q. There may be overlap across sections. Some sections may be missing or empty; in that case, you ignore them.

YOUR GOALS

1. Identify key financing arrangements and obligations:
   - Revolving credit facilities and term loans (total capacity, amounts outstanding, maturity dates, interest rates if given).
   - Convertible notes, bonds, and other long-term debt (principal amounts, maturities, key terms).
   - Significant purchase obligations, lease commitments, and other off-balance-sheet arrangements.
   - Any minimum lease payments, non-cancelable purchase commitments, or similar long-dated obligations.

2. Assess financing risk:
   - Describe leverage and refinancing risk qualitatively (e.g., "low", "moderate", "elevated") based on the size and timing of obligations relative to the company scale implied by the text.
   - Highlight covenant requirements mentioned (e.g., leverage covenants, minimum liquidity) and whether management states the company is currently in compliance.
   - Comment on near-term vs long-term pressure: large maturities or commitments within the next 12–24 months versus later years.
   - Note any dependence on a single revolver or facility for liquidity.

3. Summarize management's own liquidity stance:
   - Extract and summarize management's statements about sufficiency of cash, cash equivalents, short-term investments, and operating cash flow to meet obligations.
   - Note any explicit warnings or uncertainty language (e.g., "substantial doubt", "may not be able to", "material uncertainty") versus confident language ("we believe", "we expect to be able to", "no required principal payments").

4. Produce structured output PLUS a narrative:
   - FIRST, output a concise JSON summary with this schema:

     {
       "ticker": "<ticker from input>",
       "filing_date": "<filing_date from input>",
       "total_revolver_capacity": "<string or null>",
       "revolver_drawn": "<string or null>",
       "revolver_maturity": "<string or null>",
       "key_debt_instruments": [
         {
           "type": "convertible_notes | term_loan | other_debt",
           "principal_amount": "<string>",
           "maturity": "<string>",
           "notable_terms": "<string>"
         }
       ],
       "purchase_obligations_description": "<string or null>",
       "lease_commitments_description": "<string or null>",
       "covenant_summary": "<string or null>",
       "management_liquidity_view": "<string>",
       "qualitative_risk_level": "low | moderate | elevated | unknown",
       "key_risk_drivers": [
         "<short phrase 1>",
         "<short phrase 2>"
       ]
     }

     - Use strings like "approximately $500 million", "no borrowings outstanding", etc., when needed.
     - If information is not disclosed, set the field to null and explain that in the narrative.

   - THEN, write the full narrative (3–6 paragraphs) as PLAIN TEXT:
     - Plain paragraphs only. Do NOT add any Markdown headings (## or ###) or bold (**) in the narrative.
     - Explain the company's financing position in plain English.
     - Highlight the most important obligations, covenants, and refinancing risks.
     - Clearly state why you labeled the qualitative risk level as low, moderate, elevated, or unknown.
     - Headings will be added separately; your output must be heading-free narrative only.

   - FINALLY, add a "## Key points" section for users who want a quick read:
     - Start with 2–3 sentences giving a high-level overview.
     - Then 3–5 bullet points covering: leverage level, revolver usage, near-term maturities, covenant situation, and qualitative risk level.
     - This section should be materially shorter than the full narrative but accurate and faithful to it.

GUARDRAILS

- Base ALL facts strictly on the supplied text excerpts. If a detail is not in the text, do NOT invent numbers or terms.
- You may infer reasonable qualitative judgments (e.g., "revolver currently undrawn, which reduces near-term refinancing pressure") as long as they are clearly supported by the text.
- Do NOT give investment advice (no buy/sell/hold or price targets). Focus only on financing and liquidity risk.
- If the text is too sparse to assess risk, say so explicitly and return "qualitative_risk_level": "unknown" with an explanation."""

USER_PROMPT_TEMPLATE = """You will receive the financing-related sections from the company's latest Form 10-Q as a JSON object.

Here is the JSON:

{SEC_SECTIONS_JSON}

Please follow your system instructions and:
1) Return the JSON summary first, in a fenced ```json code block.
2) Then return the full narrative as plain paragraphs (no headings).
3) Finally return the "## Key points" summary section."""


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
        # Build from accessionNo and cik if available
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


def _parse_llm_response(text: str) -> tuple[dict | None, str, str]:
    """Parse LLM response into JSON, narrative, and summary. Returns (json_obj, narrative, summary)."""
    json_obj = None
    narrative = ""
    summary = ""

    # Extract JSON from ```json ... ``` block
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if json_match:
        try:
            json_obj = json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Split on "## Key points" - narrative before, summary after
    key_points_marker = "## Key points"
    if key_points_marker in text:
        parts = text.split(key_points_marker, 1)
        before = parts[0].strip()
        summary = (key_points_marker + "\n\n" + parts[1].strip()) if len(parts) > 1 else ""
        # Narrative is everything after the JSON block
        if json_match:
            narrative = before[json_match.end() :].strip()
        else:
            narrative = before
    else:
        if json_match:
            narrative = text[json_match.end() :].strip()
        else:
            narrative = text.strip()

    return json_obj, narrative, summary


HEADINGS_ONLY_PROMPT = """You are a formatting assistant. Your ONLY task is to add Markdown headings to the text below.

RULES (strict):
- Insert ## or ### heading lines BEFORE logical sections or groups of paragraphs.
- You may add a top-level heading like "## Financing risk analysis" at the start if appropriate.
- Do NOT change, add, or remove any words, punctuation, or sentences from the body text.
- Do NOT add bullet points, bold, or other formatting.
- Output the exact same content with ONLY heading lines inserted (e.g., ## Revolver and debt, ## Covenants, ## Purchase obligations).
- Preserve all paragraph breaks and text exactly as given."""


def _add_headings_only(api_key: str, narrative: str) -> str:
    """Add Markdown headings to narrative without changing any body text. Falls back to original if LLM fails."""
    if not narrative or len(narrative.strip()) < 50:
        return narrative
    try:
        resp = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://investorterminal-production.up.railway.app",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": HEADINGS_ONLY_PROMPT},
                    {"role": "user", "content": f"Add headings only to this text:\n\n{narrative}"},
                ],
                "max_tokens": 4096,
                "temperature": 0.0,
            },
            timeout=60,
        )
        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("choices", [])
            if choices:
                out = choices[0].get("message", {}).get("content", "").strip()
                if out and len(out) > 20:
                    return out
    except Exception:
        pass
    return narrative


def _extract_section(url: str, item: str, sec_key: str) -> str:
    """Extract a 10-Q item via sec-api Extractor API."""
    params = {
        "url": url,
        "item": item,
        "type": "text",
        "token": sec_key,
    }
    resp = requests.get(SEC_EXTRACTOR_URL, params=params, timeout=90)
    if resp.status_code != 200:
        return ""
    text = (resp.text or "").strip()
    if len(text) > MAX_SECTION_CHARS:
        text = text[:MAX_SECTION_CHARS] + "\n\n[Content truncated due to length.]"
    return text


@router.post("/financing-risk/{ticker}")
async def analyze_financing_risk(ticker: str):
    """Fetch latest 10-Q, extract financing sections, send to OpenRouter (Gemini), return analysis."""
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

        ctx = f"{ticker_upper}:{filing_date}"
        cached = await db.fetch_llm_cache_row("financing_risk", ticker_upper, ctx)
        if cached and not db.is_llm_cache_stale(cached) and isinstance(cached.get("payload"), dict):
            return dict(cached["payload"])

        # part1item2 = MD&A (includes Liquidity and Capital Resources)
        # part1item1 = Financial Statements (includes debt, lease, commitment notes)
        mda_text = _extract_section(filing_url, "part1item2", sec_key)
        fs_text = _extract_section(filing_url, "part1item1", sec_key)

        # Map to the four sections. MD&A typically has Liquidity and Capital Resources.
        # Financial Statements contain debt, leases, purchase obligations in the notes.
        sec = {
            "liquidity_and_capital_resources": mda_text,
            "purchase_obligations_and_commitments": "",  # Often embedded in part1item1
            "debt_and_credit_facilities": "",  # Often embedded in part1item1
            "other_financing_notes": fs_text,
        }
        # If we only got FS text, put it in other_financing_notes; LLM will parse.
        # If MD&A is empty, try to use FS for liquidity (some 10-Qs structure differently)
        if not mda_text and fs_text:
            sec["liquidity_and_capital_resources"] = ""
            sec["other_financing_notes"] = fs_text

        payload = {
            "ticker": ticker_upper,
            "filing_date": filing_date,
            "sections": sec,
        }
        sec_json = json.dumps(payload, indent=2)
        user_content = USER_PROMPT_TEMPLATE.format(SEC_SECTIONS_JSON=sec_json)

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
                "temperature": 0.2,
            },
            timeout=180,
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
        financing_risk_json, raw_narrative, financing_risk_summary = _parse_llm_response(
            analysis_text
        )

        # Fallback: if parsing failed, use raw analysis
        if not raw_narrative and not financing_risk_summary:
            raw_narrative = analysis_text

        # AI narrative with headings for "Summary" tab
        financing_risk_narrative = _add_headings_only(api_key, raw_narrative) if raw_narrative else ""

        # Raw SEC filing text for "Original" tab (unprocessed content from the 10-Q)
        raw_sections = []
        if sec.get("liquidity_and_capital_resources"):
            raw_sections.append("## Liquidity and Capital Resources (MD&A)\n\n" + sec["liquidity_and_capital_resources"])
        if sec.get("other_financing_notes"):
            raw_sections.append("## Financial Statements and Notes\n\n" + sec["other_financing_notes"])
        financing_risk_raw = "\n\n---\n\n".join(raw_sections) if raw_sections else ""

        out = {
            "ticker": ticker_upper,
            "filing_date": filing_date,
            "financing_risk_json": financing_risk_json,
            "financing_risk_raw": financing_risk_raw,
            "financing_risk_narrative": financing_risk_narrative,
            "financing_risk_summary": financing_risk_summary,
            "analysis": analysis_text,
        }
        await db.upsert_llm_cache("financing_risk", ticker_upper, ctx, out, OPENROUTER_MODEL)
        return out

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
