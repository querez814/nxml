import { fetchIncomeStatement } from '../../../../api/incomesheet/incomedata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchIncomeStatement(ticker);
	return { quarters };
}) satisfies PageLoad;
