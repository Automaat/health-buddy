export interface LabResultValue {
	id: number;
	lab_result_id: number;
	test_name: string;
	value: string;
	unit: string;
	reference_range?: string;
	is_abnormal: boolean;
	notes?: string;
}

export interface LabResult {
	id: number;
	owner: string;
	test_date: string;
	lab_name?: string;
	ordering_doctor?: string;
	notes?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
	values: LabResultValue[];
}

export interface LabResultValueCreate {
	test_name: string;
	value: string;
	unit: string;
	reference_range?: string;
	is_abnormal?: boolean;
	notes?: string;
}

export interface LabResultCreate {
	owner: string;
	test_date: string;
	lab_name?: string;
	ordering_doctor?: string;
	notes?: string;
	values: LabResultValueCreate[];
}

export interface LabResultUpdate {
	test_date?: string;
	lab_name?: string;
	ordering_doctor?: string;
	notes?: string;
	is_active?: boolean;
}
