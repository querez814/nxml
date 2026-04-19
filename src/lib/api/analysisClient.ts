const API_URL = import.meta.env.VITE_API_URL;

export type StatementAnalysisType =
	| 'income-statement'
	| 'balancesheet-statement'
	| 'cashflow-statement';

export type StatementAnalysisResult = {
	analysis: string;
};

export type RevenueSegmentsResult = {
	has_segment_disclosure: boolean;
	segments: Array<Record<string, unknown>>;
	no_segment_reason?: string | null;
	[key: string]: unknown;
};

export type FinancingRiskResult = {
	financing_risk_json: Record<string, unknown> | null;
	financing_risk_raw: string | null;
	financing_risk_narrative: string | null;
	financing_risk_summary: string | null;
	filing_date: string | null;
};

type Cached<T> = { promise: Promise<T>; at: number };
const cache = new Map<string, Cached<unknown>>();
const TTL_MS = 5 * 60 * 1000;

function cacheKey(kind: string, ticker: string): string {
	return `${kind}:${ticker.toUpperCase()}`;
}

async function postJson<T>(path: string): Promise<T> {
	const res = await fetch(`${API_URL}${path}`, { method: 'POST' });
	const json = await res.json().catch(() => ({}));
	if (!res.ok) {
		const detail = (json as { detail?: string })?.detail ?? `Request failed: ${res.status}`;
		throw new Error(detail);
	}
	return json as T;
}

function memoize<T>(key: string, factory: () => Promise<T>): Promise<T> {
	const hit = cache.get(key);
	if (hit && Date.now() - hit.at < TTL_MS) {
		return hit.promise as Promise<T>;
	}
	const promise = factory().catch((err) => {
		cache.delete(key);
		throw err;
	});
	cache.set(key, { promise, at: Date.now() });
	return promise;
}

export function fetchStatementAnalysis(
	type: StatementAnalysisType,
	ticker: string
): Promise<StatementAnalysisResult> {
	const key = cacheKey(type, ticker);
	return memoize(key, () =>
		postJson<StatementAnalysisResult>(`/analysis/${type}/${ticker.toUpperCase()}`)
	);
}

export function fetchRevenueSegments(ticker: string): Promise<RevenueSegmentsResult> {
	const key = cacheKey('revenue-segments', ticker);
	return memoize(key, () =>
		postJson<RevenueSegmentsResult>(`/analysis/revenue-segments/${ticker.toUpperCase()}`)
	);
}

export function fetchFinancingRisk(ticker: string): Promise<FinancingRiskResult> {
	const key = cacheKey('financing-risk', ticker);
	return memoize(key, () =>
		postJson<FinancingRiskResult>(`/analysis/financing-risk/${ticker.toUpperCase()}`)
	);
}

export function clearAnalysisCache(ticker?: string): void {
	if (!ticker) {
		cache.clear();
		return;
	}
	const prefix = ticker.toUpperCase();
	for (const key of cache.keys()) {
		if (key.endsWith(`:${prefix}`)) cache.delete(key);
	}
}
