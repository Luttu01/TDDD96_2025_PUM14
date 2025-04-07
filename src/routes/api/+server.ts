import { json } from '@sveltejs/kit';

function createBasicAuth(username: string, password: string): string {
  return 'Basic ' + btoa(`${username}:${password}`);
}

const config = {
  username: 'liu',
  password: 'pum',
};

const ehrId = '2b8d6cc8-0e30-439f-aeaa-0b0edfa09127';

export async function GET() {
  const authHeader = createBasicAuth(config.username, config.password);
  const caseNoteListUrl = `https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNoteList`;

  try {
    const res = await fetch(caseNoteListUrl, {
      method: 'GET',
      headers: {
        'Authorization': authHeader,
      },
    });

    if (!res.ok) {
      return json({ ehrId, error: `Failed to fetch case note list: ${res.status}` }, { status: res.status });
    }

    const notes = await res.json();
    const enrichedNotes = [];

    for (const note of notes) {
      const compositionId = note.compositionId;

      if (!compositionId) {
        enrichedNotes.push({ ...note, CaseData: null, error: 'Missing compositionId' });
        continue;
      }

      const detailUrl = `https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNote?compositionId=${compositionId}`;

      try {
        const detailRes = await fetch(detailUrl, {
          method: 'GET',
          headers: {
            'Authorization': authHeader,
          },
        });

        if (!detailRes.ok) {
          enrichedNotes.push({ ...note, CaseData: null, error: `Detail fetch failed: ${detailRes.status}` });
          continue;
        }

        const detailData = await detailRes.json();
        const caseData = detailData?.CaseData ?? null;

        enrichedNotes.push({ ...note, CaseData: caseData });

      } catch (e) {
        const errorMessage = e instanceof Error ? e.message : String(e);
        enrichedNotes.push({ ...note, CaseData: null, error: `Error fetching detail: ${errorMessage}` });
      }
    }

    return json({ ehrId, notes: enrichedNotes });

  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    return json({ ehrId, error: `Network error: ${errorMessage}` }, { status: 500 });
  }
}
