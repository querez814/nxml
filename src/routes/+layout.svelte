<script lang="ts">
    import '../app.css';
    import { ModeWatcher } from "mode-watcher";
    import siteMetaData from '$lib/config/site-metadata';
</script>
    
<svelte:head>
    <title>{ siteMetaData.title }</title> 
</svelte:head>
<ModeWatcher />
<slot />