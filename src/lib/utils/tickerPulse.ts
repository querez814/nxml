import type { ValuationLayout } from '../../api/valuation/valuationdata';
import {
	balanceSheetHealth,
	cashFlowHealth,
	incomeStatementHealth,
	valuationHealth,
	type HealthResult
} from './healthRules';

export function parseLocaleNumber(value: unknown): number | null {
	if (value === null || value === undefined) return null;
	if (typeof value === 'number') return Number.isFinite(value) ? value : null;
	const s = String(value).trim().replace(/,/g, '');
	if (s === '' || s === '—' || s === '-') return null;
	const n = parseFloat(s);
	return Number.isFinite(n) ? n : null;
}

/** Parse margin strings like "24.1%" or decimal 0.241 */
export function parseMarginPercent(value: unknown): number | null {
	if (value === null || value === undefined) return null;
	if (typeof value === 'number') return value > 1 ? value : value * 100;
	const s = String(value).trim();
	const n = parseFloat(s.replace('%', ''));
	if (!Number.isFinite(n)) return null;
	return s.includes('%') || n > 1 ? n : n * 100;
}

export function sortQuartersDesc<T extends { fiscalDateEnding: string }>(rows: T[]): T[] {
	return [...rows].sort(
		(a, b) => new Date(b.fiscalDateEnding).getTime() - new Date(a.fiscalDateEnding).getTime()
	);
}

export function sumTrailingField(
	rows: Record<string, unknown>[],
	field: string,
	n: number
): number | null {
	const sorted = sortQuartersDesc(rows as { fiscalDateEnding: string }[]);
	if (sorted.length < n) return null;
	let sum = 0;
	for (let i = 0; i < n; i++) {
		const row = sorted[i] as Record<string, unknown>;
		const v = parseLocaleNumber(row[field]);
		if (v === null) return null;
		sum += v;
	}
	return sum;
}

export function ttmYoYGrowthPct(
	rows: Record<string, unknown>[],
	field: string
): number | null {
	const ttm = sumTrailingField(rows, field, 4);
	const sorted = sortQuartersDesc(rows as { fiscalDateEnding: string }[]);
	if (sorted.length < 8 || ttm === null) return null;
	let prior = 0;
	for (let i = 4; i < 8; i++) {
		const row = sorted[i] as Record<string, unknown>;
		const v = parseLocaleNumber(row[field]);
		if (v === null) return null;
		prior += v;
	}
	if (prior === 0) return null;
	return ((ttm - prior) / Math.abs(prior)) * 100;
}

export function latestQuarter(rows: Record<string, unknown>[]): Record<string, unknown> | null {
	const s = sortQuartersDesc(rows as { fiscalDateEnding: string }[]);
	return s[0] ?? null;
}

export function stringField(row: Record<string, unknown> | null, key: string): string {
	if (!row) return '—';
	const v = row[key];
	if (v === null || v === undefined) return '—';
	return String(v);
}

export type KpiDelta = { qoq: string; yoy: string };

export type PulseKpi = {
	label: string;
	value: string;
	qoq: string;
	yoy: string;
	mode: 'growth' | 'margin' | 'ratio' | 'valuation';
};

function fmtGrowthPctFromString(raw: unknown): string {
	if (raw === null || raw === undefined || raw === '') return '—';
	const s = String(raw).trim();
	if (s === 'N/A' || s === '—') return '—';
	return s.includes('%') ? s : `${s}%`;
}

/**
 * Use `_QoQ` / `_YoY` for headline growth. `_QoQ_Derivative` / `_YoY_Derivative` are **changes in those growth
 * rates** (acceleration), not period growth — see `backend/analysis/income_statement.py`.
 */
export function growthQoQ(row: Record<string, unknown> | null | undefined, fieldPrefix: string): string {
	if (!row) return '—';
	return fmtGrowthPctFromString(row[`${fieldPrefix}_QoQ`]);
}

export function growthYoY(row: Record<string, unknown> | null | undefined, fieldPrefix: string): string {
	if (!row) return '—';
	return fmtGrowthPctFromString(row[`${fieldPrefix}_YoY`]);
}

