import { writable } from 'svelte/store';
import type { EhrNotes } from '../models';

export const filteredNotes = writable([]);
export const allNotes = writable<EhrNotes[]>([]);
export const selectedNotes = writable<{ CaseData: string } | null>(null);
export const filter = writable([]);