import { get } from '$lib/utils/api';
import type { DashboardData } from '$lib/types/dashboard';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	try {
		const data = await get<DashboardData>('/api/dashboard');
		return {
			dashboardData: data
		};
	} catch (error) {
		console.error('Failed to load dashboard data:', error);
		// Return empty data structure if API fails
		return {
			dashboardData: {
				latest_vitals: [],
				active_medications_count: 0,
				active_medications: [],
				upcoming_appointments: [],
				recent_lab_results: [],
				health_goals: []
			}
		};
	}
};
