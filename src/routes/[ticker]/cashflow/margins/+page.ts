import { fetchCashFlowMargins } from '../../../../api/cashflowsheet/cashflowdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchCashFlowMargins(ticker); // Fetch the first item
	return { quarters };
}) satisfies PageLoad;
