import { describe, it, expect } from 'vitest';
import { balanceSheetHealth, incomeStatementHealth, valuationHealth } from './healthRules';

describe('balanceSheetHealth', () => {
	it('flags debt/equity override', () => {
		const r = balanceSheetHealth(2, 2.5);
		expect(r.level).toBe('concern');
	});
	it('healthy current ratio', () => {
		const r = balanceSheetHealth(1.6, 0.5);
		expect(r.level).toBe('healthy');
	});
});

describe('incomeStatementHealth', () => {
	it('healthy when both positive', () => {
		const r = incomeStatementHealth(5, 10);
		expect(r.level).toBe('healthy');
	});
});

describe('valuationHealth', () => {
	it('cheap when far below 5y', () => {
		const r = valuationHealth(10, 30);
		expect(r.level).toBe('healthy');
	});
});
