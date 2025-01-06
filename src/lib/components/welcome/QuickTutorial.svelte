<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import * as Button from '$lib/components/ui/button';
	import {
		Terminal,
		Command,
		Search,
		LineChart,
		Brain,
		Keyboard,
		ChevronLeft,
		ChevronRight
	} from 'lucide-svelte';

	let currentStep = $state(0);

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
			example: '> search revenue\n> search tech companies\n> search high growth'
		},
		{
			title: 'Analysis Commands',
			icon: LineChart,
			description: 'Access deep financial analysis with specialized commands.',
			example:
				'> bs     // Balance Sheet\n> is     // Income Statement\n> cf     // Cash Flow\n> r      // Key Ratios'
		},
		{
			title: 'Advanced Features',
			icon: Brain,
			description: 'Use advanced commands for comparative and technical analysis.',
			example: '> compare AAPL MSFT\n> technical AAPL\n> forecast revenue'
		},
		{
			title: 'Keyboard Shortcuts',
			icon: Keyboard,
			description: 'Master these shortcuts for rapid analysis:',
			example: '/ - Focus command line\n↑↓ - Command history\nTab - Auto-complete\nEsc - Clear line'
		}
	];

	function nextStep() {
		if (currentStep < tutorialSteps.length - 1) {
			currentStep = currentStep + 1;
		}
	}

	function prevStep() {
		if (currentStep > 0) {
			currentStep = currentStep - 1;
		}
	}
</script>

<Card.Root
	class="w-full max-w-2xl border-2 bg-background/95 backdrop-blur transition-all duration-300 hover:border-primary/50 supports-[backdrop-filter]:bg-background/80"
>
	<Card.Header class="flex items-center justify-between space-y-1">
		<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
			{@const CurrentIcon = tutorialSteps[currentStep].icon}
			<CurrentIcon class="h-6 w-6 text-primary" />
			{tutorialSteps[currentStep].title}
		</Card.Title>
		<div class="flex gap-2">
			<Button.Root variant="outline" size="sm" on:click={prevStep} disabled={currentStep === 0}>
				<ChevronLeft class="h-4 w-4" />
				Previous
			</Button.Root>
			<Button.Root
				variant="outline"
				size="sm"
				on:click={nextStep}
				disabled={currentStep === tutorialSteps.length - 1}
			>
				Next
				<ChevronRight class="h-4 w-4" />
			</Button.Root>
		</div>
	</Card.Header>

	<Card.Content>
		<div class="flex flex-col gap-6">
			<p class="text-lg text-muted-foreground">
				{tutorialSteps[currentStep].description}
			</p>

			<div class="rounded-md bg-muted p-4">
				<pre class="font-mono text-sm"><code>{tutorialSteps[currentStep].example}</code></pre>
			</div>

			<div class="flex justify-center gap-2">
				{#each tutorialSteps as _, i}
					<div
						class="h-2 w-2 rounded-full transition-colors duration-200"
						class:bg-primary={i === currentStep}
						class:bg-muted={i !== currentStep}
					></div>
				{/each}
			</div>
		</div>
	</Card.Content>
</Card.Root>

<style>
	pre {
		white-space: pre-wrap;
		word-wrap: break-word;
	}
</style>
