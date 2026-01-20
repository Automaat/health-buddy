export interface Symptom {
	id: number;
	owner: string;
	symptom_type: string;
	severity: number;
	occurred_at: string;
	duration_minutes?: number;
	notes?: string;
	related_condition_id?: number;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface SymptomCreate {
	owner: string;
	symptom_type: string;
	severity: number;
	occurred_at: string;
	duration_minutes?: number;
	notes?: string;
	related_condition_id?: number;
}

export interface SymptomUpdate {
	symptom_type?: string;
	severity?: number;
	occurred_at?: string;
	duration_minutes?: number;
	notes?: string;
	related_condition_id?: number;
	is_active?: boolean;
}
