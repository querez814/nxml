import type { PageServerLoad } from './$types';
import { fetchCashFlowAnnual } from '../../../../../../api/cashflowsheet/cashflowdata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchCashFlowAnnual(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
