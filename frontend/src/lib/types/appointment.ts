export interface Appointment {
	id: number;
	owner: string;
	doctor_name: string;
	specialty?: string;
	appointment_date: string;
	purpose?: string;
	location?: string;
	notes?: string;
	follow_up_required: boolean;
	is_completed: boolean;
	created_at: string;
	updated_at: string;
}

export interface AppointmentCreate {
	owner: string;
	doctor_name: string;
	specialty?: string;
	appointment_date: string;
	purpose?: string;
	location?: string;
	notes?: string;
	follow_up_required?: boolean;
}

export interface AppointmentUpdate {
	doctor_name?: string;
	specialty?: string;
	appointment_date?: string;
	purpose?: string;
	location?: string;
	notes?: string;
	follow_up_required?: boolean;
	is_completed?: boolean;
}
