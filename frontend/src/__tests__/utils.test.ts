/**
 * Tests for utility functions.
 */

import { describe, it, expect } from 'vitest';
import { cn } from '../lib/utils';

describe('cn utility', () => {
    it('merges class names correctly', () => {
        const result = cn('base-class', 'additional-class');
        expect(result).toContain('base-class');
        expect(result).toContain('additional-class');
    });

    it('handles conditional classes', () => {
        const isActive = true;
        const result = cn('base', isActive && 'active');
        expect(result).toContain('base');
        expect(result).toContain('active');
    });

    it('filters out falsy values', () => {
        const result = cn('base', false, null, undefined, 'valid');
        expect(result).not.toContain('false');
        expect(result).not.toContain('null');
        expect(result).not.toContain('undefined');
        expect(result).toContain('base');
        expect(result).toContain('valid');
    });

    it('merges Tailwind classes correctly', () => {
        // Test that tailwind-merge works (removes duplicate utilities)
        const result = cn('px-2 py-1', 'px-4');
        expect(result).toContain('px-4');
        expect(result).toContain('py-1');
    });
});

describe('Basic test', () => {
    it('works correctly', () => {
        expect(1 + 1).toBe(2);
    });
});
