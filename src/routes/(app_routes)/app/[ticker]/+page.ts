import type { ValuationMetrics } from '$lib/types/news/news';
import type { PageLoad } from './$types';
import { getTickerNews } from '../../../../api/media/tickernews';
import type Page from '../+page.svelte';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const response = await getTickerNews(ticker);
	return {
		news: response
	};
}) satisfies PageLoad;
