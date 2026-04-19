import {
	parseMillionsString,
	parsePercentString,
	parseRatioString
} from './financeFormat';
import type { ValuationSnapshot, ValuationLayout } from '../../api/valuation/valuationdata';

export type PulseKpi = {
	label: string;
	value: string;
	qoq: { text: string; numeric: number | null };
	yoy: { text: string; numeric: number | null };
	hint?: string;
};

export type PulseCardData = {
	kpis: PulseKpi[];
	sparkline: (number | null)[];
	health: {
		currentRatio?: number | null;
		debtToEquity?: number | null;
		revGrowthYoY?: number | null;
		netMargin?: number | null;
		fcf?: number | null;
		ocf?: number | null;
		pe?: number | null;
		pe5y?: number | null;
	};
};

export type VitalsData = {
	revenueTTM: number | null;
	revenueQoQ: number | null;
	revenueYoY: number | null;
	netIncomeTTM: number | null;
	netIncomeQoQ: number | null;
	netIncomeYoY: number | null;
	fcfTTM: number | null;
	fcfQoQ: number | null;
	fcfYoY: number | null;
	epsTTM: number | null;
	epsSurprise: number | null;
};

const fmtPct = (n: number | null): string => {
	if (n == null || !Number.isFinite(n)) return '—';
	const sign = n > 0 ? '+' : '';
	return `${sign}${n.toFixed(1)}%`;
};

const fmtPp = (n: number | null): string => {
	if (n == null || !Number.isFinite(n)) return '—';
	const sign = n > 0 ? '+' : '';
	return `${sign}${n.toFixed(1)}pp`;
};

const fmtRatioDelta = (n: number | null): string => {
	if (n == null || !Number.isFinite(n)) return '—';
	const sign = n > 0 ? '+' : '';
	return `${sign}${n.toFixed(2)}`;
};

const fmtMillionsCompact = (mm: number | null): string => {
	if (mm == null || !Number.isFinite(mm)) return '—';
	const abs = Math.abs(mm);
	if (abs >= 1_000_000) return `$${(mm / 1_000_000).toFixed(2)}T`;
	if (abs >= 1_000) return `$${(mm / 1_000).toFixed(2)}B`;
	return `$${mm.toFixed(1)}M`;
};

const fmtRatioValue = (n: number | null, digits = 2): string => {
	if (n == null || !Number.isFinite(n)) return '—';
	return n.toFixed(digits);
};

const fmtPctValue = (n: number | null, digits = 1): string => {
	if (n == null || !Number.isFinite(n)) return '—';
	return `${n.toFixed(digits)}%`;
};

function sum4(arr: (number | null)[]): number | null {
	const clean = arr.slice(0, 4).filter((v): v is number => v != null && Number.isFinite(v));
	if (clean.length === 0) return null;
	if (clean.length < 4) return null;
	return clean.reduce((a, b) => a + b, 0);
}

export function buildIncomeCard(incomeQuarters: any[]): PulseCardData {
	const q = incomeQuarters ?? [];
	const latest = q[0] ?? null;
	const revenue = latest ? parseMillionsString(latest.totalRevenue) : null;
	const revQoQ = latest ? parsePercentString(latest.totalRevenue_QoQ) : null;
	const revYoY = latest ? parsePercentString(latest.totalRevenue_YoY) : null;
	const netMargin = latest ? parsePercentString(latest.netMargin) : null;
	const netMarginQoQ = latest ? parsePercentString(latest.netMargin_QoQ) : null;
	const netMarginYoY = latest ? parsePercentString(latest.netMargin_YoY) : null;

	const sparkline = q
		.slice(0, 8)
		.reverse()
		.map((row) => parseMillionsString(row.totalRevenue));

	return {
		kpis: [
			{
				label: 'Revenue',
				value: fmtMillionsCompact(revenue),
				qoq: { text: fmtPct(revQoQ), numeric: revQoQ },
				yoy: { text: fmtPct(revYoY), numeric: revYoY }
			},
			{
				label: 'Net margin',
				value: fmtPctValue(netMargin),
				qoq: { text: fmtPct(netMarginQoQ), numeric: netMarginQoQ },
				yoy: { text: fmtPct(netMarginYoY), numeric: netMarginYoY }
			}
		],
		sparkline,
		health: {
			revGrowthYoY: revYoY,
			netMargin
		}
	};
}

export function buildBalanceCard(balanceQuarters: any[]): PulseCardData {
	const q = balanceQuarters ?? [];
	const latest = q[0] ?? null;
	const cash = latest
		? parseMillionsString(latest.cashAndCashEquivalentsAtCarryingValue)
		: null;
	const cashQoQ = latest
		? parsePercentString(latest.cashAndCashEquivalentsAtCarryingValue_QoQ)
		: null;
	const cashYoY = latest
		? parsePercentString(latest.cashAndCashEquivalentsAtCarryingValue_YoY)
		: null;
	const de = latest ? parseRatioString(latest.debt_to_equity_ratio) : null;
	const deQoQ = latest ? parsePercentString(latest.debt_to_equity_ratio_QoQ) : null;
	const deYoY = latest ? parsePercentString(latest.debt_to_equity_ratio_YoY) : null;
	const currentRatio = latest ? parseRatioString(latest.current_ratio) : null;

	const sparkline = q
		.slice(0, 8)
		.reverse()
		.map((row) => parseRatioString(row.current_ratio));

	return {
		kpis: [
			{
				label: 'Cash & equiv',
				value: fmtMillionsCompact(cash),
				qoq: { text: fmtPct(cashQoQ), numeric: cashQoQ },
				yoy: { text: fmtPct(cashYoY), numeric: cashYoY }
			},
			{
				label: 'Debt / Equity',
				value: fmtRatioValue(de),
				qoq: { text: fmtPct(deQoQ), numeric: deQoQ == null ? null : -deQoQ },
				yoy: { text: fmtPct(deYoY), numeric: deYoY == null ? null : -deYoY },
				hint: 'Lower is better'
			}
		],
		sparkline,
		health: {
			currentRatio,
			debtToEquity: de
		}
	};
}

