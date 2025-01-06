<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import * as Carousel from '$lib/components/ui/carousel';
	import { ChevronLeft, ChevronRight, TrendingUp, Laugh, DollarSign, Brain } from 'lucide-svelte';

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
</script>

<div class="mx-auto w-full max-w-xl px-4">
	<Carousel.Root class="w-full">
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
		<div class="mt-4 flex items-center justify-center gap-2">
			<Carousel.Previous class="relative left-0">
				<ChevronLeft class="h-4 w-4" />
			</Carousel.Previous>
			<Carousel.Next class="relative right-0">
				<ChevronRight class="h-4 w-4" />
			</Carousel.Next>
		</div>
	</Carousel.Root>
</div>
