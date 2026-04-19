/**
 * Builds DataTable props from raw financial rows — mirrors sub-route pages so the drawer matches full pages.
 */

import { formatRatio } from '../../api/valuation/valuationdata';
import { keepVarianceKey } from './financialTableKeys';

function incomeFormatMetricName(name: string): string {
	const specialCases: Record<string, string> = {
		costofGoodsAndServicesSold: 'Cost of Goods and Services Sold',
		sellingGeneralAndAdministrative: 'Selling, General and Administrative',
		researchAndDevelopment: 'Research and Development',
		interestAndDebtExpense: 'Interest and Debt Expense',
		ebit: 'EBIT',
		ebitda: 'EBITDA',
		reportedEPS: 'Reported EPS ',
		estimatedEPS: 'Estimated EPS',
		surprise: 'EPS Surprise'
	};
	if (specialCases[name]) return specialCases[name];
	return name
		.replace(/([A-Z])/g, ' $1')
		.split('_')
		.join(' ')
		.trim()
		.replace(/\b\w/g, (c) => c.toUpperCase());
}

function bsCfFormatMetricName(name: string): string {
	return name
		.replace(/([A-Z])/g, ' $1')
		.split('_')
		.join(' ')
		.trim()
		.replace(/\b\w/g, (c) => c.toUpperCase());
}

const incomeMarginMetrics = ['grossMargin', 'ebitMargin', 'ebitdaMargin', 'operatingMargin', 'netMargin'];

const incomeExcludedKeys = [
	'_id',
	'symbol',
	'reportedCurrency',
	'__v',
	'surprisePercentage',
	'ebitMargin',
	'fiscalDateEnding',
	...incomeMarginMetrics
];

