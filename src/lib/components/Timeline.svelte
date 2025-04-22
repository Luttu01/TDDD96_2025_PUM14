<script lang="ts">
  import { writable } from "svelte/store";
  import NotePreview from "./NotePreview.svelte";

  import type { Note, Year, Month } from "$lib/models";
  import { buildDateHierarchy } from "$lib/utils";
  import { filteredNotes, selectedNotes } from "$lib/stores";

  const noteHierarchy = writable<Year[]>([]);

  $: {
    noteHierarchy.set(buildDateHierarchy($filteredNotes));
  }

  function toggleGroup(group: Year | Month) {
    group.isCollapsed = !group.isCollapsed;
    noteHierarchy.set($noteHierarchy);
  }

  function handleNoteClick(noteData: Note) {
    $selectedNotes = $selectedNotes || [];

    const foundIndex = $selectedNotes.findIndex(
      (n) => n.CaseData === noteData.CaseData
    );

    let newSelectedNotes = [...$selectedNotes];

    if (foundIndex >= 0) {
      newSelectedNotes.splice(foundIndex, 1);
    } else {
      newSelectedNotes.push(noteData);
    }

    selectedNotes.set(newSelectedNotes);
  }

  function getNoteSizeState(yearGroup: Year, monthGroup: Month) {
    if (yearGroup.isCollapsed) return 'compact';
    if (monthGroup.isCollapsed) return 'medium';
    return 'expanded';
  }
</script>

<div class="relative h-full bg-gray-100 overflow-x-auto overflow-y-hidden">
  <div class="flex flex-row w-max h-full space-x-[2px]">
    {#each $noteHierarchy as yearGroup (yearGroup.year)}
      <div class="relative h-full flex flex-col">
        <button
          class="flex bg-purple-200 py-1 text-left px-2 w-full shadow-xs"
          on:click={() => toggleGroup(yearGroup)}
          aria-label="Toggle year {yearGroup.year}"
        >
          <div class="text-md sticky left-1 w-10 font-bold text-gray-900">
            {yearGroup.year}
          </div>
        </button>
        <div
          class="flex flex-grow flex-row overflow-y-hidden space-x-[2px]"
        >
          {#each yearGroup.months as monthGroup}
            <div class="flex flex-col">
              <button
                class="{yearGroup.isCollapsed
                  ? 'hidden'
                  : 'flex'} bg-purple-300 py-1 px-1 justify-between w-full shadow-xs"
                on:click={() => toggleGroup(monthGroup)}
                aria-label="Toggle month {monthGroup.month}"
              >
                <div
                  class="text-sm sticky left-1 px-1 w-10 font-semibold text-gray-900 text-left"
                >
                    {new Date(0, monthGroup.month).toLocaleString("sv-SE", {
                    month: "short",
                  })}
                </div>
              </button>
              <div
                class="relative flex flex-row overflow-y-hidden p-[2px] gap-[4px] flex-grow"
              >
              {#each monthGroup.notes as note}
              {#key note.Dokument_ID}
                <button
                  class={`transition-all duration-300 ease-in-out border border-gray-200 rounded-md shadow-xs bg-white ${
                    getNoteSizeState(yearGroup, monthGroup) === 'compact'
                      ? 'flex flex-col py-2 px-1 w-13 h-full space-y-1'
                      : getNoteSizeState(yearGroup, monthGroup) === 'medium'
                      ? 'flex flex-col py-1 px-2 w-45 text-sm text-left'
                      : 'flex justify-between p-2 w-120 h-full overflow-y-auto'
                  }`}
                  on:click={() => handleNoteClick(note)}
                  aria-label="Select note {note.Dokument_ID}"
                >
                  {#if getNoteSizeState(yearGroup, monthGroup) === 'compact'}
                    <span class="text-[10px] text-gray-700">
                      {new Date(note.DateTime).toLocaleDateString("sv-SE", {
                        month: "2-digit",
                        day: "2-digit",
                      })}
                    </span>
                    <span class="text-[10px] font-bold border border-gray-200 rounded-md h-18">
                      Filter
                      <NotePreview {note} />
                    </span>
                    <span class="text-[10px] font-bold border border-gray-200 rounded-md flex-grow">
                      Sökord
                    </span>
            
                  {:else if getNoteSizeState(yearGroup, monthGroup) === 'medium'}
                    <div class="text-gray-900 font-semibold flex justify-between">
                      {note.Dokumentnamn}
                      <NotePreview {note} />
                    </div>
                    <div class="text-gray-800 text-xs">
                      {new Date(note.DateTime).toLocaleDateString("sv-SE")}
                    </div>
                    <div class="text-gray-800 text-xs">
                      {note.Dokument_skapad_av_yrkestitel_Namn}
                    </div>
            
                  {:else}
                    <div class="text-gray-900 min-w-80 max-w-120 text-left text-xs">
                      <NotePreview {note} />
                      {@html note.CaseData}
                    </div>
                  {/if}
                </button>
              {/key}
            {/each}
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>
