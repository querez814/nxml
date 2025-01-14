<script lang="ts">
	import AppHeader from '$lib/components/app/app-header.svelte';
	import '../../../app.css';
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import { redirect } from '@sveltejs/kit';
	import siteMetaData from '$lib/config/site-metadata';
	import { goto } from '$app/navigation';

	const alwaysRedirect = false;
</script>

<svelte:head>
	<title>{siteMetaData.title} | App</title>
</svelte:head>

<SignedIn let:user>
	{console.log(user?.publicMetadata)}
	<!-- Add some check here to see if user has free trial days left or not!  -->
	{#if alwaysRedirect}
		{#await goto(siteMetaData.urls.web.pricing)}
			<!-- This will never actually render, as the redirect will happen first -->
		{/await}
	{/if}
	<div class="flex min-h-screen w-full flex-col">
		<AppHeader />
		<main class="flex flex-1 flex-col">
			<slot />
		</main>
	</div>
</SignedIn>

<style>
	:global(body) {
		background-color: rgb(2, 6, 23);
	}
</style>
