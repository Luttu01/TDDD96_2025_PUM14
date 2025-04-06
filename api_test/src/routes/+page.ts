import { allNotes } from '$lib/stores'; // Import the store you want to use

export async function load({ fetch }) {
    try {
      const res = await fetch('/api');  // Make request to your backend API
  
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
  
      
      const allData = await res.json();
    console.log('allData', allData);

    if (Array.isArray(allData) && allData.length > 0) {
      allNotes.set(allData); // Only use the store
    } else {
      allNotes.set([]); // Set empty array if no data
    }

    return {}; // Don't return data manually if you're using stores only

  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    console.error('Error loading data:', errorMessage);
    allNotes.set([]); // Clear or reset store on failure

    return {}; // Still return an empty object to satisfy the load function
  }
}
      
    /*
      const allData = await res.json();  // Parse the JSON response
      
      console.log("allData", allData);  // Debugging to check what data is returned
  
      // Check if data is valid
      if (Array.isArray(allData) && allData.length > 0) {
        //return { data: allData };  // Return data if it's valid
        allNotes.set(allData);  // Update the store with fetched data
        return { data: allData };  // Return data if it's valid
    } else {
      return { data: null, error: 'No data found' };  // Return an error if no data
      }
    } catch (e: unknown) {
      console.error('Error loading data:', e);
      const errorMessage = e instanceof Error ? e.message : String(e);
      return { data: null, error: `Network error: ${errorMessage}` };  // Return error message
    }
  }*/
  