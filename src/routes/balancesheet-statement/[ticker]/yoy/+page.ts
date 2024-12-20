export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/balancesheet-statement/quarterly/${ticker}/yoy`
	);

	const bs_yoy_data = await response.json();
	console.log('Income Data Fetched:', bs_yoy_data);

	return {
		bs_yoy_data
	};
};
