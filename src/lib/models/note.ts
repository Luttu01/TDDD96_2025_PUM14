export interface Document {
    id: number;
    patient_id: number;
    title: string;
    type: string;
    category: string;
    unit: string;
    professional: string;
    date: string;
    abstract: string;
    content: string;
    [key: string]: string | number;  // Index signature for dynamic access
} 

export type Note = {
  CompositionId: string;
  CaseData: string;
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
