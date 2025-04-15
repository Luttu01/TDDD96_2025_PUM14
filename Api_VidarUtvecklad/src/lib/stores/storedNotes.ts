import type { CaseNoteCollection, Note} from '$lib/models';
import { writable } from 'svelte/store';


export const filteredNotes = writable([]);
export const allNotes = writable<CaseNoteCollection[]>([]);
//export const selectedNotes = writable<{ CaseData: string } | null>(null);
export const selectedNotes = writable<Note | null>(null);
export const filter = writable([]);