/** Millions → $12.3B / $450M */
export function formatUsdFromMillions(millions: number | null): string {
	if (millions === null || !Number.isFinite(millions)) return '—';
	const abs = Math.abs(millions);
	if (abs >= 1_000_000) return `$${(millions / 1_000_000).toFixed(2)}T`;
	if (abs >= 1_000) return `$${(millions / 1_000).toFixed(1)}B`;
	return `$${millions.toFixed(1)}M`;
}

export function buildIncomePulse(quarters: Record<string, unknown>[]): {
	kpis: PulseKpi[];
	sparkline: { date: string; value: number }[];
	health: HealthResult;
} {
	const sorted = sortQuartersDesc(quarters as { fiscalDateEnding: string }[]);
	const latest = latestQuarter(quarters);
	const rev = parseLocaleNumber(latest?.totalRevenue);
	const revStr = rev !== null ? formatUsdFromMillions(rev) : '—';

	const qoqRev = growthQoQ(latest, 'totalRevenue');
	const yoyRev = growthYoY(latest, 'totalRevenue');

	const nmRaw = latest?.netMargin;
	const netMarginPct = parseMarginPercent(nmRaw);
	const nmStr =
		netMarginPct !== null ? `${netMarginPct.toFixed(1)}%` : nmRaw != null ? String(nmRaw) : '—';
	const qoqNm = stringField(latest, 'netMargin_QoQ');
	const yoyNm = stringField(latest, 'netMargin_YoY');

	const revTtmYoy = ttmYoYGrowthPct(quarters, 'totalRevenue');

	const sparkline = sorted
		.slice(0, 8)
		.reverse()
		.map((q) => {
			const row = q as Record<string, unknown>;
			return {
				date: q.fiscalDateEnding,
				value: parseLocaleNumber(row.totalRevenue) ?? 0
			};
		})
		.filter((p) => p.value !== 0);

	const health = incomeStatementHealth(
		revTtmYoy,
		netMarginPct !== null ? netMarginPct : null
	);

	return {
		kpis: [
			{
				label: 'Revenue (latest Q)',
				value: revStr,
				qoq: qoqRev === '—' ? '—' : `QoQ ${qoqRev}`,
				yoy: yoyRev === '—' ? '—' : `YoY ${yoyRev}`,
				mode: 'growth'
			},
			{
				label: 'Net margin',
				value: nmStr,
				qoq: qoqNm === '—' ? '—' : `QoQ ${qoqNm}`,
				yoy: yoyNm === '—' ? '—' : `YoY ${yoyNm}`,
				mode: 'margin'
			}
		],
		sparkline,
		health
	};
}

export function buildBalancePulse(quarters: Record<string, unknown>[]): {
	kpis: PulseKpi[];
	sparkline: { date: string; value: number }[];
	health: HealthResult;
} {
	const sorted = sortQuartersDesc(quarters as { fiscalDateEnding: string }[]);
	const latest = latestQuarter(quarters);
	const cash = parseLocaleNumber(latest?.cashAndCashEquivalentsAtCarryingValue);
	const cashStr = cash !== null ? formatUsdFromMillions(cash) : '—';

	const qoqCash = growthQoQ(latest, 'cashAndCashEquivalentsAtCarryingValue');
	const yoyCash = growthYoY(latest, 'cashAndCashEquivalentsAtCarryingValue');

	const de = parseLocaleNumber(latest?.debt_to_equity_ratio);
	const deStr = de !== null ? de.toFixed(2) : '—';
	const qoqDe = stringField(latest, 'debt_to_equity_ratio_QoQ');
	const yoyDe = stringField(latest, 'debt_to_equity_ratio_YoY');

	const cr = parseLocaleNumber(latest?.current_ratio);
	const sparkline = sorted
		.slice(0, 8)
		.reverse()
		.map((q) => {
			const row = q as Record<string, unknown>;
			return {
				date: q.fiscalDateEnding,
				value: parseLocaleNumber(row.current_ratio) ?? 0
			};
		});

	const health = balanceSheetHealth(cr, de);

	return {
		kpis: [
			{
				label: 'Cash & equivalents',
				value: cashStr,
				qoq: qoqCash === '—' ? '—' : `QoQ ${qoqCash}`,
				yoy: yoyCash === '—' ? '—' : `YoY ${yoyCash}`,
				mode: 'growth'
			},
			{
				label: 'Debt / equity',
				value: deStr,
				qoq: qoqDe === '—' ? '—' : `QoQ ${qoqDe}`,
				yoy: yoyDe === '—' ? '—' : `YoY ${yoyDe}`,
				mode: 'ratio'
			}
		],
		sparkline,
		health
	};
}

