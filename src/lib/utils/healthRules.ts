export type HealthLevel = 'healthy' | 'watch' | 'concern';

export type HealthResult = { level: HealthLevel; tooltip: string };

/** Balance sheet: current ratio + debt/equity override */
export function balanceSheetHealth(
	currentRatio: number | null,
	debtToEquity: number | null
): HealthResult {
	if (debtToEquity != null && debtToEquity > 2) {
		return {
			level: 'concern',
			tooltip: `Debt/equity ${debtToEquity.toFixed(2)} is above 2.0 — leverage may be elevated.`
		};
	}
	if (currentRatio == null || !Number.isFinite(currentRatio)) {
		return { level: 'watch', tooltip: 'Current ratio unavailable for this period.' };
	}
	if (currentRatio >= 1.5) {
		return {
			level: 'healthy',
			tooltip: `Current ratio ${currentRatio.toFixed(2)} is at or above 1.5 — liquidity looks adequate.`
		};
	}
	if (currentRatio >= 1.0) {
		return {
			level: 'watch',
			tooltip: `Current ratio ${currentRatio.toFixed(2)} is between 1.0 and 1.5 — monitor working capital.`
		};
	}
	return {
		level: 'concern',
		tooltip: `Current ratio ${currentRatio.toFixed(2)} is below 1.0 — short-term liquidity pressure.`
	};
}

/** Income: revenue YoY + net margin sign */
export function incomeStatementHealth(revGrowthYoyPct: number | null, netMarginPct: number | null): HealthResult {
	const revOk = revGrowthYoyPct != null && revGrowthYoyPct > 0;
	const marginOk = netMarginPct != null && netMarginPct > 0;
	if (revOk && marginOk) {
		return {
			level: 'healthy',
			tooltip: 'Revenue grew YoY and net margin is positive — earnings quality looks supportive.'
		};
	}
	if (!revOk && !marginOk) {
		return {
			level: 'concern',
			tooltip: 'Revenue declined YoY and net margin is not positive — check drivers and cost structure.'
		};
	}
	return {
		level: 'watch',
		tooltip: 'Mixed signals: either revenue growth or net margin is weak versus the other.'
	};
}

/** Cash flow: OCF and FCF signs (latest quarter, $M) */
export function cashFlowHealth(ocfMillions: number | null, fcfMillions: number | null): HealthResult {
	if (ocfMillions == null || fcfMillions == null || !Number.isFinite(ocfMillions) || !Number.isFinite(fcfMillions)) {
		return { level: 'watch', tooltip: 'Operating or free cash flow data missing for this period.' };
	}
	if (ocfMillions > 0 && fcfMillions > 0) {
		return {
			level: 'healthy',
			tooltip: 'Both operating cash flow and free cash flow are positive this quarter.'
		};
	}
	if (ocfMillions > 0 && fcfMillions <= 0) {
		return {
			level: 'watch',
			tooltip: 'OCF is positive but FCF is not — capex or other investing uses may be heavy.'
		};
	}
	return {
		level: 'concern',
		tooltip: 'Operating cash flow is not positive — review cash generation and one-time items.'
	};
}

/** Valuation: P/E vs 5-year average (±20% green, 20–50% yellow, >50% rich red; cheap if >50% below) */
export function valuationHealth(pe: number | null, pe5y: number | null): HealthResult {
	if (pe == null || pe5y == null || !Number.isFinite(pe) || !Number.isFinite(pe5y) || pe5y === 0) {
		return { level: 'watch', tooltip: 'P/E or 5-year average P/E unavailable — valuation chip is informational only.' };
	}
	const premium = (pe - pe5y) / Math.abs(pe5y);
	if (premium <= -0.5) {
		return {
			level: 'healthy',
			tooltip: `P/E is roughly ${(premium * 100).toFixed(0)}% below the 5-year average — relatively cheap vs history.`
		};
	}
	if (premium <= 0.2) {
		return {
			level: 'healthy',
			tooltip: `P/E is within ~20% of the 5-year average (${pe.toFixed(1)}x vs ${pe5y.toFixed(1)}x).`
		};
	}
	if (premium <= 0.5) {
		return {
			level: 'watch',
			tooltip: `P/E is ${(premium * 100).toFixed(0)}% above the 5-year average — moderately rich vs history.`
		};
	}
	return {
		level: 'concern',
		tooltip: `P/E is more than 50% above the 5-year average — valuation is stretched vs history.`
	};
}
