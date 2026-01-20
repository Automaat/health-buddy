// Health Metric Types
export const METRIC_TYPES = {
	BLOOD_PRESSURE_SYSTOLIC: 'blood_pressure_systolic',
	BLOOD_PRESSURE_DIASTOLIC: 'blood_pressure_diastolic',
	HEART_RATE: 'heart_rate',
	WEIGHT: 'weight',
	BMI: 'bmi',
	GLUCOSE: 'glucose',
	SPO2: 'spo2',
	TEMPERATURE: 'temperature',
	SLEEP_HOURS: 'sleep_hours',
	STEPS: 'steps',
	HRV: 'hrv'
} as const;

export const METRIC_TYPE_LABELS: Record<string, string> = {
	[METRIC_TYPES.BLOOD_PRESSURE_SYSTOLIC]: 'Blood Pressure (Systolic)',
	[METRIC_TYPES.BLOOD_PRESSURE_DIASTOLIC]: 'Blood Pressure (Diastolic)',
	[METRIC_TYPES.HEART_RATE]: 'Heart Rate',
	[METRIC_TYPES.WEIGHT]: 'Weight',
	[METRIC_TYPES.BMI]: 'BMI',
	[METRIC_TYPES.GLUCOSE]: 'Blood Glucose',
	[METRIC_TYPES.SPO2]: 'SpO2',
	[METRIC_TYPES.TEMPERATURE]: 'Temperature',
	[METRIC_TYPES.SLEEP_HOURS]: 'Sleep Hours',
	[METRIC_TYPES.STEPS]: 'Steps',
	[METRIC_TYPES.HRV]: 'Heart Rate Variability'
};

// Units
export const UNITS = {
	MMHG: 'mmHg',
	BPM: 'bpm',
	KG: 'kg',
	LBS: 'lbs',
	MG_DL: 'mg/dL',
	MMOL_L: 'mmol/L',
	PERCENT: '%',
	CELSIUS: '°C',
	FAHRENHEIT: '°F',
	HOURS: 'hours',
	COUNT: 'count',
	MS: 'ms'
} as const;

// Lab Test Types
export const LAB_TEST_TYPES = {
	// Lipid Panel
	TOTAL_CHOLESTEROL: 'Total Cholesterol',
	LDL: 'LDL Cholesterol',
	HDL: 'HDL Cholesterol',
	TRIGLYCERIDES: 'Triglycerides',
	// Glucose Tests
	FASTING_GLUCOSE: 'Fasting Glucose',
	HBA1C: 'HbA1c',
	// Kidney Function
	CREATININE: 'Creatinine',
	EGFR: 'eGFR',
	BUN: 'BUN',
	// Liver Function
	ALT: 'ALT',
	AST: 'AST',
	ALKALINE_PHOSPHATASE: 'Alkaline Phosphatase',
	BILIRUBIN: 'Bilirubin',
	// Complete Blood Count
	WBC: 'White Blood Cells',
	RBC: 'Red Blood Cells',
	HEMOGLOBIN: 'Hemoglobin',
	HEMATOCRIT: 'Hematocrit',
	PLATELETS: 'Platelets',
	// Vitamins
	VITAMIN_D: 'Vitamin D',
	VITAMIN_B12: 'Vitamin B12',
	FOLATE: 'Folate',
	// Thyroid
	TSH: 'TSH',
	T3: 'T3',
	T4: 'T4'
} as const;

// Condition Types
export const CONDITION_TYPES = {
	CHRONIC: 'chronic',
	ACUTE: 'acute',
	HEREDITARY: 'hereditary',
	INFECTIOUS: 'infectious',
	AUTOIMMUNE: 'autoimmune',
	MENTAL_HEALTH: 'mental_health'
} as const;

export const CONDITION_TYPE_LABELS: Record<string, string> = {
	[CONDITION_TYPES.CHRONIC]: 'Chronic',
	[CONDITION_TYPES.ACUTE]: 'Acute',
	[CONDITION_TYPES.HEREDITARY]: 'Hereditary',
	[CONDITION_TYPES.INFECTIOUS]: 'Infectious',
	[CONDITION_TYPES.AUTOIMMUNE]: 'Autoimmune',
	[CONDITION_TYPES.MENTAL_HEALTH]: 'Mental Health'
};

