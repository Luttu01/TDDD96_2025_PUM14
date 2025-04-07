<script lang="ts">
    import { selectedNotes } from "$lib/stores/storedNotes";
    import { derived, writable } from "svelte/store";
    //let scale: number = 1;
    //const baseWidth: number = 320;
  </script>


<div class="h-full bg-yellow-100 flex">
    <div class="flex-1 overflow-x-auto p-4">
      <div class="flex space-x-4 h-full min-w-full">
        {#each $selectedNotes as note (note.CaseData)}
          <div class="w-[100vw] bg-red-100 p-6 rounded-lg shadow-md h-full overflow-y-auto">
            {@html note.CaseData}
          </div>
        {/each}
      </div>
    </div>
  </div>