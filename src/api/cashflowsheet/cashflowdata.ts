const api_url = import.meta.env.VITE_API_URL;
export const fetchCashFlow = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/cashflow-statement/quarterly/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch balance sheet data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanCashFlowData(rawData);
};

export const fetchCashFlowMargins = async (ticker: string): Promise<any[]> => {
	const response = await fetch(
		`${api_url}/financials/cashflow-statement/quarterly/${ticker}/margins`
	);
	if (!response.ok) {
		throw new Error(`Failed to fetch cash flow margin data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanCashFlowMarginsData(rawData);
};

export const fetchCashFlowRatios = async (ticker: string): Promise<any[]> => {
	const response = await fetch(
		`${api_url}/financials/cashflow-statement/quarterly/${ticker}/ratios`
	);
	if (!response.ok) {
		throw new Error(`Failed to fetch cash flow ratios data: ${response.statusText}`);
	}
	const rawData = await response.json();
	return cleanCashFlowRatiosData(rawData);
};

const cleanCashFlowData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		operatingCashflow: parseFloat(item.operatingCashflow) / 1e6,
		capitalExpenditures: parseFloat(item.capitalExpenditures) / 1e6,
		freeCashFlow: parseFloat(item.freeCashFlow) / 1e6,
		changeInInventory: parseFloat(item.changeInInventory) / 1e6,
		changeInReceivables: parseFloat(item.changeInReceivables) / 1e6,
		cashflowFromInvestment: parseFloat(item.cashFlowFromInvestment) / 1e6,
		cashflowFromFinancing: parseFloat(item.cashflowFromFinancing) / 1e6,
		paymentsForRepurchaseOfCommonStock: parseFloat(item.paymentsForRepurchaseOfCommonStock) / 1e6,
		paymentsForRepurchaseOfEquity: parseFloat(item.paymentsForRepurchaseOfEquity) / 1e6,
		dividendPayout: parseFloat(item.dividendPayout) / 1e6
	}));
};

const cleanCashFlowMarginsData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		net_profit_margin: parseFloat(item.net_profit_margin),
		ocf_margin: parseFloat(item.ocf_margin),
		fcf_margin: parseFloat(item.fcf_margin)
	}));
};

const cleanCashFlowRatiosData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		roce: parseFloat(item.roce),
		cfa_ratio: parseFloat(item.cfa_ratio),
		capex_ratio: parseFloat(item.capex_ratio),
		change_working_capital: parseFloat(item.change_working_capital) / 1e6
	}));
};
