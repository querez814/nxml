const api_url = import.meta.env.VITE_API_URL;

export const fetchBalanceSheet = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/balancesheet-statement/quarterly/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch balance sheet data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanBalanceSheetData(rawData);
};

export const fetchBalanceSheetAnnual = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/balancesheet-statement/annual/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch balance sheet data: ${response.statusText}`);
	}
	const rawData = await response.json();
	return cleanBalanceSheetDataAnnual(rawData);
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
		currentDebt: (parseFloat(item.currentDebt) / 1e6).toLocaleString(),
		current_ratio: parseFloat(item.current_ratio).toFixed(2),
		quick_ratio: parseFloat(item.quick_ratio).toFixed(2),
		cash_ratio: parseFloat(item.cash_ratio).toFixed(2),
		debt_to_equity_ratio: parseFloat(item.debt_to_equity_ratio).toFixed(2),
		debt_to_asset_ratio: parseFloat(item.debt_to_asset_ratio).toFixed(2),
		book_value_per_share: parseFloat(item.book_value_per_share).toFixed(2),
		totalCurrentAssets_YoY: item.totalCurrentAssets_YoY,
		totalAssets_YoY: item.totalAssets_YoY,
		totalCurrentLiabilities_YoY: item.totalCurrentLiabilities_YoY,
		totalLiabilities_YoY: item.totalLiabilities_YoY,
		working_capital_YoY: item.working_capital_YoY,
		totalShareholderEquity_YoY: item.totalShareholderEquity_YoY,
		commonStockSharesOutstanding_YoY: item.commonStockSharesOutstanding_YoY,
		cashAndCashEquivalentsAtCarryingValue_YoY: item.cashAndCashEquivalentsAtCarryingValue_YoY,
		inventory_YoY: item.inventory_YoY,
		propertyPlantEquipment_YoY: item.propertyPlantEquipment_YoY,
		deferredRevenue_YoY: item.deferredRevenue_YoY,
		currentDebt_YoY: item.currentDebt_YoY,
		current_ratio_YoY: item.current_ratio_YoY,
		quick_ratio_YoY: item.quick_ratio_YoY,
		cash_ratio_YoY: item.cash_ratio_YoY,
		debt_to_equity_ratio_YoY: item.debt_to_equity_ratio_YoY,
		debt_to_asset_ratio_YoY: item.debt_to_asset_ratio_YoY,
		book_value_per_share_YoY: item.book_value_per_share_YoY,
		totalCurrentAssets_QoQ: item.totalCurrentAssets_QoQ,
		totalAssets_QoQ: item.totalAssets_QoQ,
		totalCurrentLiabilities_QoQ: item.totalCurrentLiabilities_QoQ,
		totalLiabilities_QoQ: item.totalLiabilities_QoQ,
		working_capital_QoQ: item.working_capital_QoQ,
		totalShareholderEquity_QoQ: item.totalShareholderEquity_QoQ,
		commonStockSharesOutstanding_QoQ: item.commonStockSharesOutstanding_QoQ,
		cashAndCashEquivalentsAtCarryingValue_QoQ: item.cashAndCashEquivalentsAtCarryingValue_QoQ,
		inventory_QoQ: item.inventory_QoQ,
		propertyPlantEquipment_QoQ: item.propertyPlantEquipment_QoQ,
		deferredRevenue_QoQ: item.deferredRevenue_QoQ,
		currentDebt_QoQ: item.currentDebt_QoQ,
		current_ratio_QoQ: item.current_ratio_QoQ,
		quick_ratio_QoQ: item.quick_ratio_QoQ,
		cash_ratio_QoQ: item.cash_ratio_QoQ,
		debt_to_equity_ratio_QoQ: item.debt_to_equity_ratio_QoQ,
		debt_to_asset_ratio_QoQ: item.debt_to_asset_ratio_QoQ,
		book_value_per_share_QoQ: item.book_value_per_share_QoQ
	}));
};

const cleanBalanceSheetDataAnnual = (data: any[]): any[] => {
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
		currentDebt: (parseFloat(item.currentDebt) / 1e6).toLocaleString(),
		current_ratio: parseFloat(item.current_ratio).toFixed(2),
		quick_ratio: parseFloat(item.quick_ratio).toFixed(2),
		cash_ratio: parseFloat(item.cash_ratio).toFixed(2),
		debt_to_equity_ratio: parseFloat(item.debt_to_equity_ratio).toFixed(2),
		debt_to_asset_ratio: parseFloat(item.debt_to_asset_ratio).toFixed(2),
		book_value_per_share: parseFloat(item.book_value_per_share).toFixed(2),
		totalCurrentAssets_YoY: item.totalCurrentAssets_YoY,
		totalAssets_YoY: item.totalAssets_YoY,
		totalCurrentLiabilities_YoY: item.totalCurrentLiabilities_YoY,
		totalLiabilities_YoY: item.totalLiabilities_YoY,
		working_capital_YoY: item.working_capital_YoY,
		totalShareholderEquity_YoY: item.totalShareholderEquity_YoY,
		commonStockSharesOutstanding_YoY: item.commonStockSharesOutstanding_YoY,
		cashAndCashEquivalentsAtCarryingValue_YoY: item.cashAndCashEquivalentsAtCarryingValue_YoY,
		inventory_YoY: item.inventory_YoY,
		propertyPlantEquipment_YoY: item.propertyPlantEquipment_YoY,
		deferredRevenue_YoY: item.deferredRevenue_YoY,
		currentDebt_YoY: item.currentDebt_YoY,
		current_ratio_YoY: item.current_ratio_YoY,
		quick_ratio_YoY: item.quick_ratio_YoY,
		cash_ratio_YoY: item.cash_ratio_YoY,
		debt_to_equity_ratio_YoY: item.debt_to_equity_ratio_YoY,
		debt_to_asset_ratio_YoY: item.debt_to_asset_ratio_YoY,
		book_value_per_share_YoY: item.book_value_per_share_YoY
	}));
};
