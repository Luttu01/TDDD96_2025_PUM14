<script lang="ts">
  import { onMount } from "svelte";
  import { derived, writable } from "svelte/store";
  import { flip } from "svelte/animate";
  import { fade } from "svelte/transition";

  import type { Note, Year, Month, Day } from "$lib/models";
  import {
    buildDateHierarchy,
    buildVisibleNotes,
    countVisibleNotesWithinGroup,
  } from "$lib/utils";
  import { allNotes, selectedNotes } from "$lib/stores";

  let scale: number = 1;
  const ZOOMSPEED: number = 0.01;
  const MINSCALE: number = 0.5;
  const MAXSCALE: number = 3;
  const BASEWIDTH: number = 320;
  const DATEGROUPPADDING: number = 40;
  const NOTESPACING: number = 4;

  const noteHierarchy = writable<Year[]>(buildDateHierarchy($allNotes));
  const visibleNotes = derived(noteHierarchy, ($noteHierarchy) => {
    return buildVisibleNotes($noteHierarchy);
  });

  let enableTransition = writable(false);
  $: scale, enableTransition.set(false);

  function toggleCollapse(
    group: { isCollapsed: boolean },
    event?: Event
  ): void {
    if (event) event.stopPropagation();
    setTimeout(() => enableTransition.set(true), 300);
    group.isCollapsed = !group.isCollapsed;
    noteHierarchy.update((n) => [...n]);
  }

  function calculateWidth(group: Year | Month | Day) {
    const groupsNotesWidth =
      countVisibleNotesWithinGroup([group]) * (BASEWIDTH * scale + NOTESPACING);
    // If the group is a month or day, we need to reduce width including it's parents padding
    const groupsWidthReduction =
      DATEGROUPPADDING * ("month" in group ? 2 : "day" in group ? 3 : 1);

    return groupsNotesWidth - groupsWidthReduction;
  }

  function handleZoom(event: WheelEvent): void {
    if (event.ctrlKey) {
      event.preventDefault();
      scale -= event.deltaY * ZOOMSPEED;
      scale = Math.min(MAXSCALE, Math.max(MINSCALE, scale));
    }
  }

  function calculateNoteXPosition(item: { note?: Note; type: string }) {
    const index = $visibleNotes.findIndex((n) => n === item);
    const halfNoteWidth = (BASEWIDTH * scale) / 2;
    const notePosition = index * (BASEWIDTH * scale + NOTESPACING);
    return notePosition + halfNoteWidth;
  }

  onMount(() => {
    window.addEventListener("wheel", handleZoom, { passive: false });
    return () => {
      window.removeEventListener("wheel", handleZoom);
    };
  });

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

<div class="relative h-full bg-gray-100 overflow-x-auto no-scrollbar">
  <div
    class="relative flex space-x-4 h-full px-2 border-2 border-red-500"
    style="width: calc(600vw * {scale});"
  >
    <!-- Hierarchical Date Structure -->
    <div class="relative flex flex-grow space-x-4 h-full px-2">
      {#each $noteHierarchy as yearGroup}
        <div class="relative flex flex-col flex-grow">
          <div class="flex bg-purple-200 py-1 px-6 rounded-b-full">
            <div class="text-lg sticky left-0 w-20 font-bold text-gray-900">
              {yearGroup.year}
            </div>
          </div>
          {#if !yearGroup.isCollapsed}
            <div class="flex space-x-4 flex-grow px-8">
              {#each yearGroup.months as monthGroup}
                <div class="flex flex-col flex-grow">
                  <div class="flex bg-purple-300 py-1 px-6 rounded-b-full">
                    <div
                      class="text-md sticky left-0 w-20 font-medium text-gray-800"
                    >
                      {new Date(0, monthGroup.month).toLocaleString("default", {
                        month: "long",
                      })}
                    </div>
                  </div>
                  {#if !monthGroup.isCollapsed}
                    <div class="flex space-x-4 flex-grow px-8">
                      {#each monthGroup.days as dayGroup}
                        <div class="flex flex-col flex-grow">
                          <div
                            class="flex bg-purple-400 py-1 px-6 rounded-b-full"
                          >
                            <div
                              class="text-sm sticky left-0 w-4 text-gray-800"
                            >
                              {dayGroup.day + 1}
                            </div>
                          </div>
                          <div class="flex flex-col space-x-2 pb-2 flex-grow">
                            {#each dayGroup.notes as note}
                              <div class="bg-white p-2 rounded-md w-80">
                                <h3>{note.Dokumentnamn}</h3>
                                <div class="text-xs text-gray-500">
                                  {note.Dokument_skapad_av_yrkestitel_Namn}
                                </div>
                              </div>
                            {/each}
                          </div>
                        </div>
                      {/each}
                    </div>
                  {/if}
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
</div>
