<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	let revenue = $state(100);
	let cogs = $state(50);
	let grossProfit = $derived(revenue - cogs);
</script>

<div class="w-full max-w-4xl space-y-6 p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400"
				>Understanding the Income Statement</Card.Title
			>
			<Card.Description class="space-y-8">
				<section class="space-y-4">
					<div class="rounded-lg bg-slate-800 p-6">
						<h2 class="mb-4 text-xl text-green-400">The Basics</h2>
					</div>
					<p class="mb-4 text-lg text-slate-300">
						The Income Statement (sometimes called the Profit & Loss Statement or Statement of
						Earnings) tells you how much money a company made and spent over a certain period of
						time—often a quarter (3 months) or a year. Think of it as a “scorecard” that shows: 1.
						How much revenue (money in) was earned 2. How much did it cost to generate that money
						(money out) 3. How much profit in the end This statement is typically found in SEC
						Filings but I did the work for you!
					</p>
				</section>

				<section class="space-y-4">
					<div class="bg slate-800 rounded-lg p-6">
						<h2 class="mb-4 text-xl text-green-400">What is on the Income Statement?</h2>
						<div class="space-y-4">
							<div class="space-y-4">
								<div class="rounded-lg bg-slate-700">
									<p class="text-base text-slate-300">
										Total Revenue, Cost of Revenue, Gross Profit, Operating Expenses, EBITDA,
										Operating Income, Net Income, EPS
									</p>
								</div>
								<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
									<div class="rounded-lg bg-slate-700 p-4">
										<h5 class="mb-2 text-green-400">Total Revenue</h5>
										<p class="text-slate-300">
											How much money the company brought in from selling their products, services,
											or oftentimes, both.
										</p>
									</div>
									<div class="rounded-lg bg-slate-700 p-4">
										<h5 class="mb-2 text-green-400">Cost of Revenue/Cost of Sales</h5>
										<p class="text-slate-300">
											These are the direct costs tied to making or delivering whatever the company
											sells. Cloud computing costs, materials, manufacturing
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>
			</Card.Description>
		</Card.Header>
	</Card.Root>
</div>
