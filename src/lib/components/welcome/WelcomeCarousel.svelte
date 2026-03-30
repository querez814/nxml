<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import * as Carousel from '$lib/components/ui/carousel';
	import { ChevronLeft, ChevronRight, TrendingUp, Laugh, DollarSign, Brain } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let api: any;
	let current = 0;

	const slides = [
		{
			icon: TrendingUp,
			title: 'Trade Smarter',
			content: "Because even your cat's nap schedule has more strategy than using just charts"
		},
		{
			icon: Laugh,
			title: 'Market Wisdom',
			content:
				'Wait? You can make money by looking at fundamentals. Who would have thought the price is coorelated'
		},
		{
			icon: Brain,
			title: 'Analysis Paralysis',
			content:
				"While you're not using us to analyze that stock, someone just bought their next house"
		}
	];

	function onInitialized(event: any) {
		api = event.detail;
	}

	function scrollPrev() {
		api?.scrollPrev();
	}

	function scrollNext() {
		api?.scrollNext();
	}

	function scrollTo(index: number) {
		api?.scrollTo(index);
	}

	$: if (api) {
		api.on('select', () => {
			current = api.selectedScrollSnap();
		});
	}
</script>

<div class="mx-auto w-full max-w-xl px-4">
	<Carousel.Root
		class="w-full"
		opts={{
			align: 'start',
			loop: true
		}}
		on:init={onInitialized}
	>
		<Carousel.Content class="-ml-1">
			{#each slides as slide, i}
				<Carousel.Item class="pl-1 md:basis-1/2 lg:basis-1/3">
					<Card.Root class="border-2 transition-all hover:border-primary">
						<Card.Header class="flex flex-col items-center">
							<svelte:component this={slide.icon} class="mb-2 h-8 w-8 text-primary" />
							<Card.Title class="text-lg font-bold">{slide.title}</Card.Title>
						</Card.Header>
						<Card.Content>
							<p class="text-center text-muted-foreground">{slide.content}</p>
						</Card.Content>
					</Card.Root>
				</Carousel.Item>
			{/each}
		</Carousel.Content>
		<div class="mt-4 flex flex-col items-center gap-2">
			<div class="flex items-center justify-center gap-2">
				<button class="relative left-0" on:click={scrollPrev}>
					<ChevronLeft class="h-4 w-4" />
				</button>
				<div class="flex gap-1">
					{#each slides as _, i}
						<button
							class="h-2 w-2 rounded-full transition-colors duration-200 {current === i
								? 'bg-primary'
								: 'bg-muted'}"
							on:click={() => scrollTo(i)}
							aria-label="Go to slide {i + 1}"
						></button>
					{/each}
				</div>
				<button class="relative right-0" on:click={scrollNext}>
					<ChevronRight class="h-4 w-4" />
				</button>
			</div>
		</div>
	</Carousel.Root>
</div>
