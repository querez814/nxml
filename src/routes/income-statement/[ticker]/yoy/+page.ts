export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/income-statement/quarterly/${ticker}/yoy`
	);

	const income_yoy_data = await response.json();
	console.log('Income Data Fetched:', income_yoy_data);

	return {
		income_yoy_data
	};
};