// Condition Status
export const CONDITION_STATUS = {
	ACTIVE: 'active',
	RESOLVED: 'resolved',
	MANAGED: 'managed',
	MONITORING: 'monitoring'
} as const;

// Severity Levels
export const SEVERITY_LEVELS = {
	MILD: 'mild',
	MODERATE: 'moderate',
	SEVERE: 'severe',
	CRITICAL: 'critical'
} as const;

export const SEVERITY_LABELS: Record<string, string> = {
	[SEVERITY_LEVELS.MILD]: 'Mild',
	[SEVERITY_LEVELS.MODERATE]: 'Moderate',
	[SEVERITY_LEVELS.SEVERE]: 'Severe',
	[SEVERITY_LEVELS.CRITICAL]: 'Critical'
};

// Symptom Types
export const SYMPTOM_TYPES = [
	'Headache',
	'Fever',
	'Cough',
	'Fatigue',
	'Nausea',
	'Dizziness',
	'Pain',
	'Shortness of Breath',
	'Chest Pain',
	'Abdominal Pain',
	'Joint Pain',
	'Muscle Ache',
	'Rash',
	'Insomnia',
	'Anxiety',
	'Depression',
	'Other'
] as const;

// Medical History Event Types
export const EVENT_TYPES = {
	SURGERY: 'surgery',
	HOSPITALIZATION: 'hospitalization',
	INJURY: 'injury',
	FAMILY_HISTORY: 'family_history',
	PROCEDURE: 'procedure'
} as const;

export const EVENT_TYPE_LABELS: Record<string, string> = {
	[EVENT_TYPES.SURGERY]: 'Surgery',
	[EVENT_TYPES.HOSPITALIZATION]: 'Hospitalization',
	[EVENT_TYPES.INJURY]: 'Injury',
	[EVENT_TYPES.FAMILY_HISTORY]: 'Family History',
	[EVENT_TYPES.PROCEDURE]: 'Procedure'
};

// Medication Frequency
export const MEDICATION_FREQUENCIES = [
	'Once daily',
	'Twice daily',
	'Three times daily',
	'Four times daily',
	'Every 4 hours',
	'Every 6 hours',
	'Every 8 hours',
	'Every 12 hours',
	'As needed',
	'Weekly',
	'Monthly',
	'Other'
] as const;

// Goal Types
export const GOAL_TYPES = {
	WEIGHT: 'weight',
	BLOOD_PRESSURE: 'blood_pressure',
	CHOLESTEROL: 'cholesterol',
	GLUCOSE: 'glucose',
	FITNESS: 'fitness',
	SLEEP: 'sleep',
	STEPS: 'steps',
	OTHER: 'other'
} as const;

export const GOAL_TYPE_LABELS: Record<string, string> = {
	[GOAL_TYPES.WEIGHT]: 'Weight',
	[GOAL_TYPES.BLOOD_PRESSURE]: 'Blood Pressure',
	[GOAL_TYPES.CHOLESTEROL]: 'Cholesterol',
	[GOAL_TYPES.GLUCOSE]: 'Blood Glucose',
	[GOAL_TYPES.FITNESS]: 'Fitness',
	[GOAL_TYPES.SLEEP]: 'Sleep',
	[GOAL_TYPES.STEPS]: 'Steps',
	[GOAL_TYPES.OTHER]: 'Other'
};

// Medical Specialties
export const MEDICAL_SPECIALTIES = [
	'General Practice',
	'Cardiology',
	'Dermatology',
	'Endocrinology',
	'Gastroenterology',
	'Neurology',
	'Oncology',
	'Orthopedics',
	'Pediatrics',
	'Psychiatry',
	'Pulmonology',
	'Rheumatology',
	'Urology',
	'Ophthalmology',
	'ENT',
	'Dentistry',
	'Physical Therapy',
	'Other'
] as const;

// Allergy Reaction Types
export const REACTION_TYPES = [
	'Anaphylaxis',
	'Hives',
	'Rash',
	'Itching',
	'Swelling',
	'Respiratory',
	'Gastrointestinal',
	'Other'
] as const;

// API Base URL
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
