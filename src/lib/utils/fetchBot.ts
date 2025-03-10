
export interface document {
    abstract: string,
    category: string,
    content: string,
    date: string,
    id: number,
    patient_id: number,
    professional: string,
    title: string,
    type: string,
    unit: string
}

export async function fetchData(param: string): Promise<document[]> {

    const url = 'http://127.0.0.1:3333/';
    
    const response = await fetch(url+param);
    const jsonData: document[] = await response.json();
    const jsonObjects: document[] = jsonData["documents"];

    return jsonObjects;
}

