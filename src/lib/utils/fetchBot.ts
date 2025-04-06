import type { Document } from "../models/note"

export async function fetchData(param: string): Promise<Document[]> {

    const url = 'http://127.0.0.1:3333/';
    
    const response = await fetch(url+param);
    const jsonData: { documents: Document[] } = await response.json();
    const jsonObjects: Document[] = jsonData.documents;

    return jsonObjects;
}