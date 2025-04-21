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
</script>

<div class="relative h-full bg-gray-100 overflow-x-auto overflow-y-hidden">
  <div class="flex flex-row w-max h-full space-x-[2px]">
    {#each $noteHierarchy as yearGroup (yearGroup.year)}
      <div class="relative min-w-80 h-full flex flex-col">
        <button
          class="flex bg-purple-200 py-1 text-left px-2 w-full shadow-xs"
          on:click={() => toggleGroup(yearGroup)}
          aria-label="Toggle year {yearGroup.year}"
        >
          <div class="text-md sticky left-1 w-20 font-bold text-gray-900">
            {yearGroup.year}
          </div>
        </button>
        <div
          class="flex flex-grow {yearGroup.isCollapsed
            ? 'flex-col'
            : 'flex-row'} overflow-y-hidden space-x-[2px]"
        >
          {#each yearGroup.months as monthGroup}
            <div class="flex flex-col min-w-80">
              <button
                class="{yearGroup.isCollapsed
                  ? 'hidden'
                  : 'flex'} bg-purple-300 py-1 px-1 justify-between w-full shadow-xs"
                on:click={() => toggleGroup(monthGroup)}
                aria-label="Toggle month {monthGroup.month}"
              >
                <div
                  class="text-sm sticky left-1 px-1 w-20 font-semibold text-gray-900 text-left"
                >
                    {new Date(0, monthGroup.month).toLocaleString("sv-SE", {
                    month: "long",
                  })}
                </div>
              </button>
              <div
                class="relative flex {monthGroup.isCollapsed || yearGroup.isCollapsed
                  ? 'flex-col'
                  : 'flex-row'} overflow-y-hidden p-[2px] gap-[4px]"
              >
                {#each monthGroup.notes as note}
                  {#if yearGroup.isCollapsed}
                    <button
                      class="flex bg-white py-1 px-2 justify-between w-full rounded-md shadow-xs border border-gray-200"
                      on:click={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                    >
                      <div
                        class="text-gray-900 font-semibold text-left text-xs"
                      >
                        {note.Dokumentnamn}
                      </div>
                      <NotePreview {note} />
                    </button>
                  {:else if monthGroup.isCollapsed}
                    <button
                      class="flex bg-white py-1 px-2 outline-1 outline-gray-100 flex-col w-full text-sm text-left border-1 border-gray-200"
                      on:click={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                    >
                      <div class="text-gray-900 font-semibold flex justify-between">
                        {note.Dokumentnamn} <NotePreview {note} />
                      </div>
                      <div class="text-gray-800 text-xs">
                        {new Date(note.DateTime).toLocaleDateString("sv-SE")}
                      </div>
                      <div class="text-gray-800 text-xs">
                        {note.Dokument_skapad_av_yrkestitel_Namn}
                      </div>
                    </button>
                  {:else}
                    <button
                      class="flex bg-white p-2 outline-1 outline-gray-100 justify-between w-full h-full overflow-y-auto border-1 border-gray-200"
                      on:click={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                    >
                      <div
                        class="text-gray-900 min-w-80 max-w-120 text-left text-xs"
                      >
                      <NotePreview {note} />
                        {@html note.CaseData}
                      </div>
                    </button>
                  {/if}
                {/each}
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>
