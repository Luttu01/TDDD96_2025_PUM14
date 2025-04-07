<script lang="ts">
 import { dummySelectedNotes, allTestNotes  } from "../stores/dummyDataSelected"; 
  
  
  let selectedNotes = $dummySelectedNotes;
  
  let noteCount = 1;
  $: displayedNotes = selectedNotes.length > 0 ? selectedNotes : allTestNotes.slice(0, noteCount);
 
  function getGridLayout(count: number): string {
  return `grid-cols-1 sm:grid-cols-2 md:grid-cols-1 lg:grid-cols-${count}`;
}
</script>

<div class="w-full h-full">
    <div class="flex space-x-2 mb-4">
      {#each [1, 2, 3, 4, 5] as num}
        <button
          class="px-4 py-2 rounded-md transition-colors
                {noteCount === num 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 hover:bg-gray-300'}"
          on:click={() => noteCount = num}
        >
          Show {num} Note{num !== 1 ? 's' : ''}
        </button>
      {/each}
    </div>

  <div id="notes-container" class="w-full h-full p-4 overflow-y-auto">
    <div class={`grid ${getGridLayout(displayedNotes.length)} gap-4 min-h-0 h-full`}>
      {#each displayedNotes as note, index}
        <div class="bg-yellow-100 rounded-2xl shadow-md p-4 flex flex-col min-h-0 h-full">
          <h2 class="text-xl font-semibold mb-2">Journalanteckning {index + 1}</h2>

          <div class="mb-3 min-h-0 overflow-y-auto">
            <h3 class="font-bold">Anamnes:</h3>
            <p class="text-sm whitespace-pre-line mt-1">{note.anamnes}</p>
          </div>

          <div class="mb-3 min-h-0 overflow-y-auto">
            <h3 class="font-bold text-red-500">Text:</h3>
            <p class="text-sm whitespace-pre-line mt-1">{note.text}</p>
          </div>

          <div class="mb-2 min-h-0 overflow-y-auto">
            <h3 class="font-bold">Arbetsdiagnos:</h3>
            <p class="text-sm whitespace-pre-line mt-1">{note.diagnos}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>