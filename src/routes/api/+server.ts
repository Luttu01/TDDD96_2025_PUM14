import { json } from '@sveltejs/kit';
import { ehrIds } from '$lib/utils';  

function createBasicAuth(username: string, password: string): string {
  return 'Basic ' + btoa(`${username}:${password}`);
}

const config = {
  username: 'liu',
  password: 'pum',
};

export async function GET() {
  const authHeader = createBasicAuth(config.username, config.password);

  const allData = [];

  for (const ehrId of ehrIds) {
    const apiUrl = `https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNoteList`;

    try {
      const res = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Authorization': authHeader,
        },
      });

      console.debug('Fetch status:', res.status, res.statusText);

      if (!res.ok) {
        console.error(`Fetch failed for ehrId: ${ehrId} with status:`, res.status);
        allData.push({ ehrId, error: `API request failed with status: ${res.status}` });
        continue;  
      }

      let data;
      try {
        data = await res.json();  
      } catch (jsonError) {
        console.error('Failed to parse JSON for ehrId:', ehrId, jsonError);
        allData.push({ ehrId, error: 'Failed to parse response data' });
        continue;  
      }

      if (!data || data.length === 0) {
        allData.push({ ehrId, error: 'No data found for this ehrId' });
      } else {
        allData.push({ ehrId, data });
      }

    } catch (e: unknown) {
      console.error(`Fetch error for ehrId: ${ehrId}`, e);

      const errorMessage = e instanceof Error ? e.message : String(e);
      allData.push({ ehrId, error: `Network error: ${errorMessage}` });
    }
  }

  return json(allData);
}
