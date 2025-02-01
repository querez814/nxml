<script lang="ts">
    import '../app.css';
    import { ModeWatcher } from "mode-watcher";
    import siteMetaData from '$lib/config/site-metadata';
    import posthog from 'posthog-js'
    import { browser } from '$app/environment';

    import { beforeNavigate, afterNavigate } from '$app/navigation';

    if (browser) {
        beforeNavigate(() => posthog.capture('$pageleave'));
        afterNavigate(() => posthog.capture('$pageview'));
    }
    
    export const load = async () => {

        if (browser) {
            console.log('Posthog initialized')
            posthog.init(
                'phc_7nwb1TqRRPtYnzMUuvTmal38GQs2zHMjhzRzc4dIc6',
                { 
                    api_host: 'https://us.i.posthog.com',
                    person_profiles: 'identified_only', // or 'always' to create profiles for anonymous users as well
                }
            )
        }
        
        return
    };

    load();
</script>
    


<svelte:head>
    <title>{ siteMetaData.title }</title> 
</svelte:head>
<ModeWatcher />
<slot />