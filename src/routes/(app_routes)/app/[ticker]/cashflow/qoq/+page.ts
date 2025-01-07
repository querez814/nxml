import type { PageLoad } from './$types';
import { fetchCashFlowQoq } from '../../../../../../api/cashflowsheet/cashflowdata';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchCashFlowQoq(ticker);
	return { quarters };
}) satisfies PageLoad;
