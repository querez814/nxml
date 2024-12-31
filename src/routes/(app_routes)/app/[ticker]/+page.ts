import { fetchValuation } from '../../../../api/valuation/valuationdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const data = await fetchValuation(ticker);
	return { data };
}) satisfies PageLoad;
