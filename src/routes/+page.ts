import { allNotes, allKeywords, CaseNoteFilter } from '$lib/stores';

export async function load({ fetch }) {
  try {
    const res = await fetch('/api');

    if (!res.ok) {
      const errorMessages: Record<number, string> = {
        400: 'Bad Request: The requested view does not exist.',
        401: 'Unauthorized: Could not authenticate the user.',
        403: 'Forbidden: You do not have the required permissions.',
        408: 'Request Timeout: View processing took too long and was canceled.',
      };

      const errorMessage = errorMessages[res.status] || `Error: ${res.status} - ${res.statusText}`;
      throw new Error(errorMessage);
    }

    const { notes = [], keywords = [], caseNoteFilter = [] } = await res.json();

    allNotes.set(notes);
    allKeywords.set(keywords);
    CaseNoteFilter.set(caseNoteFilter);

    return {};
  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : String(e);

    console.error('Error loading data:', errorMessage);

    allNotes.set([]);
    allKeywords.set([]);
    CaseNoteFilter.set([]);

    return { error: errorMessage };
  }
}