<script lang="ts">
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte'
	import SignInButton from 'clerk-sveltekit/client/SignInButton.svelte'
	import SignUpButton from 'clerk-sveltekit/client/SignUpButton.svelte'
	import UserButton from 'clerk-sveltekit/client/UserButton.svelte'
	import Button from '$lib/components/ui/button/button.svelte';
    import { Wallet } from 'lucide-svelte'
	import siteMetadata from '$lib/config/site-metadata';

    const customerPortalLink = siteMetadata.urls.subscription.portal;
</script>

<SignedIn let:user>
    <header class="flex flex-row justify-between px-4 md:px-12 py-6">
        <div class="text-xl md:text-2xl font-bold">
            InvestorTerminal
        </div>
        <div class="hidden md:flex justify-end items-center gap-6">
            <a href={
                    customerPortalLink +
                    '?prefilled_email=' +
                    user?.primaryEmailAddress?.toString()
                }
                target="_blank"
            >
                <Button size="icon" variant="secondary" class=" hover:text-foreground">
                    <Wallet class="stroke-white" size={24} />
                </Button>
            </a>
            <UserButton />
        </div>
    </header>
</SignedIn>