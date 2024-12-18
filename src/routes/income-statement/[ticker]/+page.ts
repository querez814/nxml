export const load = async ({ params, fetch }) => {
	const ticker = params.ticker;

	// Fetch the transformed data from the backend
	const response = await fetch(
		`http://127.0.0.1:8000/financials/income-statement/quarterly/${ticker}`
	);

	// Parse the JSON response
	const income_data = await response.json();
	console.log('Income Data Fetched:', income_data); // Debug the response

	// Return the data directly
	return {
		income_data // This will be accessible in the +page.svelte file
	};
};
