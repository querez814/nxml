<script lang="ts">
	import AppHeader from '$lib/components/app/app-header.svelte';
	import '../../../app.css';
	import siteMetaData from '$lib/config/site-metadata';
	import { navigating } from '$app/state';
	import { goto } from '$app/navigation';
	import { QueryClientProvider } from '@tanstack/svelte-query';
	import { queryClient } from '$lib/queries/client';

	const alwaysRedirect = false;
	const { children } = $props();
</script>

<svelte:head>
	<title>{siteMetaData.title} | App</title>
</svelte:head>

<!-- Add some check here to see if user has free trial days left or not!  -->
{#if alwaysRedirect}
	{#await goto(siteMetaData.urls.web.pricing)}
		<!-- This will never actually render, as the redirect will happen first -->
	{/await}
{/if}
<QueryClientProvider client={queryClient}>
	<div class="relative flex min-h-screen w-full flex-col">
		{#if navigating.to}
			<div class="pointer-events-none absolute inset-x-0 top-0 z-50">
				<div class="h-0.5 w-full overflow-hidden bg-slate-800/70">
					<div class="h-full w-1/3 animate-pulse bg-cyan-400"></div>
				</div>
				<p class="px-3 pt-1 text-[11px] text-slate-300" role="status" aria-live="polite">
					Loading page...
				</p>
			</div>
		{/if}
		<AppHeader />
		<main class="flex flex-1 flex-col">
			{@render children()}
		</main>
	</div>
</QueryClientProvider>

<style>
	:global(body) {
		background-color: rgb(2, 6, 23);
	}
</style>
