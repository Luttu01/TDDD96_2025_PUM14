<script lang="ts">
  import { allNotes } from '$lib/stores';
  import { selectedNotes } from '$lib/stores';

  let isTextVisible = false;
  const toggleTextVisibility = () => {
    isTextVisible = !isTextVisible;
  };

  // Define Basic Authentication credentials
  const username = 'liu';
  const password = 'pum';

  // Helper to create Basic Auth header
  const createBasicAuth = (username: string, password: string): string => {
    return 'Basic ' + btoa(`${username}:${password}`);
  };

  // Fetch function that will handle the API request
  const handleViewCaseNotesClick = async (ehrId: string, compositionId: string) => {
    const authHeader = createBasicAuth(username, password);
    
    try {
      // Fetch case note with Basic Auth header
      const response = await fetch(`https://open-platform-migration.service.tietoevry.com/ehr/rest/v1/view/${ehrId}/RSK.View.CaseNote?compId=${compositionId}`, {
        method: 'GET',
        headers: {
          'Authorization': authHeader,
        },
      });

      // Check if the response is successful
      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.statusText} (Status: ${response.status})`);
      }

      const data = await response.json();

      // Check if data is valid and has case note
      if (data && data.length > 0) {
        // Assuming the first item in the response contains the case note
        selectedNotes.set(data[0]);
      } else {
        throw new Error('No case note data returned.');
      }
    } catch (error: unknown) {
      // Handle error properly, check if it's an instance of Error
      if (error instanceof Error) {
        console.error('Error fetching case note:', error);
        alert(`Error fetching case note: ${error.message}`);  // Show an alert with the error message
      } else {
        console.error('Unexpected error:', error);
        alert('An unexpected error occurred.');
      }
    }
  };

</script>

<div class="h-full bg-white p-4">
  <h1 class="text-2xl font-bold mb-4">Case Notes</h1>

  {#if $allNotes.length > 0}
    <div class="grid grid-cols-2 gap-4">
      <!-- Left column: Case notes and toggle button -->
      <div>
        <button
          class="mb-4 p-2 bg-blue-500 text-white rounded"
          on:click={toggleTextVisibility}>
          {isTextVisible ? 'Hide Details' : 'Show Details'}
        </button>

        {#if isTextVisible}
          <div>
            {#each $allNotes as item}
              {#each item.data as note (note.CompositionId)}
                <div class="mb-4">
                  <p class="text-sm text-blue-600"><strong>CompositionId:</strong> {note.CompositionId}</p>
                  <p class="text-sm text-green-600"><strong>DateTime:</strong> {note.DateTime}</p>
                  <p class="text-sm text-green-500"><strong>DisplayDateTime:</strong> {note.DisplayDateTime}</p>
                  <p class="text-sm text-purple-600"><strong>Dokument_ID:</strong> {note.Dokument_ID}</p>
                  <p class="text-sm text-orange-600"><strong>Dokument_skapad_av_yrkestitel_ID:</strong> {note.Dokument_skapad_av_yrkestitel_ID}</p>
                  <p class="text-sm text-orange-500"><strong>Dokument_skapad_av_yrkestitel_Namn:</strong> {note.Dokument_skapad_av_yrkestitel_Namn}</p>
                  <p class="text-sm text-red-500"><strong>Dokumentationskod:</strong> {note.Dokumentationskod}</p>
                  <p class="text-sm text-red-600"><strong>Dokumentnamn:</strong> {note.Dokumentnamn}</p>
                  <p class="text-sm text-yellow-600"><strong>Tidsstämpel_för_sparat_dokument:</strong> {note.Tidsstämpel_för_sparat_dokument}</p>
                  <p class="text-sm text-teal-600"><strong>Vårdenhet_Identifierare:</strong> {note.Vårdenhet_Identifierare}</p>
                  <p class="text-sm text-teal-500"><strong>Vårdenhet_Namn:</strong> {note.Vårdenhet_Namn}</p>
                </div>
              {/each}
            {/each}
          </div>
        {/if}
      </div>

      <!-- Right column: View Case Note buttons and Display fetched case notes -->
      <div class="flex flex-col space-y-2">
        {#each $allNotes as item}
          {#each item.data as note (note.CompositionId)}
            <button
              class="p-2 bg-green-500 text-white rounded"
              on:click={() => handleViewCaseNotesClick(item.ehrId, note.CompositionId)}>
              View CaseNote {note.CompositionId}
            </button>
          {/each}
        {/each}

        <!-- Display fetched case notes -->
        {#if $selectedNotes}
          <div class="mt-4">
            <h2 class="text-xl font-bold">Fetched Case Note</h2>
            <!-- Render the CaseData HTML content -->
            <div class="case-data">{@html $selectedNotes.CaseData}</div>
          </div>
        {/if}
      </div>
    </div>
  {:else}
    <p class="text-gray-500">No case notes available.</p>
  {/if}
</div>
