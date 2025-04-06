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
};

// Add this:
export type EhrNotes = {
  ehrId: string;
  data: Note[];
};