import type { Note } from "../models/note";

// Create mock journal data with minimal content for better performance
export const mockJournals: Note[] = [
    {
        CompositionId: "1",
        DateTime: "2024-03-15",
        DisplayDateTime: "2024-03-15 09:30",
        Dokument_ID: "DOC1001",
        Dokument_skapad_av_yrkestitel_ID: "12345",
        Dokument_skapad_av_yrkestitel_Namn: "Dr. Anna Andersson",
        Dokumentationskod: "Journal",
        Dokumentnamn: "Yearly Health Checkup",
        Tidsstämpel_för_sparat_dokument: "2024-03-15T09:30:00",
        Vårdenhet_Identifierare: "PCU001",
        Vårdenhet_Namn: "Primary Care Unit"
    },
    {
        CompositionId: "2",
        DateTime: "2024-02-10",
        DisplayDateTime: "2024-02-10 14:15",
        Dokument_ID: "DOC1002",
        Dokument_skapad_av_yrkestitel_ID: "23456",
        Dokument_skapad_av_yrkestitel_Namn: "Dr. Erik Svensson",
        Dokumentationskod: "Consultation",
        Dokumentnamn: "Dermatology Consultation",
        Tidsstämpel_för_sparat_dokument: "2024-02-10T14:15:00",
        Vårdenhet_Identifierare: "DERM001",
        Vårdenhet_Namn: "Dermatology Department"
    },
    {
        CompositionId: "3",
        DateTime: "2024-01-20",
        DisplayDateTime: "2024-01-20 10:45",
        Dokument_ID: "DOC1003",
        Dokument_skapad_av_yrkestitel_ID: "34567",
        Dokument_skapad_av_yrkestitel_Namn: "Dr. Maria Johansson",
        Dokumentationskod: "Evaluation",
        Dokumentnamn: "Orthopedic Evaluation",
        Tidsstämpel_för_sparat_dokument: "2024-01-20T10:45:00",
        Vårdenhet_Identifierare: "ORTH001",
        Vårdenhet_Namn: "Orthopedic Clinic"
    },
    {
        CompositionId: "4",
        DateTime: "2023-12-05",
        DisplayDateTime: "2023-12-05 11:30",
        Dokument_ID: "DOC1004",
        Dokument_skapad_av_yrkestitel_ID: "45678",
        Dokument_skapad_av_yrkestitel_Namn: "Dr. Lars Nilsson",
        Dokumentationskod: "Assessment",
        Dokumentnamn: "Cardiology Assessment",
        Tidsstämpel_för_sparat_dokument: "2023-12-05T11:30:00",
        Vårdenhet_Identifierare: "CARD001",
        Vårdenhet_Namn: "Cardiology Department"
    },
    {
        CompositionId: "5",
        DateTime: "2023-11-15",
        DisplayDateTime: "2023-11-15 13:00",
        Dokument_ID: "DOC1005",
        Dokument_skapad_av_yrkestitel_ID: "56789",
        Dokument_skapad_av_yrkestitel_Namn: "Dr. Karin Lindberg",
        Dokumentationskod: "Consultation",
        Dokumentnamn: "Neurology Consultation",
        Tidsstämpel_för_sparat_dokument: "2023-11-15T13:00:00",
        Vårdenhet_Identifierare: "NEUR001",
        Vårdenhet_Namn: "Neurology Department"
    }
]; 