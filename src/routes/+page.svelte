<script lang="ts">
  import List from "$lib/components/List.svelte";
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";

  const allTestNotes = [
    {
      anamnes: "Patient inkom med bröstsmärtor sedan två timmar tillbaka.",
      text: "AT Vaken, orienterad x3, saturation 98%, BT 135/85 mmHg.",
      diagnos: "Icke-ST-höjningsinfarkt (NSTEMI)?"
    },
    {
      anamnes: "Smärta som trycker och strålar mot käken.",
      text: "Pulm Vesikulära andningsljud bilateralt, ingen rassel.",
      diagnos: "Gastroesofageal reflux?"
    },
    {
      anamnes: "Huvudvärk sedan morgonen, ingen tidigare migränhistoria.",
      text: "Neurologiskt status: Inte påfallande, ingen nackstyvhet.",
      diagnos: "Spänningshuvudvärk"
    },
    {
      anamnes: "Trötthet och andfåddhet vid ansträngning sedan 2 veckor.",
      text: "Hjärta: Regelbunden rytm, inga blåsljud. Buk: Mjuk, icke öm.",
      diagnos: "Anemi?"
    }
  ];

  // Number of notes to display (1-4)
  let noteCount = 1;

  // Computed property to get the selected notes
  $: displayedNotes = allTestNotes.slice(0, noteCount);
</script>

<div class="flex flex-col w-full h-screen p-4 bg-gray-100">
  <aside class="mb-4">
    <List />
  </aside>

  <main class="flex-1 min-h-0"> 
    <div class="w-full h-full flex flex-col"> 
      <div class="flex space-x-2 mb-4">
        {#each [1, 2, 3, 4] as num}
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

      <div class="flex-1 w-full h-full p-4 bg-white rounded-lg shadow-lg overflow-y-auto"> 
        <SelectedNotes selectedNotes={displayedNotes} />
      </div>
    </div>
  </main>
</div>
