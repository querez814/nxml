<script lang="ts">
	import { TableHandler, Datatable, ThSort, ThFilter } from '@vincjo/datatables';
	import * as Tabs from '$lib/components/ui/tabs';

	interface RowData {
		metric: string;
		originalMetric: string;
		[key: string]: string;
	}

	interface Props {
		rawData?: RowData[];
		yoyData?: RowData[];
		qoqData?: RowData[];
		quarters: string[];
		title?: string;
		ratioMetrics?: string[];
	}

	let props = $props();
	let activeTab = $state('raw');

	let rawTable = $derived(
		props.rawData ? new TableHandler(props.rawData, { rowsPerPage: 20 }) : null
	);
	let yoyTable = $derived(
		props.yoyData ? new TableHandler(props.yoyData, { rowsPerPage: 20 }) : null
	);
	let qoqTable = $derived(
		props.qoqData ? new TableHandler(props.qoqData, { rowsPerPage: 20 }) : null
	);

	function formatCurrency(value: string): string {
		// Handle empty or null values
		if (value === null || value === undefined || value === '') {
			return '—';
		}

		const num = parseFloat(value);

		// Handle non-numeric values
		if (isNaN(num)) {
			console.warn(`Invalid numeric value encountered: ${value}`);
			return '—';
		}

		// Handle actual zero separately from invalid data
		if (num === 0) {
			return '$0';
		}

		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(num);
	}

	function formatValue(value: string, isRawValue: boolean, originalMetric: string): string {
		if (!isRawValue) {
			if (value === 'inf%' || value === '-inf%') return 'N/A';
			return value;
		}

		if (props.ratioMetrics?.includes(originalMetric)) {
			const num = parseFloat(value);
			return num.toFixed(2);
		}
		return value; // Just return the pre-formatted string
	}

	function getValueClass(value: string, isRawValue: boolean): string {
		if (value === 'N/A' || value === '—') return 'text-gray-500';
		const numValue = parseFloat(value);
		if (isNaN(numValue)) return '';

		if (isRawValue) {
			return numValue < 0 ? 'text-red-500' : 'text-green-500';
		}
		return value.startsWith('-') ? 'text-red-500' : 'text-green-500';
	}
</script>

<div class="w-full">
	<h2 class="mb-4 text-2xl font-bold">{props.title ?? 'Financial Metrics'}</h2>

	<Tabs.Root value={activeTab} class="w-full">
		<Tabs.List>
			{#if props.rawData}
				<Tabs.Trigger value="raw">Raw Values</Tabs.Trigger>
			{/if}
			{#if props.yoyData}
				<Tabs.Trigger value="yoy">Year over Year</Tabs.Trigger>
			{/if}
			{#if props.qoqData}
				<Tabs.Trigger value="qoq">Quarter over Quarter</Tabs.Trigger>
			{/if}
		</Tabs.List>

		{#if props.rawData && rawTable}
			<Tabs.Content value="raw">
				<div class="mt-4">
					<Datatable table={rawTable}>
						<table class="w-full border-collapse">
							<thead>
								<tr>
									<ThSort table={rawTable} field={'metric'}>Metric</ThSort>
									{#each props.quarters as quarter}
										<ThSort table={rawTable} field={quarter}>
											{new Date(quarter).toLocaleDateString('en-US', {
												year: 'numeric',
												month: 'short'
											})}
										</ThSort>
									{/each}
								</tr>
								<tr>
									<ThFilter table={rawTable} field={'metric'} />
									{#each props.quarters as quarter}
										<ThFilter table={rawTable} field={quarter} />
									{/each}
								</tr>
							</thead>
							<tbody>
								{#each rawTable.rows as row (row.metric)}
									<tr class="hover:bg-slate-800">
										<td class="border-b border-slate-700 p-2">{row.metric}</td>
										{#each props.quarters as quarter}
											<td
												class="border-b border-slate-700 p-2 text-right {getValueClass(
													row[quarter],
													true
												)}"
											>
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
				<div class="mt-4">
					<Datatable table={yoyTable}>
						<table class="w-full border-collapse">
							<thead>
								<tr>
									<ThSort table={yoyTable} field={'metric'}>Metric</ThSort>
									{#each props.quarters as quarter}
										<ThSort table={yoyTable} field={quarter}>
											{new Date(quarter).toLocaleDateString('en-US', {
												year: 'numeric',
												month: 'short'
											})}
										</ThSort>
									{/each}
								</tr>
								<tr>
									<ThFilter table={yoyTable} field={'metric'} />
									{#each props.quarters as quarter}
										<ThFilter table={yoyTable} field={quarter} />
									{/each}
								</tr>
							</thead>
							<tbody>
								{#each yoyTable.rows as row (row.metric)}
									<tr class="hover:bg-slate-800">
										<td class="border-b border-slate-700 p-2">{row.metric}</td>
										{#each props.quarters as quarter}
											<td
												class="border-b border-slate-700 p-2 text-right {getValueClass(
													row[quarter],
													false
												)}"
											>
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
				<div class="mt-4">
					<Datatable table={qoqTable}>
						<table class="w-full border-collapse">
							<thead>
								<tr>
									<ThSort table={qoqTable} field={'metric'}>Metric</ThSort>
									{#each props.quarters as quarter}
										<ThSort table={qoqTable} field={quarter}>
											{new Date(quarter).toLocaleDateString('en-US', {
												year: 'numeric',
												month: 'short'
											})}
										</ThSort>
									{/each}
								</tr>
								<tr>
									<ThFilter table={qoqTable} field={'metric'} />
									{#each props.quarters as quarter}
										<ThFilter table={qoqTable} field={quarter} />
									{/each}
								</tr>
							</thead>
							<tbody>
								{#each qoqTable.rows as row (row.metric)}
									<tr class="hover:bg-slate-800">
										<td class="border-b border-slate-700 p-2">{row.metric}</td>
										{#each props.quarters as quarter}
											<td
												class="border-b border-slate-700 p-2 text-right {getValueClass(
													row[quarter],
													false
												)}"
											>
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
