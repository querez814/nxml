import type { PageLoad } from './$types';
import { fetchIncomeStatementQoQ } from '../../../../../../api/incomesheet/incomedata';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchIncomeStatementQoQ(ticker);
	return { quarters };
}) satisfies PageLoad;
