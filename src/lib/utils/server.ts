import { json } from '@sveltejs/kit';

// Helper to create Basic Auth header
function createBasicAuth(username: string, password: string): string {
  return 'Basic ' + btoa(`${username}:${password}`);
}

// Configuration for url
const config = {
  ehrId: "d5da0dca-e915-4e55-bc0c-02e06eb0a92b", // Replace with dynamic value if needed
  username: 'liu',
  password: 'pum',
};

export async function GET() {
  const authHeader = createBasicAuth(config.username, config.password);

  // Api-url
  const apiUrl = `https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${config.ehrId}/RSK.View.CaseNoteList`;

  try {
    const res = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Authorization': authHeader,
      },
    });

    // For debugging 
    console.debug('Fetch status:', res.status, res.statusText);

    if (!res.ok) {
      console.error('Fetch failed with status:', res.status);
      return json(
        { error: 'API request failed', status: res.status, message: res.statusText },
        { status: res.status }
      );
    }

    let data;
    try {
      data = await res.json();
    } catch (jsonError) {
      console.error('Failed to parse JSON:', jsonError);
      return json({ error: 'Failed to parse response data' }, { status: 500 });
    }

    return json(data);
  } catch (e: unknown) {
    console.error('Fetch error:', e);

    // Type check
    const errorMessage = e instanceof Error ? e.message : String(e);

    return json({ error: 'Network error', details: errorMessage }, { status: 500 });
  }
}