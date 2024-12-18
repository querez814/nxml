export const load = async ({ params, fetch }: { params: any; fetch: any }) => {
	const ticker = params.ticker;
	const response = await fetch(
		`http://127.0.0.1:8000/financials/earnings-statement/quarterly/${ticker}`
	);

	const earnings_data = await response.json();

	return {
		earnings_data
	};
};
