/**
 * This file is responsible for loading data from the backend API and updating the Svelte stores (`allNotes` and `allKeywords`) 
 * with the retrieved case notes and associated keywords.
 * 
 * The `load` function is called to fetch data from the `/api` endpoint. The response is then checked:
 * - If the request is successful (`res.ok`), the `notes` data is extracted from the response and stored in the Svelte store (`allNotes`).
 *   Additionally, the `keywords` data is extracted and stored in the Svelte store (`allKeywords`).
 * - If the request fails or returns an error status, a descriptive error message is thrown based on the status code.
 * - If the response data doesn't contain valid notes or keywords, or if there's an error in processing, the respective stores 
 *   are cleared (set to empty arrays).
 * 
 * The error handling provides detailed messages for common HTTP errors (e.g., 400, 401, 403, 408), and the front-end 
 * can display these error messages accordingly.
 */

import { allNotes, allKeywords } from '$lib/stores';

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

    const allData = await res.json();

    if (Array.isArray(allData?.notes)) {
      allNotes.set(allData.notes);
    } else {
      allNotes.set([]);
    }

    if (Array.isArray(allData?.keywords)) {
      allKeywords.set(allData.keywords);
    } else {
      allKeywords.set([]);
    }

    return {};

  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : String(e);

    console.error('Error loading data:', errorMessage);

    allNotes.set([]);
    allKeywords.set([]);

    return { error: errorMessage };
  }
}