export function buildCashFlowPulse(quarters: Record<string, unknown>[]): {
	kpis: PulseKpi[];
	sparkline: { date: string; value: number }[];
	health: HealthResult;
} {
	const sorted = sortQuartersDesc(quarters as { fiscalDateEnding: string }[]);
	const latest = latestQuarter(quarters);
	const fcfTtm = sumTrailingField(quarters, 'freeCashFlow', 4);
	const fcfStr = fcfTtm !== null ? formatUsdFromMillions(fcfTtm) : '—';

	const fcfYoyTtm = ttmYoYGrowthPct(quarters, 'freeCashFlow');
	const qoqFcf = growthQoQ(latest, 'freeCashFlow');

	const ocfMargin = parseMarginPercent(latest?.ocf_margin);
	const ocfStr = ocfMargin !== null ? `${ocfMargin.toFixed(1)}%` : stringField(latest, 'ocf_margin');
	const qoqOcf = stringField(latest, 'ocf_margin_QoQ');
	const yoyOcf = stringField(latest, 'ocf_margin_YoY');

	const ocfQ = parseLocaleNumber(latest?.operatingCashflow);
	const fcfQ = parseLocaleNumber(latest?.freeCashFlow);

	const sparkline = sorted
		.slice(0, 8)
		.reverse()
		.map((q) => {
			const row = q as Record<string, unknown>;
			return {
				date: q.fiscalDateEnding,
				value: parseLocaleNumber(row.freeCashFlow) ?? 0
			};
		});

	const health = cashFlowHealth(ocfQ, fcfQ);

	return {
		kpis: [
			{
				label: 'FCF (TTM)',
				value: fcfStr,
				qoq: qoqFcf === '—' ? '—' : `QoQ ${qoqFcf}`,
				yoy: fcfYoyTtm !== null ? `YoY ${fcfYoyTtm.toFixed(1)}%` : '—',
				mode: 'growth'
			},
			{
				label: 'OCF margin',
				value: ocfStr,
				qoq: qoqOcf === '—' ? '—' : `QoQ ${qoqOcf}`,
				yoy: yoyOcf === '—' ? '—' : `YoY ${yoyOcf}`,
				mode: 'margin'
			}
		],
		sparkline,
		health
	};
}

export function buildValuationPulse(
	layout: ValuationLayout | null,
	latestPrice: number | null,
	target: number | null
): { kpis: PulseKpi[]; health: HealthResult; upsidePct: number | null } {
	if (!layout) {
		return {
			kpis: [
				{
					label: 'P/E',
					value: '—',
					qoq: 'vs 5Y —',
					yoy: '',
					mode: 'valuation'
				},
				{
					label: 'EV/EBITDA',
					value: '—',
					qoq: 'vs 5Y avg —',
					yoy: '',
					mode: 'valuation'
				}
			],
			health: valuationHealth(null, null),
			upsidePct: null
		};
	}
	const pe = layout.values.pe_ratio ?? null;
	const pe5 = layout.five_year_avg?.pe_ratio_5y ?? null;
	const evE = layout.values.ev_to_ebitda ?? null;
	const ev5 = layout.five_year_avg?.ev_to_ebitda_5y ?? null;

	const peStr = pe !== null && Number.isFinite(pe) ? `${pe.toFixed(1)}x` : '—';
	const premium =
		pe !== null && pe5 !== null && Number.isFinite(pe) && Number.isFinite(pe5) && pe5 !== 0
			? ((pe - pe5) / Math.abs(pe5)) * 100
			: null;

	const evStr = evE !== null && Number.isFinite(evE) ? `${evE.toFixed(1)}x` : '—';
	const evPrem =
		evE !== null && ev5 !== null && Number.isFinite(evE) && Number.isFinite(ev5) && ev5 !== 0
			? ((evE - ev5) / Math.abs(ev5)) * 100
			: null;

	let upsidePct: number | null = null;
	if (latestPrice != null && target != null && latestPrice > 0) {
		upsidePct = ((target - latestPrice) / latestPrice) * 100;
	}

	return {
		kpis: [
			{
				label: 'P/E',
				value: peStr,
				qoq: premium !== null ? `vs 5Y ${premium >= 0 ? '+' : ''}${premium.toFixed(1)}%` : 'vs 5Y —',
				yoy: pe5 !== null ? `5Y avg ${pe5.toFixed(1)}x` : '',
				mode: 'valuation'
			},
			{
				label: 'EV/EBITDA',
				value: evStr,
				qoq: evPrem !== null ? `vs 5Y ${evPrem >= 0 ? '+' : ''}${evPrem.toFixed(1)}%` : 'vs 5Y —',
				yoy: ev5 !== null ? `5Y avg ${ev5.toFixed(1)}x` : '',
				mode: 'valuation'
			}
		],
		health: valuationHealth(pe, pe5),
		upsidePct
	};
}

