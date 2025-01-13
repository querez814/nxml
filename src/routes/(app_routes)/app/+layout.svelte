<script lang="ts">
	import '../../../app.css';
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import { goto } from '$app/navigation';
	import siteMetaData from '$lib/config/site-metadata';
	import AppHeader from '$lib/components/app/app-header.svelte';
    import type { UserResource } from '@clerk/types'; // or '@clerk/sveltekit'

	// Helper function to check user conditions
	function shouldRedirect(user: UserResource | null | undefined): boolean {
		// Ensure user exists and the hasFreeTrial field exists and is true
		return (
			!user || 
			!user.publicMetadata || 
			typeof user.publicMetadata.hasAppAccess !== 'boolean' || 
			!user.publicMetadata.hasAppAccess
		);
	}
</script>

<svelte:head>
	<title>{siteMetaData.title} | App</title>
</svelte:head>

<SignedIn let:user>
	{#if shouldRedirect(user)}
		{#await goto(siteMetaData.urls.web.pricing)}
			<!-- This block will not render as redirect happens immediately -->
		{/await}
	{/if}

	<div class="flex flex-col min-h-screen w-full">
		<AppHeader />
		<main class="flex-1 flex flex-col">
			<slot />
		</main>
	</div>
</SignedIn>

<style>
	:global(body) {
		background-color: rgb(2, 6, 23);
	}
</style>
