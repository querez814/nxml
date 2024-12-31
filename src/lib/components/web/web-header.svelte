<script lang="ts">
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte'
	import SignInButton from 'clerk-sveltekit/client/SignInButton.svelte'
	import SignUpButton from 'clerk-sveltekit/client/SignUpButton.svelte'
	import UserButton from 'clerk-sveltekit/client/UserButton.svelte'
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<header class="flex flex-row justify-between [&>*:not(ul)]:w-64 px-4 md:px-12 my-6">
    <a href="/" class="text-xl md:text-2xl font-bold">
        InvestorTerminal
    </a>
    <ul class="flex *:md:hidden">

    </ul>
    <div class="hidden md:flex justify-end gap-6">
        <SignedIn>
            <UserButton />
        </SignedIn>
        <SignedOut>
            <SignInButton>
                <Button size="sm" variant="default" class="px-6 hover:text-foreground">
                    Login
                </Button>
            </SignInButton>
            <SignUpButton>
                <Button size="sm" variant="secondary" class="px-6">
                    Sign Up
                </Button>
            </SignUpButton>
        </SignedOut>
    </div>
</header>