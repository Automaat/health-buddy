<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { Button, Modal, Card } from '@mskalski/home-ui';
	import MedicationCard from '$lib/components/MedicationCard.svelte';
	import MedicationForm from '$lib/components/MedicationForm.svelte';
	import type { PageData } from './$types';
	import type { Medication } from '$lib/types/medication';

	export let data: PageData;

	$: ({ medications } = data);

	let showModal = false;
	let editingMedication: Medication | null = null;

	function openAddModal() {
		editingMedication = null;
		showModal = true;
	}

	function openEditModal(medication: Medication) {
		editingMedication = medication;
		showModal = true;
	}

	function closeModal() {
		showModal = false;
		editingMedication = null;
		invalidateAll();
	}

	async function handleDelete(id: number) {
		if (confirm('Are you sure you want to delete this medication?')) {
			try {
				const formData = new FormData();
				formData.append('id', id.toString());

				const response = await fetch('?/delete', {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					alert('Failed to delete medication. Please try again.');
					return;
				}

				invalidateAll();
			} catch (error) {
				console.error('Error deleting medication:', error);
				alert('Failed to delete medication. Please try again.');
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
				alert('Failed to toggle medication status. Please try again.');
				return;
			}

			invalidateAll();
		} catch (error) {
			console.error('Error toggling medication status:', error);
			alert('Failed to toggle medication status. Please try again.');
		}
	}
</script>

<svelte:head>
	<title>Medications - Health Buddy</title>
</svelte:head>

<div class="medications-page">
	<div class="header">
		<h1>Medications</h1>
		<Button on:click={openAddModal}>Add Medication</Button>
	</div>

	{#if medications.length > 0}
		<div class="medications-grid">
			{#each medications as medication}
				<MedicationCard
					{medication}
					onEdit={openEditModal}
					onDelete={handleDelete}
					onToggleActive={handleToggleActive}
				/>
			{/each}
		</div>
	{:else}
		<Card>
			<p class="empty-state">No active medications. Click "Add Medication" to get started.</p>
		</Card>
	{/if}
</div>

<Modal bind:open={showModal} title={editingMedication ? 'Edit Medication' : 'Add Medication'}>
	<MedicationForm medication={editingMedication} onClose={closeModal} />
</Modal>

<style>
	.medications-page {
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

	.medications-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: var(--size-4);
	}

	.empty-state {
		text-align: center;
		color: var(--color-text-secondary);
		padding: var(--size-6);
	}

	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--size-2);
		}

		.medications-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
