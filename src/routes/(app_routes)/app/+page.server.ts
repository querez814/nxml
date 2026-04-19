import type { PageServerLoad } from './$types';
import { fetchNewsRecapMarket } from '$lib/api/newsRecap';
import siteMetadata from '$lib/config/site-metadata';

// Return the news recap as an *unawaited* promise so SvelteKit streams it to
// the client. The page renders immediately with a loading indicator while the
// upstream news/recap call (which can be slow on a cold cache) finishes.
export const load = (({ fetch }) => {
	const startedAt = Date.now();
	const api = siteMetadata.urls.app.api;
	return {
		streamed: {
			newsRecap: fetchNewsRecapMarket(fetch, api)
		},
		serverTimingsMs: {
			startedAt
		}
	};
}) satisfies PageServerLoad;
