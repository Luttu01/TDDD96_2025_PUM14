<script lang="ts">
  import type { Note } from '../models';

  export let data: { data: { ehrId: string, data: Note[] }[] } = { data: [] };

  console.log("selectednotes", data);

  let isTextVisible = false;
  const toggleTextVisibility = () => {
    isTextVisible = !isTextVisible;
  }

  // Add your function for the new button here
  const handleViewCaseNotesClick = (ehrId:string , compositionId:string) => {
    console.log("ehrId:", ehrId)
    console.log("CompositionId:", compositionId);

    //Todo: make the fetch request using these values
  }


</script>

<div class="h-full bg-white p-4">
  <h1 class="text-2xl font-bold mb-4">Case Notes</h1>

  <!-- Check if data exists and is not empty -->
  {#if data.data && data.data.length > 0} 
    <div>
      <!-- Button to toggle visibility of case note details -->
      <button 
        class="mb-4 p-2 bg-blue-500 text-white rounded"
        on:click={toggleTextVisibility}>
        {isTextVisible ? 'Hide Details' : 'Show Details'}
      </button>
      <!-- New button next to the Show Details button -->
      <!-- Loop through the data and create a button for each CompositionId -->
      <div class="flex flex-col space-y-2"> <!-- Flex container with column direction -->
        {#each data.data as item}
          {#each item.data as note (note.CompositionId)}
            <button 
              class="p-2 bg-green-500 text-white rounded"
              on:click={() => handleViewCaseNotesClick(item.ehrId, note.CompositionId)}>
              View CaseNote {note.CompositionId}
            </button>
          {/each}
        {/each}
      </div>


      {#if isTextVisible}
        <div>
          {#each data.data as item}
            {#each item.data as note (note.CompositionId)} <!-- Nested each loop to access the note data -->
              <div class="mb-4">
                <p class="text-sm text-blue-600">
                  <strong>CompositionId:</strong> {note.CompositionId}
                </p>
                <p class="text-sm text-green-600">
                  <strong>DateTime:</strong> {note.DateTime}
                </p>
                <p class="text-sm text-green-500">
                  <strong>DisplayDateTime:</strong> {note.DisplayDateTime}
                </p>
                <p class="text-sm text-purple-600">
                  <strong>Dokument_ID:</strong> {note.Dokument_ID}
                </p>
                <p class="text-sm text-orange-600">
                  <strong>Dokument_skapad_av_yrkestitel_ID:</strong> {note.Dokument_skapad_av_yrkestitel_ID}
                </p>
                <p class="text-sm text-orange-500">
                  <strong>Dokument_skapad_av_yrkestitel_Namn:</strong> {note.Dokument_skapad_av_yrkestitel_Namn}
                </p>
                <p class="text-sm text-red-500">
                  <strong>Dokumentationskod:</strong> {note.Dokumentationskod}
                </p>
                <p class="text-sm text-red-600">
                  <strong>Dokumentnamn:</strong> {note.Dokumentnamn}
                </p>
                <p class="text-sm text-yellow-600">
                  <strong>Tidsstämpel_för_sparat_dokument:</strong> {note.Tidsstämpel_för_sparat_dokument}
                </p>
                <p class="text-sm text-teal-600">
                  <strong>Vårdenhet_Identifierare:</strong> {note.Vårdenhet_Identifierare}
                </p>
                <p class="text-sm text-teal-500">
                  <strong>Vårdenhet_Namn:</strong> {note.Vårdenhet_Namn}
                </p>
              </div>
            {/each}
          {/each}
        </div>
      {/if}
    </div>
  {:else}
    <p class="text-gray-500">No case notes available.</p>
  {/if}
</div>