export type VitalLine = { label: string; value: string; qoq: string; yoy: string };

export function buildVitalsStrip(
	income: Record<string, unknown>[],
	cash: Record<string, unknown>[],
	layout: ValuationLayout | null
): VitalLine[] {
	const revTtm = sumTrailingField(income, 'totalRevenue', 4);
	const niTtm = sumTrailingField(income, 'netIncome', 4);
	const fcfTtm = sumTrailingField(cash, 'freeCashFlow', 4);

	const incLatest = latestQuarter(income);
	const cfLatest = latestQuarter(cash);

	const revYoY = ttmYoYGrowthPct(income, 'totalRevenue');
	const niYoY = ttmYoYGrowthPct(income, 'netIncome');
	const fcfYoYTtm = ttmYoYGrowthPct(cash, 'freeCashFlow');

	const revQoQ = growthQoQ(incLatest, 'totalRevenue');
	const niQoQ = growthQoQ(incLatest, 'netIncome');
	const fcfQoQ = growthQoQ(cfLatest, 'freeCashFlow');

	const eps = layout?.latest?.diluted_eps_ttm ?? null;
	const epsStr = eps !== null && Number.isFinite(eps) ? `$${eps.toFixed(2)}` : '—';
	const epsYoY = layout?.latest?.eps_growth_yoy;
	const epsYoYStr =
		epsYoY !== null && epsYoY !== undefined && Number.isFinite(epsYoY)
			? `${(epsYoY * 100).toFixed(1)}%`
			: '—';
	const surprise = stringField(incLatest, 'surprisePercentage');

	return [
		{
			label: 'Rev TTM',
			value: revTtm !== null ? formatUsdFromMillions(revTtm) : '—',
			qoq: revQoQ === '—' ? '—' : `QoQ ${revQoQ}`,
			yoy: revYoY !== null ? `YoY ${revYoY.toFixed(1)}%` : '—'
		},
		{
			label: 'Net inc TTM',
			value: niTtm !== null ? formatUsdFromMillions(niTtm) : '—',
			qoq: niQoQ === '—' ? '—' : `QoQ ${niQoQ}`,
			yoy: niYoY !== null ? `YoY ${niYoY.toFixed(1)}%` : '—'
		},
		{
			label: 'FCF TTM',
			value: fcfTtm !== null ? formatUsdFromMillions(fcfTtm) : '—',
			qoq: fcfQoQ === '—' ? '—' : `QoQ ${fcfQoQ}`,
			yoy: fcfYoYTtm !== null ? `YoY ${fcfYoYTtm.toFixed(1)}%` : '—'
		},
		{
			label: 'EPS TTM',
			value: epsStr,
			qoq: surprise !== '—' ? `Surprise ${surprise}` : '—',
			yoy: epsYoYStr === '—' ? '—' : `YoY ${epsYoYStr}`
		}
	];
}
