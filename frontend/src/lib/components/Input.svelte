<script lang="ts">
	interface Props {
		id?: string;
		type?: 'text' | 'number' | 'email' | 'password' | 'date' | 'datetime-local' | 'time';
		name?: string;
		value?: string | number;
		placeholder?: string;
		required?: boolean;
		disabled?: boolean;
		readonly?: boolean;
		class?: string;
		min?: string | number;
		max?: string | number;
		step?: string | number;
		oninput?: (event: Event) => void;
	}

	let {
		id,
		type = 'text',
		name,
		value = $bindable(),
		placeholder = '',
		required = false,
		disabled = false,
		readonly = false,
		class: className = '',
		min,
		max,
		step,
		oninput
	}: Props = $props();
</script>

<input
	{id}
	{type}
	{name}
	bind:value
	{placeholder}
	{required}
	{disabled}
	{readonly}
	{min}
	{max}
	{step}
	class="input {className}"
	{oninput}
/>
