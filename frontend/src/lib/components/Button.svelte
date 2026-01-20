<script lang="ts">
	interface Props {
		type?: 'button' | 'submit' | 'reset';
		variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'default';
		size?: 'small' | 'medium' | 'large';
		class?: string;
		onclick?: (event: MouseEvent) => void;
		disabled?: boolean;
		children?: import('svelte').Snippet;
	}

	let {
		type = 'button',
		variant = 'primary',
		size = 'medium',
		class: className = '',
		onclick,
		disabled = false,
		children
	}: Props = $props();

	const variantClass = $derived(variant !== 'default' ? `btn-${variant}` : '');
	const sizeClass = $derived(size !== 'medium' ? `btn-${size}` : '');
</script>

<button
	{type}
	class="btn {variantClass} {sizeClass} {className}"
	{onclick}
	{disabled}
	{...$$restProps}
>
	{#if children}
		{@render children()}
	{/if}
</button>
