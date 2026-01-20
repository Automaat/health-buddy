<script lang="ts">
	import '../app.css';

	let { children } = $props();

	const navLinks = [
		{ href: '/', label: 'Dashboard', icon: '📊' },
		{ href: '/metrics', label: 'Health Metrics', icon: '📈' },
		{ href: '/medications', label: 'Medications', icon: '💊' },
		{ href: '/supplements', label: 'Supplements', icon: '🌿' },
		{ href: '/lab-results', label: 'Lab Results', icon: '🔬' },
		{ href: '/goals', label: 'Health Goals', icon: '🎯' },
		{ href: '/vaccinations', label: 'Vaccinations', icon: '💉' },
		{ href: '/history', label: 'Medical History', icon: '📋' },
		{ href: '/config', label: 'Settings', icon: '⚙️' }
	];

	let isSidebarOpen = $state(true);

	function toggleSidebar() {
		isSidebarOpen = !isSidebarOpen;
	}
</script>

<div class="app-layout">
	<aside class="sidebar" class:sidebar-closed={!isSidebarOpen}>
		<div class="sidebar-header">
			<h1 class="app-title">Health Buddy</h1>
			<button class="toggle-btn" onclick={toggleSidebar} aria-label="Toggle sidebar">
				{isSidebarOpen ? '←' : '→'}
			</button>
		</div>

		{#if isSidebarOpen}
			<nav class="nav">
				{#each navLinks as link}
					<a href={link.href} class="nav-link">
						<span class="nav-icon">{link.icon}</span>
						<span class="nav-label">{link.label}</span>
					</a>
				{/each}
			</nav>

			<div class="sidebar-footer">
				<div class="owner-selector">
					<label for="owner-select">Owner:</label>
					<select id="owner-select" class="select">
						<option value="default">Default User</option>
					</select>
				</div>
			</div>
		{/if}
	</aside>

	<main class="main-content">
		<div class="content-wrapper">
			{@render children()}
		</div>
	</main>
</div>

<style>
	.app-layout {
		display: flex;
		min-height: 100vh;
		background-color: var(--color-bg);
	}

	.sidebar {
		width: 250px;
		background-color: var(--color-bg-secondary);
		border-right: 1px solid var(--color-border);
		display: flex;
		flex-direction: column;
		transition: width 0.3s ease;
	}

	.sidebar-closed {
		width: 60px;
	}

	.sidebar-header {
		padding: var(--size-4);
		border-bottom: 1px solid var(--color-border);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.app-title {
		font-size: 1.5rem;
		margin: 0;
		color: var(--color-primary);
	}

	.sidebar-closed .app-title {
		display: none;
	}

	.toggle-btn {
		background: none;
		border: none;
		color: var(--color-text);
		font-size: 1.25rem;
		cursor: pointer;
		padding: var(--size-2);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.toggle-btn:hover {
		color: var(--color-primary);
	}

	.nav {
		flex: 1;
		padding: var(--size-3) 0;
		overflow-y: auto;
	}

	.nav-link {
		display: flex;
		align-items: center;
		gap: var(--size-3);
		padding: var(--size-3) var(--size-4);
		color: var(--color-text);
		text-decoration: none;
		transition: all 0.2s ease;
	}

	.nav-link:hover {
		background-color: var(--color-bg-tertiary);
		color: var(--color-primary);
	}

	.nav-icon {
		font-size: 1.25rem;
		min-width: 24px;
		text-align: center;
	}

	.sidebar-closed .nav-label {
		display: none;
	}

	.sidebar-footer {
		padding: var(--size-4);
		border-top: 1px solid var(--color-border);
	}

	.owner-selector {
		display: flex;
		flex-direction: column;
		gap: var(--size-2);
	}

	.owner-selector label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary);
	}

	.main-content {
		flex: 1;
		overflow-y: auto;
	}

	.content-wrapper {
		max-width: 1400px;
		margin: 0 auto;
		padding: var(--size-6) var(--size-5);
	}

	@media (max-width: 768px) {
		.sidebar {
			position: fixed;
			left: 0;
			top: 0;
			bottom: 0;
			z-index: 1000;
			width: 250px;
			transform: translateX(0);
		}

		.sidebar-closed {
			transform: translateX(-100%);
			width: 0;
		}

		.main-content {
			margin-left: 0;
		}

		.toggle-btn {
			position: fixed;
			top: var(--size-4);
			left: var(--size-4);
			z-index: 1001;
			background-color: var(--color-card-bg);
			border-radius: var(--radius-2);
			box-shadow: var(--shadow-3);
		}
	}
</style>
