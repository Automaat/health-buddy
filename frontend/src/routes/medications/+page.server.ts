import { get, post, put, del } from '$lib/utils/api';
import type { Medication } from '$lib/types/medication';
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	try {
		const medications = await get<Medication[]>('/api/medications?active=true');
		return {
			medications
		};
	} catch (error) {
		console.error('Failed to load medications:', error);
		return {
			medications: []
		};
	}
};

export const actions: Actions = {
	create: async ({ request }) => {
		const data = await request.formData();
		const medicationData = {
			name: data.get('name'),
			dosage: data.get('dosage'),
			unit: data.get('unit'),
			frequency: data.get('frequency'),
			purpose: data.get('purpose'),
			start_date: data.get('start_date'),
			end_date: data.get('end_date') || null,
			prescribing_doctor: data.get('prescribing_doctor') || null,
			refill_reminder_date: data.get('refill_reminder_date') || null,
			notes: data.get('notes') || null,
			is_active: true,
			owner: data.get('owner') || 'default'
		};

		try {
			await post('/api/medications', medicationData);
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to create medication' });
		}
	},

	update: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');
		const medicationData = {
			name: data.get('name'),
			dosage: data.get('dosage'),
			unit: data.get('unit'),
			frequency: data.get('frequency'),
			purpose: data.get('purpose'),
			start_date: data.get('start_date'),
			end_date: data.get('end_date') || null,
			prescribing_doctor: data.get('prescribing_doctor') || null,
			refill_reminder_date: data.get('refill_reminder_date') || null,
			notes: data.get('notes') || null
		};

		try {
			await put(`/api/medications/${id}`, medicationData);
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to update medication' });
		}
	},

	delete: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		try {
			await del(`/api/medications/${id}`);
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to delete medication' });
		}
	},

	toggleActive: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');
		const isActive = data.get('is_active') === 'true';

		try {
			await put(`/api/medications/${id}`, { is_active: !isActive });
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to toggle medication status' });
		}
	}
};
