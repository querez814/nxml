<script lang="ts">
	import AppHeader from '$lib/components/app/app-header.svelte';
	import '../../../app.css';
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import { redirect } from '@sveltejs/kit';
	import siteMetaData from '$lib/config/site-metadata';
	import { goto } from '$app/navigation';
	import posthog from 'posthog-js';
	import AppAnalyticsWrapper from '$lib/components/analytics/AppAnalyticsWrapper.svelte';
	import type { UserResource } from '@clerk/types';

	const alwaysRedirect = false;

	// NOT CURRENTLY USED AND NEEDS TO BE USED
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
	<!-- Add some check here to see if user has free trial days left or not!  -->
	{#if alwaysRedirect}
		{#await goto(siteMetaData.urls.web.pricing)}
			<!-- This will never actually render, as the redirect will happen first -->
		{/await}
	{/if}
	<AppAnalyticsWrapper user={user as UserResource}>
		<div class="flex min-h-screen w-full flex-col">
			<AppHeader />
			<main class="flex flex-1 flex-col">
				<slot />
			</main>
		</div>
	</AppAnalyticsWrapper>
</SignedIn>

<style>
	:global(body) {
		background-color: rgb(2, 6, 23);
	}
</style>
