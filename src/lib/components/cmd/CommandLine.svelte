<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let { onTickerChange } = $props<{
		onTickerChange?: (ticker: string) => void;
	}>();

	let inputValue = $state('');
	let history: string[] = [];
	let historyIndex = -1;
	let inputRef: HTMLInputElement;

	const sectionAliases: Record<string, string> = {
		bs: 'balancesheet',
		cf: 'cashflow',
		is: 'incomestatement',
		val: 'valuation'
	};

	const subsectionAliases: Record<string, string> = {
		q: 'quarterly',
		a: 'annual'
	};

	function parseCommand(input: string): void {
		const parts = input.toLowerCase().trim().split(/\s+/);

		if (parts[0] === 'clear') {
			inputValue = '';
			return;
		}

		if (parts.length > 0 && /^[A-Za-z]{1,5}$/.test(parts[0])) {
			const ticker = parts[0].toUpperCase();
			let path = `/app/${ticker}`;

			if (parts[1]) {
				const section = sectionAliases[parts[1] as keyof typeof sectionAliases] || parts[1];
				if (section in sectionAliases || Object.values(sectionAliases).includes(section)) {
					path += `/${section}`;

					if (parts[2]) {
						const subsection =
							subsectionAliases[parts[2] as keyof typeof subsectionAliases] || parts[2];
						if (
							subsection in subsectionAliases ||
							Object.values(subsectionAliases).includes(subsection)
						) {
							path += `/${subsection}`;
						}
					}
				}
			}

			onTickerChange?.(ticker);
			goto(path);
		}
	}

	function handleSubmit() {
		if (inputValue.trim()) {
			history = [...history, inputValue];
			historyIndex = history.length;

			parseCommand(inputValue);
			inputValue = '';
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			event.preventDefault();
			handleSubmit();
		} else if (event.key === 'ArrowUp') {
			event.preventDefault();
			if (historyIndex > 0) {
				historyIndex--;
				inputValue = history[historyIndex];
			}
		} else if (event.key === 'ArrowDown') {
			event.preventDefault();
			if (historyIndex < history.length - 1) {
				historyIndex++;
				inputValue = history[historyIndex];
			} else if (historyIndex === history.length - 1) {
				historyIndex = history.length;
				inputValue = '';
			}
		}
	}

	// Handle keyboard shortcut
	function handleGlobalKeydown(event: KeyboardEvent) {
		if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey) {
			event.preventDefault();
			inputRef?.focus();
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleGlobalKeydown);
		return () => {
			window.removeEventListener('keydown', handleGlobalKeydown);
		};
	});
</script>

<div class="flex w-full flex-col">
	<div class="flex w-full items-center rounded-md border border-gray-800 bg-gray-900 p-3">
		<span class="mr-2 font-mono text-green-400">❯</span>
		<input
			bind:this={inputRef}
			type="text"
			bind:value={inputValue}
			onkeydown={handleKeydown}
			placeholder="Try 'AAPL bs r' or type 'help'"
			class="flex-1 border-none bg-transparent font-mono text-sm text-gray-100 outline-none placeholder:text-gray-600"
		/>
	</div>
</div>
