<script lang="ts">
  import { filter } from "$lib/stores";
  import type { Note } from "$lib/models";
  import {shapeMap, colorMap} from "$lib/utils"
  export let note : Note;
  export let direction : "flex-col" | "flex-row" = "flex-row";

  function getNoteProperty(note: Note, key: string) {
    switch (key) {
      case "Vårdenhet":
        return note.Vårdenhet_Namn;
      case "Journalmall":
        return note.Dokumentnamn;
      case "Yrkesroll":
        return note.Dokument_skapad_av_yrkestitel_Namn;
      default:
        return null;
    }
  }

  let matchingIndicators: Array<{
    key: string;
    shape: "Circle" | "Triangle" | "Square";
    color: string;
  }> = [];
  $: matchingIndicators = [];

  $: if ($filter) {
    matchingIndicators = [];

    for (const [key, activeValues] of $filter.entries()) {
      if (activeValues.size === 0) continue;

      const noteValue = getNoteProperty(note, key);
      if (noteValue !== null && activeValues.has(noteValue)) {
        matchingIndicators.push({
          key,
          shape: shapeMap[key as "Vårdenhet" | "Journalmall" | "Yrkesroll"],
          color:
            colorMap[key as "Vårdenhet" | "Journalmall" | "Yrkesroll"]?.[
              noteValue
            ] || "bg-gray-400",
        });
      }
    }
  }
</script>


<div class="flex items-center" class:flex-col={direction === 'flex-col'} class:flex-row={direction === 'flex-row'} class:space-x-1={direction === 'flex-row'} class:space-y-1={direction === 'flex-col'}>
{#each matchingIndicators as indicator}
    {#if indicator.shape === "Circle"}
    <svg class="w-5 h-5 p-[2px] {indicator.color} text-white rounded-full" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
      <path fill-rule="evenodd" d="M11.293 3.293a1 1 0 0 1 1.414 0l6 6 2 2a1 1 0 0 1-1.414 1.414L19 12.414V19a2 2 0 0 1-2 2h-3a1 1 0 0 1-1-1v-3h-2v3a1 1 0 0 1-1 1H7a2 2 0 0 1-2-2v-6.586l-.293.293a1 1 0 0 1-1.414-1.414l2-2 6-6Z" clip-rule="evenodd"/>
    </svg>    
    {:else if indicator.shape === "Triangle"}
    <svg class="w-5 h-5 p-[2px] {indicator.color} text-white rounded-full" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
      <path fill-rule="evenodd" d="M9 2.221V7H4.221a2 2 0 0 1 .365-.5L8.5 2.586A2 2 0 0 1 9 2.22ZM11 2v5a2 2 0 0 1-2 2H4v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-7ZM8 16a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2H9a1 1 0 0 1-1-1Zm1-5a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2H9Z" clip-rule="evenodd"/>
    </svg>    
    {:else if indicator.shape === "Square"}
    <svg class="w-5 h-5 p-[1px] {indicator.color} text-white rounded-full" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
      <path fill-rule="evenodd" d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z" clip-rule="evenodd"/>
    </svg>
    
    {/if}
{/each}
</div>

