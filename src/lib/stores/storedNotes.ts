import { writable } from 'svelte/store';
import type { Note } from '$lib/models/note';

export const filteredNotes = writable([]);
export const allNotes = writable<Note[]>([]);
export const selectedNotes = writable<Note[]>([]);
export const filter = writable([]);

export const allKeywords = writable<any[]>([]);
export const CaseNoteFilter = writable<any[]>([]);

export const selectedKeywords = writable<string | null>(null);