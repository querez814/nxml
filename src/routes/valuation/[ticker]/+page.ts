export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/valuation/quarterly/${ticker}/ttm`
	);

	const valuation_data = await response.json();
	console.log('Valuation Data Fetched:', valuation_data);

	return {
		valuation_data
	};
};
