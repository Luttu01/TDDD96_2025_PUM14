import { writable } from 'svelte/store';
import type { Note } from '$lib/models/note';

export const filteredNotes = writable([]);
export const allNotes = writable<Note[]>([]);
export const selectedNotes = writable<Note[]>([]);
export const filter = writable([]);