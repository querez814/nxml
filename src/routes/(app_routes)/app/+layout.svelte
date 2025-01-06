<script lang="ts">
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
	{#if !(typeof user?.publicMetadata['subscriptionActive'] === 'boolean') || (user?.publicMetadata['subscriptionActive'] as boolean) === false}
		{#await goto(siteMetaData.urls.web.pricing)}{/await}
	{/if}
	<div class="relative flex min-h-screen w-full flex-col bg-background">
		<slot />
	</div>
</SignedIn>

<style>
	:global(body) {
		background-color: rgb(2, 6, 23);
	}
</style>
