<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import {
		Terminal,
		Command,
		Search,
		Brain,
		Keyboard,
		ChevronLeft,
		ChevronRight
	} from 'lucide-svelte';
	import { writable } from 'svelte/store';

	const currentStep = writable(0);

	const tutorialSteps = [
		{
			title: 'Welcome to InvestorTerminal',
			icon: Terminal,
			description: 'Your home for financial information of any publicly listed ticker.',
			example:
				"Press '/' to type the command line at any time, click the next button to learn how to navigate around the site"
		},
		{
			title: 'Basic Navigation',
			icon: Command,
			description: 'Navigate to Any Stock or Metric by using simple commands. ',
			example:
				'> AAPL CF Q    // Navigates to AAPL quarterly cash flow data along with some computations to help assess it \n> MSFT IS Q    // Navigates to Microsoft Income Statement Quarterly. Additonally writing A at the end gives you the annualized data '
		},
		{
			title: 'Quick Search',
			icon: Search,
			description:
				'Use the search command to access company financial metrics for your own analysis.',
			example:
				'> All terminal commands are in the Command List, which you can click on after this brief tutorial'
		}
	];

	$: currentTutorialStep = tutorialSteps[$currentStep];

	function nextStep() {
		currentStep.update((step) => Math.min(step + 1, tutorialSteps.length - 1));
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
					disabled={$currentStep === tutorialSteps.length - 1}
				>
					Next
					<ChevronRight class="h-4 w-4" />
				</button>
			</div>
		</Card.Header>

		<Card.Content class="px-4">
			<div class="flex flex-col gap-6">
				<p class="text-lg text-muted-foreground">
					{currentTutorialStep.description}
				</p>

				<div class="rounded-md bg-muted p-2">
					<pre class="whitespace-pre-wrap font-mono text-sm">
                        <code>{currentTutorialStep.example}</code>
                    </pre>
				</div>

				<div class="flex justify-center gap-2">
					{#each tutorialSteps as _, i}
						<div
							class="h-2 w-2 rounded-full transition-colors duration-200"
							class:bg-primary={i === $currentStep}
							class:bg-muted={i !== $currentStep}
						></div>
					{/each}
				</div>
			</div>
		</Card.Content>
	</Card.Root>
</div>
