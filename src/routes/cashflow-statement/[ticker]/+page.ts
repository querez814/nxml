export const load = async ({ params, fetch }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/cashflow-statement/quarterly/${ticker}`
	);

	const cashflow_data = await response.json();
	console.log('Cashflow Data Fetched:', cashflow_data);

	return { cashflow_data };
};
