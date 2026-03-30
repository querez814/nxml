import type { PageServerLoad } from './$types';
import { fetchIncomeStatementAnnual } from '../../../../../../api/incomesheet/incomedata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchIncomeStatementAnnual(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
