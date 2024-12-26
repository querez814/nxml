import { fetchCashFlow } from '../../../../api/cashflowsheet/cashflowdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchCashFlow(ticker);
	return { quarters };
}) satisfies PageLoad;
