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
    if (yearGroup.isCollapsed) return "compact";
    if (monthGroup.isCollapsed) return "medium";
    return "expanded";
  }

  function isInSelectedNotes(note: Note) {
    return $selectedNotes.some((n) => n.CaseData === note.CaseData);
  }
</script>

<div class="relative flex h-full bg-gray-100 overflow-x-auto overflow-y-hidden">
  <div class="flex flex-row w-max h-full space-x-[2px]">
    {#each $noteHierarchy as yearGroup (yearGroup.year)}
      <div class="relative h-full flex flex-col">
        <button
          class="flex bg-purple-200 py-1 text-left text-sm px-2 w-full shadow-xs justify-between {yearGroup.isCollapsed ? 'cursor-zoom-in' : 'cursor-zoom-out'}"
          on:click={() => toggleGroup(yearGroup)}
          aria-label="Toggle year {yearGroup.year}"
        >
          <div class="text-md sticky left-1 w-10 font-bold text-gray-900">
            {yearGroup.year}
          </div>   
        </button>
        <div class="flex flex-grow flex-row space-x-[2px]">
          {#each yearGroup.months as monthGroup}
            <div class="flex flex-col">
              <button
                class="{yearGroup.isCollapsed
                  ? 'h-0 py-0'
                  : 'h-6 py-1'} flex bg-purple-300 px-1 justify-between w-full shadow-xs transition-all duration-300 {monthGroup.isCollapsed ? 'cursor-zoom-in' : 'cursor-zoom-out'}"
                on:click={() => toggleGroup(monthGroup)}
                aria-label="Toggle month {monthGroup.month}"
              >
                <div
                  class="{yearGroup.isCollapsed
                    ? 'text-transparent'
                    : 'text-gray-900'} text-xs sticky left-1 px-1 w-10 font-semibold text-left"
                >
                  {new Date(0, monthGroup.month).toLocaleString("sv-SE", {
                    month: "short",
                  })}
                </div>                
              </button>
              <div
                class="relative flex flex-row overflow-hidden p-[2px] gap-[4px]"
              >
                {#each monthGroup.notes as note}
                  {#key note.Dokument_ID}
                    <button
                      class={`transition-all mt-2 duration-300 border rounded-md shadow-xs ${isInSelectedNotes(note) ? 'bg-purple-50 border-purple-300 hover:bg-purple-100' : 'bg-white border-gray-200 hover:bg-gray-50'} relative cursor-pointer ${
                        getNoteSizeState(yearGroup, monthGroup) === "compact"
                          ? "flex flex-col py-2 px-1 w-13 space-y-1"
                          : getNoteSizeState(yearGroup, monthGroup) === "medium"
                            ? "flex flex-col p-2 w-45 text-sm text-left"
                            : "flex justify-between p-2 w-100"
                      }`}
                      on:click={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                    >
                      <div
                        class="transition-all duration-300 absolute -top-2.5 left-1/2 -translate-x-1/2 w-0 h-0
              border-l-10 border-r-10 border-b-10 border-transparent {isInSelectedNotes(note) ? 'border-b-purple-300' : 'border-b-white'}"
                      ></div>
                      {#if getNoteSizeState(yearGroup, monthGroup) === "compact"}
                        <span class="text-[10px] text-gray-500">
                          {new Date(note.DateTime).toLocaleDateString("sv-SE", {
                            month: "2-digit",
                            day: "2-digit",
                          })}
                        </span>
                        <span class="h-16">
                          <NotePreview note={note} direction="flex-col" />
                        </span>
                        <span
                          class="text-[10px] font-medium border-t-1 border-gray-200"
                        >
                          Sökord
                          <span class="text-[10px] font-light text-gray-500">
                            (inga)
                          </span>
                        </span>
                        
                      {:else if getNoteSizeState(yearGroup, monthGroup) === "medium"}
                      <div class="text-gray-500 text-xs flex justify-between border-b-1 border-gray-200 pb-1">
                        {new Date(note.DateTime).toLocaleDateString("sv-SE")}
                        <NotePreview note={note} />
                      </div>
                      <div class="h-20">
                        <div
                          class="text-gray-900 font-semibold flex justify-between"
                        >
                          {note.Dokumentnamn}
                        </div>
                        <div class="text-gray-800 text-xs">
                          {note.Dokument_skapad_av_yrkestitel_Namn}
                        </div>
                        <div class="text-gray-800 text-xs pb-2">
                          {note.Vårdenhet_Namn}
                        </div>
                      </div>
                        <span
                          class="text-sm font-medium border-t-1 border-gray-200 flex-grow flex flex-col"
                        >
                          Sökord
                          <span class="text-sm font-light text-gray-500">
                            (inga)
                          </span>
                        </span>
                      {:else}
                        <div class="text-gray-900 text-left text-xs w-full flex flex-col">
                          <div class="text-gray-500 text-xs flex justify-between border-b-1 border-gray-200 pb-1">
                            {new Date(note.DateTime).toLocaleDateString("sv-SE")}
                            <NotePreview note={note} />
                          </div>
                          <!-- Temporary fix with max-h -->
                          <div class="overflow-y-auto w-full max-h-[280px]">
                            {@html note.CaseData}
                          </div>
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
