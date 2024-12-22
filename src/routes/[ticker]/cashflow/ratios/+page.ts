import { fetchCashFlowRatios } from '../../../../api/cashflowsheet/cashflowdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchCashFlowRatios(ticker); // Fetch the first item
	return { quarters };
}) satisfies PageLoad;
