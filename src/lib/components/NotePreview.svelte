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
    <div class={`w-4 h-4 rounded-full ${indicator.color}`}></div>
    {:else if indicator.shape === "Triangle"}
    <div
        class={`w-0 h-0 border-l-8 border-r-8 border-b-16 border-transparent border-b-current ${indicator.color}`}
    ></div>
    {:else if indicator.shape === "Square"}
    <div class={`w-4 h-4 ${indicator.color}`}></div>
    {/if}
{/each}
</div>

