import { allNotes, allKeywords } from '$lib/stores';

export async function load({ fetch }) {
    try {
      const res = await fetch('/api');
  
      if (!res.ok) {
        let errorMessage = '';
        switch (res.status) {
          case 200:
            return { data: await res.json() };
          case 400:
            errorMessage = 'Bad Request: The requested view does not exist.';
            break;
          case 401:
            errorMessage = 'Unauthorized: Could not authenticate the user.';
            break;
          case 403:
            errorMessage = 'Forbidden: You do not have the required permissions.';
            break;
          case 408:
            errorMessage = 'Request Timeout: View processing took too long and was canceled.';
            break;
          default:
            errorMessage = `Error: ${res.status} - ${res.statusText}`;
        }
        throw new Error(errorMessage);
      }
      
    const allData = await res.json();

    if (allData) {
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
    allKeywords.set([])

    return {};
  }
}
  