<script lang="ts">
  import { allNotes, selectedNotes } from '$lib/stores';
  import { handleSelectNote } from '$lib/utils';
  import type { Note } from '$lib/models';

  let activeNoteId: string | null = null;

  function onSelectNote(note: Note) {
    handleSelectNote(note);
    activeNoteId = $selectedNotes?.some((n) => n.CompositionId === note.CompositionId)
      ? note.CompositionId
      : null;
  }
</script>

<div class="h-full bg-white p-4">
  <h1 class="text-2xl font-bold mb-4">Case Notes</h1>

  {#if $allNotes.length > 0}
    <div class="overflow-x-auto">
      <div class="flex space-x-4 pb-4">
        {#each $allNotes as item}
          {#each item.notes as note (note.CompositionId)}
            <div
              class="flex flex-col w-[300px] flex-shrink-0 bg-gray-100 border rounded shadow p-4"
            >
              <!-- Meta Data -->
              <div class="text-sm space-y-1">
                <p class="text-blue-600">
                  <strong>CompositionId:</strong> {note.CompositionId}
                </p>
                <p class="text-green-600">
                  <strong>DateTime:</strong> {note.DateTime}
                </p>
                <p class="text-green-500">
                  <strong>DisplayDateTime:</strong> {note.DisplayDateTime}
                </p>
                <p class="text-purple-600">
                  <strong>Dokument_ID:</strong> {note.Dokument_ID}
                </p>
                <p class="text-orange-600">
                  <strong>Skapad av yrkestitel ID:</strong>
                  {note.Dokument_skapad_av_yrkestitel_ID}
                </p>
                <p class="text-orange-500">
                  <strong>Skapad av yrkestitel Namn:</strong>
                  {note.Dokument_skapad_av_yrkestitel_Namn}
                </p>
                <p class="text-red-500">
                  <strong>Dokumentationskod:</strong> {note.Dokumentationskod}
                </p>
                <p class="text-red-600">
                  <strong>Dokumentnamn:</strong> {note.Dokumentnamn}
                </p>
                <p class="text-yellow-600">
                  <strong>Tidsstämpel:</strong> {note.Tidsstämpel_för_sparat_dokument}
                </p>
                <p class="text-teal-600">
                  <strong>Vårdenhet ID:</strong> {note.Vårdenhet_Identifierare}
                </p>
                <p class="text-teal-500">
                  <strong>Vårdenhet Namn:</strong> {note.Vårdenhet_Namn}
                </p>
                {#if note.error}
                  <p class="text-red-600"><strong>Error:</strong> {note.error}</p>
                {/if}
              </div>

              <!-- View Button -->
              <button
                class="mt-2 w-full bg-blue-500 text-white p-2 rounded"
                class:selected={$selectedNotes?.some(
                  (n) => n.CompositionId === note.CompositionId
                )}
                on:click={() => onSelectNote(note)}
              >
                {$selectedNotes?.some((n) => n.CompositionId === note.CompositionId)
                  ? 'Hide Case Note'
                  : 'View Case Note'}
              </button>

              <!-- Case Data Output (only for selected) -->
              {#if activeNoteId === note.CompositionId && $selectedNotes?.some((n) => n.CompositionId === note.CompositionId)}
                <div class="mt-3 p-2 border bg-white rounded text-sm">
                  {@html $selectedNotes.find((n) => n.CompositionId === note.CompositionId)?.CaseData ?? 'No case data available'}
                </div>
              {/if}
            </div>
          {/each}
        {/each}
      </div>
    </div>
  {:else}
    <p class="text-gray-500">No case notes available.</p>
  {/if}
</div>

<style lang="css">
  .selected {
    background-color: #1d4ed8; /* Matches Tailwind bg-blue-700 */
  }
</style>