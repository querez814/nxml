<script lang="ts">
	import '../../app.css';
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte'
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
</script>

<SignedIn let:user>
	<div class="flex flex-col gap-8 h-screen w-screen  justify-center items-center">
		{user?.username}
		<SignOutButton>
			Click to Sign Out
		</SignOutButton>
		<a href="/">
			Back To Home
		</a>
	</div>
</SignedIn>

<style>
	:global(body) {
		min-height: 100vh;
		margin: 0;
	}
</style>