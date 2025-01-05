<script lang="ts">
    import * as Table from "$lib/components/ui/table/index.js";
    import TextCell from './table/TextCell.svelte';
    import MoneyCell from './table/MoneyCell.svelte';
    import IntegerCell from './table/IntegerCell.svelte';
    import FloatCell from './table/FloatCell.svelte';
    import YearCell from './table/YearCell.svelte';
    import PercentageCell from './table/PercentageCell.svelte';
	import type { TableColumn, TableData } from '../../../app';

    export let columns: TableColumn[] = [];
    export let data: TableData[] = [];

    function getComponent(type: string) {
        switch (type) {
            case 'text':
                return TextCell;
            case 'year':
                return YearCell;
            case 'integer':
                return IntegerCell;
            case 'float':
                return FloatCell;
            case 'ratio':
                return FloatCell;
            case 'money':
                return MoneyCell;
            case 'percentage':
                return PercentageCell; // Default fallback to text cell
            
            
            default:
                return TextCell; // Default fallback to text cell
        }
    }
</script>

<Table.Root>
    <Table.Header>
        <Table.Row>
            {#each columns as column}
                <Table.Head class="min-w-[150px]">{column.label}</Table.Head>
            {/each}
        </Table.Row>
    </Table.Header>
    <Table.Body>
        {#each data as row, rowIndex (rowIndex)}
            <Table.Row class="text-left">
                {#each columns as column}
                    <svelte:component this={getComponent(column.type)} class="text-left" value={row[column.key]} />
                {/each}
            </Table.Row>
        {/each}
    </Table.Body>
</Table.Root>