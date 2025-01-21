<script lang="ts">
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte';
	import SignInButton from 'clerk-sveltekit/client/SignInButton.svelte';
	import SignUpButton from 'clerk-sveltekit/client/SignUpButton.svelte';
	import UserButton from 'clerk-sveltekit/client/UserButton.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<header class="my-6 flex flex-row justify-between px-4 md:px-12 [&>*:not(ul)]:w-64">
	<a href="/" class="text-xl font-bold md:text-2xl"> Due Diligence </a>
	<ul class="flex *:md:hidden"></ul>
	<div class="hidden justify-end gap-6 md:flex">
		<SignedIn>
			<UserButton />
		</SignedIn>
		<SignedOut>
			<SignInButton>
				<Button size="sm" variant="default" class="px-6 hover:text-foreground">Login</Button>
			</SignInButton>
			<SignUpButton>
				<Button size="sm" variant="secondary" class="px-6">Sign Up</Button>
			</SignUpButton>
		</SignedOut>
	</div>
</header>
