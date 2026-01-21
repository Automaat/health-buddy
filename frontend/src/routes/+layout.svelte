<script lang="ts">
	import '@mskalski/home-ui/styles';
	import { Navbar } from '@mskalski/home-ui';
	import { page } from '$app/stores';

	let { children } = $props();

	const navItems = [
		{ href: '/', label: 'Dashboard', icon: '📊' },
		{ href: '/metrics', label: 'Health Metrics', icon: '📈' },
		{ href: '/medications', label: 'Medications', icon: '💊' },
		{ href: '/supplements', label: 'Supplements', icon: '🌿' },
		{ href: '/lab-results', label: 'Lab Results', icon: '🔬' },
		{ href: '/goals', label: 'Health Goals', icon: '🎯' },
		{ href: '/vaccinations', label: 'Vaccinations', icon: '💉' },
		{ href: '/history', label: 'Medical History', icon: '📋' },
		{ href: '/import', label: 'Import', icon: '📥' },
		{ href: '/config', label: 'Settings', icon: '⚙️' }
	];
</script>

<div class="app">
	<Navbar items={navItems} brand="🏥 Health Buddy" currentPath={$page.url.pathname} />

	<main class="main">
		{@render children()}
	</main>
</div>

<style>
	.app {
		display: flex;
		min-height: 100vh;
	}

	.main {
		flex: 1;
		padding: var(--size-6);
		max-width: 1200px;
		margin: 0 auto;
		width: 100%;
	}
</style>
