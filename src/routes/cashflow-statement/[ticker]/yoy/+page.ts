export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/cashflow-statement/quarterly/${ticker}/yoy`
	);

	const cashflow_yoy_data = await response.json();
	console.log('Income Data Fetched:', cashflow_yoy_data); // Debug the response

	return {
		cashflow_yoy_data
	};
};
