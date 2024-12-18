export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/balancesheet-statement/quarterly/${ticker}/yoy`
	);

	// Parse the JSON response
	const bs_yoy_data = await response.json();
	console.log('Income Data Fetched:', bs_yoy_data); // Debug the response

	// Return the data properly
	return {
		bs_yoy_data
	};
};
