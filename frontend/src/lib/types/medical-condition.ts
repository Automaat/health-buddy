export interface MedicalCondition {
	id: number;
	owner: string;
	name: string;
	condition_type?: string;
	diagnosis_date?: string;
	diagnosed_by?: string;
	status: string;
	severity?: string;
	notes?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface MedicalConditionCreate {
	owner: string;
	name: string;
	condition_type?: string;
	diagnosis_date?: string;
	diagnosed_by?: string;
	status?: string;
	severity?: string;
	notes?: string;
}

export interface MedicalConditionUpdate {
	name?: string;
	condition_type?: string;
	diagnosis_date?: string;
	diagnosed_by?: string;
	status?: string;
	severity?: string;
	notes?: string;
	is_active?: boolean;
}
