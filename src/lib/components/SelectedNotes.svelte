<script lang="ts">
  interface Note {
    anamnes: string;
    text: string;
    diagnos: string;
  }

  export let selectedNotes: Note[] = [];

  function getGridLayout(count: number): string {
    switch(count) {
      case 1: return 'grid-cols-1';
      case 2: return 'grid-cols-1 md:grid-cols-2';
      case 3: return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3';
      case 4: return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4';
      default: return 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4';
    }
  }
</script>

<div id="notes-container" class="w-full h-full p-4 overflow-y-auto">
  <div class={`grid ${getGridLayout(selectedNotes.length)} gap-4 min-h-0 h-full`}>
    {#each selectedNotes as note, index}
      <div class="bg-yellow-100 rounded-2xl shadow-md p-4 flex flex-col min-h-0 h-full">
        <h2 class="text-xl font-semibold mb-2">Journalanteckning {index + 1}</h2>

        <div class="mb-3  min-h-0 overflow-y-auto">
          <h3 class="font-bold">Anamnes:</h3>
          <p class="text-sm whitespace-pre-line mt-1">{note.anamnes}</p>
        </div>

        <div class="mb-3  min-h-0 overflow-y-auto">
          <h3 class="font-bold text-red-500">Text:</h3>
          <p class="text-sm whitespace-pre-line mt-1">{note.text}</p>
        </div>

        <div class="mb-2  min-h-0 overflow-y-auto">
          <h3 class="font-bold">Arbetsdiagnos:</h3>
          <p class="text-sm whitespace-pre-line mt-1">{note.diagnos}</p>
        </div>
      </div>
    {/each}
  </div>
</div>