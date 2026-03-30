<script lang="ts">
	import { enhance } from '$app/forms';
	import Spotlight from '$lib/components/ui/Spotlight/Spotlight.svelte';

	let { form } = $props();
</script>

<div class="relative flex min-h-screen w-full items-center justify-center">
	<Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="gray" />
	<span
		class="absolute inset-0 -z-10 h-full w-full bg-background bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"
	></span>
	<div
		class="absolute inset-0 -z-10 bg-gradient-to-b from-transparent via-background/60 to-background"
	></div>

	<div class="z-10 flex w-full max-w-sm flex-col items-center gap-6 px-6">
		<h1
			class="bg-gradient-to-b from-neutral-200 to-neutral-500 bg-clip-text text-center font-sans text-3xl font-semibold text-transparent md:text-4xl"
		>
			DDP
		</h1>
		<p class="text-center text-sm text-neutral-500">Enter the team password to continue.</p>

		<form method="POST" use:enhance class="flex w-full flex-col gap-3">
			<input
				name="password"
				type="password"
				placeholder="Password"
				required
				autocomplete="off"
				class="w-full rounded-lg border border-neutral-700/50 bg-neutral-900/60 px-4 py-2.5 font-mono text-sm text-neutral-200 placeholder-neutral-600 outline-none ring-amber-500/40 transition focus:border-amber-500/50 focus:ring-2"
			/>
			<button
				type="submit"
				class="rounded-lg bg-amber-500/20 px-4 py-2.5 font-mono text-sm font-medium text-amber-400 transition hover:bg-amber-500/30"
			>
				Enter
			</button>
			{#if form?.error}
				<p class="text-center text-xs text-red-400">{form.error}</p>
			{/if}
		</form>
	</div>
</div>
