import type {document} from "../models/note"

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
    [key: string]: string | number | undefined;
};

// Simple cache for the current session
const cache = new Map<string, document[]>();

// Add timeout protection for fetch requests
async function fetchWithTimeout(url: string, options: RequestInit = {}, timeout = 5000): Promise<Response> {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(id);
        return response;
    } catch (error) {
        clearTimeout(id);
        console.error(`Request to ${url} timed out after ${timeout}ms`);
        throw error;
    }
}

// Maintain backward compatibility with existing code
export async function fetchData(param: string, params: FilterParams = {}): Promise<document[]> {
    // Determine if we're using the old or new API pattern
    if (param.includes('/')) {
        // Full URL was provided - handle legacy case
        return fetchLegacy(param);
    }
    
    // Build query params
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) queryParams.append(key, String(value));
    });

    // Create the URL with query parameters
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    const url = `${API_BASE_URL}/${param}${queryString}`;
    
    console.log(`API request to: ${url}`);
    
    // Generate a cache key from the full URL
    const cacheKey = url;
    if (cache.has(cacheKey)) {
        console.log(`Using cached data for ${url} - found ${cache.get(cacheKey)?.length || 0} documents`);
        return cache.get(cacheKey) || [];
    }
    
    // Make the request with timeout protection
    try {
        console.log(`Making network request to ${url}`);
        const response = await fetchWithTimeout(url, {}, 5000);
        
        // Handle error responses
        if (!response.ok) {
            console.error(`API error: ${response.status} ${response.statusText}`);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse the response
        const data = await response.json();
        console.log(`API response received:`, data ? 'data present' : 'no data');
        
        // Get documents array from response
        const documents = data.documents || [];
        console.log(`Found ${documents.length} documents in API response`);
        
        // Update cache
        cache.set(cacheKey, documents);
        
        return documents;
    } catch (error) {
        console.error('Error fetching data:', error);
        // Return empty array on error to prevent UI from hanging
        return [];
    }
}

// Legacy support function
async function fetchLegacy(fullUrl: string): Promise<document[]> {
    // Check cache using the full URL as key
    if (cache.has(fullUrl)) {
        return cache.get(fullUrl) || [];
    }
    
    try {
        const response = await fetchWithTimeout(fullUrl, {}, 5000);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (!data.documents || !Array.isArray(data.documents)) {
            console.error('Invalid response format:', data);
            return [];
        }
        
        const documents = data.documents as document[];
        
        // Store in cache
        cache.set(fullUrl, documents);
        
        return documents;
    } catch (error) {
        console.error('Error fetching documents:', error);
        return [];
    }
}

export async function fetchDocument(id: number): Promise<document> {
    const url = `${API_BASE_URL}/documents/${id}`;
    
    try {
        const response = await fetchWithTimeout(url, {}, 5000);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error fetching document ${id}:`, error);
        throw error;
    }
}

export async function fetchFilterOptions() {
    const url = `${API_BASE_URL}/options`;
    
    try {
        const response = await fetchWithTimeout(url, {}, 5000);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching filter options:', error);
        return {};
    }
}

