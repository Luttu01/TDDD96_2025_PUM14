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

const getKeywordsUrl = (ehrId: string): string =>
  `${BASE_URL}${ehrId}/RSK.View.Keywords`;

const getCaseNoteFilterUrl = (ehrId: string): string =>
  `${BASE_URL}${ehrId}/RSK.View.CaseNoteFilter`;

const styleError = 'color: red; font-style: italic;';
const styleNotFound = 'text-indent:10px; margin-bottom:10px;';

const ehrId = "2b8d6cc8-0e30-439f-aeaa-0b0edfa09127";

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

    // Hämta nyckelord separat
    const keywordsUrl = getKeywordsUrl(ehrId);
    let keywords: any[] = [];
    try {
      const keywordsRes = await fetch(keywordsUrl, {
        method: 'GET',
        headers: {
          Authorization: authHeader,
        },
      });

      if (keywordsRes.ok) {
        keywords = await keywordsRes.json();
      }
    } catch (e) {
      console.error('Error fetching keywords:', e);
      keywords = [];
    }

    // Hämta CaseNoteFilter
    const caseNoteFilterUrl = getCaseNoteFilterUrl(ehrId);
    let caseNoteFilter: any[] = [];
    try {
      const filterRes = await fetch(caseNoteFilterUrl, {
        method: 'GET',
        headers: {
          Authorization: authHeader,
        },
      });

      if (filterRes.ok) {
        caseNoteFilter = await filterRes.json();
      }
    } catch (e) {
      console.error('Error fetching CaseNoteFilter:', e);
      caseNoteFilter = [];
    }

    const enrichedNotes = await Promise.all(
      notes.map(async (note: any) => {
        const compositionId = note.CompositionId;

        if (!compositionId) {
          return {
            ...note,
            CaseData: `<div style="${styleError}">Missing compositionId for EHR ID: ${ehrId}</div>`,
            error: 'Missing compositionId',
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
            `<div style="${styleNotFound}">Case data not found in successful response for EHR ID: ${ehrId}, Composition ID: ${compositionId}</div>`;

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

    return json({ ehrId, notes: enrichedNotes, keywords, caseNoteFilter });
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    return json({ ehrId, error: `Network error: ${errorMessage}` }, { status: 500 });
  }
}
