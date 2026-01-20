<script lang="ts">
	interface Props {
		open: boolean;
		title?: string;
		large?: boolean;
		children?: import('svelte').Snippet;
	}

	let { open = $bindable(false), title, large = false, children }: Props = $props();

	function handleOverlayClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			open = false;
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && open) {
			open = false;
		}
	}

	function close() {
		open = false;
	}
</script>

<svelte:window onkeydown={handleKeydown} />

{#if open}
	<div class="modal-overlay" onclick={handleOverlayClick}>
		<div class="modal" class:modal-large={large}>
			{#if title}
				<div class="modal-header">
					<h2>{title}</h2>
					<button class="close-btn" onclick={close} aria-label="Close">×</button>
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
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: var(--size-4);
	}

	.modal {
		background: var(--color-card-bg);
		border-radius: var(--radius-3);
		padding: var(--size-5);
		max-width: 600px;
		width: 100%;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
		box-shadow: var(--shadow-5);
	}

	.modal-large {
		max-width: 900px;
	}

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
		flex: 1;
		overflow-y: auto;
	}

	@media (max-width: 768px) {
		.modal,
		.modal-large {
			max-width: 100%;
		}
	}
</style>
