const api_url = import.meta.env.VITE_API_URL;

export const fetchBalanceSheet = async (ticker: string): Promise<any[]> => {
	const response = await fetch(
		`https://investorterminal-production.up.railway.app/financials/balancesheet-statement/quarterly/${ticker}`
	);
	if (!response.ok) {
		throw new Error(`Failed to fetch balance sheet data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanBalanceSheetData(rawData);
};

export const fetchBalanceSheetRatios = async (ticker: string): Promise<any[]> => {
	const response = await fetch(
		`${api_url}/financials/balancesheet-statement/quarterly/${ticker}/ratios`
	);
	if (!response.ok) {
		throw new Error(`Failed to fetch balance sheet ratios data: ${response.statusText}`);
	}
	const rawData = await response.json();
	return cleanBalanceSheetRatiosData(rawData);
};

const cleanBalanceSheetData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		totalCurrentAssets: (parseFloat(item.totalCurrentAssets) / 1e6).toLocaleString(),
		totalAssets: (parseFloat(item.totalAssets) / 1e6).toLocaleString(),
		totalCurrentLiabilities: (parseFloat(item.totalCurrentLiabilities) / 1e6).toLocaleString(),
		totalLiabilities: (parseFloat(item.totalLiabilities) / 1e6).toLocaleString(),
		working_capital: (parseFloat(item.working_capital) / 1e6).toLocaleString(),
		totalShareholderEquity: (parseFloat(item.totalShareholderEquity) / 1e6).toLocaleString(),
		commonStockSharesOutstanding: parseFloat(item.commonStockSharesOutstanding).toLocaleString(),
		cashAndCashEquivalentsAtCarryingValue: (
			parseFloat(item.cashAndCashEquivalentsAtCarryingValue) / 1e6
		).toLocaleString(),
		inventory: (parseFloat(item.inventory) / 1e6).toLocaleString(),
		propertyPlantEquipment: (parseFloat(item.propertyPlantEquipment) / 1e6).toLocaleString(),
		deferredRevenue: (parseFloat(item.deferredRevenue) / 1e6).toLocaleString(),
		currentDebt: (parseFloat(item.currentDebt) / 1e6).toLocaleString()
	}));
};

const cleanBalanceSheetRatiosData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		current_ratio: item.current_ratio,
		quick_ratio: item.quick_ratio,
		cash_ratio: item.cash_ratio,
		debt_to_equity_ratio: item.debt_to_equity_ratio,
		debt_to_asset_ratio: item.debt_to_asset_ratio,
		book_value_per_share: item.book_value_per_share
	}));
};
