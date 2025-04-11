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
  const MAXSCALE: number = 1.5;
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


<div class="relative h-full bg-gray-100 overflow-x-auto no-scrollbar p-4 pb-0">
  <!-- Hierarchical Date Structure -->
  <div class="relative flex space-x-4 h-full">
    {#each $noteHierarchy as yearGroup}
      <div class="relative bg-purple-200 p-2 pb-0 space-y-2 rounded-t-md flex flex-col flex-grow">
        <div class="text-lg sticky left-0 w-20 font-bold text-gray-900">{yearGroup.year}</div>
        {#if !yearGroup.isCollapsed}
          <div class="flex space-x-4 flex-grow">
            {#each yearGroup.months as monthGroup}
              <div class="bg-purple-300 p-2 pb-0 space-y-2 rounded-t-md flex flex-col flex-grow">
                <div class="text-md sticky left-0 w-20 font-medium text-gray-800">
                  {new Date(0, monthGroup.month).toLocaleString("default", {month: "long"})}
                </div>
                {#if !monthGroup.isCollapsed}
                  <div class="flex space-x-4 flex-grow">
                    {#each monthGroup.days as dayGroup}
                      <div class="bg-purple-400 p-2 pb-0 space-y-2 rounded-t-md flex flex-col">
                        <div class="text-sm sticky left-0 w-4 text-gray-800">
                          {dayGroup.day + 1}
                        </div>
                        <div class="flex space-x-2 pb-2 flex-grow">
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
