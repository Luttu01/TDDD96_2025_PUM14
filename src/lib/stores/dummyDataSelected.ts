import { writable, type Writable } from 'svelte/store';

interface Note {
    anamnes: string;
    text: string;
    diagnos: string;
}

export const dummySelectedNotes: Writable<Note[]> = writable([]);


  // dummy data
  export const allTestNotes: Note[] = [
    {
      anamnes: "Patient inkom med bröstsmärtor sedan två timmar tillbaka.",
      text: "AT Vaken, orienterad x3, saturation 98%, BT 135/85 mmHg.",
      diagnos: "Icke-ST-höjningsinfarkt (NSTEMI)?"
    },
    {
      anamnes: "Smärta som trycker och strålar mot käken.",
      text: "Pulm Vesikulära andningsljud bilateralt, ingen rassel.",
      diagnos: "Gastroesofageal reflux?"
    },
    {
      anamnes: "Huvudvärk sedan morgonen, ingen tidigare migränhistoria.",
      text: "Neurologiskt status: Inte påfallande, ingen nackstyvhet.",
      diagnos: "Spänningshuvudvärk"
    },
    {
      anamnes: "Trötthet och andfåddhet vid ansträngning sedan 2 veckor.",
      text: "Hjärta: Regelbunden rytm, inga blåsljud. Buk: Mjuk, icke öm.",
      diagnos: "Anemi?"
    },
    {
      anamnes: "Trötthet och andfåddhet vid ansträngning sedan 2 veckor.",
      text: "Hjärta: Regelbunden rytm, inga blåsljud. Buk: Mjuk, icke öm.",
      diagnos: "Anemi?"
    }
  ];