export function buildCashFlowCard(cashflowQuarters: any[]): PulseCardData {
	const q = cashflowQuarters ?? [];
	const fcfSeries = q.map((row) => parseMillionsString(row.freeCashFlow));
	const ocfSeries = q.map((row) => parseMillionsString(row.operatingCashflow));
	const fcfTTM = sum4(fcfSeries);
	const ocfTTM = sum4(ocfSeries);
	const latest = q[0] ?? null;
	const fcfQoQ = latest ? parsePercentString(latest.freeCashFlow_QoQ) : null;
	const fcfYoY = latest ? parsePercentString(latest.freeCashFlow_YoY) : null;
	const ocfMargin = latest ? parsePercentString(latest.ocf_margin) : null;
	const ocfMarginQoQ = latest ? parsePercentString(latest.ocf_margin_QoQ) : null;
	const ocfMarginYoY = latest ? parsePercentString(latest.ocf_margin_YoY) : null;

	const sparkline = q
		.slice(0, 8)
		.reverse()
		.map((row) => parseMillionsString(row.freeCashFlow));

	return {
		kpis: [
			{
				label: 'FCF (TTM)',
				value: fmtMillionsCompact(fcfTTM),
				qoq: { text: fmtPct(fcfQoQ), numeric: fcfQoQ },
				yoy: { text: fmtPct(fcfYoY), numeric: fcfYoY }
			},
			{
				label: 'OCF margin',
				value: fmtPctValue(ocfMargin),
				qoq: { text: fmtPp(ocfMarginQoQ), numeric: ocfMarginQoQ },
				yoy: { text: fmtPp(ocfMarginYoY), numeric: ocfMarginYoY }
			}
		],
		sparkline,
		health: {
			fcf: fcfTTM,
			ocf: ocfTTM
		}
	};
}

export function buildValuationCard(
	valuation: ValuationSnapshot | null,
	layout: ValuationLayout | null
): PulseCardData {
	const pe = valuation?.pe_ratio ?? null;
	const pe5y = layout?.five_year_avg?.pe_ratio_5y ?? null;
	const evEbitda = valuation?.ev_to_ebitda ?? null;
	const targetPrice = valuation?.analyst_target_price ?? null;
	const latestPrice = valuation?.latest_closing_price ?? valuation?.adjusted_price ?? null;

	const pePct = pe != null && pe5y != null && pe5y !== 0 ? ((pe - pe5y) / pe5y) * 100 : null;
	const upside =
		targetPrice != null && latestPrice != null && latestPrice !== 0
			? ((targetPrice - latestPrice) / latestPrice) * 100
			: null;

	return {
		kpis: [
			{
				label: 'P/E (TTM)',
				value: fmtRatioValue(pe, 1),
				qoq: {
					text: pe5y != null ? `5Y ${pe5y.toFixed(1)}` : '—',
					numeric: null
				},
				yoy: { text: pePct != null ? fmtPct(pePct) : '—', numeric: pePct },
				hint: 'vs 5Y avg'
			},
			{
				label: 'EV/EBITDA',
				value: fmtRatioValue(evEbitda, 1),
				qoq: {
					text: targetPrice != null ? `Target $${targetPrice.toFixed(2)}` : '—',
					numeric: null
				},
				yoy: { text: upside != null ? fmtPct(upside) : '—', numeric: upside },
				hint: upside != null && upside > 0 ? 'upside' : 'downside'
			}
		],
		sparkline: [],
		health: {
			pe,
			pe5y
		}
	};
}

export function buildVitals(
	income: any[],
	cashflow: any[],
	valuation: ValuationSnapshot | null
): VitalsData {
	const q = income ?? [];
	const latest = q[0] ?? null;
	const revSeries = q.map((row) => parseMillionsString(row.totalRevenue));
	const netIncomeSeries = q.map((row) => parseMillionsString(row.netIncome));
	const cf = cashflow ?? [];
	const fcfSeries = cf.map((row) => parseMillionsString(row.freeCashFlow));

	return {
		revenueTTM: sum4(revSeries),
		revenueQoQ: latest ? parsePercentString(latest.totalRevenue_QoQ) : null,
		revenueYoY: latest ? parsePercentString(latest.totalRevenue_YoY) : null,
		netIncomeTTM: sum4(netIncomeSeries),
		netIncomeQoQ: latest ? parsePercentString(latest.netIncome_QoQ) : null,
		netIncomeYoY: latest ? parsePercentString(latest.netIncome_YoY) : null,
		fcfTTM: sum4(fcfSeries),
		fcfQoQ: cf[0] ? parsePercentString(cf[0].freeCashFlow_QoQ) : null,
		fcfYoY: cf[0] ? parsePercentString(cf[0].freeCashFlow_YoY) : null,
		epsTTM: valuation?.diluted_eps_ttm ?? null,
		epsSurprise: latest ? parsePercentString(latest.surprisePercentage) : null
	};
}
