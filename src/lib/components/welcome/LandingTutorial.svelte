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
			description:
				"Your command-line interface for professional-grade financial analysis. Let's learn the basics.",
			example: "Press '/' to focus the command line at any time"
		},
		{
			title: 'Basic Navigation',
			icon: Command,
			description: 'Navigate to any stock by typing its ticker symbol.',
			example: '> AAPL    // Navigates to Apple Inc.\n> MSFT    // Navigates to Microsoft'
		},
		{
			title: 'Quick Search',
			icon: Search,
			description: 'Use the search command to find companies or explore metrics.',
			example: '> Placeholder until i can think of something coherent for users idk im tired'
		},
		{
			title: 'Analysis Commands',
			icon: Terminal,
			description: 'Access deep financial analysis with specialized commands.',
			example: '> Placeholder until i can think of something coherent for users idk im tired '
		},
		{
			title: 'Advanced Features',
			icon: Brain,
			description: 'Use advanced commands for comparative and technical analysis.',
			example: '> Placeholder until i can think of something coherent for users idk im tired'
		},
		{
			title: 'Keyboard Shortcuts',
			icon: Keyboard,
			description: 'Master these shortcuts for rapid analysis:',
			example: '>Placeholder until i can think of something coherent for users idk im tired'
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

<Card.Root
	class="w-full max-w-2xl border-2 bg-background/95 backdrop-blur transition-all duration-300 hover:border-primary/50 supports-[backdrop-filter]:bg-background/80"
>
	<Card.Header class="flex items-center justify-between space-y-1">
		<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
			<svelte:component this={currentTutorialStep.icon} class="h-6 w-6 text-primary" />
			{currentTutorialStep.title}
		</Card.Title>

		<div class="flex gap-2">
			<button
				class="flex items-center gap-1 rounded-md border px-3 py-2 hover:bg-muted disabled:opacity-50"
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

	<Card.Content>
		<div class="flex flex-col gap-6">
			<p class="text-lg text-muted-foreground">
				{currentTutorialStep.description}
			</p>

			<div class="rounded-md bg-muted p-4">
				<pre class="font-mono text-sm">
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
