<script lang="ts">
	import CommandLine from '$lib/components/cmd/CommandLine.svelte';
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte';
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Button from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Separator from '$lib/components/ui/separator';
	import { Terminal, Sparkles, Keyboard, TrendingUp } from 'lucide-svelte';
	import WelcomeCarousel from '$lib/components/welcome/WelcomeCarousel.svelte';
	import LandingTutorial from '$lib/components/welcome/LandingTutorial.svelte';

	let showTutorial = $state(false);
</script>

<SignedIn let:user>
	<div class="min-h-screen bg-gradient-to-b from-background to-muted">
		<div
			class="container mx-auto flex min-h-screen flex-col items-center justify-center gap-8 px-4"
		>
			<div class="mb-4 flex flex-col items-center gap-2">
				<h1
					class="animate-pulse bg-gradient-to-r from-primary to-primary/50 bg-clip-text text-center text-4xl font-bold tracking-tighter text-transparent sm:text-5xl"
				>
					Your Terminal, Your Edge
				</h1>
				<p class="animate-fade-in max-w-[42rem] text-center text-muted-foreground">
					Financial Data and Metrics used by the pros, at your fingertips
				</p>
			</div>

			<Card.Root
				class="w-full max-w-2xl border-2 bg-background/95 backdrop-blur transition-all duration-300 hover:border-primary/50 supports-[backdrop-filter]:bg-background/80"
			>
				<Card.Header class="flex items-center justify-between space-y-1">
					<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
						<Terminal class="h-6 w-6" />
						InvestorTerminal
					</Card.Title>
					<SignOutButton>
						<Button.Root variant="ghost" size="sm">Sign Out</Button.Root>
					</SignOutButton>
				</Card.Header>
				<Card.Content>
					<div class="flex flex-col items-center gap-6">
						<div class="flex flex-col items-center gap-2 text-center">
							<p class="flex items-center gap-2 text-lg font-medium">
								Welcome back, {user?.username}
								<Sparkles class="h-4 w-4 animate-pulse text-primary" />
							</p>
							<div class="flex items-center gap-2 text-sm text-muted-foreground">
								<Keyboard class="h-4 w-4" />
								<span>Press <kbd class="rounded bg-muted px-1 py-0.5">/ </kbd> to start</span>
							</div>
						</div>

						<div class="relative w-full">
							<div class="absolute -top-6 left-1/2 -translate-x-1/2 transform">
								<TrendingUp class="h-5 w-5 animate-bounce text-primary" />
							</div>
							<CommandLine />
						</div>

						<div class="w-full space-y-4">
							<Separator.Root />
							<div class="flex justify-center gap-4 text-sm">
								<Dialog.Root bind:open={showTutorial}>
									<Dialog.Trigger>
										<Button.Root variant="ghost" size="sm">Quick Tutorial</Button.Root>
									</Dialog.Trigger>
									<Dialog.Portal>
										<Dialog.Overlay />
										<Dialog.Content class="sm:max-w-2xl">
											<LandingTutorial />
											<Dialog.Close>
												<Button.Root variant="outline" size="sm" class="mt-4">
													Close Tutorial
												</Button.Root>
											</Dialog.Close>
										</Dialog.Content>
									</Dialog.Portal>
								</Dialog.Root>
								<Button.Root variant="ghost" size="sm">Command List (Adding Soon)</Button.Root>
							</div>
						</div>
					</div>
				</Card.Content>
			</Card.Root>

			<WelcomeCarousel />

			<footer class="text-center text-sm text-muted-foreground">
				<p>Start with any ticker symbol - e.g., "AAPL", "MSFT", "TSLA" 🚀</p>
			</footer>
		</div>
	</div>
</SignedIn>

<style lang="postcss">
	@keyframes fade-in {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	.animate-fade-in {
		animation: fade-in 0.5s ease-out;
	}
</style>
