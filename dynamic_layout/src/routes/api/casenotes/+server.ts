import { json } from '@sveltejs/kit';

export async function GET() {
  const ehrId = "d5da0dca-e915-4e55-bc0c-02e06eb0a92b"; // Ersätt med dynamiskt värde vid behov
  const username = 'liu';  // Ditt användarnamn
  const password = 'pum';  // Ditt lösenord

  // Base64-koda användarnamn och lösenord för Basic Authentication
  const authHeader = 'Basic ' + btoa(`${username}:${password}`);

  const url = `https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNoteList`;

  try {
    // Optionally, Log the URL for debugging purposes
    //console.debug('Calling API URL:', url);

    // Send request with Authorization header
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': authHeader,
      },
    });

    // Log response status for debugging
    console.debug('Fetch status:', res.status);
    console.debug('Fetch statusText:', res.statusText);

    if (!res.ok) {
      console.error('Fetch failed with status:', res.status);
      throw new Error('Failed to fetch case notes');
    }

    let data;
    try {
      // Attempt to parse the JSON response
      data = await res.json();
    } catch (jsonError) {
      console.error('Failed to parse JSON:', jsonError);
      return json({ error: 'Failed to parse response data' }, { status: 500 });
    }

    return json(data); // Return the fetched data
  } catch (e) {
    console.error('Fetch error:', e);
    return json({ error: 'Could not fetch case notes' }, { status: 500 });
  }
}