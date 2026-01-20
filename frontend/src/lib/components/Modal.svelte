<script lang="ts">
	interface Props {
		isOpen: boolean;
		onClose: () => void;
		title?: string;
		children?: import('svelte').Snippet;
	}

	let { isOpen, onClose, title, children }: Props = $props();

	function handleOverlayClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			onClose();
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && isOpen) {
			onClose();
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
	<div class="modal-overlay" onclick={handleOverlayClick}>
		<div class="modal">
			{#if title}
				<div class="modal-header">
					<h2>{title}</h2>
					<button class="close-btn" onclick={onClose} aria-label="Close">×</button>
				</div>
			{/if}
			<div class="modal-content">
				{#if children}
					{@render children()}
				{/if}
			</div>
		</div>
	</div>
{/if}

<style>
	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--size-4);
		padding-bottom: var(--size-3);
		border-bottom: 1px solid var(--color-border);
	}

	.modal-header h2 {
		margin: 0;
	}

	.close-btn {
		background: none;
		border: none;
		font-size: 2rem;
		line-height: 1;
		color: var(--color-text);
		cursor: pointer;
		padding: 0;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.close-btn:hover {
		color: var(--color-error);
	}

	.modal-content {
		max-height: calc(90vh - 100px);
		overflow-y: auto;
	}
</style>
