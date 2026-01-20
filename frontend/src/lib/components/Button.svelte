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

	const variantClass = variant !== 'default' ? `btn-${variant}` : '';
	const sizeClass = size !== 'medium' ? `btn-${size}` : '';
</script>

<button
	{type}
	class="btn {variantClass} {sizeClass} {className}"
	{onclick}
	{disabled}
>
	{#if children}
		{@render children()}
	{/if}
</button>
