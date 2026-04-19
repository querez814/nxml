from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fetch.cashflow import router as cashflow_router
from fetch.balancesheet import router as balancesheet_router
from fetch.income_statement import router as income_router
from fetch.is_computations import router as is_computations_router
from fetch.earnings import router as earnings_router
from fetch.earnings_estimates import router as earnings_estimates_router
from fetch.dividends import router as dividends_router
from fetch.valuations import router as valuation_router
from fetch.summary import router as summary_router
from fetch.prices import router as prices_router
from fetch.technicals import router as entry_router
from packages import router as pkg_router
from news_recap import router as news_recap_router
from newssearch import router as news_router
from earningscalendar import router as calendar_router
#from competitors import router as competitors_router
from fetch.latextobinaryimg import router as latex_router
from entry import router as init_router
from technicals.momentum import router as momentum_router
from movers import router as movers_router
from analysis.income_statement import router as analysis_income_router
from analysis.cashflow_statement import router as analysis_cashflow_router
from analysis.balancesheet_statement import router as analysis_balancesheet_router
from analysis.financing_risk import router as analysis_financing_risk_router
from analysis.revenue_segments import router as analysis_revenue_segments_router
from technicals.sma import router as setup_router
from technicals.rsi import router as rsi_router
from technicals.dmi import router as dmi_router
from technicals.oscillators import router as oscillator_router
from technicals.macd import router as macd_router
import db as valuation_db
import http_client as shared_http


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Record the running event loop so worker-thread sync helpers
    # (db.sync_wait_awaitable) can schedule DB work back onto the loop that
    # owns the asyncpg pool, instead of spinning up a throwaway loop that
    # would later raise "Event loop is closed".
    valuation_db.set_main_loop()
    # Warm the valuation cache pool. Failure is non-fatal (valuations fall back to on-demand compute).
    await valuation_db.get_pool()
    await shared_http.init_http_client()
    try:
        yield
    finally:
        await shared_http.close_http_client()
        await valuation_db.close_pool()
        valuation_db.set_main_loop(None)


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "https://theinvestorterminal.vercel.app",
        "https://www.yourduediligence.app",  
        "https://yourduediligence.app",  
        "https://investorterminal-production.up.railway.app",
        "https://n8n.simplicitytechsolutions.com",
        "https://byom-chat.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
@app.get("/")
def read_root():
    return {"Hello dawg"}

    
app.include_router(earnings_router, prefix="/financials", tags=["Earnings Statement"])
app.include_router(earnings_estimates_router, prefix="/financials", tags=["Earnings Estimates"])
app.include_router(dividends_router, prefix="/financials", tags=["Dividends"])
app.include_router(income_router, prefix="/financials", tags=["Income Statement"])
app.include_router(cashflow_router, prefix="/financials", tags=["Cash Flow"])
app.include_router(balancesheet_router, prefix="/financials", tags=["Balance Sheet"])
app.include_router(is_computations_router, prefix="/financials", tags=["Income Computations"])
app.include_router(valuation_router,prefix="/financials",tags=["Valuation"])
app.include_router(summary_router, prefix="/financials", tags=["Summary"])
app.include_router(prices_router, prefix="/financials", tags=["Summary"])
app.include_router(entry_router, prefix="/technicals", tags=["Technicals"])
app.include_router(pkg_router, prefix="/current", tags=["Current"])
app.include_router(news_recap_router, prefix="/news", tags=["News recap"])
app.include_router(news_router, prefix="/news", tags=["Current"])
app.include_router(calendar_router, prefix="/news", tags=["Current"])
app.include_router(latex_router, tags=["latex"])
app.include_router(init_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(momentum_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(setup_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(rsi_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(dmi_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(macd_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(oscillator_router, prefix="/technicals", tags = ["Technicals"] )
app.include_router(movers_router, prefix="/current", tags=["Current"])
app.include_router(analysis_income_router, prefix="/analysis", tags=["Analysis"])
app.include_router(analysis_cashflow_router, prefix="/analysis", tags=["Analysis"])
app.include_router(analysis_balancesheet_router, prefix="/analysis", tags=["Analysis"])
app.include_router(analysis_financing_risk_router, prefix="/analysis", tags=["Analysis"])
app.include_router(analysis_revenue_segments_router, prefix="/analysis", tags=["Analysis"])
#app.include_router(competitors_router, prefix="/current", tags=["Current"])
#app.include_router(screener_router, prefix="/screen", tags=["Current"])
