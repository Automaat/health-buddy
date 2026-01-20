import { describe, it, expect } from 'vitest';
import {
	formatDate,
	formatDateTime,
	formatMetricValue,
	formatBloodPressure,
	calculateBMI,
	formatGoalProgress
} from './format';

describe('format utilities', () => {
	describe('formatDate', () => {
		it('formats date correctly', () => {
			const result = formatDate('2024-01-15T10:30:00');
			expect(result).toBe('Jan 15, 2024');
		});
	});

	describe('formatDateTime', () => {
		it('formats datetime correctly', () => {
			const result = formatDateTime('2024-01-15T10:30:00');
			expect(result).toContain('Jan 15, 2024');
			expect(result).toContain('10:30');
		});
	});

	describe('formatMetricValue', () => {
		it('formats number with 1 decimal place', () => {
			expect(formatMetricValue(123.456, 'kg')).toBe('123.5 kg');
		});

		it('formats integer correctly', () => {
			expect(formatMetricValue(100, 'bpm')).toBe('100.0 bpm');
		});
	});

	describe('formatBloodPressure', () => {
		it('formats blood pressure correctly', () => {
			expect(formatBloodPressure(120, 80)).toBe('120/80 mmHg');
		});
	});

	describe('calculateBMI', () => {
		it('calculates BMI correctly', () => {
			const bmi = calculateBMI(70, 175);
			expect(bmi).toBeCloseTo(22.86, 2);
		});
	});

	describe('formatGoalProgress', () => {
		it('calculates progress correctly', () => {
			expect(formatGoalProgress(75, 80, 70)).toBe('50%');
		});

		it('handles completed goal', () => {
			expect(formatGoalProgress(80, 80, 70)).toBe('100%');
		});

		it('handles zero change target', () => {
			expect(formatGoalProgress(70, 70, 70)).toBe('100%');
		});
	});
});
