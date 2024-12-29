<script lang="ts">
    import '../../../app.css';
    import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
    import { redirect } from '@sveltejs/kit';
    import siteMetaData from '$lib/config/site-metadata';
    import { goto } from '$app/navigation';
    import AppHeader from '$lib/components/app/app-header.svelte';


    const alwaysRedirect = false; //NOTE: for testing purposes only

</script>
    
<SignedIn let:user>
    {#if alwaysRedirect || ( user?.publicMetadata["subscriptionActive"] as boolean ) === false }
        {#await goto(siteMetaData.urls.web.pricing) }
        {:then _}
            <!-- This will never actually render, as the redirect will happen first -->
        {/await}
    {/if}
    <div class="flex flex-col min-h-screen w-full">
        <AppHeader />
        <main class="flex-1 flex flex-col">
            <slot />
        </main>
    </div>
</SignedIn>