export function buildIncomeStatementTables(quarters: Record<string, unknown>[]) {
	if (!quarters.length) {
		return {
			rawData: [] as Record<string, unknown>[],
			yoyData: [] as Record<string, unknown>[],
			qoqData: [] as Record<string, unknown>[],
			marginsData: [] as Record<string, unknown>[],
			quarterDates: [] as string[]
		};
	}
	const q0 = quarters[0] as Record<string, unknown>;
	const quarterDates = quarters.map((q) => String((q as { fiscalDateEnding: string }).fiscalDateEnding));

	const rawData = Object.keys(q0)
		.filter(
			(key) =>
				!incomeExcludedKeys.includes(key) &&
				!key.includes('_Derivative') &&
				!key.endsWith('_YoY') &&
				!key.endsWith('_QoQ')
		)
		.map((metric) => ({
			metric: incomeFormatMetricName(metric),
			originalMetric: metric,
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const yoyData = Object.keys(q0)
		.filter(
			(key) =>
				key.endsWith('_YoY') &&
				!key.includes('_Derivative') &&
				!incomeMarginMetrics.some((m) => key.startsWith(m))
		)
		.map((metric) => ({
			metric: incomeFormatMetricName(metric.replace('_YoY', '')),
			originalMetric: metric.replace('_YoY', ''),
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const qoqData = Object.keys(q0)
		.filter(
			(key) =>
				key.endsWith('_QoQ') &&
				!key.includes('_Derivative') &&
				!incomeMarginMetrics.some((m) => key.startsWith(m))
		)
		.map((metric) => ({
			metric: incomeFormatMetricName(metric.replace('_QoQ', '')),
			originalMetric: metric.replace('_QoQ', ''),
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const marginsData = incomeMarginMetrics.map((metric) => ({
		metric: incomeFormatMetricName(metric),
		originalMetric: metric,
		...quarters.reduce(
			(acc, quarter) => ({
				...acc,
				[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[metric]
			}),
			{}
		)
	}));

	return { rawData, yoyData, qoqData, marginsData, quarterDates };
}

export function buildBalanceSheetTables(quarters: Record<string, unknown>[]) {
	if (!quarters.length) {
		return {
			rawData: [] as Record<string, unknown>[],
			yoyData: [] as Record<string, unknown>[],
			qoqData: [] as Record<string, unknown>[],
			quarterDates: [] as string[]
		};
	}
	const q0 = quarters[0] as Record<string, unknown>;
	const quarterDates = quarters.map((q) => String((q as { fiscalDateEnding: string }).fiscalDateEnding));

	const rawData = Object.keys(q0)
		.filter(
			(key) =>
				!['_id', 'symbol', 'reportedCurrency', '__v', 'fiscalDateEnding'].includes(key) &&
				!key.endsWith('_YoY') &&
				!key.endsWith('_QoQ')
		)
		.map((metric) => ({
			metric: bsCfFormatMetricName(metric),
			originalMetric: metric,
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const yoyData = Object.keys(q0)
		.filter((key) => key.endsWith('_YoY'))
		.map((metric) => ({
			metric: bsCfFormatMetricName(metric.replace('_YoY', '')),
			originalMetric: metric.replace('_YoY', ''),
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const qoqData = Object.keys(q0)
		.filter((key) => key.endsWith('_QoQ'))
		.map((metric) => ({
			metric: bsCfFormatMetricName(metric.replace('_QoQ', '')),
			originalMetric: metric.replace('_QoQ', ''),
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	return { rawData, yoyData, qoqData, quarterDates };
}

const cfMarginMetrics = [
	'net_profit_margin',
	'ocf_margin',
	'fcf_margin',
	'roce',
	'cash_flow_adequacy_ratio',
	'capex_ratio'
];

const cfExcludedKeys = ['_id', 'symbol', 'reportedCurrency', '__v', 'fiscalDateEnding', ...cfMarginMetrics];

export function buildCashFlowTables(quarters: Record<string, unknown>[]) {
	if (!quarters.length) {
		return {
			rawData: [] as Record<string, unknown>[],
			yoyData: [] as Record<string, unknown>[],
			qoqData: [] as Record<string, unknown>[],
			marginsData: [] as Record<string, unknown>[],
			quarterDates: [] as string[],
			marginMetrics: cfMarginMetrics
		};
	}
	const q0 = quarters[0] as Record<string, unknown>;
	const quarterDates = quarters.map((q) => String((q as { fiscalDateEnding: string }).fiscalDateEnding));

	const rawData = Object.keys(q0)
		.filter((key) => !cfExcludedKeys.includes(key) && !key.endsWith('_YoY') && !key.endsWith('_QoQ'))
		.map((metric) => ({
			metric: bsCfFormatMetricName(metric),
			originalMetric: metric,
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const yoyData = Object.keys(q0)
		.filter((key) => keepVarianceKey(key, cfMarginMetrics, '_YoY'))
		.map((metric) => ({
			metric: bsCfFormatMetricName(metric.replace('_YoY', '')),
			originalMetric: metric.replace('_YoY', ''),
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const qoqData = Object.keys(q0)
		.filter(
			(key) => !key.includes('_Derivative') && keepVarianceKey(key, cfMarginMetrics, '_QoQ')
		)
		.map((metric) => ({
			metric: bsCfFormatMetricName(metric.replace('_QoQ', '')),
			originalMetric: metric.replace('_QoQ', ''),
			...quarters.reduce(
				(acc, quarter) => ({
					...acc,
					[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[
						metric
					]
				}),
				{}
			)
		}));

	const marginsData = cfMarginMetrics.map((metric) => ({
		metric: bsCfFormatMetricName(metric),
		originalMetric: metric,
		...quarters.reduce(
			(acc, quarter) => ({
				...acc,
				[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: (quarter as Record<string, unknown>)[metric]
			}),
			{}
		)
	}));

	return { rawData, yoyData, qoqData, marginsData, quarterDates, marginMetrics: cfMarginMetrics };
}

const valuationMetricDisplayNames: Record<string, string> = {
	pe_ratio: 'P/E (TTM)',
	pe_fwd: 'P/E (FWD)',
	pe_fwd_nongaap: 'P/E Non-GAAP (FWD)',
	peg_ratio: 'PEG (TTM)',
	peg_nongaap_fwd: 'PEG Non-GAAP (FWD)',
	ps_ttm: 'P/S (TTM)',
	ps_fwd: 'P/S (FWD)',
	pb_ratio: 'P/B',
	price_to_cash_flow_ttm: 'P/CF (TTM)',
	price_to_fcf_ttm: 'P/FCF (TTM)',
	ev_to_revenue: 'EV/Sales (TTM)',
	ev_to_sales_fwd: 'EV/Sales (FWD)',
	ev_to_ebitda: 'EV/EBITDA (TTM)',
	ev_to_ebit: 'EV/EBIT (TTM)',
	ev_to_gross_profit: 'EV/Gross Profit (TTM)',
	ev_to_fcf_ttm: 'EV/FCF (TTM)',
	ev_to_net_income: 'EV/Net Income (TTM)',
	dividend_yield: 'Dividend Yield',
	dividend_yield_ttm: 'Dividend Yield (TTM)',
	payout_ratio: 'Payout Ratio',
	roe_ttm: 'ROE (TTM)',
	roa_ttm: 'ROA (TTM)',
	profit_margin: 'Profit Margin',
	operating_margin_ttm: 'Operating Margin (TTM)',
	book_value_per_share: 'Book Value / Share',
	revenue_per_share_ttm: 'Revenue Per Share (TTM)'
};

function valuationFormatMetricName(name: string): string {
	return (
		valuationMetricDisplayNames[name] ||
		name
			.replace(/([A-Z])/g, ' $1')
			.split('_')
			.join(' ')
			.trim()
			.replace(/\b\w/g, (c) => c.toUpperCase())
	);
}

const valuationMetrics = [
	'pe_ratio',
	'pe_fwd',
	'pe_fwd_nongaap',
	'peg_ratio',
	'peg_nongaap_fwd',
	'ps_ttm',
	'ps_fwd',
	'pb_ratio',
	'ev_to_revenue',
	'ev_to_sales_fwd',
	'ev_to_ebitda',
	'ev_to_ebit',
	'ev_to_gross_profit',
	'ev_to_net_income',
	'price_to_cash_flow_ttm',
	'price_to_fcf_ttm',
	'ev_to_fcf_ttm',
	'dividend_yield',
	'dividend_yield_ttm',
	'payout_ratio',
	'profit_margin',
	'operating_margin_ttm',
	'roa_ttm',
	'roe_ttm',
	'book_value_per_share',
	'revenue_per_share_ttm'
];

function parseValuationField(value: unknown): number | null {
	if (value === null || value === undefined) return null;
	if (typeof value === 'number') return Number.isFinite(value) ? value : null;
	const s = String(value).trim().replace(/,/g, '');
	if (s === '' || s === '-' || s === 'None' || s === 'NM' || s === 'N/A') return null;
	const n = Number(s);
	return Number.isFinite(n) ? n : null;
}

/** True when at least two periods have numeric values that differ (TTM / trailing actually moves). */
export function metricVariesAcrossPeriods(
	quarters: Record<string, unknown>[],
	metric: string
): boolean {
	const nums = quarters
		.map((q) => parseValuationField((q as Record<string, unknown>)[metric]))
		.filter((n): n is number => n !== null);
	if (nums.length <= 1) return false;
	const ref = nums[0];
	const scale = Math.max(Math.abs(ref), 1e-9);
	return nums.some((n) => Math.abs(n - ref) > 1e-6 * scale);
}

function latestNonNullRaw(
	quarters: Record<string, unknown>[],
	metric: string
): number | null {
	const sorted = [...quarters].sort(
		(a, b) =>
			new Date((b as { fiscalDateEnding: string }).fiscalDateEnding).getTime() -
			new Date((a as { fiscalDateEnding: string }).fiscalDateEnding).getTime()
	);
	for (const q of sorted) {
		const v = parseValuationField((q as Record<string, unknown>)[metric]);
		if (v !== null) return v;
	}
	return null;
}

export type ValuationStaticRow = { label: string; value: string };

/**
 * Splits valuation metrics: **by period** when values change across fiscal dates; **spot / forward** when the
 * source repeats the same figure every column (no TTM, forward only, or duplicated spot fields).
 */
export function buildValuationTable(quarters: Record<string, unknown>[]) {
	if (!quarters.length) {
		return {
			rawData: [] as Record<string, unknown>[],
			quarterDates: [] as string[],
			ratioMetrics: [] as string[],
			staticRows: [] as ValuationStaticRow[]
		};
	}
	const quarterDates = quarters.map((q) => String((q as { fiscalDateEnding: string }).fiscalDateEnding));

	const varyingKeys: string[] = [];
	const staticKeys: string[] = [];
	for (const metric of valuationMetrics) {
		if (metricVariesAcrossPeriods(quarters, metric)) varyingKeys.push(metric);
		else staticKeys.push(metric);
	}

	const rawData = varyingKeys.map((metric) => ({
		metric: valuationFormatMetricName(metric),
		originalMetric: metric,
		...quarters.reduce(
			(acc, quarter) => ({
				...acc,
				[(quarter as { fiscalDateEnding: string }).fiscalDateEnding]: formatRatio(
					metric,
					(quarter as Record<string, number | null>)[metric] ?? null
				)
			}),
			{}
		)
	}));

	const staticRows: ValuationStaticRow[] = staticKeys.map((metric) => ({
		label: valuationFormatMetricName(metric),
		value: formatRatio(metric, latestNonNullRaw(quarters, metric))
	}));

	return {
		rawData,
		quarterDates,
		ratioMetrics: varyingKeys,
		staticRows
	};
}
