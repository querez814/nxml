const api_url: string = import.meta.env.VITE_API_URL;

export const fetchValuation = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/valuation/quarterly/${ticker}/ttm`);
	if (!response.ok) {
		throw new Error(`Failed to fetch income statement data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return cleanValuationStatementData(rawData);
};

const cleanValuationStatementData = (data: any[]): any[] => {
	return data.map((item) => ({
		fiscalDateEnding: item.fiscalDateEnding,
		symbol: item.symbol,
		evtosales: parseNumber(item.evtosales),
		evtogrossprofit: parseNumber(item.evtogrossprofit),
		evtoebit: parseNumber(item.evtoebit),
		evtoebitda: parseNumber(item.evtoebitda),
		evtonetincome: parseNumber(item.evtonetincome),
		revenue_per_share_ttm: parseNumber(item.revenue_per_share_ttm),
		price_to_sales_ratio_ttm: parseNumber(item.price_to_sales_ratio_ttm),
		AnalystTargetPrice: parseNumber(item.AnalystTargetPrice),
		AnalystRatingStrongBuy: parseNumber(item.AnalystRatingStrongBuy),
		AnalystRatingBuy: parseNumber(item.AnalystRatingBuy),
		AnalystRatingHold: parseNumber(item.AnalystRatingHold),
		AnalystRatingSell: parseNumber(item.AnalystRatingSell),
		AnalystRatingStrongSell: parseNumber(item.AnalystRatingStrongSell),
		TrailingPE: parseNumber(item.TrailingPE),
		ForwardPE: parseNumber(item.ForwardPE)
	}));
};

const parseNumber = (value: any): number | null => {
	return value === 'None' ? null : Number(value);
};
