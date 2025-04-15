<script lang="ts">
  import { allNotes, selectedNotes } from '$lib/stores';
  import { handleSelectNote } from '$lib/utils';
  import type { Note } from '$lib/models';

  let isTextVisible = false;

  const toggleTextVisibility = () => {
    isTextVisible = !isTextVisible;
  };

  const onSelectNote = (note: Note) => {
    handleSelectNote(note);
  };
</script>

<div class="h-full bg-white p-4">
  <h1 class="text-2xl font-bold mb-4">Case Notes</h1>

  {#if $allNotes.length > 0}
    <div class="grid grid-cols-2 gap-4">
      <div>
        <button
          class="mb-4 p-2 bg-blue-500 text-white rounded"
          on:click={toggleTextVisibility}>
          {isTextVisible ? 'Hide Details' : 'Show Details'}
        </button>

        {#if isTextVisible}
          <div>
            {#each $allNotes as item}
              {#each item.notes as note (note.CompositionId)}
                <div class="mb-4 border p-2 rounded shadow">
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
                  {#if note.error}
                    <p class="text-sm text-red-600"><strong>Error:</strong> {note.error}</p>
                  {/if}
                </div>
              {/each}
            {/each}
          </div>
        {/if}
      </div>

      <div class="flex flex-col space-y-2">
        {#each $allNotes as item}
          {#each item.notes as note (note.CompositionId)}
            <button
              class="p-2 bg-green-500 text-white rounded"
              on:click={() => onSelectNote(note)}>
              View CaseNote {note.CompositionId}
            </button>
          {/each}
        {/each}

        <div class="mt-4">
          <h2 class="text-xl font-bold mb-2">Fetched Case Note</h2>
          <div class="case-data p-2 border rounded bg-gray-50">
            {#if $selectedNotes}
              {@html $selectedNotes.CaseData ?? 'No case data available'}
            {:else}
              <p class="text-gray-500">Select a note to view its details.</p>
            {/if}
          </div>
        </div>
      </div>
    </div>
  {:else}
    <p class="text-gray-500">No case notes available.</p>
  {/if}
</div>