import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		globals: true,
		environment: 'jsdom',
		coverage: {
			provider: 'v8',
			reporter: ['text', 'json', 'html', 'lcov'],
			exclude: [
				'node_modules/',
				'build/',
				'.svelte-kit/',
				'**/*.config.*',
				'**/*.d.ts',
				'src/app.d.ts',
				'src/app.html'
			]
		}
	}
});
