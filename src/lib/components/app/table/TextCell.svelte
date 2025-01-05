<script lang="ts">
    import { Cell } from "$lib/components/ui/table/index.js";

    let { value, class: className } = $props();
</script>

<Cell class={className}>{value.toString()}</Cell>


