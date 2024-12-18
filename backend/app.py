from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from fetch.income_statement import router as income_router
from fetch.cashflow import router as cf_router
from fetch.balancesheet import router as bs_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello dawg"}

    
    
app.include_router(income_router,prefix="/financials",tags=["Income Statement"])
app.include_router(cf_router,prefix="/financials", tags=["Cash Flow"] )
app.include_router(bs_router,prefix="/financials", tags=["Balance Sheet"])