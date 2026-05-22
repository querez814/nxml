import siteMetadata from '$lib/config/site-metadata';

/** Server load helper: stream Alpha Vantage market news JSON from the FastAPI backend. */
export function loadMarketSentimentStream(fetch: typeof globalThis.fetch) {
	const api = siteMetadata.urls.app.api;
	if (!api) {
		return {
			streamed: {
				marketSentiment: Promise.resolve(null as Record<string, unknown> | null)
			}
		};
	}
	const base = api.replace(/\/$/, '');
	return {
		streamed: {
			marketSentiment: fetch(`${base}/news/sentiment/market`)
				.then((r) => (r.ok ? (r.json() as Promise<Record<string, unknown>>) : null))
				.catch(() => null)
		}
	};
}
