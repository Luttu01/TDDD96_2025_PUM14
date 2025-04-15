export type Note = {
  CompositionId: string;
  DateTime: string;
  DisplayDateTime: string;
  Dokument_ID: string;
  Dokument_skapad_av_yrkestitel_ID: string;
  Dokument_skapad_av_yrkestitel_Namn: string;
  Dokumentationskod: string;
  Dokumentnamn: string;
  Tidsstämpel_för_sparat_dokument: string;
  Vårdenhet_Identifierare: string;
  Vårdenhet_Namn: string;
  CaseData?: string | null | undefined 
  error?: string;
};

export type CaseNoteCollection = {
  ehrId: string;
  notes: Note[];
  error?: string;
};