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
  import { allNotes } from "$lib/stores";

  let scale: number = 1;
  const zoomSpeed: number = 0.01;
  const minScale: number = 0.5;
  const maxScale: number = 1.5;
  const baseWidth: number = 320;
  const buttonPaddingX: number = 20;

  const noteHierarchy = writable<Year[]>(buildDateHierarchy($allNotes));
  const visibleNotes = derived(noteHierarchy, ($noteHierarchy) => {
    return buildVisibleNotes($noteHierarchy);
  });

  let enableTransition = writable(false);
  $: scale, enableTransition.set(false);

  let currentDate: string = "";
  let timelineContainer: HTMLDivElement;

  let buttons: HTMLElement[] = [];

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
    return (
      baseWidth * countVisibleNotesWithinGroup([group]) * scale +
      4 * countVisibleNotesWithinGroup([group]) -
      buttonPaddingX * 2 * ("month" in group ? 2 : "day" in group ? 3 : 1)
    );
  }

  function handleZoom(event: WheelEvent): void {
    if (event.ctrlKey) {
      event.preventDefault();
      scale -= event.deltaY * zoomSpeed;
      scale = Math.min(maxScale, Math.max(minScale, scale));
    }
  }

  function registerButton(node: HTMLElement) {
    buttons.push(node);
    return {
      destroy() {
        buttons = buttons.filter((b) => b !== node);
      }
    };
  }

  function updateCurrentDate() {
    const targetX = window.innerWidth / 2;
    let closest: HTMLElement | null = null;
    let minDistance = Infinity;
    buttons.forEach((btn) => {
      const rect = btn.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const distance = Math.abs(centerX - targetX);
      if (distance < minDistance) {
        minDistance = distance;
        closest = btn as HTMLElement;
      }
    });
    if (closest) {
      currentDate = (closest as HTMLElement).getAttribute('data-date') || "";
    }
  }

  onMount(() => {
    window.addEventListener("wheel", handleZoom, { passive: false });
    updateCurrentDate();
    window.addEventListener('wheel', updateCurrentDate);
    return () => {
      window.removeEventListener("wheel", handleZoom);
      window.removeEventListener('wheel', updateCurrentDate);
    };
  });
</script>

<div class="hidden w-full text-center transform bg-gray-800 text-white text-sm rounded shadow z-10">
  {currentDate}
</div>

<div class="h-full bg-gray-100 flex overflow-x-auto no-scrollbar" bind:this={timelineContainer}>
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
                  style="width: {calculateWidth(monthGroup)}px;"
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
                          use:registerButton
                          class="h-3 bg-green-400 rounded-full outline-2 outline-gray-100"
                          class:transition-width={$enableTransition}
                          style="width: {calculateWidth(dayGroup)}px;"
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
    <div class="flex flex-grow space-x-1 overflow-hidden">
      {#each $visibleNotes as item (item.type === "note" ? item.note?.DateTime : item.text)}
        <div class="flex flex-grow overflow-hidden" animate:flip={{ duration: 250 }}>
          {#if item.type === "summary"}
            <button
              transition:fade={{ duration: 150 }}
              class="bg-gray-200 flex-none p-1 rounded-md shadow-sm text-gray-700 overflow-y-auto"
              style="width: {baseWidth * scale}px;"
              on:click={() => {
                if (item.year) toggleCollapse(item.year);
                else if (item.month) toggleCollapse(item.month);
                else if (item.day) toggleCollapse(item.day);
              }}
            >
              {item.text}
            </button>
          {:else}
            <div
              transition:fade={{ duration: 150 }}
              class="bg-white flex-none p-2 rounded-md shadow-sm overflow-y-auto overflow-x-hidden"
              style="width: {baseWidth * scale}px;"
            >
              <div class="text-left text-sm text-gray-500">
                {item.note?.DateTime}
              </div>
                {@html item.note?.CaseData}
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
