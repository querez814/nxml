<script lang="ts">
	import CommandLine from '$lib/components/cmd/CommandLine.svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Button from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Separator from '$lib/components/ui/separator';
	import { Terminal, Sparkles, Keyboard } from 'lucide-svelte';
	import LandingTutorial from '$lib/components/welcome/LandingTutorial.svelte';
	import CommandList from '$lib/components/welcome/CommandList.svelte';

	let showTutorial = $state(false);
	let showCommands = $state(false);

</script>

<div class="min-h-screen bg-gradient-to-b from-background to-muted">
		<div class="container mx-auto flex min-h-screen flex-col px-4 py-8">
			<div class="mb-12 flex flex-col items-center">
				<h1
					class="animate-pulse bg-gradient-to-r from-primary to-primary/50 bg-clip-text text-center text-4xl font-bold tracking-tighter text-transparent sm:text-5xl"
				>
					Your Terminal, Your Edge
				</h1>
				<p
					class="mt-4 max-w-[42rem] animate-[fade-in_0.5s_ease-out] text-center text-muted-foreground"
				>
					Fundamental, Essential Financial Data and Metrics used by the pros, at your fingertips
				</p>
			</div>

			<div class="flex flex-1 justify-center">
				<div class="w-full max-w-4xl space-y-6">
					<Card.Root class="border-2 bg-background/95 backdrop-blur">
						<Card.Header class="flex items-center justify-between space-y-1">
							<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
								<Terminal class="h-6 w-6" />
								Terminal
							</Card.Title>
							<Button.Root variant="ghost" size="sm">Sign Out</Button.Root>
						</Card.Header>
						<Card.Content>
							<div class="flex flex-col items-center gap-6">
								<div class="flex flex-col items-center gap-2 text-center">
									<p class="flex items-center gap-2 text-lg font-medium">
										Welcome back
										<Sparkles class="h-4 w-4 animate-pulse text-primary" />
									</p>
									<div class="flex items-center gap-2 text-sm text-muted-foreground">
										<Keyboard class="h-4 w-4" />
										<span>Press <kbd class="rounded bg-muted px-1 py-0.5">/ </kbd> to start</span>
									</div>
								</div>

								<div class="relative w-full">
									<CommandLine />
								</div>

								<div class="w-full space-y-4">
									<Separator.Root />
									<div class="flex justify-center gap-4 text-sm">
										<Dialog.Root bind:open={showTutorial}>
											<Dialog.Trigger
												class="inline-flex h-9 items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
											>
												Quick Tutorial
											</Dialog.Trigger>
											<Dialog.Portal>
												<Dialog.Overlay />
												<Dialog.Content class="sm:max-w-2xl">
													<LandingTutorial />
													<Dialog.Close>
														<Button.Root variant="outline" size="sm" class="mt-4"
															>Close Tutorial</Button.Root
														>
													</Dialog.Close>
												</Dialog.Content>
											</Dialog.Portal>
										</Dialog.Root>

										<Dialog.Root bind:open={showCommands}>
											<Dialog.Trigger
												class="inline-flex h-9 items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
											>
												Command List
											</Dialog.Trigger>
											<Dialog.Portal>
												<Dialog.Overlay />
												<Dialog.Content class="sm:max-w-2xl">
													<CommandList />
													<Dialog.Close>
														<Button.Root variant="outline" size="sm" class="mt-4"
															>Close Commands</Button.Root
														>
													</Dialog.Close>
												</Dialog.Content>
											</Dialog.Portal>
										</Dialog.Root>
									</div>
								</div>
							</div>
						</Card.Content>
					</Card.Root>
				</div>
			</div>
		</div>
	</div>

<style>
	:global(.group) {
		transform: translateZ(0);
	}
	:global(.group:hover) {
		background-color: rgba(255, 255, 255, 0.02);
	}
</style>
