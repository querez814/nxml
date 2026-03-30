import type { PageServerLoad } from './$types';
import { fetchValuation } from '../../../../api/valuation/valuationdata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const valuations = await fetchValuation(ticker);
		const valuation = Array.isArray(valuations) ? (valuations[0] ?? null) : null;
		return { ticker, valuation };
	} catch {
		return { ticker, valuation: null };
	}
}) satisfies PageServerLoad;
