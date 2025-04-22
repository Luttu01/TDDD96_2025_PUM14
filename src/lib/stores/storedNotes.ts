import { writable } from 'svelte/store';
import type { Note } from '$lib/models/note';

export const filteredNotes = writable<Note[]>([]);
export const allNotes = writable<Note[]>([]);
export const selectedNotes = writable<Note[]>([]);
export const filter = writable<Map<string, Set<string>>>(new Map<string, Set<string>>());

//export const allKeywords = writable<any[]>([]);
export const CaseNoteFilter = writable<any[]>([]);

//export const selectedKeywords = writable<string | null>(null);