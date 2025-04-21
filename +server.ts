/**
 * This file defines an API endpoint for fetching case notes and their details 
 * for a given EHR (Electronic Health Record) ID. It performs the following steps:
 * 
 * 1. Retrieves a list of case notes associated with the provided `ehrId` by making a GET request to an API.
 * 2. For each case note, it attempts to fetch detailed information using the composition ID from the case note.
 * 3. If any error occurs at any point (e.g., missing composition ID, failed fetch request, or missing case data), 
 *    appropriate error messages are added to the response with specific styles for visual distinction.
 * 4. The response contains either the enriched case notes (with data or error messages) or a network error if something 
 *    fails during the process.
 * 
 * The file uses basic authentication for API access and employs HTML styles to show error messages in the response.
 */

import { json } from '@sveltejs/kit';

const config = {
  username: 'liu',
  password: 'pum',
};

const BASE_URL = 'https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/';

const createBasicAuth = (username: string, password: string): string =>
  'Basic ' + btoa(`${username}:${password}`);

const getCaseNoteListUrl = (ehrId: string): string =>
  `${BASE_URL}${ehrId}/RSK.View.CaseNoteList`;

const getCaseNoteDetailUrl = (ehrId: string, compositionId: string): string =>
  `${BASE_URL}${ehrId}/RSK.View.CaseNote?compId=${compositionId}`;

const styleError = 'color: red; font-style: italic;'; 
const styleNotFound = 'text-indent:10px; margin-bottom:10px;'; 

const ehrId = "2b8d6cc8-0e30-439f-aeaa-0b0edfa09127";
//const ehrId ="d5da0dca-e915-4e55-bc0c-02e06eb0a92b"

export async function GET() {
  const authHeader = createBasicAuth(config.username, config.password);
  const caseNoteListUrl = getCaseNoteListUrl(ehrId);

  try {
    const res = await fetch(caseNoteListUrl, {
      method: 'GET',
      headers: {
        Authorization: authHeader,
      },
    });

    if (!res.ok) {
      return json({ ehrId, error: `Failed to fetch case note list: ${res.status}` }, { status: res.status });
    }

    const notes = await res.json();

    const enrichedNotes = await Promise.all(
      notes.map(async (note: any) => {
        const compositionId = note.CompositionId;

        if (!compositionId) {
          return { 
            ...note, 
            CaseData: `<div style="${styleError}">Missing compositionId for EHR ID: ${ehrId}</div>`, 
            error: 'Missing compositionId' 
          };
        }

        const detailUrl = getCaseNoteDetailUrl(ehrId, compositionId);

        try {
          const detailRes = await fetch(detailUrl, {
            method: 'GET',
            headers: {
              Authorization: authHeader,
            },
          });

          if (!detailRes.ok) {
            const errorText = `Failed to fetch detail for EHR ID: ${ehrId}, Composition ID: ${compositionId} - ${detailRes.status} ${detailRes.statusText}`;
            return {
              ...note,
              CaseData: `<div style="${styleError}">${errorText}</div>`, 
              error: errorText,
            };
          }

          const detailData = await detailRes.json();
          const caseData: string =
            detailData[0]?.CaseData ??
            `<div style="${styleNotFound}">Case data not found in successful response for EHR ID: ${ehrId}, Composition ID: ${compositionId}</div>`; // <-- updated

          return { ...note, CaseData: caseData };
        } catch (e) {
          const errorMessage = e instanceof Error ? e.message : String(e);
          const errorText = `Error fetching detail for EHR ID: ${ehrId}, Composition ID: ${compositionId} - ${errorMessage}`;
          return {
            ...note,
            CaseData: `<div style="${styleError}">${errorText}</div>`, 
            error: errorText,
          };
        }
      })
    );

    return json({ ehrId, notes: enrichedNotes });
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    return json({ ehrId, error: `Network error: ${errorMessage}` }, { status: 500 });
  }
}
