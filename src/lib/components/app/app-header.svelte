<script lang="ts">
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte'
	import SignInButton from 'clerk-sveltekit/client/SignInButton.svelte'
	import SignUpButton from 'clerk-sveltekit/client/SignUpButton.svelte'
	import UserButton from 'clerk-sveltekit/client/UserButton.svelte'
	import Button from '$lib/components/ui/button/button.svelte';
    import { ChevronDown, CircleHelp, CircleUserRound, SquareUser, Wallet, X } from 'lucide-svelte'
	import siteMetadata from '$lib/config/site-metadata';
    import CirclePlus from "lucide-svelte/icons/circle-plus";
    import Cloud from "lucide-svelte/icons/cloud";
    import CreditCard from "lucide-svelte/icons/credit-card";
    import Github from "lucide-svelte/icons/github";
    import Keyboard from "lucide-svelte/icons/keyboard";
    import LifeBuoy from "lucide-svelte/icons/life-buoy";
    import LogOut from "lucide-svelte/icons/log-out";
    import Mail from "lucide-svelte/icons/mail";
    import MessageSquare from "lucide-svelte/icons/message-square";
    import Plus from "lucide-svelte/icons/plus";
    import Settings from "lucide-svelte/icons/settings";
    import User from "lucide-svelte/icons/user";
    import UserPlus from "lucide-svelte/icons/user-plus";
    import Users from "lucide-svelte/icons/users";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { cn } from '$lib/utils';
    import { onMount, onDestroy } from 'svelte';
	import { getTerminalGridState } from '$lib/state/terminal-grid-state.svelte';
	import { getTerminalCommandState } from '$lib/state/terminal-command-state.svelte';
	import Separator from '../ui/separator/separator.svelte';

    let divElement: HTMLDivElement;
    let width: number = 0;

    // Update width based on the div element
    $: width = divElement?.offsetWidth;

    // Function to handle resize
    function handleResize() {
        if (divElement) {
        width = divElement.offsetWidth;
        }
    }

    // Set up and tear down the window resize listener
    onMount(() => {
        window.addEventListener('resize', handleResize);
        return () => {
        window.removeEventListener('resize', handleResize);
        };
    });

    const customerPortalLink = siteMetadata.urls.subscription.portal;

    
	const terminalGridState = getTerminalGridState();
    const terminalCommandState = getTerminalCommandState();

    // Time stuff --------------------------------------------

   
    let now: Date = new Date();
    let useTwentyFourHourFormat: boolean = true; // State to track which format to display

   // Function to get the timezone abbreviation
   const getTimezone = (): string => {
        return new Intl.DateTimeFormat('en-US', { timeZoneName: 'short' }).format(now).split(' ')[2];
    };

    // Function to format the date and time
    const updateTime = (): string => {
        now = new Date();
        const timezone: string = now.toLocaleTimeString('en-us',{timeZoneName:'short'}).split(' ')[2] // Get current timezone abbreviation
        let hours: number = now.getHours();
        let minutes: string = now.getMinutes().toString().padStart(2, '0');
        let seconds: string = now.getSeconds().toString().padStart(2, '0');
        let suffix: string = '';

        if (!useTwentyFourHourFormat) {
            suffix = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; // the hour '0' should be '12'
        }

        let hourString = hours.toString().padStart(2, '0');

        return `${hourString}:${minutes}:${seconds} ${suffix} ${timezone}`;
    };

    let currentTime: string = updateTime();

    // Update the time every second
    onMount(() => {
        const interval = setInterval(() => {
            currentTime = updateTime();
        }, 1000);

        return () => {
            clearInterval(interval);
        };
    });

    // Function to toggle time format
    const toggleFormat = (): void => {
        useTwentyFourHourFormat = !useTwentyFourHourFormat;
        currentTime = updateTime(); // Update time immediately on toggle
    };
</script>

