/**
 * This file defines a SvelteKit API endpoint (`GET /api`) that fetches case notes from an EHR (Electronic Health Record) system.
 * For each EHR ID in `ehrIds`, it:
 * 1. Fetches a list of case notes from the `RSK.View.CaseNoteList` endpoint, which provides the CompositionId for each note.
 * 2. For each case note, uses the CompositionId to fetch additional details (`caseData`) from the `RSK.View.CaseNote` endpoint.
 * 3. Combines the case notes and their details into a `CaseNoteCollection` object.
 * 
 * If an error occurs (e.g., network failure, invalid response), the error is captured in the `CaseNoteCollection` or `Note` object.
 * The endpoint returns a JSON array of `CaseNoteCollection` objects, each containing an `ehrId`, a list of `notes`, and an optional `error` field.
 */

import { json } from '@sveltejs/kit';
import { ehrIds } from '$lib/utils';
import type { CaseNoteCollection, Note } from '$lib/models';

// Config for basic authentication
const config = {
  username: 'liu',
  password: 'pum',
};

// Base URL for API endpoints
const BASE_URL = 'https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/';

// Creates a Basic Authentication header
const createBasicAuth = (username: string, password: string): string =>
  'Basic ' + btoa(`${username}:${password}`);

// Builds the URL for fetching the list of case notes for a given EHR ID.
const getCaseNoteListUrl = (ehrId: string): string =>
  `${BASE_URL}${ehrId}/RSK.View.CaseNoteList`;

// Builds the URL for fetching the details of a specific case note.
const getCaseNoteDetailUrl = (ehrId: string, compositionId: string): string =>
  `${BASE_URL}${ehrId}/RSK.View.CaseNote?compId=${compositionId}`;

// Interface for the case note detail API response
interface CaseNoteDetail {
  CaseData?: string; // Made optional to align with the code and Note type
}


export async function GET() {
  const authHeader = createBasicAuth(config.username, config.password);
  const caseNoteCollections: CaseNoteCollection[] = [];

  for (const ehrId of ehrIds) {
    const caseNoteListUrl = getCaseNoteListUrl(ehrId);

    try {
      // Fetch the list of case notes for the EHR ID
      const res = await fetch(caseNoteListUrl, {
        headers: {
          Authorization: authHeader,
        },
      });

      if (!res.ok) {
        caseNoteCollections.push({ ehrId, notes: [], error: `Failed to fetch case note list for EHR ID ${ehrId}: ${res.status}` });
      } else {
        const notes: Note[] = await res.json();

        // Fetch details for all case notes in parallel
        const notesWithDetails = await Promise.all(
          notes.map(async (note: Note) => {
            const compositionId = note.CompositionId;

            if (!compositionId) {
              return { ...note, CaseData: null, error: `No CompositionId provided for note in EHR ID ${ehrId}` };
            }

            const detailUrl = getCaseNoteDetailUrl(ehrId, compositionId);
            const detailRes = await fetch(detailUrl, {
              headers: { Authorization: authHeader },
            });

            if (!detailRes.ok) {
              return {
                ...note,
                CaseData: null,
                error: `Failed to fetch case note details for CompositionId ${compositionId} in EHR ID ${ehrId}: ${detailRes.status} ${detailRes.statusText}`,
              };
            }

            const detailData = await detailRes.json() as CaseNoteDetail[];
            const CaseData = detailData[0]?.CaseData ?? null; 
            return { ...note, CaseData };
          })
        );

        caseNoteCollections.push({ ehrId, notes: notesWithDetails });
      }
    } catch (e) {
      caseNoteCollections.push({
        ehrId,
        notes: [],
        error: `Network error for EHR ID ${ehrId}: ${e instanceof Error ? e.message : String(e)}`,
      });
    }
  }

  return json(caseNoteCollections);
}