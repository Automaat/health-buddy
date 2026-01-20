<script lang="ts">
	import Card from '$lib/components/Card.svelte';
	import MetricCard from '$lib/components/MetricCard.svelte';

	const welcomeMessage = 'Welcome to Health Buddy';
</script>

<div class="dashboard">
	<h1>{welcomeMessage}</h1>
	<p class="subtitle">Your personal health tracking companion</p>

	<div class="dashboard-grid">
		<Card variant="blue">
			<h2>📊 Dashboard</h2>
			<p>Track your health metrics, medications, and appointments all in one place.</p>
		</Card>

		<MetricCard
			title="Blood Pressure"
			value={120}
			unit="mmHg"
			variant="blue"
			trend="stable"
		/>

		<MetricCard
			title="Heart Rate"
			value={72}
			unit="bpm"
			variant="green"
			trend="stable"
		/>

		<MetricCard
			title="Weight"
			value={75}
			unit="kg"
			variant="teal"
			trend="down"
		/>

		<Card variant="teal">
			<h3>💊 Active Medications</h3>
			<p class="metric-value">0</p>
			<p class="text-secondary">No medications tracked yet</p>
		</Card>

		<Card variant="yellow">
			<h3>📅 Upcoming Appointments</h3>
			<p class="metric-value">0</p>
			<p class="text-secondary">No appointments scheduled</p>
		</Card>

		<Card variant="green">
			<h3>🎯 Health Goals</h3>
			<p class="metric-value">0</p>
			<p class="text-secondary">Set your first health goal</p>
		</Card>

		<Card>
			<h3>🔬 Recent Lab Results</h3>
			<p class="text-secondary">No lab results recorded yet</p>
		</Card>
	</div>

	<div class="getting-started">
		<Card>
			<h2>Getting Started</h2>
			<ul>
				<li>Track your daily health metrics like blood pressure, weight, and heart rate</li>
				<li>Manage your medications and supplements</li>
				<li>Record lab results and monitor trends</li>
				<li>Track medical conditions and symptoms</li>
				<li>Schedule and track appointments</li>
				<li>Set and monitor health goals</li>
			</ul>
		</Card>
	</div>
</div>

<style>
	.dashboard {
		padding: var(--size-4) 0;
	}

	h1 {
		margin-bottom: var(--size-2);
	}

	.subtitle {
		color: var(--color-text-secondary);
		margin-bottom: var(--size-6);
		font-size: 1.125rem;
	}

	.dashboard-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: var(--size-4);
		margin-bottom: var(--size-6);
	}

	.metric-value {
		font-size: 2rem;
		font-weight: 600;
		color: var(--color-text);
		margin: var(--size-2) 0;
	}

	.text-secondary {
		color: var(--color-text-secondary);
		font-size: 0.875rem;
	}

	.getting-started {
		margin-top: var(--size-6);
	}

	.getting-started ul {
		margin-top: var(--size-3);
		padding-left: var(--size-5);
	}

	.getting-started li {
		margin-bottom: var(--size-2);
		color: var(--color-text-secondary);
	}

	@media (max-width: 768px) {
		.dashboard-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
