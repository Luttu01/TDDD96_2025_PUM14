<script lang="ts">
  // Import necessary stores, types, and the handleSelectNote function
  import { allNotes, selectedNotes } from '$lib/stores';
  import { handleSelectNote } from '$lib/utils';
  import type { Note } from '$lib/models';

  // Boolean flag to control the visibility of case note details
  let isTextVisible = false;
  // Variable to store error messages for display
  let errorMessage: string | null = null;

  // Function to toggle visibility of case note details
  const toggleTextVisibility = () => {
    isTextVisible = !isTextVisible;
  };

  // Function to handle note selection and capture errors
  const onSelectNote = (note: Note) => {
    errorMessage = null; // Reset error message
    const result = handleSelectNote(note);
    if (result.error) {
      errorMessage = result.error;
    }
  };
</script>

<div class="h-full bg-white p-4">
  <h1 class="text-2xl font-bold mb-4">Case Notes</h1>

  <!-- Check if there are any case notes available -->
  {#if $allNotes.length > 0}
    <div class="grid grid-cols-2 gap-4">
      <!-- Left column: Display case notes with a toggle button to show/hide details -->
      <div>
        <!-- Button to toggle the visibility of the case notes details -->
        <button
          class="mb-4 p-2 bg-blue-500 text-white rounded"
          on:click={toggleTextVisibility}>
          {isTextVisible ? 'Hide Details' : 'Show Details'}
        </button>

        <!-- Conditionally render case notes details when isTextVisible is true -->
        {#if isTextVisible}
          <div>
            <!-- Loop through all notes and display their details -->
            {#each $allNotes as item}
              {#each item.notes as note (note.CompositionId)}
                <div class="mb-4 border p-2 rounded shadow">
                  <!-- Display individual note details -->
                  <p class="text-sm text-blue-600"><strong>CompositionId:</strong> {note.CompositionId}</p>
                  <p class="text-sm text-green-600"><strong>DateTime:</strong> {note.DateTime}</p>
                  <p class="text-sm text-green-500"><strong>DisplayDateTime:</strong> {note.DisplayDateTime}</p>
                  <p class="text-sm text-purple-600"><strong>Dokument_ID:</strong> {note.Dokument_ID}</p>
                  <p class="text-sm text-orange-600"><strong>Skapad av yrkestitel ID:</strong> {note.Dokument_skapad_av_yrkestitel_ID}</p>
                  <p class="text-sm text-orange-500"><strong>Skapad av yrkestitel Namn:</strong> {note.Dokument_skapad_av_yrkestitel_Namn}</p>
                  <p class="text-sm text-red-500"><strong>Dokumentationskod:</strong> {note.Dokumentationskod}</p>
                  <p class="text-sm text-red-600"><strong>Dokumentnamn:</strong> {note.Dokumentnamn}</p>
                  <p class="text-sm text-yellow-600"><strong>Tidsstämpel för sparat dokument:</strong> {note.Tidsstämpel_för_sparat_dokument}</p>
                  <p class="text-sm text-teal-600"><strong>Vårdenhet Identifierare:</strong> {note.Vårdenhet_Identifierare}</p>
                  <p class="text-sm text-teal-500"><strong>Vårdenhet Namn:</strong> {note.Vårdenhet_Namn}</p>
                  <!-- Display error if present -->
                  {#if note.error}
                    <p class="text-sm text-red-600"><strong>Error:</strong> {note.error}</p>
                  {/if}
                </div>
              {/each}
            {/each}
          </div>
        {/if}
      </div>

      <!-- Right column: Buttons to select a specific note and view its details -->
      <div class="flex flex-col space-y-2">
        <!-- Loop through all notes and display buttons to select each one -->
        {#each $allNotes as item}
          {#each item.notes as note (note.CompositionId)}
            <button
              class="p-2 bg-green-500 text-white rounded"
              on:click={() => onSelectNote(note)}>
              View CaseNote {note.CompositionId}
            </button>
          {/each}
        {/each}

        <!-- Conditionally render the selected note details or error message -->
        <div class="mt-4">
          <h2 class="text-xl font-bold mb-2">Fetched Case Note</h2>
          <div class="case-data p-2 border rounded bg-gray-50">
            {#if errorMessage}
              <p class="text-red-500">{errorMessage}</p>
            {:else if $selectedNotes}
              {@html $selectedNotes.CaseData ?? 'No case data available'}
            {:else}
              <p class="text-gray-500">Select a note to view its details.</p>
            {/if}
          </div>
        </div>
      </div>
    </div>
  {:else}
    <!-- Message when no case notes are available -->
    <p class="text-gray-500">No case notes available.</p>
  {/if}
</div>