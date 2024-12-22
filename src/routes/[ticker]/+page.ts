import { fetchValuation } from '../../api/valuation/valuationdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const data = await fetchValuation(ticker); // Fetch the first item
	return { data };
}) satisfies PageLoad;
