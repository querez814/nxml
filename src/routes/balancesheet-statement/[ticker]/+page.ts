export const load = async ({ params, fetch }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/balancesheet-statement/quarterly/${ticker}`
	);

	const balancesheet_data = await response.json();
	console.log('Balance Sheet Data Fetched:', balancesheet_data);

	return { balancesheet_data };
};
