export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	// Fetch the transformed data from the backend
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/cashflow-statement/quarterly/${ticker}/qoq`
	);

	// Parse the JSON response
	const cashflow_qoq_data = await response.json();
	console.log('Income Data Fetched:', cashflow_qoq_data); // Debug the response

	// Return the data properly
	return {
		cashflow_qoq_data
	};
};
