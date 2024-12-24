const api_url = import.meta.env.VITE_API_URL;

export const fetchIncomeStatement = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/income-statement/quarterly/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch income statement data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanIncomeStatementData(rawData);
};

export const fetchIncomeStatementMargins = async (ticker: string): Promise<any[]> => {
	const response = await fetch(
		`${api_url}/financials/income-statement/quarterly/${ticker}/margins`
	);
	if (!response.ok) {
		throw new Error(`Failed to fetch income statement margins data: ${response.statusText}`);
	}
	const rawData = await response.json();
	return cleanIncomeStatementMarginsData(rawData);
};
const cleanIncomeStatementData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		totalRevenue: (parseFloat(item.totalRevenue) / 1e6).toLocaleString(),
		costOfRevenue: (parseFloat(item.costOfRevenue) / 1e6).toLocaleString(),
		costofGoodsAndServicesSold: (
			parseFloat(item.costofGoodsAndServicesSold) / 1e6
		).toLocaleString(),
		grossProfit: (parseFloat(item.grossProfit) / 1e6).toLocaleString(),
		operatingIncome: (parseFloat(item.operatingIncome) / 1e6).toLocaleString(),
		sellingGeneralAndAdministrative: (
			parseFloat(item.sellingGeneralAndAdministrative) / 1e6
		).toLocaleString(),
		researchAndDevelopment: (parseFloat(item.researchAndDevelopment) / 1e6).toLocaleString(),
		operatingExpenses: (parseFloat(item.operatingExpenses) / 1e6).toLocaleString(),
		interestIncome: (parseFloat(item.interestIncome) / 1e6).toLocaleString(),
		interestExpense: (parseFloat(item.interestExpense) / 1e6).toLocaleString(),
		incomeBeforeTax: (parseFloat(item.incomeBeforeTax) / 1e6).toLocaleString(),
		incomeTaxExpense: (parseFloat(item.incomeTaxExpense) / 1e6).toLocaleString(),
		interestAndDebtExpense: (parseFloat(item.interestAndDebtExpense) / 1e6).toLocaleString(),
		ebitda: (parseFloat(item.ebitda) / 1e6).toLocaleString(),
		netIncome: (parseFloat(item.netIncome) / 1e6).toLocaleString(),
		reportedEPS: parseFloat(item.reportedEPS).toFixed(2),
		estimatedEPS: parseFloat(item.estimatedEPS).toFixed(2),
		surprise: parseFloat(item.surprise).toFixed(2),
		surprisePercentage: parseFloat(item.surprisePercentage).toFixed(2)
	}));
};

const cleanIncomeStatementMarginsData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		grossMargin: item.grossMargin,
		ebitdaMargin: item.ebitdaMargin,
		operatingMargin: item.operatingMargin,
		netMargin: item.netMargin
	}));
};
