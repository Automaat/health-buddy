import { get, post, put, del } from '$lib/utils/api';
import type { Supplement } from '$lib/types/supplement';
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	try {
		const supplements = await get<Supplement[]>('/api/supplements?active=true');
		return {
			supplements
		};
	} catch (error) {
		console.error('Failed to load supplements:', error);
		return {
			supplements: []
		};
	}
};

export const actions: Actions = {
	create: async ({ request }) => {
		const data = await request.formData();
		const supplementData = {
			name: data.get('name'),
			dosage: data.get('dosage'),
			unit: data.get('unit'),
			frequency: data.get('frequency'),
			purpose: data.get('purpose'),
			start_date: data.get('start_date'),
			end_date: data.get('end_date') || null,
			brand: data.get('brand') || null,
			notes: data.get('notes') || null,
			is_active: true,
			owner: data.get('owner') || 'default'
		};

		try {
			await post('/api/supplements', supplementData);
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to create supplement' });
		}
	},

	update: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');
		const supplementData = {
			name: data.get('name'),
			dosage: data.get('dosage'),
			unit: data.get('unit'),
			frequency: data.get('frequency'),
			purpose: data.get('purpose'),
			start_date: data.get('start_date'),
			end_date: data.get('end_date') || null,
			brand: data.get('brand') || null,
			notes: data.get('notes') || null
		};

		try {
			await put(`/api/supplements/${id}`, supplementData);
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to update supplement' });
		}
	},

	delete: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		try {
			await del(`/api/supplements/${id}`);
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to delete supplement' });
		}
	},

	toggleActive: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');
		const isActive = data.get('is_active') === 'true';

		try {
			await put(`/api/supplements/${id}`, { is_active: !isActive });
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to toggle supplement status' });
		}
	}
};