<SignedIn let:user>
    <header class="flex items-center flex-row  px-4 py-1 border border-b">
        <div class="flex flex-1 relative pr-2">
            <Label class="absolute top-1/2 transform -translate-y-1/2" >
                <div class="flex gap-0 text-[0.900rem] font-bold" bind:this={divElement} >
                    <span class="text-green-400">
                        { user?.username }@investor-terminal
                    </span>
                    : 
                    <span class="text-blue-500">
                        /app/
                    </span>
                     $ 
                </div>
            </Label>
            <Input 
                style="padding-left: { width + 8 }px"
                class="flex items-center w-full border-none focus:!ring-0 focus:!ring-transparent focus:!ring-offset-0 font-semibold" 
                bind:value={terminalCommandState.pendingCommand}
                disabled={terminalCommandState.isDisabled}
                on:keydown={(e) => {
                    if (e.key === 'Enter') {
                        terminalCommandState.executeCommand();
                        //set atimeout and disabled for a few seconds
                        terminalCommandState.isDisabled = true;
                        setTimeout(() => {
                            terminalCommandState.isDisabled = false;
                        }, 2000);
                    } else if (e.key === 'ArrowUp') {
                        terminalCommandState.navigateHistory('up');
                    } else if (e.key === 'ArrowDown') {
                        terminalCommandState.navigateHistory('down');
                    }
                }}

            />
        </div>
        <div class="hidden md:flex justify-end items-center gap-2">     
            <Button class="h-8 w-8 rounded-full !p-0 [&_svg]:stroke-muted-foreground hover:[&_svg]:stroke-foreground" variant="ghost">
                <CircleHelp size={22}  />
            </Button>
            <Button size="sm" variant="ghost" 
                style={   useTwentyFourHourFormat ? 'min-width: 5rem' : 'min-width: 6.5rem' }
                class="h-7 text-xs text-foreground/50 font-semibold tracking-wider !py-1 !px-0  min-w-24 hover:bg-background hover:text-foreground/75"
                onclick={toggleFormat}
            >
                {currentTime}
            </Button>
            <span class="text-base text-foreground/50 font-semibold pr-1">•</span>
            <div class="flex flex-row gap-0 items-center hover:text-foreground/75 text-foreground/50">
                <span class="text-xs tracking-wide font-semibold">
                    Grid Layout:
                </span>
                <Input type="number" class="text-xs text-center w-5 h-5 !py-0 !px-0 border-none focus:!ring-0 focus:!ring-transparent focus:!ring-offset-0  [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none" 
                    min={terminalGridState.minRows}
                    max={terminalGridState.maxRows}
                    disabled
                    bind:value={terminalGridState.gridRows}
                />
                <X size={14}  />
                <Input type="number" class=" text-xs text-center w-5 h-5 !py-0 !px-0 border-none focus:!ring-0 focus:!ring-transparent focus:!ring-offset-0   [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    min={terminalGridState.minCols}
                    max={terminalGridState.maxCols}
                    disabled
                    bind:value={terminalGridState.gridCols}
                />
            </div>
            <DropdownMenu.Root>
                <DropdownMenu.Trigger disabled>
                    <Button class="h-8 w-8 rounded-full !p-0 [&_svg]:stroke-muted-foreground hover:[&_svg]:stroke-foreground" variant="ghost">
                        <CircleUserRound size={22}  />
                    </Button>
                </DropdownMenu.Trigger>
                <DropdownMenu.Content class="w-56" align="end">
                <DropdownMenu.Label>My Account</DropdownMenu.Label>
                <DropdownMenu.Separator />
                <DropdownMenu.Group>

                        <DropdownMenu.Item>
                            <User class="mr-2 h-4 w-4" />
                            <span>Profile</span>
                            <DropdownMenu.Shortcut>⇧⌘P</DropdownMenu.Shortcut>
                        </DropdownMenu.Item>

                        <a href={
                                customerPortalLink +
                                '?prefilled_email=' +
                                user?.primaryEmailAddress?.toString()
                            }
                            target="_blank"
                        >
                            <DropdownMenu.Item>
                                <CreditCard class="mr-2 h-4 w-4" />
                                <span>Billing</span>
                                <DropdownMenu.Shortcut>⌘B</DropdownMenu.Shortcut>
                            </DropdownMenu.Item>
                        </a>
                
                    <DropdownMenu.Item>
                    <Settings class="mr-2 h-4 w-4" />
                    <span>Settings</span>
                    <DropdownMenu.Shortcut>⌘S</DropdownMenu.Shortcut>
                    </DropdownMenu.Item>
                    <DropdownMenu.Item>
                    <Keyboard class="mr-2 h-4 w-4" />
                    <span>Keyboard shortcuts</span>
                    <DropdownMenu.Shortcut>⌘K</DropdownMenu.Shortcut>
                    </DropdownMenu.Item>
                </DropdownMenu.Group>
                </DropdownMenu.Content>
            </DropdownMenu.Root>
        </div>
    </header>
</SignedIn>
