<script lang="ts">
	import '../app.css';
	import SignIn from 'clerk-sveltekit/client/SignIn.svelte'
	import SignUp from 'clerk-sveltekit/client/SignUp.svelte'
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte'
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte'
	import SignInButton from 'clerk-sveltekit/client/SignInButton.svelte'
	import SignUpButton from 'clerk-sveltekit/client/SignUpButton.svelte'
	import UserButton from 'clerk-sveltekit/client/UserButton.svelte'
</script>

<div class="flex flex-col gap-8 h-screen w-screen  justify-center items-center">
	<SignedIn>
		<SignOutButton>
			Click to Sign Out
		</SignOutButton>
		<UserButton />
		<a href="/app">
			Go To App
		</a>
	</SignedIn>
	<SignedOut>
		<SignInButton>
			Sign In
		</SignInButton>
		<SignUpButton>
			Sign Up
		</SignUpButton>
	</SignedOut>
</div>

<style>
	:global(body) {
		min-height: 100vh;
		margin: 0;
	}
</style>