import { dedupeRequest } from '$lib/utils/inflightRequestCache';
const api_url = import.meta.env.VITE_API_URL;

export type ValuationSnapshot = {
	fiscalDateEnding: string;
	symbol: string;
	sector: string | null;
	industry: string | null;

	shares_outstanding: number | null;
	market_cap: number | null;
	enterprise_value: number | null;
	adjusted_price: number | null;
	latest_closing_price: number | null;
	latest_market_cap: number | null;
	latest_enterprise_value: number | null;

	pe_ratio: number | null;
	pe_fwd: number | null;
	pe_fwd_nongaap: number | null;
	peg_ratio: number | null;
	peg_nongaap_fwd: number | null;
	ps_ttm: number | null;
	ps_fwd: number | null;
	pb_ratio: number | null;
	price_to_cash_flow_ttm: number | null;
	price_to_fcf_ttm: number | null;

	ev_to_revenue: number | null;
	ev_to_sales_fwd: number | null;
	ev_to_ebitda: number | null;
	ev_to_ebit: number | null;
	ev_to_gross_profit: number | null;
	ev_to_fcf_ttm: number | null;
	ev_to_net_income: number | null;

	dividend_yield: number | null;
	dividend_yield_ttm: number | null;
	dividend_per_share: number | null;
	payout_ratio: number | null;

	profit_margin: number | null;
	operating_margin_ttm: number | null;
	roa_ttm: number | null;
	roe_ttm: number | null;
	book_value_per_share: number | null;
	diluted_eps_ttm: number | null;
	revenue_per_share_ttm: number | null;
	rev_growth_yoy: number | null;
	eps_growth_yoy: number | null;

	beta: number | null;
	week52_high: number | null;
	week52_low: number | null;
	ma_50d: number | null;
	ma_200d: number | null;

	analyst_target_price: number | null;
	analyst_rating_strong_buy: number | null;
	analyst_rating_buy: number | null;
	analyst_rating_hold: number | null;
	analyst_rating_sell: number | null;
	analyst_rating_strong_sell: number | null;
};

export type ValuationLayout = {
	symbol: string;
	sector: string | null;
	industry: string | null;
	order: string[];
	labels: Record<string, string>;
	values: Record<string, number | null>;
	latest: ValuationSnapshot;
	five_year_avg: Record<string, number | null>;
};

const NUMERIC_KEYS: (keyof ValuationSnapshot)[] = [
	'shares_outstanding', 'market_cap', 'enterprise_value', 'adjusted_price',
	'latest_closing_price', 'latest_market_cap', 'latest_enterprise_value',
	'pe_ratio', 'pe_fwd', 'pe_fwd_nongaap', 'peg_ratio', 'peg_nongaap_fwd',
	'ps_ttm', 'ps_fwd', 'pb_ratio', 'price_to_cash_flow_ttm', 'price_to_fcf_ttm',
	'ev_to_revenue', 'ev_to_sales_fwd', 'ev_to_ebitda', 'ev_to_ebit',
	'ev_to_gross_profit', 'ev_to_fcf_ttm', 'ev_to_net_income',
	'dividend_yield', 'dividend_yield_ttm', 'dividend_per_share', 'payout_ratio',
	'profit_margin', 'operating_margin_ttm', 'roa_ttm', 'roe_ttm',
	'book_value_per_share', 'diluted_eps_ttm', 'revenue_per_share_ttm',
	'rev_growth_yoy', 'eps_growth_yoy',
	'beta', 'week52_high', 'week52_low', 'ma_50d', 'ma_200d',
	'analyst_target_price', 'analyst_rating_strong_buy', 'analyst_rating_buy',
	'analyst_rating_hold', 'analyst_rating_sell', 'analyst_rating_strong_sell'
];

const parseNumber = (value: unknown): number | null => {
	if (value === null || value === undefined) return null;
	if (typeof value === 'number') return Number.isFinite(value) ? value : null;
	const s = String(value).trim();
	if (s === '' || s === '-' || s === 'None' || s === 'NM' || s === 'N/A') return null;
	const n = Number(s.replace(/,/g, ''));
	return Number.isFinite(n) ? n : null;
};

const cleanSnapshot = (raw: Record<string, unknown>): ValuationSnapshot => {
	const out = { ...raw } as Record<string, unknown>;
	for (const k of NUMERIC_KEYS) {
		out[k] = parseNumber(raw[k as string]);
	}
	return out as unknown as ValuationSnapshot;
};

export const fetchValuation = async (ticker: string): Promise<ValuationSnapshot[]> => {
	const url = `${api_url}/financials/valuation/quarterly/${ticker}/ttm`;
	return dedupeRequest(`valuation-q:${ticker.toUpperCase()}`, async () => {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`Failed to fetch valuation data: ${response.statusText}`);
		}
		const rawData = (await response.json()) as Record<string, unknown>[];
		return rawData.map(cleanSnapshot);
	});
};

export const fetchValuationLayout = async (ticker: string): Promise<ValuationLayout> => {
	const url = `${api_url}/financials/valuation/layout/${ticker}`;
	return dedupeRequest(`valuation-layout:${ticker.toUpperCase()}`, async () => {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`Failed to fetch valuation layout: ${response.statusText}`);
		}
		const raw = (await response.json()) as {
			symbol: string;
			sector: string | null;
			industry: string | null;
			order: string[];
			labels: Record<string, string>;
			values: Record<string, unknown>;
			latest: Record<string, unknown>;
			five_year_avg: Record<string, unknown>;
		};

		const values: Record<string, number | null> = {};
		for (const col of raw.order) values[col] = parseNumber(raw.values?.[col]);

		const fiveY: Record<string, number | null> = {};
		for (const [k, v] of Object.entries(raw.five_year_avg ?? {})) fiveY[k] = parseNumber(v);

		return {
			symbol: raw.symbol,
			sector: raw.sector,
			industry: raw.industry,
			order: raw.order,
			labels: raw.labels,
			values,
			latest: cleanSnapshot(raw.latest),
			five_year_avg: fiveY
		};
	});
};

const PERCENT_KEYS = new Set([
	'dividend_yield', 'dividend_yield_ttm', 'payout_ratio',
	'profit_margin', 'operating_margin_ttm', 'roa_ttm', 'roe_ttm',
	'rev_growth_yoy', 'eps_growth_yoy'
]);

export const formatRatio = (key: string, value: number | null): string => {
	if (value === null || !Number.isFinite(value)) return '-';
	if (PERCENT_KEYS.has(key)) return `${(value * 100).toFixed(2)}%`;
	return `${value.toFixed(2)}x`;
};
