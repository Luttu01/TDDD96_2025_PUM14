import { json } from '@sveltejs/kit';
import * as dotenv from 'dotenv';
dotenv.config();

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
  const authHeader = createBasicAuth(process.env.USER as string, process.env.PASS as string);

  const caseNoteListUrl = getCaseNoteListUrl(ehrId);
  const keywordsUrl = getKeywordsUrl(ehrId);
  const caseNoteFilterUrl = getCaseNoteFilterUrl(ehrId);

  try {
    const [notesRes, keywordsRes, filterRes] = await Promise.all([
      fetch(caseNoteListUrl, { method: 'GET', headers: { Authorization: authHeader } }),
      fetch(keywordsUrl, { method: 'GET', headers: { Authorization: authHeader } }),
      fetch(caseNoteFilterUrl, { method: 'GET', headers: { Authorization: authHeader } }),
    ]);

    if (!notesRes.ok) {
      return json({ ehrId, error: `Failed to fetch case note list: ${notesRes.status}` }, { status: notesRes.status });
    }

    const notes = await notesRes.json();
    const keywords = keywordsRes.ok ? await keywordsRes.json() : [];
    const caseNoteFilter = filterRes.ok ? await filterRes.json() : [];

    const enrichedNotes: any[] = [];

    for (const note of notes) {
      const compositionId = note.CompositionId;

      if (!compositionId) {
        enrichedNotes.push({
          ...note,
          CaseData: `<div style="${styleError}">Missing compositionId for EHR ID: ${ehrId}</div>`,
          error: 'Missing compositionId',
        });
        continue;
      }

      const detailUrl = getCaseNoteDetailUrl(ehrId, compositionId);

      try {
        const detailRes = await fetch(detailUrl, {
          method: 'GET',
          headers: { Authorization: authHeader },
        });

        if (!detailRes.ok) {
          if (detailRes.status === 500) {
            // Skip this note entirely on server error
            continue;
          }

          const errorText = `Failed to fetch detail for Composition ID: ${compositionId} - ${detailRes.status} ${detailRes.statusText}`;
          enrichedNotes.push({
            ...note,
            CaseData: `<div style="${styleError}">${errorText}</div>`,
            error: errorText,
          });
          continue;
        }

        const detailData = await detailRes.json();
        const caseData = detailData[0]?.CaseData ?? `<div style="${styleNotFound}">Case data not found</div>`;
        enrichedNotes.push({ ...note, CaseData: caseData });

      } catch (e) {
        const errorMessage = e instanceof Error ? e.message : String(e);
        const errorText = `Error fetching detail for Composition ID: ${compositionId} - ${errorMessage}`;
        enrichedNotes.push({
          ...note,
          CaseData: `<div style="${styleError}">${errorText}</div>`,
          error: errorText,
        });
      }
    }

    return json({ ehrId, notes: enrichedNotes, keywords, caseNoteFilter });
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    return json({ ehrId, error: `Network error: ${errorMessage}` }, { status: 500 });
  }
}