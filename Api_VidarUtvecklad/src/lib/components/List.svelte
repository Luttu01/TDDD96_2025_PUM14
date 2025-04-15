<script lang="ts">
    import { allNotes, selectedNotes } from '$lib/stores';
    import { handleSelectNote } from '$lib/utils';
    import type { Note } from '$lib/models';
  
    let isTextVisible = false;
    let errorMessage: string | null = null;
    let selectedCompositionId: string | null = null;
  
    const toggleTextVisibility = () => {
      isTextVisible = !isTextVisible;
    };
  
    const onSelectNote = (note: Note) => {
      selectedCompositionId = note.CompositionId;
      errorMessage = null;
      const result = handleSelectNote(note);
      if (result.error) {
        errorMessage = result.error;
      }
    };
  </script>
  
  <div class="h-full bg-yellow-500 p-4 overflow-y-auto">
    <h1 class="text-xl font-bold mb-4 text-white">Case Notes List</h1>
  
    <!-- Table Header -->
    <div class="grid grid-cols-1 gap-2 font-semibold text-white text-sm border-b border-white pb-1 mb-2">
      <div>Dokumentnamn</div>
    </div>
  
    <!-- Notes List -->
    <div class="space-y-1 overflow-y-auto">
      {#each $allNotes as item}
        {#each item.notes as note (note.CompositionId)}
          <button
            type="button"
            on:click={() => onSelectNote(note)}
            class="w-full text-left bg-yellow-500 rounded px-3 py-2 hover:bg-gray-300 transition-all duration-200 text-xs
              {selectedCompositionId === note.CompositionId ? 'border border-blue-500' : 'border border-transparent'}"
          >
            <span class="truncate">{note.Dokumentnamn}</span>
          </button>
        {/each}
      {/each}
    </div>
  </div>
  