<script lang="ts">
import { powerMode, showTimeline, resetFilter, resetOpenDocs} from "$lib/stores";
import { selectedNotes } from "$lib/stores";

function reset() {
    resetFilter.set(true);
}

function closeDocs() {
    selectedNotes.set([]);
}

</script>
<div id="SecondaryHeader" class="flex flex-row flex-grow bg-white border-gray-200 justify-beginning px-1">
    <div id="ToggleCanvas" class="p-1 flex">
        <label for="toggleCanvas" class="text-sm items-center flex gap-1">
          Canvas Läge
        <div class="relative inline-block w-8 h-4 items-center">
          <input
            id="toggleCanvas"
            type="checkbox"
            bind:checked={$powerMode}
            class="sr-only peer"
          />
          <div
            class="w-full h-full bg-gray-300 rounded-full peer-checked:bg-purple-500 transition-colors"
          ></div>
          <div
            class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow-md transition-all peer-checked:translate-x-4"
          ></div>
        </div>
      </label>
      </div>
    
      <div id="ToggleTimeline" class="p-1 flex">
        <label for="toggleTimeline" class="text-sm items-center flex gap-1">
          Tidslinje Läge
        <div class="relative inline-block w-8 h-4 items-center">
          <input
            id="toggleTimeline"
            type="checkbox"
            bind:checked={$showTimeline}
            class="sr-only peer"
          />
          <div
            class="w-full h-full bg-gray-300 rounded-full peer-checked:bg-purple-500 transition-colors"
          ></div>
          <div
            class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow-md transition-all peer-checked:translate-x-4"
          ></div>
        </div>
      </label>
      </div>

      <div id="CloseDocs" class="p-1 flex items-center">
        <button id="Close" class="hover:text-purple-500 self-center text-sm" on:click={closeDocs}>Återställ Journalvy</button>
    </div>
    
      <div id="ResetFilters" class="p-1 flex items-center">
        <button id="Reset" class="hover:text-purple-500 self-center text-sm" on:click={reset}>Återställ Filter</button>
      </div>
</div>