export interface TechnicalResponse {
	ticker: string;
	interval: string;
	last_updated: string;
	analysis: Analysis;
}

interface Analysis {
	[date: string]: {
		price_data: PriceData;
		indicators: Indicators;
		summary: Summary;
	};
}

interface PriceData {
	open: number;
	high: number;
	low: number;
	close: number;
	volume: number;
}

interface Indicators {
	macd: MACD;
	rsi: RSI;
	aroon: AROON;
	stochastic: Stochastic;
}

interface MACD {
	values: {
		macd: number;
		signal: number;
		histogram: number;
	};
	signals: {
		trend: string;
		momentum: string;
		signal: string;
		strength: string;
		acceleration: string;
	};
}

interface RSI {
	value: number;
	status: string;
	trend: string;
	strenght: string;
}

interface AROON {
	values: {
		aroon_up: number;
		aroon_down: number;
		aroon_oscillator: number;
	};

	signals: {
		trend: string;
		strength: string;
		consolidation: string;
		signal: string;
	};
}

interface Stochastic {
	values: {
		k_line: number;
		d_line: number;
	};
	signals: {
		status: string;
		trend: string;
		strength: string;
		signal: string;
	};
}

interface Summary {
	overall_trend: string;
	signal_strength: string;
	recommended_action: string;
}
