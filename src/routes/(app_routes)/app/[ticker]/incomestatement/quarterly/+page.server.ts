import type { PageServerLoad } from './$types';
import { fetchIncomeStatement } from '../../../../../../api/incomesheet/incomedata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchIncomeStatement(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
