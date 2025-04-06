// Import necessary utilities
import { json } from '@sveltejs/kit';
import { ehrIds } from '$lib/utils';  
import { allNotes } from '$lib/models'; // Import the store you want to use

// Helper to create Basic Auth header
function createBasicAuth(username: string, password: string): string {
  return 'Basic ' + btoa(`${username}:${password}`);
}

// Configuration for API request
const config = {
  username: 'liu',
  password: 'pum',
};

export async function GET() {
  const authHeader = createBasicAuth(config.username, config.password);

  // Array to hold the data from all ehrIds
  const allData = [];

  // Loop through all ehrIds and fetch data for each one
  for (const ehrId of ehrIds) {
    const apiUrl = `https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNoteList`;

    //const response = await fetch(`https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNote?compId=${compositionId}`);

    

    try {
      // Make the API request for each ehrId
      const res = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Authorization': authHeader,
        },
      });

      // For debugging
      console.debug('Fetch status:', res.status, res.statusText);

      // Handle the response
      if (!res.ok) {
        console.error(`Fetch failed for ehrId: ${ehrId} with status:`, res.status);
        allData.push({ ehrId, error: `API request failed with status: ${res.status}` });
        continue;  
      }


      let data;
      try {
        // Attempt to parse the JSON response
        data = await res.json();  
      } catch (jsonError) {
        // If parsing fails, handle the error and push an error message to allData
        console.error('Failed to parse JSON for ehrId:', ehrId, jsonError);
        allData.push({ ehrId, error: 'Failed to parse response data' });
        continue;  
      }

      // Check if the data is empty
      if (!data || data.length === 0) {
        allData.push({ ehrId, error: 'No data found for this ehrId' });
      } else {
        // If parsing was successful and data is not empty, add the data to the allData array
        allData.push({ ehrId, data });
      }

    } catch (e: unknown) {
      console.error(`Fetch error for ehrId: ${ehrId}`, e);

      // Type check for error
      const errorMessage = e instanceof Error ? e.message : String(e);
      allData.push({ ehrId, error: `Network error: ${errorMessage}` });
    }
  }

  // Return the collected data for all ehrIds
  return json(allData);
}
