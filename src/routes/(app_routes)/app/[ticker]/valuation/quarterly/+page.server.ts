import type { PageServerLoad } from './$types';
import { fetchValuation } from '../../../../../../api/valuation/valuationdata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchValuation(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
