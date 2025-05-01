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