import type { HealthMetric } from './health-metric';
import type { Medication } from './medication';
import type { LabResult } from './lab-result';
import type { HealthGoal } from './health-goal';

export interface DashboardData {
	latest_vitals: HealthMetric[];
	active_medications_count: number;
	active_medications: Medication[];
	recent_lab_results: LabResult[];
	health_goals: HealthGoal[];
}

export interface VitalsSummary {
	blood_pressure?: {
		systolic: number;
		diastolic: number;
		measured_at: string;
	};
	heart_rate?: {
		value: number;
		measured_at: string;
	};
	weight?: {
		value: number;
		unit: string;
		measured_at: string;
	};
	glucose?: {
		value: number;
		unit: string;
		measured_at: string;
	};
}
