import { writable } from 'svelte/store';


export const powerMode = writable(false);
export const showTimeline = writable(false);
export const resetOpenDocs = writable(false);
export const destructMode = writable(false);