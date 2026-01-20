<script lang="ts">
	import Card from '$lib/components/Card.svelte';
	import MetricCard from '$lib/components/MetricCard.svelte';
	import ChartCard from '$lib/components/ChartCard.svelte';
	import { METRIC_TYPES } from '$lib/constants';
	import { formatDate, formatDateTime } from '$lib/utils/format';
	import type { PageData } from './$types';
	import type { EChartsOption } from 'echarts';

	export let data: PageData;

	const welcomeMessage = 'Welcome to Health Buddy';

	$: ({ dashboardData } = data);

	// Extract latest vitals
	$: bloodPressureSystolic = dashboardData.latest_vitals.find(
		(v) => v.metric_type === METRIC_TYPES.BLOOD_PRESSURE_SYSTOLIC
	);
	$: bloodPressureDiastolic = dashboardData.latest_vitals.find(
		(v) => v.metric_type === METRIC_TYPES.BLOOD_PRESSURE_DIASTOLIC
	);
	$: heartRate = dashboardData.latest_vitals.find((v) => v.metric_type === METRIC_TYPES.HEART_RATE);
	$: weight = dashboardData.latest_vitals.find((v) => v.metric_type === METRIC_TYPES.WEIGHT);
	$: glucose = dashboardData.latest_vitals.find((v) => v.metric_type === METRIC_TYPES.GLUCOSE);

	// Weight trend chart
	const weightChartOptions: EChartsOption = {
		tooltip: {
			trigger: 'axis',
			formatter: '{b}: {c} kg'
		},
		xAxis: {
			type: 'category',
			data: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
		},
		yAxis: {
			type: 'value',
			name: 'Weight (kg)'
		},
		series: [
			{
				data: [75, 74.8, 74.5, 74.7, 74.3, 74.2, 74],
				type: 'line',
				smooth: true,
				itemStyle: { color: '#8fbcbb' }
			}
		]
	};

	// Blood pressure trend chart
	const bpChartOptions: EChartsOption = {
		tooltip: {
			trigger: 'axis'
		},
		legend: {
			data: ['Systolic', 'Diastolic']
		},
		xAxis: {
			type: 'category',
			data: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
		},
		yAxis: {
			type: 'value',
			name: 'BP (mmHg)'
		},
		series: [
			{
				name: 'Systolic',
				data: [120, 122, 118, 121, 119, 120, 120],
				type: 'line',
				smooth: true,
				itemStyle: { color: '#5e81ac' }
			},
			{
				name: 'Diastolic',
				data: [80, 81, 79, 80, 78, 80, 80],
				type: 'line',
				smooth: true,
				itemStyle: { color: '#a3be8c' }
			}
		]
	};
</script>

<div class="dashboard">
	<h1>{welcomeMessage}</h1>
	<p class="subtitle">Your personal health tracking companion</p>

	<div class="dashboard-grid">
		<Card variant="blue">
			<h2>📊 Dashboard</h2>
			<p>Track your health metrics, medications, and appointments all in one place.</p>
		</Card>

		{#if bloodPressureSystolic && bloodPressureDiastolic}
			<MetricCard
				title="Blood Pressure"
				value={`${bloodPressureSystolic.value}/${bloodPressureDiastolic.value}`}
				unit="mmHg"
				variant="blue"
				trend="stable"
			/>
		{:else}
			<Card variant="blue">
				<h3>Blood Pressure</h3>
				<p class="text-secondary">No readings yet</p>
			</Card>
		{/if}

		{#if heartRate}
			<MetricCard
				title="Heart Rate"
				value={heartRate.value}
				unit={heartRate.unit}
				variant="green"
				trend="stable"
			/>
		{:else}
			<Card variant="green">
				<h3>Heart Rate</h3>
				<p class="text-secondary">No readings yet</p>
			</Card>
		{/if}

		{#if weight}
			<MetricCard
				title="Weight"
				value={weight.value}
				unit={weight.unit}
				variant="teal"
				trend="down"
			/>
		{:else}
			<Card variant="teal">
				<h3>Weight</h3>
				<p class="text-secondary">No readings yet</p>
			</Card>
		{/if}

		<Card variant="teal">
			<h3>💊 Active Medications</h3>
			<p class="metric-value">{dashboardData.active_medications_count}</p>
			{#if dashboardData.active_medications_count === 0}
				<p class="text-secondary">No medications tracked yet</p>
			{:else}
				<ul class="medication-list">
					{#each dashboardData.active_medications as med}
						<li>{med.name} - {med.dosage} {med.unit}</li>
					{/each}
				</ul>
			{/if}
		</Card>

		<Card variant="yellow">
			<h3>📅 Upcoming Appointments</h3>
			<p class="metric-value">{dashboardData.upcoming_appointments.length}</p>
			{#if dashboardData.upcoming_appointments.length === 0}
				<p class="text-secondary">No appointments scheduled</p>
			{:else}
				<ul class="appointment-list">
					{#each dashboardData.upcoming_appointments as appt}
						<li>
							{formatDate(appt.appointment_date)} - {appt.doctor_name} ({appt.specialty})
						</li>
					{/each}
				</ul>
			{/if}
		</Card>

		<Card variant="green">
			<h3>🎯 Health Goals</h3>
			<p class="metric-value">{dashboardData.health_goals.length}</p>
			{#if dashboardData.health_goals.length === 0}
				<p class="text-secondary">Set your first health goal</p>
			{:else}
				<ul class="goal-list">
					{#each dashboardData.health_goals as goal}
						<li>
							{goal.name}: {goal.current_value}/{goal.target_value}
							{goal.target_unit}
						</li>
					{/each}
				</ul>
			{/if}
		</Card>

		<Card>
			<h3>🔬 Recent Lab Results</h3>
			{#if dashboardData.recent_lab_results.length === 0}
				<p class="text-secondary">No lab results recorded yet</p>
			{:else}
				<ul class="lab-list">
					{#each dashboardData.recent_lab_results as lab}
						<li>
							{formatDate(lab.test_date)} - {lab.lab_name}
							{#if lab.values.some((v) => v.is_abnormal)}
								<span class="abnormal-flag">⚠️ Abnormal values</span>
							{/if}
						</li>
					{/each}
				</ul>
			{/if}
		</Card>
	</div>

	<!-- Charts Section -->
	<div class="charts-section">
		<ChartCard title="Weight Trend (Last 7 Days)" options={weightChartOptions} variant="teal" />
		<ChartCard
			title="Blood Pressure Trend (Last 7 Days)"
			options={bpChartOptions}
			variant="blue"
		/>
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

	.medication-list,
	.appointment-list,
	.goal-list,
	.lab-list {
		margin-top: var(--size-2);
		padding-left: var(--size-4);
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.medication-list li,
	.appointment-list li,
	.goal-list li,
	.lab-list li {
		margin-bottom: var(--size-1);
	}

	.abnormal-flag {
		color: var(--color-error);
		font-weight: 600;
	}

	.charts-section {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
		gap: var(--size-4);
		margin-bottom: var(--size-6);
	}

	@media (max-width: 768px) {
		.dashboard-grid {
			grid-template-columns: 1fr;
		}

		.charts-section {
			grid-template-columns: 1fr;
		}
	}
</style>
