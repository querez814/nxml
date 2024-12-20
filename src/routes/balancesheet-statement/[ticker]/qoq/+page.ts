export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/balancesheet-statement/quarterly/${ticker}/qoq`
	);

	const balancesheet_qoq_data = await response.json();
	console.log('Income Data Fetched:', balancesheet_qoq_data);

	return {
		balancesheet_qoq_data
	};
};
