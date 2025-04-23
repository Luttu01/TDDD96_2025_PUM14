<script lang="ts">
  import { onMount } from "svelte";
  import interact from "interactjs";
  import { selectedNotes } from "$lib/stores";
  import type { Note } from "$lib/models";
  import { powerMode } from "$lib/stores";

  
  let interactInstance: any;
  let initialPositions = new Map<string, { x: number; y: number }>();

  function handleNoteClick(noteData: Note) {
    $selectedNotes = $selectedNotes || [];
    const foundIndex = $selectedNotes.findIndex(
      (n) => n.CaseData === noteData.CaseData
    );
    let newSelectedNotes = [...$selectedNotes];
    if (foundIndex >= 0) {
      newSelectedNotes.splice(foundIndex, 1);
    }
    selectedNotes.set(newSelectedNotes);
  }

  onMount(() => {
    if ($powerMode) {
      setupInteract();
    }
  });

  function setupInteract() {
    interact(".draggable").unset();
    interactInstance = interact(".draggable")
      .draggable({
        inertia: true,
        modifiers: [
          interact.modifiers.snap({
            targets: [interact.snappers.grid({ x: 50, y: 50 })],
            range: Infinity,
            relativePoints: [{ x: 0, y: 0 }],
          }),
          interact.modifiers.restrictRect({
            restriction: "parent",
            endOnly: true,
          }),
        ],
        listeners: {
          move(event) {
            const target = event.target;
            const x =
              (parseFloat(target.getAttribute("data-x")) || 0) + event.dx;
            const y =
              (parseFloat(target.getAttribute("data-y")) || 0) + event.dy;

            target.style.transform = `translate(${x}px, ${y}px)`;
            target.setAttribute("data-x", x);
            target.setAttribute("data-y", y);
          },
        },
      })
      .resizable({
        edges: { left: true, right: true, bottom: true, top: true },
        modifiers: [
          interact.modifiers.snapSize({
            targets: [interact.snappers.grid({ width: 50, height: 50 })],
          }),
          interact.modifiers.restrictSize({
            min: { width: 200, height: 150 },
            max: { width: 1000, height: 1000 },
          }),
        ],
        inertia: true,
        listeners: {
          move(event) {
            const target = event.target;
            const { width, height } = event.rect;

            target.style.width = `${width}px`;
            target.style.height = `${height}px`;
          },
        },
      });
  }

  $: if ($powerMode) {
    setupInteract();
    $selectedNotes.forEach((note) => {
      if (!initialPositions.has(note.CaseData)) {
        initialPositions.set(note.CaseData, {
          x: Math.random() * 50,
          y: Math.random() * 50,
        });
      }
    });
  }

  $: if (!$powerMode && interactInstance) {
    interactInstance.unset();
    interactInstance = null;
  }
</script>

<!-- 🧭 Main Layout -->
<div
  id="main-container"
  class="h-[100vh] w-full relative overflow-auto bg-gray-100 {$powerMode
    ? ''
    : 'no-gridlines'}"
>
  {#if $powerMode}
    {#each $selectedNotes as note, i (note.CaseData)}
      <div
        class="draggable bg-white rounded-lg shadow-md flex flex-col overflow-hidden"
        style="transform: translate({initialPositions.get(note.CaseData)?.x ||
          0}px, {initialPositions.get(note.CaseData)?.y || 0}px);"
        on:mousedown={() => {}}
        role="button"
        tabindex="0"
        aria-label="Draggable note"
      >
        <div
          class="text-left text-sm text-gray-500 flex justify-between p-4 border-b bg-gray-50 cursor-move"
        >
          {note?.DateTime}
          <button
            class="h-6 w-6 bg-red-500 rounded-md fa fa-caret-down text-white"
            on:click={() => handleNoteClick(note)}
            aria-label="deselect note"
          ></button>
        </div>
        <div class="flex-1 overflow-y-auto p-4 text-sm">
          {@html note.CaseData}
        </div>
      </div>
    {/each}
  {:else}
    <div class="h-full bg-gray-100 flex">
      <div class="flex-1 overflow-x-auto p-2">
        <div class="flex space-x-2 h-full min-w-full">
          {#each $selectedNotes as note (note.CaseData)}
            <div class="w-[100vw] bg-white p-4 rounded-lg shadow-md">
              <div class="text-left text-sm text-gray-500 flex justify-between">
                {note?.DateTime}
                <button
                  class="h-6 w-6 bg-red-500 rounded-md fa fa-caret-down text-white"
                  on:click={() => note?.CaseData && handleNoteClick(note)}
                  class:selected={$selectedNotes?.find(
                    (n) => n.CaseData === note?.CaseData
                  )}
                  aria-label="deselect note"
                ></button>
              </div>
              <div class="h-full overflow-y-auto">
                {@html note.CaseData}
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .draggable {
    position: absolute;
    width: 400px;
    height: 300px;
    user-select: none;
    touch-action: none;
    box-sizing: border-box;
  }

  #main-container {
    background-size: 50px 50px;
    background-image: linear-gradient(to right, #e5e7eb 1px, transparent 1px),
      linear-gradient(to bottom, #e5e7eb 1px, transparent 1px);
  }

  #main-container.no-gridlines {
    background-image: none;
  }
</style>
