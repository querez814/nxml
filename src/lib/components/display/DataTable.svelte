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

	function formatValue(value: string, isRawValue: boolean, originalMetric: string): string {
		if (!isRawValue) {
			if (value === 'inf%' || value === '-inf%') return 'N/A';
			return value;
		}

		if (props.ratioMetrics?.includes(originalMetric)) {
			const num = parseFloat(value);
			return num.toFixed(2);
		}
		return value;
	}

	function getValueClass(value: string, isRawValue: boolean): string {
		if (value === 'N/A' || value === '—') return 'text-gray-500';
		const numValue = parseFloat(value);
		if (isNaN(numValue)) return '';

		if (isRawValue) {
			return numValue < 0 ? 'text-red-400' : 'text-emerald-400';
		}
		return value.startsWith('-') ? 'text-red-400' : 'text-emerald-400';
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
			</Tabs.List>

			{#if props.rawData && rawTable}
				<Tabs.Content value="raw">
					<div class="overflow-x-auto rounded-lg">
						<Datatable table={rawTable}>
							<table class="w-full border-separate border-spacing-0">
								<thead>
									<tr class="bg-slate-800/70">
										<th class="sticky left-0 z-20 bg-slate-800/70 px-4 py-3 text-left">
											<ThSort table={rawTable} field={'metric'}>Metric</ThSort>
										</th>
										{#each props.quarters as quarter}
											<th class="px-4 py-3 text-right">
												<ThSort table={rawTable} field={quarter}>
													{new Date(quarter).toLocaleDateString('en-US', {
														year: 'numeric',
														month: 'short'
													})}
												</ThSort>
											</th>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<th class="sticky left-0 z-20 bg-slate-800/40 p-2">
											<ThFilter table={rawTable} field={'metric'} />
										</th>
										{#each props.quarters as quarter}
											<th class="p-2">
												<ThFilter table={rawTable} field={quarter} />
											</th>
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
										<th class="sticky left-0 z-20 bg-slate-800/70 px-4 py-3 text-left">
											<ThSort table={yoyTable} field={'metric'}>Metric</ThSort>
										</th>
										{#each props.quarters as quarter}
											<th class="px-4 py-3 text-right">
												<ThSort table={yoyTable} field={quarter}>
													{new Date(quarter).toLocaleDateString('en-US', {
														year: 'numeric',
														month: 'short'
													})}
												</ThSort>
											</th>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<th class="sticky left-0 z-20 bg-slate-800/40 p-2">
											<ThFilter table={yoyTable} field={'metric'} />
										</th>
										{#each props.quarters as quarter}
											<th class="p-2">
												<ThFilter table={yoyTable} field={quarter} />
											</th>
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
										<th class="sticky left-0 z-20 bg-slate-800/70 px-4 py-3 text-left">
											<ThSort table={qoqTable} field={'metric'}>Metric</ThSort>
										</th>
										{#each props.quarters as quarter}
											<th class="px-4 py-3 text-right">
												<ThSort table={qoqTable} field={quarter}>
													{new Date(quarter).toLocaleDateString('en-US', {
														year: 'numeric',
														month: 'short'
													})}
												</ThSort>
											</th>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<th class="sticky left-0 z-20 bg-slate-800/40 p-2">
											<ThFilter table={qoqTable} field={'metric'} />
										</th>
										{#each props.quarters as quarter}
											<th class="p-2">
												<ThFilter table={qoqTable} field={quarter} />
											</th>
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

			{#if props.marginsData && marginsTable}
				<Tabs.Content value="margins">
					<div class="overflow-x-auto rounded-lg">
						<Datatable table={marginsTable}>
							<table class="w-full border-separate border-spacing-0">
								<thead>
									<tr class="bg-slate-800/70">
										<th class="sticky left-0 z-20 bg-slate-800/70 px-4 py-3 text-left">
											<ThSort table={marginsTable} field={'metric'}>Metric</ThSort>
										</th>
										{#each props.quarters as quarter}
											<th class="px-4 py-3 text-right">
												<ThSort table={marginsTable} field={quarter}>
													{new Date(quarter).toLocaleDateString('en-US', {
														year: 'numeric',
														month: 'short'
													})}
												</ThSort>
											</th>
										{/each}
									</tr>
									<tr class="bg-slate-800/40">
										<th class="sticky left-0 z-20 bg-slate-800/40 p-2">
											<ThFilter table={marginsTable} field={'metric'} />
										</th>
										{#each props.quarters as quarter}
											<th class="p-2">
												<ThFilter table={marginsTable} field={quarter} />
											</th>
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
