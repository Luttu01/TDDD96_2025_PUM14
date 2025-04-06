export async function load({ fetch }) {
    try {
      const res = await fetch('/api');  // Call the API
  
      // Check for successful response
      if (!res.ok) {
        let errorMessage = '';
        switch (res.status) {
          case 200:
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
        throw new Error(errorMessage);  // Throw the specific error based on status
      }
  
      const allData = await res.json();  // Assuming the response contains an array of notes
      
      console.log("allData", allData);  // Debugging to check what data is returned
  
      if (Array.isArray(allData) && allData.length > 0) {
        return { data: allData };  // Return data if it's valid
      } else {
        return { data: null, error: 'No valid data received.' };  // Handle no data case
      }
    } catch (e: unknown) {
      console.error('Error loading data:', e);
      const errorMessage = e instanceof Error ? e.message : String(e);
      return { data: null, error: `Network error: ${errorMessage}` };  // Return error message
    }
  }
  