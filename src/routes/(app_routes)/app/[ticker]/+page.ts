import type { PageLoad } from './$types';
import { getTickerNews } from '../../../../api/media/tickernews';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const response = await getTickerNews(ticker);
		return {
			ticker,
			valuation: response?.valuation || null,
			news: response?.news || [],
			analystCoverage: response?.analystcoverage || []
		};
	} catch (error) {
		return {
			ticker,
			valuation: null,
			news: [],
			analystCoverage: []
		};
	}
}) satisfies PageLoad;
