import { allNotes } from '$lib/stores';

export async function load({ fetch }) {
  try {
    const res = await fetch('/api');

    if (!res.ok) {
      switch (res.status) {
        case 400:
          throw new Error('Bad Request: The requested view does not exist.');
        case 401:
          throw new Error('Unauthorized: Could not authenticate the user.');
        case 403:
          throw new Error('Forbidden: You do not have the required permissions.');
        case 408:
          throw new Error('Request Timeout: View processing took too long and was canceled.');
        default:
          throw new Error(`Error: ${res.status} - ${res.statusText}`);
      }
    }

    const allData = await res.json();
    allNotes.set(allData);
  } catch (e) {
    console.error('Error loading notes:', e instanceof Error ? e.message : String(e));
    allNotes.set([]);
    return {};
  }
}