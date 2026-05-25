<script lang="ts">
	import { TableHandler, Datatable, ThSort, ThFilter, RowsPerPage } from '@vincjo/datatables';
	import * as Tabs from '$lib/components/ui/tabs';

	let props = $props();
	let activeTab = $state('raw');

	let rawTable = $derived(
		props.rawData ? new TableHandler(props.rawData, { rowsPerPage: 40 }) : null
	);
	let yoyTable = $derived(
		props.yoyData ? new TableHandler(props.yoyData, { rowsPerPage: 40 }) : null
	);
	let qoqTable = $derived(
		props.qoqData ? new TableHandler(props.qoqData, { rowsPerPage: 40 }) : null
	);
	let marginsTable = $derived(
		props.marginsData ? new TableHandler(props.marginsData, { rowsPerPage: 40 }) : null
	);

	// Transform revenue segments to match Raw Values: rows = segment names, columns = periods (chronological, newest first)
	function buildSegmentsTableData(seg: { segments?: Array<{ name: string; period?: string | null; revenue_amount?: string | null; revenue_percentage_of_total?: string | null; trend_comment?: string | null }> }) {
		if (!seg?.segments?.length) return { data: [], columns: [] };
		const segments = seg.segments;

		// Extract unique periods and sort chronologically (3 mo before 9 mo, etc.)
		const periodOrder = (p: string) => {
			const m = p.match(/(\d+)\s*month|(three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*month/i);
			if (m) {
				const num = m[1] ? parseInt(m[1], 10) : { three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12 }[m[2]?.toLowerCase() ?? ''] ?? 12;
				return num;
			}
			return 12;
		};
		const uniquePeriods = [...new Set(segments.map((s) => s.period || '').filter(Boolean))];
		uniquePeriods.sort((a, b) => periodOrder(a) - periodOrder(b));

		// Unique segment names (order: first occurrence in data)
		const seen = new Set<string>();
		const segmentNames: string[] = [];
		for (const s of segments) {
			if (!seen.has(s.name)) {
				seen.add(s.name);
				segmentNames.push(s.name);
			}
		}

		// Build lookup: (segmentName, period) -> { revenue, pct, trend }
		const lookup = new Map<string, { revenue: string; pct: string; trend: string }>();
		for (const s of segments) {
			const period = s.period || '';
			const key = `${s.name}\0${period}`;
			lookup.set(key, {
				revenue: s.revenue_amount ?? '—',
				pct: s.revenue_percentage_of_total ?? '—',
				trend: s.trend_comment ?? '—',
			});
		}

		// Rows = segments; Columns = periods. Show Revenue as primary (like Raw Values shows metric values per quarter)
		const data = segmentNames.map((name) => {
			const row: Record<string, string> = { metric: name, originalMetric: 'segment' };
			for (const period of uniquePeriods) {
				const key = `${name}\0${period}`;
				const v = lookup.get(key);
				row[period] = v?.revenue ?? '—';
			}
			return row;
		});

		return { data, columns: uniquePeriods };
	}

	let segmentsTableData = $derived(
		props.revenueSegments?.has_segment_disclosure && props.revenueSegments?.segments?.length
			? buildSegmentsTableData(props.revenueSegments)
			: { data: [], columns: [] }
	);
	let segmentsTable = $derived(
		segmentsTableData.data.length
			? new TableHandler(segmentsTableData.data, { rowsPerPage: 40 })
			: null
	);

	function formatValue(value: unknown, isRawValue: boolean, originalMetric: string): string {
		if (value == null || value === '') return '—';
		const s = String(value);
		if (!isRawValue) {
			if (s === 'inf%' || s === '-inf%') return 'N/A';
			return s;
		}
		if (props.ratioMetrics?.includes(originalMetric)) {
			const num = parseFloat(s.replace(/,/g, ''));
			return isNaN(num) ? s : num.toFixed(2);
		}
		return s;
	}

	function getValueClass(value: unknown, isRawValue: boolean): string {
		if (value == null || value === '') return 'text-gray-500';
		const s = String(value);
		if (s === 'N/A' || s === '—') return 'text-gray-500';
		const numValue = parseFloat(s);
		if (isNaN(numValue)) return '';

		if (isRawValue) {
			return numValue < 0 ? 'text-red-400' : 'text-emerald-400';
		}
		return s.startsWith('-') ? 'text-red-400' : 'text-emerald-400';
	}

	function formatPeriodHeader(period: unknown): string {
		const value = String(period);
		if (/^Q[1-4]\s+\d{4}$/.test(value)) return value;

		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return value;

		return date.toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short'
		});
	}
