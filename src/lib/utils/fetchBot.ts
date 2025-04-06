import type {document} from "../models/note"

export async function fetchData(param: string): Promise<document[]> {

    const url = 'http://127.0.0.1:3333/';
    
    const response = await fetch(url+param);
    const jsonData: document[] = await response.json();
    const jsonObjects: document[] = jsonData["documents"];

    return jsonObjects;
}

