<script lang="ts" >
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte'
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import { draggable, droppable } from '@thisux/sveltednd';
	import Card from "$lib/components/ui/card/card.svelte";

	//-----------------------
	import {flip} from "svelte/animate";
    import {dndzone} from "svelte-dnd-action";
	import { Button } from '$lib/components/ui/button';
	import Separator from '$lib/components/ui/separator/separator.svelte';
	import type { TerminalCardType, TableColumn, TableData } from '../../../app';
	import { getTerminalGridState } from '$lib/state/terminal-grid-state.svelte';
	import DynamicTable from '$lib/components/app/DynamicTable.svelte';
	import { is } from 'drizzle-orm';

	// X ucin form lucide icons
	import X  from "lucide-svelte/icons/x";

	// each of these types will need a type that says how their data is formatted


    let items: {
		id: number;
		name: string;
		cardType: TerminalCardType;
	}[] = [
        {id: 1, name: "AMD", cardType: "budget"},
        {id: 2, name: "AMD", cardType: "stock"},
		{id: 3, name: "AAPL", cardType: "table"},
		{id: 4, name: "MSFT", cardType: "table"},
		{id: 5, name: "AMZN", cardType: "table"},
		{id: 6, name: "NFLX", cardType: "table"},
		{id: 7, name: "FB", cardType: "table" },
		{id: 8, name: "TWTR", cardType: "table"},
		{id: 9, name: "SNAP", cardType: "table"},
		{id: 10, name: "SPOT", cardType: "table"},
		{id: 11, name: "DIS", cardType: "table"},
    ];

	const terminalGridState = getTerminalGridState();

    const flipDurationMs = 300;
    function handleDndConsider(e) {
        items = e.detail.items;
    }

    function handleDndFinalize(e) {
        items = e.detail.items;
    }

	let columns: TableColumn[] = [
        { key: 'invoice', label: 'Invoice', type: 'text' },
        { key: 'totalAmount', label: 'Amount', type: 'money' },
        { key: 'year', label: 'Year', type: 'year' },
        // Add more columns with classes as needed
    ];

    let data: TableData[] = [
        { invoice: 'INV001', totalAmount: 250.00, year: 2022 },
        { invoice: 'INV002', totalAmount: 150.00, year: 2021 },
		{ invoice: 'INV001', totalAmount: 250.00, year: 2022 },
        { invoice: 'INV002', totalAmount: 150.00, year: 2021 },
		{ invoice: 'INV001', totalAmount: 250.00, year: 2022 },
        { invoice: 'INV002', totalAmount: 150.00, year: 2021 },
        // More invoices...
    ];

</script>

<SignedIn let:user>
	<div class={`grid grid-rows-${terminalGridState.gridRows} grid-cols-${terminalGridState.gridCols} p-3 gap-3 min-h-0 min-w-0 h-[90vh]`}
	 	use:dndzone="{{items, flipDurationMs}}" onconsider="{handleDndConsider}" onfinalize="{handleDndFinalize}"
	>
		{#each items.slice(0, terminalGridState.gridRows * terminalGridState.gridCols) as item, i (item.id)}
			<div animate:flip="{{duration: flipDurationMs}}">
				<Card class="relative flex flex-col h-full w-full rounded-none">
					<div class="absolute z-[9999] flex w-full h-10 justify-between items-center px-[0.35rem] border-b bg-background rounded-t-md">
						<div class="flex flex-row gap-2 text-sm font-semibold pl-1">
							{ item.name } 
							<Separator class="w-[0.100rem]" orientation="vertical" />
							{  item.cardType === "budget" ? "Quarterly Balance Sheet Ratios" : "Quarterly Balance Sheet Statements" } 
						</div>
						<Button class="h-7 w-7 !p-0" variant="ghost">
							<X size={16}  />
						</Button>
					</div>
					<div class="mt-10 flex flex-1 justify-center items-start z-[99] overflow-y-scroll">
						{#if item.cardType === "stock"}
							STOCK
						{:else if item.cardType === "table"}
							<DynamicTable columns={columns} data={data} />
						{:else}
							OTHER
						{/if}
					</div>
				</Card>
			</div>
		{/each}
	</div>
</SignedIn>