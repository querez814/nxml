export interface TickerData {
	ticker: string;
	price: string;
	change_amount: string;
	change_percentage: string;
	volume: string;
}

export interface MarketDataResponse {
	metadata: string;
	last_updated: string;
	top_gainers: TickerData[];
	top_losers: TickerData[];
	most_actively_traded: TickerData[];
}

async function fetchMarketData(): Promise<MarketDataResponse> {
	try {
		const response = await fetch('your_api_endpoint');
		const data: MarketDataResponse = await response.json();
		return data;
	} catch (error) {
		console.error('Error fetching market data:', error);
		throw error;
	}
}

interface ParsedTickerData {
	ticker: string;
	price: number;
	change_amount: number;
	change_percentage: number;
	volume: number;
}

function parseTickerData(data: TickerData): ParsedTickerData {
	return {
		ticker: data.ticker,
		price: parseFloat(data.price),
		change_amount: parseFloat(data.change_amount),
		change_percentage: parseFloat(data.change_percentage.replace('%', '')),
		volume: parseInt(data.volume, 10)
	};
}

function parseMarketData(response: MarketDataResponse) {
	return {
		metadata: response.metadata,
		last_updated: response.last_updated,
		top_gainers: response.top_gainers.map(parseTickerData),
		top_losers: response.top_losers.map(parseTickerData),
		most_actively_traded: response.most_actively_traded.map(parseTickerData)
	};
}
