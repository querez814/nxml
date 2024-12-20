export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/income-statement/quarterly/${ticker}/margins`
	);
	const margin_data = await response.json();
	return {
		margin_data
	};
};
