export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/cashflow-statement/quarterly/${ticker}/qoq`
	);

	const cashflow_qoq_data = await response.json();
	console.log('Income Data Fetched:', cashflow_qoq_data);

	return {
		cashflow_qoq_data
	};
};
