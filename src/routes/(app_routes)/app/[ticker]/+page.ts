import type { PageLoad } from './$types';
import { getTickerNews } from '../../../../api/media/tickernews';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const response = await getTickerNews(ticker);
	const valuation = response.valuation;
	const news = response.news;
	const analystCoverage = response.analystcoverage;
	return {
		ticker,
		valuation,
		news,
		analystCoverage
	};
}) satisfies PageLoad;
