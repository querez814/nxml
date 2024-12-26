import { fetchIncomeStatement } from '../../../api/incomesheet/incomedata';
import type { PageLoad } from './$types';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const data = await fetchIncomeStatement(ticker);
	return { data };
}) satisfies PageLoad;
