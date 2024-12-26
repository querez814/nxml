import { fetchCashFlowRatios } from '../../../../api/cashflowsheet/cashflowdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchCashFlowRatios(ticker);
	return { quarters };
}) satisfies PageLoad;
