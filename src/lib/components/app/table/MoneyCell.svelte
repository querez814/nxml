<script lang="ts">
    import { Cell } from "$lib/components/ui/table/index.js";
    let { value, class: className } = $props();
</script>

<Cell class={`text-right ${className}`}>
    ${ (parseFloat(value) / 1e6).toLocaleString()}
</Cell>