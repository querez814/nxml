import type { PageLoad } from './$types';
import { fetchTickerNews } from '../../../../api/media/tickernews';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const response = await fetchTickerNews(ticker);
	return {
		news: response
	};
}) satisfies PageLoad;
