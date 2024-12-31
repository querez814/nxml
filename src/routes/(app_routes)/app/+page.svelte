<script lang="ts">
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte'
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
</script>

<SignedIn let:user>
	<div class="flex flex-1 flex-col gap-8 h-full w-full  justify-center items-center">
		{ user?.username }
		<a href="/">
			Back To Home
		</a>
	</div>
</SignedIn>