import type { PageServerLoad } from './$types';
import { fetchCashFlow } from '../../../../../../api/cashflowsheet/cashflowdata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchCashFlow(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
