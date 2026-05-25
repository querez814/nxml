const quarterLabelByIndex = ['Q1', 'Q2', 'Q3', 'Q4'] as const;

function getFiscalMonth(dateValue: string): { year: number; month: number } | null {
	const isoMatch = dateValue.match(/^(\d{4})-(\d{2})-\d{2}/);
	if (isoMatch) {
		return {
			year: Number(isoMatch[1]),
			month: Number(isoMatch[2])
		};
	}

	const parsed = new Date(dateValue);
	if (Number.isNaN(parsed.getTime())) return null;

	return {
		year: parsed.getUTCFullYear(),
		month: parsed.getUTCMonth() + 1
	};
}

export function formatFiscalQuarterLabel(fiscalDateEnding: unknown): string {
	const originalDate = String(fiscalDateEnding ?? '');
	const parsed = getFiscalMonth(originalDate);
	if (!parsed || parsed.month < 1 || parsed.month > 12) return originalDate;

	const quarterIndex = Math.ceil(parsed.month / 3) - 1;
	return `${quarterLabelByIndex[quarterIndex]} ${parsed.year}`;
}
