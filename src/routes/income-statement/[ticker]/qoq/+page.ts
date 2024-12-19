export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	// Fetch the transformed data from the backend
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/income-statement/quarterly/${ticker}/qoq`
	);

	const margin_data = await fetch(
		`http://127.0.0.1:8000/financials/income-statement/quarterly/${ticker}/margins`
	);
	const income_qoq_data = await response.json();
	const margin_data_json = await margin_data.json();
	return {
		income_qoq_data,
		margin_data_json
	};
};
