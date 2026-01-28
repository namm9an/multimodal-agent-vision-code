/**
 * Basic tests to verify vitest is working.
 */

import { describe, it, expect } from 'vitest';

describe('Basic tests', () => {
    it('performs arithmetic correctly', () => {
        expect(1 + 1).toBe(2);
        expect(10 - 5).toBe(5);
        expect(2 * 3).toBe(6);
    });

    it('handles string operations', () => {
        const greeting = 'Hello, World!';
        expect(greeting).toContain('Hello');
        expect(greeting.length).toBe(13);
    });

    it('handles array operations', () => {
        const items = ['a', 'b', 'c'];
        expect(items).toHaveLength(3);
        expect(items).toContain('b');
    });

    it('handles object matching', () => {
        const user = { name: 'Test', id: 123 };
        expect(user).toHaveProperty('name');
        expect(user.name).toBe('Test');
    });
});

describe('Async tests', () => {
    it('handles promises', async () => {
        const result = await Promise.resolve(42);
        expect(result).toBe(42);
    });
});
