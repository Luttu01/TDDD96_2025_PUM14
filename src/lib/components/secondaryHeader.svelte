<script lang="ts">
import { powerMode, toggleTimeline, resetFilter, resetOpenDocs } from "$lib/stores";

function reset() {
    resetFilter.set(true);
}

function closeDocs() {
    resetOpenDocs.set(true);
}

</script>
<div id="SecondaryHeader" class="flex flex-row bg-white border-b-1 border-gray-200">
    <div id="PowerPointToggle" class="p-2 flex items-center gap-2">
        <label for="powerModeToggle" class="text-sm font-medium"
          >PowerPoint Läge</label
        >
        <input
          id="powerModeToggle"
          type="checkbox"
          bind:checked={$powerMode}
          class="toggle"
        />
      </div>
    
      <div id="ToggleTimeline" class="p-2 flex items-center gap-2">
        <label for="toggleTimeline" class="text-sm font-medium"
          >Visa tidslinje</label
        >
        <input
          id="toggleTimeline"
          type="checkbox"
          bind:checked={$toggleTimeline}
          class="toggle"
        />
      </div>
    
      <div id="ResetFilters" class="p-2 flex items-center gap-2">
        <button id="Reset" class="hover:text-purple-500 self-center" on:click={reset}>Återställ Filter</button>
      </div>
    
      <div id="CloseDocs" class="p-2 flex items-center gap-2">
        <button id="Close" class="hover:text-purple-500 self-center" on:click={closeDocs}>Återställ Journalvy</button>
    </div>
</div>