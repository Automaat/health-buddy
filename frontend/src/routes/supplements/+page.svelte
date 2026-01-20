<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { enhance } from '$app/forms';
	import { Button, Modal, Card, Input, Select } from '@mskalski/home-ui';
	import { MEDICATION_FREQUENCIES } from '$lib/constants';
	import type { PageData } from './$types';
	import type { Supplement } from '$lib/types/supplement';

	export let data: PageData;

	$: ({ supplements } = data);

	let showModal = false;
	let editingSupplement: Supplement | null = null;

	const frequencyOptions = MEDICATION_FREQUENCIES.map((freq) => ({
		value: freq,
		label: freq
	}));

	function openAddModal() {
		editingSupplement = null;
		showModal = true;
	}

	function openEditModal(supplement: Supplement) {
		editingSupplement = supplement;
		showModal = true;
	}

	function closeModal() {
		showModal = false;
		editingSupplement = null;
		invalidateAll();
	}

	async function handleDelete(id: number) {
		if (confirm('Are you sure you want to delete this supplement?')) {
			try {
				const formData = new FormData();
				formData.append('id', id.toString());

				const response = await fetch('?/delete', {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					alert('Failed to delete supplement. Please try again.');
					return;
				}

				invalidateAll();
			} catch (error) {
				console.error('Error deleting supplement:', error);
				alert('Failed to delete supplement. Please try again.');
			}
		}
	}

	async function handleToggleActive(id: number, isActive: boolean) {
		try {
			const formData = new FormData();
			formData.append('id', id.toString());
			formData.append('is_active', isActive.toString());

			const response = await fetch('?/toggleActive', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				alert('Failed to toggle supplement status. Please try again.');
				return;
			}

			invalidateAll();
		} catch (error) {
			console.error('Error toggling supplement status:', error);
			alert('Failed to toggle supplement status. Please try again.');
		}
	}

	function formatDateForInput(dateStr: string | null): string {
		if (!dateStr) return '';
		return new Date(dateStr).toISOString().slice(0, 10);
	}

	function formatDate(dateStr: string): string {
		return new Date(dateStr).toLocaleDateString();
	}
</script>

<svelte:head>
	<title>Supplements - Health Buddy</title>
</svelte:head>

<div class="supplements-page">
	<div class="header">
		<h1>Supplements</h1>
		<Button on:click={openAddModal}>Add Supplement</Button>
	</div>

	{#if supplements.length > 0}
		<div class="supplements-grid">
			{#each supplements as supplement}
				<Card variant="green">
					<div class="supplement-card">
						<div class="card-header">
							<h3>{supplement.name}</h3>
							{#if supplement.is_active}
								<span class="badge active">Active</span>
							{:else}
								<span class="badge inactive">Inactive</span>
							{/if}
						</div>

						<div class="details">
							<div class="detail-row">
								<span class="label">Dosage:</span>
								<span class="value">{supplement.dosage} {supplement.unit}</span>
							</div>
							<div class="detail-row">
								<span class="label">Frequency:</span>
								<span class="value">{supplement.frequency}</span>
							</div>
							{#if supplement.purpose}
								<div class="detail-row">
									<span class="label">Purpose:</span>
									<span class="value">{supplement.purpose}</span>
								</div>
							{/if}
							{#if supplement.brand}
								<div class="detail-row">
									<span class="label">Brand:</span>
									<span class="value">{supplement.brand}</span>
								</div>
							{/if}
							<div class="detail-row">
								<span class="label">Start Date:</span>
								<span class="value">{formatDate(supplement.start_date)}</span>
							</div>
							{#if supplement.end_date}
								<div class="detail-row">
									<span class="label">End Date:</span>
									<span class="value">{formatDate(supplement.end_date)}</span>
								</div>
							{/if}
							{#if supplement.notes}
								<div class="detail-row">
									<span class="label">Notes:</span>
									<span class="value">{supplement.notes}</span>
								</div>
							{/if}
						</div>

						<div class="actions">
							<Button variant="secondary" size="small" on:click={() => openEditModal(supplement)}>
								Edit
							</Button>
							<Button
								variant="secondary"
								size="small"
								on:click={() => handleToggleActive(supplement.id, supplement.is_active)}
							>
								{supplement.is_active ? 'Deactivate' : 'Activate'}
							</Button>
							<Button variant="danger" size="small" on:click={() => handleDelete(supplement.id)}>
								Delete
							</Button>
						</div>
					</div>
				</Card>
			{/each}
		</div>
	{:else}
		<Card>
			<p class="empty-state">No active supplements. Click "Add Supplement" to get started.</p>
		</Card>
	{/if}
</div>

<Modal bind:open={showModal} title={editingSupplement ? 'Edit Supplement' : 'Add Supplement'}>
	<form
		method="POST"
		action={editingSupplement ? '?/update' : '?/create'}
		use:enhance={() => {
			return async () => {
				closeModal();
			};
		}}
	>
		{#if editingSupplement}
			<input type="hidden" name="id" value={editingSupplement.id} />
		{/if}
		<input type="hidden" name="owner" value="default" />

		<div class="form-group">
			<label for="name">Supplement Name *</label>
			<Input id="name" name="name" type="text" value={editingSupplement?.name || ''} required />
		</div>

		<div class="form-row">
			<div class="form-group">
				<label for="dosage">Dosage *</label>
				<Input
					id="dosage"
					name="dosage"
					type="text"
					value={editingSupplement?.dosage || ''}
					required
				/>
			</div>

			<div class="form-group">
				<label for="unit">Unit *</label>
				<Input
					id="unit"
					name="unit"
					type="text"
					value={editingSupplement?.unit || ''}
					required
					placeholder="mg, IU, etc."
				/>
			</div>
		</div>

		<div class="form-group">
			<label for="frequency">Frequency *</label>
			<Select
				id="frequency"
				name="frequency"
				options={frequencyOptions}
				value={editingSupplement?.frequency || MEDICATION_FREQUENCIES[0]}
			/>
		</div>

		<div class="form-group">
			<label for="purpose">Purpose</label>
			<Input id="purpose" name="purpose" type="text" value={editingSupplement?.purpose || ''} />
		</div>

		<div class="form-group">
			<label for="brand">Brand</label>
			<Input id="brand" name="brand" type="text" value={editingSupplement?.brand || ''} />
		</div>

		<div class="form-row">
			<div class="form-group">
				<label for="start_date">Start Date *</label>
				<Input
					id="start_date"
					name="start_date"
					type="date"
					value={formatDateForInput(
						editingSupplement?.start_date || new Date().toISOString()
					)}
					required
				/>
			</div>

			<div class="form-group">
				<label for="end_date">End Date</label>
				<Input
					id="end_date"
					name="end_date"
					type="date"
					value={formatDateForInput(editingSupplement?.end_date || null)}
				/>
			</div>
		</div>

		<div class="form-group">
			<label for="notes">Notes</label>
			<textarea id="notes" name="notes" rows="3">{editingSupplement?.notes || ''}</textarea>
		</div>

		<div class="form-actions">
			<Button type="button" variant="secondary" on:click={closeModal}>Cancel</Button>
			<Button type="submit" variant="primary">{editingSupplement ? 'Update' : 'Add'} Supplement</Button>
		</div>
	</form>
</Modal>

<style>
	.supplements-page {
		padding: var(--size-4) 0;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--size-4);
	}

	h1 {
		margin: 0;
	}

	.supplements-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: var(--size-4);
	}

	.supplement-card {
		display: flex;
		flex-direction: column;
		gap: var(--size-3);
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--size-2);
	}

	h3 {
		margin: 0;
		color: var(--color-text);
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
		min-width: 100px;
	}

	.value {
		color: var(--color-text);
	}

	.actions {
		display: flex;
		gap: var(--size-2);
		margin-top: var(--size-2);
	}

	.empty-state {
		text-align: center;
		color: var(--color-text-secondary);
		padding: var(--size-6);
	}

	.form-group {
		margin-bottom: var(--size-4);
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--size-4);
	}

	label {
		display: block;
		margin-bottom: var(--size-2);
		font-weight: 600;
		color: var(--color-text);
	}

	textarea {
		width: 100%;
		padding: var(--size-2);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-2);
		background: var(--color-bg);
		color: var(--color-text);
		font-family: inherit;
		resize: vertical;
	}

	textarea:focus {
		outline: none;
		border-color: var(--color-primary);
	}

	.form-actions {
		display: flex;
		gap: var(--size-2);
		justify-content: flex-end;
		margin-top: var(--size-4);
	}

	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--size-2);
		}

		.supplements-grid {
			grid-template-columns: 1fr;
		}

		.card-header {
			flex-direction: column;
			align-items: flex-start;
		}

		.actions {
			flex-wrap: wrap;
		}

		.form-row {
			grid-template-columns: 1fr;
		}
	}
</style>
