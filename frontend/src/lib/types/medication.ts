export interface Medication {
	id: number;
	owner: string;
	name: string;
	dosage: string;
	unit: string;
	frequency: string;
	purpose?: string;
	start_date: string;
	end_date?: string;
	prescribing_doctor?: string;
	refill_reminder_date?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface MedicationCreate {
	owner: string;
	name: string;
	dosage: string;
	unit: string;
	frequency: string;
	purpose?: string;
	start_date: string;
	end_date?: string;
	prescribing_doctor?: string;
	refill_reminder_date?: string;
}

export interface MedicationUpdate {
	name?: string;
	dosage?: string;
	unit?: string;
	frequency?: string;
	purpose?: string;
	start_date?: string;
	end_date?: string;
	prescribing_doctor?: string;
	refill_reminder_date?: string;
	is_active?: boolean;
}
