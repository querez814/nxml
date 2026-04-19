export type NewsRecapArticle = {
	id: string;
	title: string;
	url: string;
	publisher: string;
	published_at: string;
	related_tickers: string[];
	source_symbol: string;
	snippet: string;
	thumbnail_url?: string;
};

export type NewsRecapAI = {
	generated_at: string;
	week_start: string;
	model: string;
	recap_md: string;
	themes: string[];
	watch_items: string[];
	per_article: Record<string, unknown>[];
	disagreements_or_noise: string | null;
	error: string | null;
};

export type NewsRecapPayload = {
	scope: 'market' | 'ticker';
	ticker: string | null;
	articles: NewsRecapArticle[];
	ai: NewsRecapAI;
	cache: { hit?: boolean; layer?: string; articles_layer_hit?: boolean };
};

function apiBase(): string {
	return (
		(typeof process !== 'undefined' && process.env?.API_URL) ||
		(typeof process !== 'undefined' && process.env?.VITE_API_URL) ||
		''
	);
}

/** Server load: pass fetch + base URL from caller (SvelteKit load). */
export async function fetchNewsRecapMarket(
	fetchFn: typeof fetch,
	baseUrl: string
): Promise<NewsRecapPayload | null> {
	const root = baseUrl || apiBase();
	if (!root) return null;
	try {
		const r = await fetchFn(`${root.replace(/\/$/, '')}/news/recap/market`);
		if (!r.ok) return null;
		return (await r.json()) as NewsRecapPayload;
	} catch {
		return null;
	}
}

export async function fetchNewsRecapTicker(
	fetchFn: typeof fetch,
	baseUrl: string,
	ticker: string
): Promise<NewsRecapPayload | null> {
	const root = baseUrl || apiBase();
	if (!root) return null;
	const sym = encodeURIComponent(ticker.trim().toUpperCase());
	try {
		const r = await fetchFn(`${root.replace(/\/$/, '')}/news/recap/${sym}`);
		if (!r.ok) return null;
		return (await r.json()) as NewsRecapPayload;
	} catch {
		return null;
	}
}
