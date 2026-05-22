<script lang="ts">
	import type { PageData } from './$types';
	import './landing/landing.css';
	import MarketHeadlinesStrip from '$lib/components/landing/MarketHeadlinesStrip.svelte';

	let { data }: { data: PageData } = $props();

	let scrollPosition = $state(0);
	let isScrolled = $derived(scrollPosition > 50);
	let isMobileMenuOpen = $state(false);

	const navItems = [
		{ label: 'About', href: '#about' },
		{ label: 'Contact', href: '#contact' }
	];

	function handleScroll() {
		scrollPosition = window.scrollY;
	}

	function toggleMobileMenu() {
		isMobileMenuOpen = !isMobileMenuOpen;
	}

	function closeMobileMenu() {
		isMobileMenuOpen = false;
	}
</script>

<svelte:window onscroll={handleScroll} />

<div class="tzr-landing">
	<header class={`navbar ${isScrolled ? 'is-scrolled' : ''}`}>
		<div class="navbar-inner">
			<a class="brand" href="/" aria-label="TZR Fund home">
				<span class="brand-mark">TZR</span>
				<span class="brand-name">Fund</span>
			</a>

			<nav class="desktop-nav" aria-label="Primary">
				{#each navItems as item (item.href)}
					<a href={item.href}>{item.label}</a>
				{/each}
				<a class="cta-link" href="/programs-password">Click here to enter DDP</a>
			</nav>

			<button
				type="button"
				class="mobile-toggle"
				aria-label={isMobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
				aria-expanded={isMobileMenuOpen}
				aria-controls="mobile-nav"
				onclick={toggleMobileMenu}
			>
				{#if isMobileMenuOpen}
					<svg viewBox="0 0 24 24" aria-hidden="true">
						<path d="M6 6L18 18M18 6L6 18" />
					</svg>
				{:else}
					<svg viewBox="0 0 24 24" aria-hidden="true">
						<path d="M3 6h18M3 12h18M3 18h18" />
					</svg>
				{/if}
			</button>
		</div>

		{#if isMobileMenuOpen}
			<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile">
				{#each navItems as item (item.href)}
					<a href={item.href} onclick={closeMobileMenu}>{item.label}</a>
				{/each}
				<a class="cta-link" href="/programs-password" onclick={closeMobileMenu}>Click here to enter DDP</a>
			</nav>
		{/if}
	</header>

	<main>
		<section id="about" class="hero">
			<div class="hero-content">
				<p class="eyebrow">Multi-Strategy Opportunity Fund</p>
				<h1>
					Discerning capital meets
					<span>disciplined strategy.</span>
				</h1>
				<p>
					Uncovering latent value in the global technology sector through sophisticated equity and
					options management.
				</p>
				<div class="hero-actions">
					<a class="cta-link" href="/programs-password">Click here to enter DDP</a>
					<a class="secondary-link" href="#contact">Contact investor relations</a>
				</div>
			</div>
		</section>

		<MarketHeadlinesStrip sentiment={data.streamed.marketSentiment} />

		<section id="contact" class="contact">
			<div class="contact-content">
				<p class="eyebrow">Investor Relations</p>
				<h2>Inquiry for qualified investors.</h2>
				<p>
					TZR Fund is open to accredited individuals and institutional partners who share our long-term
					vision for disciplined growth.
				</p>
				<a href="mailto:investorrelations@tzrfund.com">investorrelations@tzrfund.com</a>
			</div>
		</section>
	</main>

	<footer class="footer">
		<div class="footer-inner">
			<div>
				<p class="brand-line">TZR Fund</p>
				<p>
					A multi-strategy opportunity fund specializing in technology and undervalued global equities.
				</p>
			</div>
			<nav aria-label="Footer">
				<a href="#about">About</a>
				<a href="#contact">Contact</a>
				<a href="/programs-password">Click here to enter DDP</a>
			</nav>
		</div>
	</footer>
</div>
