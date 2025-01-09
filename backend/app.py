from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from fetch.cashflow import router as cashflow_router
from fetch.balancesheet import router as balancesheet_router
from fetch.income_statement import router as income_router
from fetch.is_computations import router as is_computations_router
from fetch.earnings import router as earnings_router
from fetch.valuations import router as valuation_router
from fetch.summary import router as summary_router
from fetch.prices import router as prices_router
from fetch.technicals import router as entry_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "https://theinvestorterminal.vercel.app",  
        "https://investorterminal-production.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello dawg"}

    
app.include_router(earnings_router, prefix="/financials", tags=["Earnings Statement"])    
app.include_router(income_router, prefix="/financials", tags=["Income Statement"])
app.include_router(cashflow_router, prefix="/financials", tags=["Cash Flow"])
app.include_router(balancesheet_router, prefix="/financials", tags=["Balance Sheet"])
app.include_router(is_computations_router, prefix="/financials", tags=["Income Computations"])
app.include_router(valuation_router,prefix="/financials",tags=["Valuation"])
app.include_router(summary_router, prefix="/financials", tags=["Summary"])
app.include_router(prices_router, prefix="/financials", tags=["Summary"])
app.include_router(entry_router, prefix="/technicals", tags=["Technicals"])