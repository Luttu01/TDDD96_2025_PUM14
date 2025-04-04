<script lang="ts">
    export let data: any = {}; // Expecting an object with a 'data' property
  </script>
  
  <div class="h-full bg-red-500 p-4">
    <h1 class="text-2xl font-bold mb-4">Case Notes</h1>
  
    {#if data.data && data.data.length > 0} <!-- Check if data.data exists and is not empty -->
      <div>
        {#each data.data as note (note.CompositionId)}
          <div class="mb-4"> <!-- Adds space between each note -->
            <p class="text-lg font-semibold"><strong>Dokumentnamn:</strong> {note.Dokumentnamn}</p>
            <p class="text-lg"><strong>CompositionId:</strong> {note.CompositionId}</p>
          </div>
        {/each}
      </div>
    {:else}
      <p class="text-gray-500">No case notes available.</p>
    {/if}
  </div>