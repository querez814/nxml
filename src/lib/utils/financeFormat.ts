export function parseMillionsString(value: unknown): number | null {
	if (value == null) return null;
	const s = String(value).trim();
	if (s === '' || s === '-' || s === 'NaN' || s === 'None') return null;
	const n = Number(s.replace(/,/g, ''));
	return Number.isFinite(n) ? n : null;
}

export function parsePercentString(value: unknown): number | null {
	if (value == null) return null;
	const s = String(value).trim();
	if (s === '' || s === '-' || s === 'inf%' || s === '-inf%' || s === 'NaN' || s === 'None')
		return null;
	const n = Number(s.replace('%', '').replace(/,/g, ''));
	return Number.isFinite(n) ? n : null;
}

export function parseRatioString(value: unknown): number | null {
	if (value == null) return null;
	const s = String(value).trim();
	if (s === '' || s === '-' || s === 'NaN' || s === 'None') return null;
	const n = Number(s.replace(/,/g, ''));
	return Number.isFinite(n) ? n : null;
}

const MAGNITUDE = [
	{ v: 1e12, s: 'T' },
	{ v: 1e9, s: 'B' },
	{ v: 1e6, s: 'M' },
	{ v: 1e3, s: 'K' }
];

export function formatCurrencyCompact(value: number | null, prefix = '$'): string {
	if (value == null || !Number.isFinite(value)) return '—';
	const abs = Math.abs(value);
	for (const m of MAGNITUDE) {
		if (abs >= m.v) {
			return `${prefix}${(value / m.v).toFixed(abs >= m.v * 100 ? 1 : 2)}${m.s}`;
		}
	}
	return `${prefix}${value.toFixed(2)}`;
}

export function formatMillionsCompact(valueMillions: number | null, prefix = '$'): string {
	if (valueMillions == null || !Number.isFinite(valueMillions)) return '—';
	return formatCurrencyCompact(valueMillions * 1e6, prefix);
}

export function formatPercentDelta(value: number | null, digits = 1): string {
	if (value == null || !Number.isFinite(value)) return '—';
	const sign = value > 0 ? '+' : '';
	return `${sign}${value.toFixed(digits)}%`;
}

export function formatPPDelta(value: number | null, digits = 1): string {
	if (value == null || !Number.isFinite(value)) return '—';
	const sign = value > 0 ? '+' : '';
	return `${sign}${value.toFixed(digits)}pp`;
}

export function formatRatioDelta(value: number | null, digits = 2): string {
	if (value == null || !Number.isFinite(value)) return '—';
	const sign = value > 0 ? '+' : '';
	return `${sign}${value.toFixed(digits)}`;
}

export function formatPlainNumber(value: number | null, digits = 2): string {
	if (value == null || !Number.isFinite(value)) return '—';
	return value.toFixed(digits);
}

export function deltaClass(value: number | null): string {
	if (value == null || !Number.isFinite(value)) return 'text-gray-500';
	if (value > 0) return 'text-emerald-400';
	if (value < 0) return 'text-rose-400';
	return 'text-gray-400';
}
