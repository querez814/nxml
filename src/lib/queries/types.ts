export type CardType = 'metrics' | 'valuation' | 'balance' | 'income';

export interface CardData {
	metrics?: {
		pe_ratio: number;
		market_cap: number;
	};
	valuation?: {};
}

export interface Position {
	x: number;
	y: number;
}

export interface DashboardCard {
	id: string;
	ticker: string;
	type: CardType;
	position: Position;
	isMinimized: boolean;
}
