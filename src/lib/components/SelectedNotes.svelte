<script lang="ts">
    import { selectedNotes } from "$lib/stores/storedNotes";
    import { derived, writable } from "svelte/store";
    import type { Note } from "$lib/models";
    import { searchQuery } from '$lib/stores/searchStore';
    
    function handleNoteClick(noteData: Note) {
    $selectedNotes = $selectedNotes || []; 

    const foundIndex = $selectedNotes.findIndex(n => n.CaseData === noteData.CaseData);


    let newSelectedNotes = [...$selectedNotes]; // Copy array

    if (foundIndex >= 0) {
    
      newSelectedNotes.splice(foundIndex, 1);
    }

    selectedNotes.set(newSelectedNotes);
  }


  function highlightMatches(text: string, query: string): string {
    if (!query) return text;
    const escapedQuery = query.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }
  </script>


<div class="h-full bg-gray-100 flex">
    <div class="flex-1 overflow-x-auto p-2">
      <div class="flex space-x-2 h-full min-w-full">
        {#each $selectedNotes as note (note.CaseData)}
          <div class="w-[100vw] bg-white p-4 rounded-lg shadow-md">
            <div class="text-left text-sm text-gray-500 flex justify-between">
              {note?.DateTime}
              <button class="h-6 w-6 bg-red-500 rounded-md fa fa-caret-down text-white"
                on:click={() => note?.CaseData && handleNoteClick(note)} 
                class:selected={$selectedNotes?.find(n => n.CaseData === note?.CaseData)}
                aria-label="deselect note"
              ></button>
            </div>
            <div class="h-full overflow-y-auto">
              {@html highlightMatches(note.CaseData, $searchQuery)}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>