export async function load({ fetch }) {
    try {
        // Make the request to the API
        const res = await fetch('/api/casenotes');

        // Check if the response is OK (status 200-299)
        if (!res.ok) {
            throw new Error(`Failed to fetch: ${res.status} ${res.statusText}`);
        }

        // Try to parse the JSON response
        const data = await res.json();

        // Optionally, log the data for debugging purposes
        // console.log('Data in +page.ts:', data);

        return { data }; // Return the data
    } catch (error) {
        console.error('Error loading data:', error);

        // You can either return an empty object or a specific error message
        return { data: null, error: 'Could not fetch case notes' };
    }
}