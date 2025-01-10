<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Terminal, Keyboard, ChevronLeft, ChevronRight } from 'lucide-svelte';
	import { writable } from 'svelte/store';

	const currentStep = writable(0);

	const commands = [
		{
			title: '[ticker]',
			icon: Keyboard,
			desc: 'This leads you to an overview of the ticker with the most recent technical information to assess an entry point, and curated news!'
		},
		{
			title: 'Balance Sheet Commands',
			icon: Keyboard,
			desc: '[ticker] BS Q for Quarterly Balance Sheet and [ticker] BS A gets you the annual'
		},
		{
			title: 'Cash Flow Commands',
			icon: Keyboard,
			desc: '[ticker] CF Q for Quarterly Cash Flow Statement and [ticker] CF A gets you the annual'
		},
		{
			title: 'Income Statement Commands',
			icon: Keyboard,
			desc: '[ticker] IS Q for Quarterly Income Statement and [ticker] IS A gets you the annual'
		},
		{
			title: 'Valuation Commands',
			icon: Keyboard,
			desc: '[ticker] VAL Q for TTM Valuation Metrics'
		}
	];

	$: currentTutorialStep = commands[$currentStep];

	function nextStep() {
		currentStep.update((step) => Math.min(step + 1, commands.length - 1));
	}

	function prevStep() {
		currentStep.update((step) => Math.max(step - 1, 0));
	}
</script>

<div class="fixed inset-0 flex items-center justify-center">
	<Card.Root
		class="mx-8 w-full min-w-[1000px] border-2 bg-background/95 backdrop-blur transition-all duration-300 hover:border-primary/50 supports-[backdrop-filter]:bg-background/80"
	>
		<Card.Header class="flex items-center justify-between space-y-1 px-4">
			<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
				<svelte:component this={currentTutorialStep.icon} class="h-6 w-6 text-primary" />
				{currentTutorialStep.title}
			</Card.Title>

			<div class="flex gap-2">
				<button
					class="flex items-center gap-1 rounded-md border px-5 py-3 hover:bg-muted disabled:opacity-50"
					on:click={prevStep}
					disabled={$currentStep === 0}
				>
					<ChevronLeft class="h-4 w-4" />
					Previous
				</button>

				<button
					class="flex items-center gap-1 rounded-md border px-3 py-2 hover:bg-muted disabled:opacity-50"
					on:click={nextStep}
					disabled={$currentStep === commands.length - 1}
				>
					Next
					<ChevronRight class="h-4 w-4" />
				</button>
			</div>
		</Card.Header>

		<Card.Content class="px-4">
			<div class="flex flex-col gap-6">
				<p class="text-lg text-muted-foreground">
					{currentTutorialStep.desc}
				</p>

				<div class="flex justify-center gap-2">
					{#each commands as _, i}
						<div
							class="h-2 w-2 rounded-full transition-colors duration-200"
							class:bg-primary={i === $currentStep}
							class:bg-muted={i !== $currentStep}
						/>
					{/each}
				</div>
			</div>
		</Card.Content>
	</Card.Root>
</div>
