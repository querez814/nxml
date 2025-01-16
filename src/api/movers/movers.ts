const api_url = import.meta.env.VITE_API_URL;

export const fetchGLT = async (): Promise<any[]> => {
	const response = await fetch(`${api_url}/current/cgl`);
	if (!response.ok) {
		throw new Error(`Failed to fetch gainers data: ${response.statusText}`);
	}
	const rawData = await response.json();
	return rawData;
};

export const fetchGainers = async (): Promise<any[]> => {
	const response = await fetch(`${api_url}/gainers`);
	if (!response.ok) {
		throw new Error(`Failed to fetch gainers data: ${response.statusText}`);
	}
	const rawData = await response.json();
	return rawData;
};

export const fetchLosers = async (): Promise<any[]> => {
	const response = await fetch(`${api_url}/losers`);
	if (!response.ok) {
		throw new Error(`Failed to fetch losers data: ${response.statusText}`);
	}

	const rawData = await response.json();
	return rawData;
};

export const fetchMostTraded = async (): Promise<any[]> => {
	const response = await fetch(`${api_url}/mosttraded`);
	if (!response.ok) {
		throw new Error(`Failed to fetch most traded data: ${response.statusText}`);
	}

	const rawData = await response.json();

	return rawData;
};

//TODO Ticker is String, price is .toFixed(2) and change is .toFixed(2), volume is .toLocaleString()
