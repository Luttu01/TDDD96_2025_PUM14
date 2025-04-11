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
    const groupsNotesWidth = countVisibleNotesWithinGroup([group]) * (BASEWIDTH * scale + NOTESPACING);
    // If the group is a month or day, we need to reduce width including it's parents padding
    const groupsWidthReduction = DATEGROUPPADDING * ("month" in group ? 2 : "day" in group ? 3 : 1)

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
    const index = $visibleNotes.findIndex(n => n === item);
    const halfNoteWidth = (BASEWIDTH * scale) / 2;
    const notePosition = index * ((BASEWIDTH * scale)+NOTESPACING);
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

    const foundIndex = $selectedNotes.findIndex(n => n.CaseData === noteData.CaseData);


    let newSelectedNotes = [...$selectedNotes];

    if (foundIndex >= 0) {
    
      newSelectedNotes.splice(foundIndex, 1);
    } else {
     
      newSelectedNotes.push(noteData);
    }

   
    selectedNotes.set(newSelectedNotes);
  }
</script>

<div class="h-full bg-gray-100 flex overflow-x-auto no-scrollbar relative">

  <!-- Timeline -->

  <div class="absolute top-0 left-0 pointer-events-none z-10">
    {#each $visibleNotes as item}
    {#if item.type === "note"}
        <div
          class="absolute w-3 h-3 bg-black rounded-full outline-2 outline-gray-100 pointer-events-none"
          style="
            left: {calculateNoteXPosition(item)}px;
            top: 0.5rem;
          "
        ></div>
      {/if}
    {/each}
  </div>
  <div class="w-max flex-col flex p-2 space-y-2">
    <div
      class="flex relative min-w-max px-[20px] justify-between"
      transition:fade={{ duration: 150 }}
    >
      {#each $noteHierarchy as yearGroup}
        <button
          on:click={(event) => toggleCollapse(yearGroup, event)}
          class="h-3 bg-purple-400 rounded-full outline-2 outline-gray-100"
          class:transition-width={$enableTransition}
          style="width: {calculateWidth(yearGroup)}px;"
          data-date={yearGroup.year}
          aria-label="Toggle year group"
        >
          {#if !yearGroup.isCollapsed}
            <div
              class="flex justify-between px-[20px]"
              transition:fade={{ duration: 150 }}
            >
              {#each yearGroup.months as monthGroup}
                <!-- svelte-ignore node_invalid_placement_ssr -->
                <button
                  on:click={(event) => toggleCollapse(monthGroup, event)}
                  class="h-3 bg-blue-400 rounded-full outline-2 outline-gray-100"
                  class:transition-width={$enableTransition}
                  style="width: {calculateWidth(monthGroup)}px; opacity: {monthGroup.days.length > 1 ? 1 : 0}; pointer-events: {monthGroup.days.length > 1 ? 'auto' : 'none'}"
                  data-date={monthGroup.month}
                  aria-label="Toggle month group"
                >
                  {#if !monthGroup.isCollapsed}
                    <div
                      class="flex justify-between px-[20px]"
                      transition:fade={{ duration: 150 }}
                    >
                      {#each monthGroup.days as dayGroup}
                        <button
                          on:click={(event) => toggleCollapse(dayGroup, event)}
                          class="h-3 bg-green-400 rounded-full outline-2 outline-gray-100"
                          class:transition-width={$enableTransition}
                          style="width: {calculateWidth(dayGroup)}px; opacity: {dayGroup.notes.length > 1 ? 1 : 0}; pointer-events: {dayGroup.notes.length > 1 ? 'auto' : 'none'}"
                          data-date={dayGroup.notes[0].DateTime}
                          aria-label="Toggle day group"
                        >
                      </button>
                      {/each}
                    </div>
                  {/if}
                </button>
              {/each}
            </div>
          {/if}
        </button>
      {/each}
    </div>

    <!-- Notes -->
    <div class="flex flex-grow space-x-1 overflow-hidden">
      {#each $visibleNotes as item (item.id)}
        <div class="flex flex-grow overflow-hidden" animate:flip={{ duration: 250 }}>
          {#if item.type === "summary"}
            <button
              transition:fade={{ duration: 150 }}
              class="bg-gray-200 flex-none p-1 rounded-md shadow-sm text-gray-700 overflow-y-auto"
              style="width: {BASEWIDTH * scale}px;"
              on:click={() => {
                if (item.context === "year") toggleCollapse(item.context);
                else if (item.context === "month") toggleCollapse(item.context);
                else if (item.context === "day") toggleCollapse(item.context);
              }}
            >
              {item.text}
            </button>
          {:else}
            <div
              transition:fade={{ duration: 150 }}
                class="flex-none p-4 rounded-md shadow-sm overflow-x-hidden { $selectedNotes?.find(n => n.CaseData === item.context.CaseData) ? 'bg-purple-100' : 'bg-white' }"
              style="width: {BASEWIDTH * scale}px;"
            >
              <div class="text-left text-sm text-gray-500 flex justify-between">
                {item.context.DateTime}
                <button class="h-6 w-6 rounded-md fa text-white { $selectedNotes?.find(n => n.CaseData === item.context.CaseData) ? 'bg-red-500 fa-caret-down' : 'bg-green-500 fa-caret-up' }"
                on:click={() => item.context.CaseData && handleNoteClick(item.context)} 
              class:selected={$selectedNotes?.find(n => n.CaseData === item.context.CaseData)}
              aria-label="select note"
                ></button>
              </div>
              <div class="h-full overflow-y-auto">
                {@html item.context.CaseData}
                </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .transition-width {
    transition: width 250ms ease-in-out;
  }
</style>
