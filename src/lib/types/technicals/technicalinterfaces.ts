export type Trend = 'bullish' | 'bearish' | 'neutral';
export type Strength = 'weak' | 'moderate' | 'strong';
export type Signal = 'buy' | 'sell' | 'hold';
export type Status = 'oversold' | 'neutral' | 'overbought';

export interface MasterResponse {
	status: string;
	data: DataObject;
}

export interface DataObject {
	ticker: string;
	interval: string;
	last_updated: string;
	analysis: Record<string, DailyAnalysis>;
}

export interface DailyAnalysis {
	price_data: PriceData;
	indicators: TechnicalIndicators;
	summary: Summary;
}

export interface TechnicalIndicators {
	macd: MACD;
	rsi: RSI;
	aroon: AROON;
	stochastic: Stochastic;
}

export interface PriceData {
	open: number;
	high: number;
	low: number;
	close: number;
	volume: number;
}

export interface RSI {
	value: number;
	status: Status;
	trend: Trend;
	strength: Strength;
}

export interface MACD {
	values: MACDValues;
	signals: MACDSignals;
}

export interface MACDValues {
	macd: number;
	signal: number;
	histogram: number;
}

export interface MACDSignals {
	trend: Trend;
	momentum: string;
	signal: Signal;
	strength: Strength;
	crossover?: string;
	acceleration?: string;
}

export interface AROON {
	values: AROONValues;
	signals: AROONSignals;
}

export interface AROONValues {
	aroon_up: number;
	aroon_down: number;
	aroon_oscillator: number;
}

export interface AROONSignals {
	trend: Trend;
	strength: Strength;
	consolidation: string;
	signal: Signal;
	momentum?: string;
}

export interface Stochastic {
	values: StochasticValues;
	signals: StochasticSignals;
}

export interface StochasticValues {
	k_line: number;
	d_line: number;
}

export interface StochasticSignals {
	status: Status;
	trend: Trend;
	strength: Strength;
	signal: Signal;
	momentum?: string;
	crossover?: string;
}

export interface Summary {
	overall_trend: Trend;
	signal_strength: Strength;
	recommended_action: Signal;
}
