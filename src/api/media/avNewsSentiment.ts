const api_url = import.meta.env.VITE_API_URL ?? '';

export type AvNewsSentimentQuery = {
	topics?: string;
	tickers?: string;
	time_from?: string;
	time_to?: string;
	sort?: string;
	limit?: number;
	sort_by?: string;
	min_relevance?: number;
	min_ticker_relevance?: number;
	excluded_sources?: string;
};

function appendParams(q: URLSearchParams, params?: AvNewsSentimentQuery) {
	if (!params) return;
	for (const [k, v] of Object.entries(params)) {
		if (v === undefined || v === null || v === '') continue;
		q.set(k, String(v));
	}
}

/** GET /news/sentiment/market — broad market news (Alpha Vantage NEWS_SENTIMENT). */
export async function fetchMarketNewsSentiment(params?: AvNewsSentimentQuery) {
	const q = new URLSearchParams();
	appendParams(q, params);
	const qs = q.toString();
	const url = `${api_url}/news/sentiment/market${qs ? `?${qs}` : ''}`;
	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`Failed to fetch market news sentiment: ${response.statusText}`);
	}
	return response.json() as Promise<Record<string, unknown>>;
}

/** GET /news/sentiment/{ticker} — ticker-scoped curated news. */
export async function fetchTickerNewsSentiment(ticker: string, params?: AvNewsSentimentQuery) {
	const q = new URLSearchParams();
	appendParams(q, params);
	const qs = q.toString();
	const url = `${api_url}/news/sentiment/${encodeURIComponent(ticker)}${qs ? `?${qs}` : ''}`;
	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`Failed to fetch ticker news sentiment: ${response.statusText}`);
	}
	return response.json() as Promise<Record<string, unknown>>;
}
