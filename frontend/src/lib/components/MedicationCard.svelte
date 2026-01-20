<script lang="ts">
	import Card from './Card.svelte';
	import Button from './Button.svelte';
	import { formatDate } from '$lib/utils/format';
	import type { Medication } from '$lib/types/medication';

	export let medication: Medication;
	export let onEdit: (med: Medication) => void;
	export let onDelete: (id: number) => void;
	export let onToggleActive: (id: number, isActive: boolean) => void;

	$: isRefillSoon =
		medication.refill_reminder_date &&
		new Date(medication.refill_reminder_date) <= new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
</script>

<Card variant="teal">
	<div class="medication-card">
		<div class="header">
			<h3>{medication.name}</h3>
			<div class="badges">
				{#if isRefillSoon}
					<span class="badge warning">Refill Soon</span>
				{/if}
				{#if medication.is_active}
					<span class="badge active">Active</span>
				{:else}
					<span class="badge inactive">Inactive</span>
				{/if}
			</div>
		</div>

		<div class="details">
			<div class="detail-row">
				<span class="label">Dosage:</span>
				<span class="value">{medication.dosage} {medication.unit}</span>
			</div>
			<div class="detail-row">
				<span class="label">Frequency:</span>
				<span class="value">{medication.frequency}</span>
			</div>
			{#if medication.purpose}
				<div class="detail-row">
					<span class="label">Purpose:</span>
					<span class="value">{medication.purpose}</span>
				</div>
			{/if}
			{#if medication.prescribing_doctor}
				<div class="detail-row">
					<span class="label">Prescribed by:</span>
					<span class="value">{medication.prescribing_doctor}</span>
				</div>
			{/if}
			<div class="detail-row">
				<span class="label">Start Date:</span>
				<span class="value">{formatDate(medication.start_date)}</span>
			</div>
			{#if medication.end_date}
				<div class="detail-row">
					<span class="label">End Date:</span>
					<span class="value">{formatDate(medication.end_date)}</span>
				</div>
			{/if}
			{#if medication.refill_reminder_date}
				<div class="detail-row">
					<span class="label">Refill Date:</span>
					<span class="value">{formatDate(medication.refill_reminder_date)}</span>
				</div>
			{/if}
			{#if medication.notes}
				<div class="detail-row">
					<span class="label">Notes:</span>
					<span class="value">{medication.notes}</span>
				</div>
			{/if}
		</div>

		<div class="actions">
			<Button variant="secondary" size="small" onclick={() => onEdit(medication)}>Edit</Button>
			<Button
				variant="secondary"
				size="small"
				onclick={() => onToggleActive(medication.id, medication.is_active)}
			>
				{medication.is_active ? 'Deactivate' : 'Activate'}
			</Button>
			<Button variant="danger" size="small" onclick={() => onDelete(medication.id)}>Delete</Button>
		</div>
	</div>
</Card>

<style>
	.medication-card {
		display: flex;
		flex-direction: column;
		gap: var(--size-3);
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--size-2);
	}

	h3 {
		margin: 0;
		color: var(--color-text);
	}

	.badges {
		display: flex;
		gap: var(--size-2);
	}

	.badge {
		padding: var(--size-1) var(--size-2);
		border-radius: var(--radius-2);
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
	}

	.badge.active {
		background: var(--color-success);
		color: white;
	}

	.badge.inactive {
		background: var(--color-text-secondary);
		color: white;
	}

	.badge.warning {
		background: var(--color-warning);
		color: var(--color-bg);
	}

	.details {
		display: flex;
		flex-direction: column;
		gap: var(--size-2);
	}

	.detail-row {
		display: flex;
		gap: var(--size-2);
	}

	.label {
		font-weight: 600;
		color: var(--color-text-secondary);
		min-width: 120px;
	}

	.value {
		color: var(--color-text);
	}

	.actions {
		display: flex;
		gap: var(--size-2);
		margin-top: var(--size-2);
	}

	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			align-items: flex-start;
		}

		.actions {
			flex-wrap: wrap;
		}
	}
</style>
