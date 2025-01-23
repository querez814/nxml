import { fetchTechnicals } from '$lib/types/technicals/technicals';
import type { PageLoad } from './$types';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const interval = 'daily';

	// Fetch the technicals data
	const response = await fetchTechnicals(interval, ticker);

	// Validate and cast response
	const parsedResponse = response as unknown as { data: unknown };
	if (
		parsedResponse &&
		typeof parsedResponse === 'object' &&
		parsedResponse.data &&
		typeof parsedResponse.data === 'object' &&
		'status' in parsedResponse.data &&
		'data' in parsedResponse.data
	) {
		const data = parsedResponse.data as TechnicalsResponse;

		// Extract the analysis for the latest date
		const analysisDate = data.data.last_updated;
		const analysis = data.data.analysis[analysisDate];

		// Return the parsed data to be accessible in the Svelte component
		return {
			priceData: analysis.price_data,
			macd: analysis.indicators.macd,
			rsi: analysis.indicators.rsi,
			aroon: analysis.indicators.aroon,
			stochastic: analysis.indicators.stochastic,
			summary: analysis.summary
		};
	} else {
		throw new Error('Invalid response structure from fetchTechnicals');
	}
}) satisfies PageLoad;

interface PriceData {
	open: number;
	high: number;
	low: number;
	close: number;
	volume: number;
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
	};
}

interface RSI {
	value: number;
	status: string;
	trend: string;
	strength: string;
}

interface Aroon {
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

interface Indicators {
	macd: MACD;
	rsi: RSI;
	aroon: Aroon;
	stochastic: Stochastic;
}

interface AnalysisSummary {
	overall_trend: string;
	signal_strength: string;
	recommended_action: string;
}

interface Analysis {
	[date: string]: {
		price_data: PriceData;
		indicators: Indicators;
		summary: AnalysisSummary;
	};
}

interface TechnicalsResponse {
	status: string;
	data: {
		ticker: string;
		interval: string;
		last_updated: string;
		analysis: Analysis;
	};
}
