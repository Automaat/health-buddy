import { z } from 'zod';

export const healthMetricSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	metric_type: z.string().min(1, 'Metric type is required'),
	value: z.number().min(0, 'Value must be positive'),
	unit: z.string().min(1, 'Unit is required'),
	measured_at: z.string().min(1, 'Measurement date is required'),
	notes: z.string().optional()
});

export const medicationSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	name: z.string().min(1, 'Medication name is required'),
	dosage: z.string().min(1, 'Dosage is required'),
	unit: z.string().min(1, 'Unit is required'),
	frequency: z.string().min(1, 'Frequency is required'),
	purpose: z.string().optional(),
	start_date: z.string().min(1, 'Start date is required'),
	end_date: z.string().optional(),
	prescribing_doctor: z.string().optional(),
	refill_reminder_date: z.string().optional()
});

export const supplementSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	name: z.string().min(1, 'Supplement name is required'),
	dosage: z.string().min(1, 'Dosage is required'),
	unit: z.string().min(1, 'Unit is required'),
	frequency: z.string().min(1, 'Frequency is required'),
	purpose: z.string().optional(),
	start_date: z.string().min(1, 'Start date is required'),
	end_date: z.string().optional(),
	brand: z.string().optional()
});

export const labResultSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	test_date: z.string().min(1, 'Test date is required'),
	lab_name: z.string().optional(),
	ordering_doctor: z.string().optional(),
	notes: z.string().optional(),
	values: z.array(
		z.object({
			test_name: z.string().min(1, 'Test name is required'),
			value: z.string().min(1, 'Value is required'),
			unit: z.string().min(1, 'Unit is required'),
			reference_range: z.string().optional(),
			is_abnormal: z.boolean().optional(),
			notes: z.string().optional()
		})
	).min(1, 'At least one test value is required')
});

export const appointmentSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	doctor_name: z.string().min(1, 'Doctor name is required'),
	specialty: z.string().optional(),
	appointment_date: z.string().min(1, 'Appointment date is required'),
	purpose: z.string().optional(),
	location: z.string().optional(),
	notes: z.string().optional(),
	follow_up_required: z.boolean().optional()
});

export const symptomSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	symptom_type: z.string().min(1, 'Symptom type is required'),
	severity: z.number().min(1).max(10, 'Severity must be between 1 and 10'),
	occurred_at: z.string().min(1, 'Occurrence date is required'),
	duration_minutes: z.number().min(0).optional(),
	notes: z.string().optional(),
	related_condition_id: z.number().optional()
});

export const healthGoalSchema = z.object({
	owner: z.string().min(1, 'Owner is required'),
	name: z.string().min(1, 'Goal name is required'),
	goal_type: z.string().min(1, 'Goal type is required'),
	target_value: z.number().min(0, 'Target value must be positive'),
	target_unit: z.string().min(1, 'Target unit is required'),
	target_date: z.string().optional(),
	current_value: z.number().optional(),
	start_value: z.number().optional()
});
