export async function load({ fetch }) {
    try {
        // Make the request to the API
        const res = await fetch('/api');

        // Check if the response is OK (status 200)
        if (!res.ok) {
            let errorMessage = '';

            switch (res.status) {
                case 200:
                    // Success, no need to handle, it's already a valid response
                    return { data: await res.json() };

                case 400:
                    errorMessage = 'Bad Request: The requested view does not exist.';
                    break;

                case 401:
                    errorMessage = 'Unauthorized: Could not authenticate the user.';
                    break;

                case 403:
                    errorMessage = 'Forbidden: You do not have the required permissions.';
                    break;

                case 408:
                    errorMessage = 'Request Timeout: View processing took too long and was canceled.';
                    break;

                default:
                    errorMessage = `Error: ${res.status} - ${res.statusText}`;
            }

            throw new Error(errorMessage);  // Throw the specific error based on the status code
        }

        // Try to parse the JSON response if status is OK (Code-200)
        const data = await res.json();

        return { data }; // Return the data to the page as a prop

    } catch (e: unknown) {
        console.error('Error loading data:', e);

        // Type check
        const errorMessage = e instanceof Error ? e.message : String(e);

        // Return a detailed error message to the page
        return { data: null, error: `Network error: ${errorMessage}` };
    }
}
