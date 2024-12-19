export const load = async ({ params, fetch }) => {
	const ticker = params.ticker;

	const response = await fetch(
		`http://127.0.0.1:8000/financials/income-statement/quarterly/${ticker}`
	);

	const income_data = await response.json();
	console.log('Income Data Fetched:', income_data);

	return {
		income_data
	};
};