</script>

<div class="container mx-auto px-4 py-6">
	<div class="mb-8 flex items-center justify-between">
		<h2 class="text-3xl font-bold tracking-tight text-slate-50">
			{props.title ?? 'Financial Metrics'}
		</h2>
	</div>

	<div class="rounded-xl bg-slate-900/50 p-6 shadow-2xl ring-1 ring-slate-800">
		<Tabs.Root value={activeTab} class="w-full">
			<Tabs.List class="mb-6 flex space-x-1 rounded-lg bg-slate-800/50 p-1">
				{#if props.rawData}
					<Tabs.Trigger
						value="raw"
						class="rounded-md px-4 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-700/50 hover:text-slate-100 data-[state=active]:bg-slate-700 data-[state=active]:text-slate-100"
						>Raw Values</Tabs.Trigger
					>
				{/if}
				{#if props.yoyData}
					<Tabs.Trigger
						value="yoy"
						class="rounded-md px-4 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-700/50 hover:text-slate-100 data-[state=active]:bg-slate-700 data-[state=active]:text-slate-100"
						>Year over Year</Tabs.Trigger
					>
				{/if}
				{#if props.qoqData}
					<Tabs.Trigger
						value="qoq"
						class="rounded-md px-4 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-700/50 hover:text-slate-100 data-[state=active]:bg-slate-700 data-[state=active]:text-slate-100"
						>Quarter over Quarter</Tabs.Trigger
					>
				{/if}
				{#if props.marginsData}
					<Tabs.Trigger
						value="margins"
						class="rounded-md px-4 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-700/50 hover:text-slate-100 data-[state=active]:bg-slate-700 data-[state=active]:text-slate-100"
						>Margins</Tabs.Trigger
					>
				{/if}
				{#if props.onFetchRevenueSegments != null}
					<Tabs.Trigger
						value="revenueSegments"
						class="rounded-md px-4 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-700/50 hover:text-slate-100 data-[state=active]:bg-slate-700 data-[state=active]:text-slate-100"
						>Revenue Segments</Tabs.Trigger
					>
				{/if}
			</Tabs.List>

			{#if props.rawData && rawTable}
				<Tabs.Content value="raw">
					<div class="overflow-x-auto rounded-lg">
						<Datatable table={rawTable}>
							<table class="w-full border-separate border-spacing-0">
								<thead>
									<tr class="bg-slate-800/70">
										<ThSort table={rawTable} field={'metric'}>Metric</ThSort>
										{#each props.quarters as quarter}
											<ThSort table={rawTable} field={quarter}>
												{formatPeriodHeader(quarter)}
											</ThSort>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<ThFilter table={rawTable} field={'metric'} />
										{#each props.quarters as quarter}
											<ThFilter table={rawTable} field={quarter} />
										{/each}
									</tr>
								</thead>
								<tbody>
									{#each rawTable.rows as row (row.metric)}
										<tr class="group transition-colors hover:bg-slate-800/30">
											<td
												class="sticky left-0 z-10 bg-slate-900/50 px-4 py-3 font-medium text-slate-200 backdrop-blur group-hover:bg-slate-800/30"
											>
												{row.metric}
											</td>
											{#each props.quarters as quarter}
												<td class="px-4 py-3 text-right {getValueClass(row[quarter], true)}">
													{formatValue(row[quarter], true, row.originalMetric)}
												</td>
											{/each}
										</tr>
									{/each}
								</tbody>
							</table>
						</Datatable>
					</div>
				</Tabs.Content>
			{/if}

			{#if props.yoyData && yoyTable}
				<Tabs.Content value="yoy">
					<div class="overflow-x-auto rounded-lg">
						<Datatable table={yoyTable}>
							<table class="w-full border-separate border-spacing-0">
								<thead>
									<tr class="bg-slate-800/70">
										<ThSort table={yoyTable} field={'metric'}>Metric</ThSort>
										{#each props.quarters as quarter}
											<ThSort table={yoyTable} field={quarter}>
												{formatPeriodHeader(quarter)}
											</ThSort>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<ThFilter table={yoyTable} field={'metric'} />
										{#each props.quarters as quarter}
											<ThFilter table={yoyTable} field={quarter} />
										{/each}
									</tr>
								</thead>
								<tbody>
									{#each yoyTable.rows as row (row.metric)}
										<tr class="group transition-colors hover:bg-slate-800/30">
											<td
												class="sticky left-0 z-10 bg-slate-900/50 px-4 py-3 font-medium text-slate-200 backdrop-blur group-hover:bg-slate-800/30"
											>
												{row.metric}
											</td>
											{#each props.quarters as quarter}
												<td class="px-4 py-3 text-right {getValueClass(row[quarter], false)}">
													{formatValue(row[quarter], false, row.originalMetric)}
												</td>
											{/each}
										</tr>
									{/each}
								</tbody>
							</table>
						</Datatable>
					</div>
				</Tabs.Content>
			{/if}

			{#if props.qoqData && qoqTable}
				<Tabs.Content value="qoq">
					<div class="overflow-x-auto rounded-lg">
						<Datatable table={qoqTable}>
							<table class="w-full border-separate border-spacing-0">
								<thead>
									<tr class="bg-slate-800/70">
										<ThSort table={qoqTable} field={'metric'}>Metric</ThSort>
										{#each props.quarters as quarter}
											<ThSort table={qoqTable} field={quarter}>
												{formatPeriodHeader(quarter)}
											</ThSort>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<ThFilter table={qoqTable} field={'metric'} />
										{#each props.quarters as quarter}
											<ThFilter table={qoqTable} field={quarter} />
										{/each}
									</tr>
								</thead>
								<tbody>
									{#each qoqTable.rows as row (row.metric)}
										<tr class="group transition-colors hover:bg-slate-800/30">
											<td
												class="sticky left-0 z-10 bg-slate-900/50 px-4 py-3 font-medium text-slate-200 backdrop-blur group-hover:bg-slate-800/30"
											>
												{row.metric}
											</td>
											{#each props.quarters as quarter}
												<td class="px-4 py-3 text-right {getValueClass(row[quarter], false)}">
													{formatValue(row[quarter], false, row.originalMetric)}
												</td>
											{/each}
										</tr>
									{/each}
								</tbody>
							</table>
						</Datatable>
					</div>
				</Tabs.Content>
			{/if}

			{#if props.onFetchRevenueSegments != null}
				<Tabs.Content value="revenueSegments">
					<div class="rounded-lg">
						{#if props.revenueSegmentsLoading}
							<p class="py-8 text-center text-sm text-slate-400">
								Fetching MD&A from latest 10-Q and extracting revenue segments...
							</p>
						{:else if segmentsTable && segmentsTableData.columns.length > 0}
							{#if props.revenueSegments?.filing_date}
								<p class="mb-4 font-mono text-xs text-slate-500">
									From 10-Q filed {props.revenueSegments.filing_date}
									{#if props.revenueSegments.segment_basis}
										· Basis: {String(props.revenueSegments.segment_basis).replace(/_/g, ' ')}
									{/if}
								</p>
							{/if}
							<div class="overflow-x-auto rounded-lg">
								<Datatable table={segmentsTable}>
									<table class="w-full border-separate border-spacing-0">
										<thead>
											<tr class="bg-slate-800/70">
												<ThSort table={segmentsTable} field={'metric'}>Segment</ThSort>
												{#each segmentsTableData.columns as period}
													<ThSort table={segmentsTable} field={period as any}>
														{period}
													</ThSort>
												{/each}
											</tr>
											<tr class="bg-slate-800/40">
												<ThFilter table={segmentsTable} field={'metric'} />
												{#each segmentsTableData.columns as period}
													<ThFilter table={segmentsTable} field={period as any} />
												{/each}
											</tr>
										</thead>
										<tbody>
											{#each segmentsTable.rows as row (row.metric)}
												<tr class="group transition-colors hover:bg-slate-800/30">
													<td
														class="sticky left-0 z-10 bg-slate-900/50 px-4 py-3 font-medium text-slate-200 backdrop-blur group-hover:bg-slate-800/30"
													>
														{row.metric}
													</td>
													{#each segmentsTableData.columns as period}
														<td class="px-4 py-3 text-right {getValueClass(row[period], true)}">
															{formatValue(row[period], true, 'segment')}
														</td>
													{/each}
												</tr>
											{/each}
										</tbody>
									</table>
								</Datatable>
							</div>
						{:else if props.revenueSegments}
							{@const seg = props.revenueSegments}
							{#if seg.filing_date}
								<p class="mb-4 font-mono text-xs text-slate-500">
									From 10-Q filed {seg.filing_date}
								</p>
							{/if}
							<p class="py-6 text-sm text-slate-400">
								{seg.no_segment_reason ?? 'No revenue segment disclosure found in MD&A.'}
							</p>
						{:else}
							<div class="py-8 text-center">
								<p class="mb-4 text-sm text-slate-400">
									Revenue segments are extracted from the MD&A section of the latest 10-Q.
								</p>
								<button
									class="rounded border border-amber-400/30 px-4 py-2 font-mono text-sm text-amber-400 hover:bg-amber-400/10 hover:text-amber-300 disabled:opacity-50"
									onclick={props.onFetchRevenueSegments}
								>
									Fetch Revenue Segments
								</button>
							</div>
						{/if}
					</div>
				</Tabs.Content>
			{/if}

			{#if props.marginsData && marginsTable}
				<Tabs.Content value="margins">
					<div class="overflow-x-auto rounded-lg">
						<Datatable table={marginsTable}>
							<table class="w-full border-separate border-spacing-0">
								<thead>
									<tr class="bg-slate-800/70">
										<ThSort table={marginsTable} field={'metric'}>Metric</ThSort>
										{#each props.quarters as quarter}
											<ThSort table={marginsTable} field={quarter}>
												{formatPeriodHeader(quarter)}
											</ThSort>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<ThFilter table={marginsTable} field={'metric'} />
										{#each props.quarters as quarter}
											<ThFilter table={marginsTable} field={quarter} />
										{/each}
									</tr>
								</thead>
								<tbody>
									{#each marginsTable.rows as row (row.metric)}
										<tr class="group transition-colors hover:bg-slate-800/30">
											<td
												class="sticky left-0 z-10 bg-slate-900/50 px-4 py-3 font-medium text-slate-200 backdrop-blur group-hover:bg-slate-800/30"
											>
												{row.metric}
											</td>
											{#each props.quarters as quarter}
												<td class="px-4 py-3 text-right {getValueClass(row[quarter], false)}">
													{formatValue(row[quarter], false, row.originalMetric)}
												</td>
											{/each}
										</tr>
									{/each}
								</tbody>
							</table>
						</Datatable>
					</div>
				</Tabs.Content>
			{/if}
		</Tabs.Root>
	</div>
</div>
