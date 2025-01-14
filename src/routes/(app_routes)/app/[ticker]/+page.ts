import type { PageLoad } from './$types';
import { fetchNewsData } from '../../../../api/media/newscuration';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const newsData = await fetchNewsData(ticker);

	return {
		newsData
	};
}) satisfies PageLoad;
