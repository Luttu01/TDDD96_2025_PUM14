import { writable } from 'svelte/store';

export const filteredNotes = writable([]);
export const allNotes = writable([]);
export const selectedNotes = writable([]);
export const filter = writable([]);