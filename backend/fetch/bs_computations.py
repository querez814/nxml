from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
import pandas as pd

router = APIRouter()


@router.get("/balancesheet-statement/quarterly/{ticker}/ratios")
def bs_ratios(ticker: str):
    raw_bs_data = get_quarterly_balance_sheet_data(ticker)
    if not isinstance(raw_bs_data, list) or len(raw_bs_data) == 0:
        raise HTTPException(status_code=404, detail="No balance sheet data found.")
    
    bs_df = pd.DataFrame(raw_bs_data)
    
    numeric_columns = [
        "totalCurrentAssets", "totalCurrentLiabilities", "cashAndCashEquivalentsAtCarryingValue",
        "inventory", "totalLiabilities", "totalAssets", "totalShareholderEquity", "commonStockSharesOutstanding"
    ]
    for col in numeric_columns:
        bs_df[col] = pd.to_numeric(bs_df[col], errors="coerce")
    
    try:
        current_ratio = bs_df["totalCurrentAssets"] / bs_df["totalCurrentLiabilities"]
        quick_ratio = (bs_df["totalCurrentAssets"] - bs_df["inventory"]) / bs_df["totalCurrentLiabilities"]
        cash_ratio = bs_df["cashAndCashEquivalentsAtCarryingValue"] / bs_df["totalCurrentLiabilities"]
        debt_to_equity_ratio = bs_df["totalLiabilities"] / bs_df["totalShareholderEquity"]
        debt_to_asset_ratio = bs_df["totalLiabilities"] / bs_df["totalAssets"]
        book_value_per_share = bs_df["totalShareholderEquity"] / bs_df["commonStockSharesOutstanding"]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing column in data: {str(e)}")
    
    bs_ratios_df = pd.DataFrame({
        "fiscalDateEnding": bs_df["fiscalDateEnding"],
        "current_ratio": current_ratio,
        "quick_ratio": quick_ratio,
        "cash_ratio": cash_ratio,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "debt_to_asset_ratio": debt_to_asset_ratio,
        "book_value_per_share": book_value_per_share
    })
    
    bs_ratios_df = bs_ratios_df.fillna(0)
    for col in bs_ratios_df.columns:
        if col != "fiscalDateEnding":
            bs_ratios_df[col] = bs_ratios_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0")
    
    return bs_ratios_df.to_dict(orient="records")


@router.get("/balancesheet-statement/quarterly/{ticker}/yoy")
def get_yoy(ticker: str):
    """
    Calculate Year-Over-Year (YoY) changes for balance sheet items.
    """
    raw_bs_data = get_quarterly_balance_sheet_data(ticker)
    if not isinstance(raw_bs_data, list) or len(raw_bs_data) == 0:
        raise HTTPException(status_code=404, detail="No balance sheet data found.")
    
    bs_df = pd.DataFrame(raw_bs_data)
    
    for col in bs_df.columns:
        if col != "fiscalDateEnding":
            bs_df[col] = pd.to_numeric(bs_df[col], errors="coerce")
    
    bs_df = bs_df.iloc[::-1].reset_index(drop=True)
    yoy_df = bs_df.set_index("fiscalDateEnding").pct_change(periods=4) * 100
    
    yoy_df.columns = [f"{col}_YoY" for col in yoy_df.columns]
    yoy_df = yoy_df.reset_index().iloc[::-1].reset_index(drop=True)
    
    for col in yoy_df.columns:
        if col != "fiscalDateEnding":
            yoy_df[col] = yoy_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    return yoy_df.to_dict(orient="records")



@router.get("/balancesheet-statement/quarterly/{ticker}/qoq")
def get_qoq(ticker: str):
    raw_bs_data = get_quarterly_balance_sheet_data(ticker)
    if not isinstance(raw_bs_data, list) or len(raw_bs_data) == 0:
        raise HTTPException(status_code=404, detail="No balance sheet data found.")
    
    bs_df = pd.DataFrame(raw_bs_data)
    
    for col in bs_df.columns:
        if col != "fiscalDateEnding":
            bs_df[col] = pd.to_numeric(bs_df[col], errors="coerce")
    
    bs_df = bs_df.iloc[::-1].reset_index(drop=True)
    qoq_df = bs_df.set_index("fiscalDateEnding").pct_change(periods=1) * 100
    
    qoq_df.columns = [f"{col}_QoQ" for col in qoq_df.columns]
    qoq_df = qoq_df.reset_index().iloc[::-1].reset_index(drop=True)
    
    for col in qoq_df.columns:
        if col != "fiscalDateEnding":
            qoq_df[col] = qoq_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    return qoq_df.to_dict(orient="records")
