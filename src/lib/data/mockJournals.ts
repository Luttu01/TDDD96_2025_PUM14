import type { document } from "../models/note";

// Create mock journal data with minimal content for better performance
export const mockJournals: document[] = [
    {
        id: 1,
        title: "Yearly Health Checkup",
        type: "Journal",
        category: "General Medicine",
        unit: "Primary Care Unit",
        professional: "Dr. Anna Andersson",
        date: "2024-03-15",
        abstract: "Regular yearly checkup shows good overall health with minor vitamin D deficiency.",
        content: "Patient presents with good overall health. Physical examination normal. Blood tests show slight vitamin D deficiency (42 nmol/L). Recommended vitamin D supplementation 800 IU daily for 3 months.",
        patient_id: 1001
    },
    {
        id: 2,
        title: "Dermatology Consultation",
        type: "Consultation",
        category: "Dermatology",
        unit: "Dermatology Department",
        professional: "Dr. Erik Svensson",
        date: "2024-02-10",
        abstract: "Assessment of eczema on both hands, prescribed hydrocortisone cream.",
        content: "Patient presents with dry, itchy patches on both hands, worse between fingers.",
        patient_id: 1001
    },
    {
        id: 3,
        title: "Orthopedic Evaluation",
        type: "Evaluation",
        category: "Orthopedics",
        unit: "Orthopedic Clinic",
        professional: "Dr. Maria Johansson",
        date: "2024-01-20",
        abstract: "Follow-up after ankle sprain, good recovery progress noted.",
        content: "Patient recovering well from grade 2 ankle sprain sustained 4 weeks ago.",
        patient_id: 1001
    },
    {
        id: 4,
        title: "Cardiology Assessment",
        type: "Assessment",
        category: "Cardiology",
        unit: "Cardiology Department",
        professional: "Dr. Lars Nilsson",
        date: "2023-12-05",
        abstract: "Evaluation for occasional heart palpitations, ECG within normal limits.",
        content: "Patient reports occasional heart palpitations, typically after caffeine consumption.",
        patient_id: 1001
    },
    {
        id: 5,
        title: "Neurology Consultation",
        type: "Consultation",
        category: "Neurology",
        unit: "Neurology Department",
        professional: "Dr. Karin Lindberg",
        date: "2023-11-15",
        abstract: "Consultation for recurring migraine headaches, treatment plan updated.",
        content: "Patient reports increasing frequency of migraine attacks (3-4 per month).",
        patient_id: 1001
    }
]; 