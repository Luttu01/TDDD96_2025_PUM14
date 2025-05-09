import { writable } from 'svelte/store';

export const searchQuery = writable('');
export const allKeywords = writable<{ Id: string; Name: string; CompositionId: string }[]>([]);
export const selectedKeywords = writable<Set<string>>(new Set<string>());