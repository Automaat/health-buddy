<script lang="ts">
	import Card from './Card.svelte';
	import Button from './Button.svelte';
	import { formatDate } from '$lib/utils/format';
	import type { LabResult } from '$lib/types/lab-result';

	export let labResult: LabResult;
	export let onDelete: (id: number) => void;

	let expanded = false;

	function toggleExpanded() {
		expanded = !expanded;
	}

	$: hasAbnormalValues = labResult.values.some((v) => v.is_abnormal);
</script>

<Card variant={hasAbnormalValues ? 'red' : 'default'}>
	<div class="lab-result-card">
		<div class="header" on:click={toggleExpanded} on:keydown={toggleExpanded} role="button" tabindex="0">
			<div class="header-info">
				<h3>{formatDate(labResult.test_date)} - {labResult.lab_name}</h3>
				{#if labResult.ordering_doctor}
					<p class="doctor">Ordered by: {labResult.ordering_doctor}</p>
				{/if}
			</div>
			<div class="header-actions">
				{#if hasAbnormalValues}
					<span class="abnormal-badge">⚠️ Abnormal</span>
				{/if}
				<span class="expand-icon">{expanded ? '▼' : '▶'}</span>
			</div>
		</div>

		{#if expanded}
			<div class="values-section">
				<table>
					<thead>
						<tr>
							<th>Test Name</th>
							<th>Value</th>
							<th>Unit</th>
							<th>Reference Range</th>
							<th>Status</th>
						</tr>
					</thead>
					<tbody>
						{#each labResult.values as value}
							<tr class:abnormal={value.is_abnormal}>
								<td>{value.test_name}</td>
								<td class="value-cell">{value.value}</td>
								<td>{value.unit || '-'}</td>
								<td>{value.reference_range || '-'}</td>
								<td>
									{#if value.is_abnormal}
										<span class="status-badge abnormal">Abnormal</span>
									{:else}
										<span class="status-badge normal">Normal</span>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>

				{#if labResult.notes}
					<div class="notes">
						<strong>Notes:</strong>
						<p>{labResult.notes}</p>
					</div>
				{/if}

				<div class="actions">
					<Button variant="danger" size="small" on:click={() => onDelete(labResult.id)}>
						Delete
					</Button>
				</div>
			</div>
		{/if}
	</div>
</Card>

<style>
	.lab-result-card {
		display: flex;
		flex-direction: column;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		cursor: pointer;
		user-select: none;
	}

	.header:hover {
		opacity: 0.8;
	}

	.header-info h3 {
		margin: 0 0 var(--size-1) 0;
		color: var(--color-text);
	}

	.doctor {
		margin: 0;
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.header-actions {
		display: flex;
		align-items: center;
		gap: var(--size-2);
	}

	.abnormal-badge {
		background: var(--color-error);
		color: white;
		padding: var(--size-1) var(--size-2);
		border-radius: var(--radius-2);
		font-size: 0.75rem;
		font-weight: 600;
	}

	.expand-icon {
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.values-section {
		margin-top: var(--size-4);
		border-top: 1px solid var(--color-border);
		padding-top: var(--size-4);
	}

	table {
		width: 100%;
		border-collapse: collapse;
		margin-bottom: var(--size-4);
	}

	thead {
		background: var(--color-bg-secondary);
	}

	th {
		padding: var(--size-2);
		text-align: left;
		font-weight: 600;
		font-size: 0.875rem;
		border-bottom: 2px solid var(--color-border);
	}

	td {
		padding: var(--size-2);
		border-bottom: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	tr.abnormal {
		background: rgba(191, 97, 106, 0.1);
	}

	.value-cell {
		font-weight: 600;
	}

	.status-badge {
		padding: var(--size-1) var(--size-2);
		border-radius: var(--radius-2);
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
	}

	.status-badge.normal {
		background: var(--color-success);
		color: white;
	}

	.status-badge.abnormal {
		background: var(--color-error);
		color: white;
	}

	.notes {
		margin-bottom: var(--size-4);
		padding: var(--size-3);
		background: var(--color-bg-secondary);
		border-radius: var(--radius-2);
	}

	.notes strong {
		display: block;
		margin-bottom: var(--size-2);
	}

	.notes p {
		margin: 0;
		color: var(--color-text-secondary);
	}

	.actions {
		display: flex;
		justify-content: flex-end;
	}

	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--size-2);
		}

		table {
			font-size: 0.75rem;
		}

		th,
		td {
			padding: var(--size-1);
		}
	}
</style>
