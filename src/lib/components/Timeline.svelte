<script lang="ts">
  import { onMount } from "svelte";
  import { flip } from "svelte/animate";
  import { writable } from "svelte/store";

  import type { Note, Year } from "$lib/models";
  import { buildDateHierarchy, countVisibleNotesWithinGroup } from "$lib/utils";
  import { allNotes, selectedNotes } from "$lib/stores";

  let scale: number = 1;
  const ZOOMSPEED: number = 0.06;
  const MINSCALE: number = 1;
  const MAXSCALE: number = $allNotes.length / 4;

  const noteHierarchy = writable<Year[]>(buildDateHierarchy($allNotes));

  $: scale;

  function handleZoom(event: WheelEvent): void {
    if (event.ctrlKey) {
      event.preventDefault();
      scale -= event.deltaY * ZOOMSPEED;
      scale = Math.min(MAXSCALE, Math.max(MINSCALE, scale));
    }
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

<div class="relative h-full bg-gray-100 overflow-x-auto overflow-y-hidden">
  <div
    class="relative flex h-full @container"
    style="width: calc(100vw * {scale});"
  >
    <!-- Hierarchical Date Structure -->
    <div class="relative flex flex-grow h-full">
      {#each $noteHierarchy as yearGroup}
        <div
          class="relative flex flex-col flex-grow"
        >
          <div class="flex bg-purple-200 py-1 px-2 outline-1 outline-gray-100 justify-between">
            <div class="text-lg sticky left-0 w-10 font-bold text-gray-900">
              {yearGroup.year}
            </div>
          </div>
          <div class="relative flex flex-1 flex-col @min-[200vw]:flex-row">
            {#each yearGroup.months as monthGroup}
                <div
                class="flex-col flex @min-[200vw]:flex-1"
              >
                <div
                  class="relative bg-purple-300 py-1 px-2 outline-1 outline-gray-100 hidden @min-[200vw]:flex"
                >
                  <div
                    class="text-md sticky left-0 w-20 font-medium text-gray-800"
                  >
                    {new Date(0, monthGroup.month).toLocaleString("default", {
                      month: "long",
                    })}
                  </div>
                </div>
                <div class="relative flex-col">
                  {#each monthGroup.notes as note (note.Dokument_ID)}
                    <div class="bg-white p-1 m-1 rounded-full shadow-sm h-6 text-sm justify-between flex-row flex">
                      <p class="overflow-hidden">{note.Dokumentnamn}</p>
                      <button 
                        class="rounded-full bg-green-500 w-4 h-4 text-white text-xs"
                        on:click={() => handleNoteClick(note)}
                        aria-label="Remove note {note.Dokumentnamn}"
                      >^</button>
                    </div>
                  {/each}
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>
