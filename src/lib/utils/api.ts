import type { Document } from '$lib/models/document';

const API_BASE_URL = 'http://127.0.0.1:3333';

export type FilterParams = {
    search?: string;
    type?: string;
    category?: string;
    unit?: string;
    professional?: string;
    start_date?: string;
    end_date?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
    patient_id?: number;
    limit?: number;
};

export async function fetchDocuments(params: FilterParams = {}): Promise<Document[]> {
    // Set default limit if not provided
    if (!params.limit) {
        params.limit = 30; // Default limit to prevent browser hanging
    }
    
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) queryParams.append(key, String(value));
    });

    console.log(`Fetching documents with params: ${queryParams.toString()}`);
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    try {
        const url = `${API_BASE_URL}/documents${queryString}`;
        console.log(`Making request to: ${url}`);
        
        const response = await fetch(url);
        
        if (!response.ok) {
            console.error(`API returned error status: ${response.status}`);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw API response:', data);
        
        // Check if data has a documents property
        if (!data.documents) {
            console.error('API response missing documents property:', data);
            return [];
        }
        
        // Check if documents is an array
        if (!Array.isArray(data.documents)) {
            console.error('API documents is not an array:', data.documents);
            return [];
        }
        
        console.log(`API returned ${data.documents.length} documents`);
        
        // Return the documents array
        return data.documents;
    } catch (error) {
        console.error('Error fetching documents:', error);
        throw error;
    }
}

export async function fetchDocument(id: number): Promise<Document> {
    const response = await fetch(`${API_BASE_URL}/documents/${id}`);
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

export async function fetchFilterOptions() {
    const response = await fetch(`${API_BASE_URL}/options`);
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
} 