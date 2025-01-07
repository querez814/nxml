const api_url = import.meta.env.VITE_API_URL;

export const fetchCashFlow = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/cashflow-statement/quarterly/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch cash flow data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanCashFlowData(rawData);
};

const cleanCashFlowData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,

		operatingCashflow: (parseFloat(item.operatingCashflow) / 1e6).toLocaleString(),
		paymentsForOperatingActivities: (
			parseFloat(item.paymentsForOperatingActivities) / 1e6
		).toLocaleString(),
		proceedsFromOperatingActivities: (
			parseFloat(item.proceedsFromOperatingActivities) / 1e6
		).toLocaleString(),
		changeInOperatingLiabilities: (
			parseFloat(item.changeInOperatingLiabilities) / 1e6
		).toLocaleString(),
		changeInOperatingAssets: (parseFloat(item.changeInOperatingAssets) / 1e6).toLocaleString(),
		depreciationDepletionAndAmortization: (
			parseFloat(item.depreciationDepletionAndAmortization) / 1e6
		).toLocaleString(),
		capitalExpenditures: (parseFloat(item.capitalExpenditures) / 1e6).toLocaleString(),
		changeInReceivables: (parseFloat(item.changeInReceivables) / 1e6).toLocaleString(),
		changeInInventory: (parseFloat(item.changeInInventory) / 1e6).toLocaleString(),
		profitLoss: (parseFloat(item.profitLoss) / 1e6).toLocaleString(),
		cashflowFromInvestment: (parseFloat(item.cashflowFromInvestment) / 1e6).toLocaleString(),
		cashflowFromFinancing: (parseFloat(item.cashflowFromFinancing) / 1e6).toLocaleString(),
		proceedsFromRepaymentsOfShortTermDebt: (
			parseFloat(item.proceedsFromRepaymentsOfShortTermDebt) / 1e6
		).toLocaleString(),
		paymentsForRepurchaseOfCommonStock: (
			parseFloat(item.paymentsForRepurchaseOfCommonStock) / 1e6
		).toLocaleString(),
		paymentsForRepurchaseOfEquity: (
			parseFloat(item.paymentsForRepurchaseOfEquity) / 1e6
		).toLocaleString(),
		paymentsForRepurchaseOfPreferredStock: (
			parseFloat(item.paymentsForRepurchaseOfPreferredStock) / 1e6
		).toLocaleString(),
		dividendPayout: (parseFloat(item.dividendPayout) / 1e6).toLocaleString(),
		dividendPayoutCommonStock: (parseFloat(item.dividendPayoutCommonStock) / 1e6).toLocaleString(),
		dividendPayoutPreferredStock: (
			parseFloat(item.dividendPayoutPreferredStock) / 1e6
		).toLocaleString(),
		proceedsFromRepurchaseOfEquity: (
			parseFloat(item.proceedsFromRepurchaseOfEquity) / 1e6
		).toLocaleString(),
		netIncome: (parseFloat(item.netIncome) / 1e6).toLocaleString(),
		freeCashFlow: (parseFloat(item.freeCashFlow) / 1e6).toLocaleString(),
		change_working_capital: (parseFloat(item.change_working_capital) / 1e6).toLocaleString(),

		// Parsing Cash Flow Ratios
		net_profit_margin: item.net_profit_margin,
		ocf_margin: item.ocf_margin,
		fcf_margin: item.fcf_margin,
		roce: parseFloat(item.roce).toFixed(2),
		cash_flow_adequacy_ratio: parseFloat(item.cash_flow_adequacy_ratio).toFixed(2),
		capex_ratio: parseFloat(item.capex_ratio).toFixed(2),

		// Mapping YoY
		operatingCashflow_YoY: item.operatingCashflow_YoY,
		paymentsForOperatingActivities_YoY: item.paymentsForOperatingActivities_YoY,
		proceedsFromOperatingActivities_YoY: item.proceedsFromOperatingActivities_YoY,
		changeInOperatingLiabilities_YoY: item.changeInOperatingLiabilities_YoY,
		changeInOperatingAssets_YoY: item.changeInOperatingAssets_YoY,
		depreciationDepletionAndAmortization_YoY: item.depreciationDepletionAndAmortization_YoY,
		capitalExpenditures_YoY: item.capitalExpenditures_YoY,
		changeInReceivables_YoY: item.changeInReceivables_YoY,
		changeInInventory_YoY: item.changeInInventory_YoY,
		profitLoss_YoY: item.profitLoss_YoY,
		cashflowFromInvestment_YoY: item.cashflowFromInvestment_YoY,
		cashflowFromFinancing_YoY: item.cashflowFromFinancing_YoY,
		proceedsFromRepaymentsOfShortTermDebt_YoY: item.proceedsFromRepaymentsOfShortTermDebt_YoY,
		paymentsForRepurchaseOfCommonStock_YoY: item.paymentsForRepurchaseOfCommonStock_YoY,
		paymentsForRepurchaseOfEquity_YoY: item.paymentsForRepurchaseOfEquity_YoY,
		paymentsForRepurchaseOfPreferredStock_YoY: item.paymentsForRepurchaseOfPreferredStock_YoY,
		dividendPayout_YoY: item.dividendPayout_YoY,
		dividendPayoutCommonStock_YoY: item.dividendPayoutCommonStock_YoY,
		dividendPayoutPreferredStock_YoY: item.dividendPayoutPreferredStock_YoY,
		proceedsFromRepurchaseOfEquity_YoY: item.proceedsFromRepurchaseOfEquity_YoY,
		netIncome_YoY: item.netIncome_YoY,
		freeCashFlow_YoY: item.freeCashFlow_YoY,
		net_profit_margin_YoY: item.net_profit_margin_YoY,
		ocf_margin_YoY: item.ocf_margin_YoY,
		fcf_margin_YoY: item.fcf_margin_YoY,
		roce_YoY: item.roce_YoY,
		cash_flow_adequacy_ratio_YoY: item.cash_flow_adequacy_ratio_YoY,
		capex_ratio_YoY: item.capex_ratio_YoY,
		change_working_capital_YoY: item.change_working_capital_YoY,

		// Mapping QoQ
		operatingCashflow_QoQ: item.operatingCashflow_QoQ,
		paymentsForOperatingActivities_QoQ: item.paymentsForOperatingActivities_QoQ,
		proceedsFromOperatingActivities_QoQ: item.proceedsFromOperatingActivities_QoQ,
		changeInOperatingLiabilities_QoQ: item.changeInOperatingLiabilities_QoQ,
		changeInOperatingAssets_QoQ: item.changeInOperatingAssets_QoQ,
		depreciationDepletionAndAmortization_QoQ: item.depreciationDepletionAndAmortization_QoQ,
		capitalExpenditures_QoQ: item.capitalExpenditures_QoQ,
		changeInReceivables_QoQ: item.changeInReceivables_QoQ,
		changeInInventory_QoQ: item.changeInInventory_QoQ,
		profitLoss_QoQ: item.profitLoss_QoQ,
		cashflowFromInvestment_QoQ: item.cashflowFromInvestment_QoQ,
		cashflowFromFinancing_QoQ: item.cashflowFromFinancing_QoQ,
		proceedsFromRepaymentsOfShortTermDebt_QoQ: item.proceedsFromRepaymentsOfShortTermDebt_QoQ,
		paymentsForRepurchaseOfCommonStock_QoQ: item.paymentsForRepurchaseOfCommonStock_QoQ,
		paymentsForRepurchaseOfEquity_QoQ: item.paymentsForRepurchaseOfEquity_QoQ,
		paymentsForRepurchaseOfPreferredStock_QoQ: item.paymentsForRepurchaseOfPreferredStock_QoQ,
		dividendPayout_QoQ: item.dividendPayout_QoQ,
		dividendPayoutCommonStock_QoQ: item.dividendPayoutCommonStock_QoQ,
		dividendPayoutPreferredStock_QoQ: item.dividendPayoutPreferredStock_QoQ,
		proceedsFromRepurchaseOfEquity_QoQ: item.proceedsFromRepurchaseOfEquity_QoQ,
		netIncome_QoQ: item.netIncome_QoQ,
		freeCashFlow_QoQ: item.freeCashFlow_QoQ,
		net_profit_margin_QoQ: item.net_profit_margin_QoQ,
		ocf_margin_QoQ: item.ocf_margin_QoQ,
		fcf_margin_QoQ: item.fcf_margin_QoQ,
		roce_QoQ: item.roce_QoQ,
		cash_flow_adequacy_ratio_QoQ: item.cash_flow_adequacy_ratio_QoQ,
		capex_ratio_QoQ: item.capex_ratio_QoQ,
		change_working_capital_QoQ: item.change_working_capital_QoQ
	}));
};
