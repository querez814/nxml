/**
 * Statement YoY/QoQ keys like `ocf_margin_YoY` start with margin metric names, so naive
 * `key.startsWith(metric)` filters wrongly drop them. Keep those; still exclude raw margin
 * series from the main variance grid via structure (only *_YoY / *_QoQ here).
 */
export function keepVarianceKey(
	key: string,
	marginMetrics: readonly string[],
	suffix: '_YoY' | '_QoQ'
): boolean {
	if (!key.endsWith(suffix)) return false;
	const base = key.slice(0, -suffix.length);
	if (marginMetrics.includes(base)) return true;
	return !marginMetrics.some((m) => key.startsWith(m));
}
