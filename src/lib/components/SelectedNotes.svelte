<script lang="ts">
  import { browser } from "$app/environment";
  import { onMount } from "svelte";
  import interact from "interactjs";
  import { selectedNotes } from "$lib/stores";
  import type { Note } from "$lib/models";
  import SearchInput from "./SearchInput.svelte";
  import { searchQuery } from "$lib/stores/searchStore";
  import { powerMode } from "$lib/stores";
  import { stringToColor } from "$lib/utils";
  import NotePreview from "$lib/components/NotePreview.svelte";

  
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
  if (!browser) return;

  if ($powerMode) {
    setupInteract();
  }

  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      showSearchInput = true;
    }
  });
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

  function highlightMatches(html: string, query: string): string {
    if (!browser || !query) return html;

    const escapedQuery = query.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
    const regex = new RegExp(`(${escapedQuery})`, 'gi');

    const container = document.createElement('div');
    container.innerHTML = html;

    function walk(node: Node) {
      if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent;
        if (text) {
          const newText = text.replace(regex, '<mark>$1</mark>');
          if (newText !== text) {
            const span = document.createElement('span');
            span.innerHTML = newText;
            (node as ChildNode).replaceWith(...Array.from(span.childNodes));
          }
        }
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        for (const child of Array.from(node.childNodes)) {
          walk(child);
        }
      }
    }

    walk(container);

    return container.innerHTML;
  }

  /**
   * Show search field after ctrl+f / cmd+f
  */
  let showSearchInput = false;

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
  class="flex-grow w-full relative overflow-hidden bg-gray-100 {$powerMode
    ? ''
    : 'no-gridlines'}"
>
  {#if $selectedNotes.length <= 0}
    <div id="Absence_of_notes" class="flex items-center justify-center h-full">
      <p class="text-gray-400 text-lg">Tryck på Journalanteckningar i listan eller tidslinjen för att öppna här</p>
    </div>
  {/if}
  {#if showSearchInput}
  <div id="SearchInput" class="fixed top-10 left-1/2 transform -translate-x-1/2 z-50 bg-white rounded-md shadow-lg max-w-md w-[90%] p-2">
    <SearchInput on:close={() => showSearchInput = false} />
  </div>
  {/if}
  {#if $powerMode}
    {#each $selectedNotes as note, i (note.CaseData)}
      <div
        id="note_nr_{i}"
        class="draggable bg-white rounded-lg shadow-md flex flex-col overflow-hidden"
        style="transform: translate({initialPositions.get(note.CaseData)?.x ||
          0}px, {initialPositions.get(note.CaseData)?.y || 0}px);"
        on:mousedown={() => {}}
        role="button"
        tabindex="0"
        aria-label="Draggable note"
      >
        <div
          id="note_date_{i}"
          class="text-left text-xs text-gray-500 flex justify-between items-center font-mono p-2 border-b border-gray-200 cursor-move h-8"
        >
            {new Date(note?.DateTime).toLocaleDateString('sv-SE', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            })}
            <div id="note_preview_{i}" class="flex items-center space-x-2">
          <NotePreview {note} />
          <button
            class="font-bold text-lg font-sans text-red-500 hover:text-red-700"
            on:click={() => handleNoteClick(note)}
            aria-label="deselect note"
          >X</button>
            </div>
        </div>
        <div id="note_keywords_{i}" class="flex-1 overflow-y-auto p-4 text-xs">
          {@html highlightMatches(note.CaseData.replace(
            new RegExp(
              `(<b>(${note.keywords.join("|")})</b>)`,
              "gi"
            ),
            (match, p1, p2) =>
              `<span style="background-color: ${stringToColor(p2)}; font-weight: bold;">${p2}</span>`
            ), $searchQuery)}
        </div>
      </div>
    {/each}
  {:else}
    <div id="normal_note_collection" class="h-full bg-gray-100 flex overflow-hidden">
      <div id="note_collection_container" class="flex-1 overflow-x-auto p-2">
        <div id="note_collection_container_2" class="flex space-x-2 h-full min-w-full">
          {#each $selectedNotes as note, i (note.CaseData)}
            <div id="normal_note_{i}" class="w-[100vw] min-w-120 bg-white rounded-lg shadow-md flex-grow overflow-hidden">
              <div id="normal_note_info_{i}" class="text-left text-xs text-gray-500 flex justify-between items-center border-b border-gray-200 px-2 font-mono">
                {new Date(note?.DateTime).toLocaleDateString('sv-SE', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit',
                  })}
                  <div id="normal_note_preview_{i}" class="flex items-center space-x-2">
                  <NotePreview {note} />
                <button
                  class="font-bold text-lg font-sans text-red-500 hover:text-red-700"
                  on:click={() => note?.CaseData && handleNoteClick(note)}
                  class:selected={$selectedNotes?.find(
                    (n) => n.CaseData === note?.CaseData
                  )}
                  aria-label="deselect note"
                >X</button>
                  </div>
              </div>
              <div id="normal_note_matches_{i}" class="h-full overflow-y-auto text-xs p-2">
                {@html highlightMatches(note.CaseData.replace(
                  new RegExp(
                  `(<b>(${note.keywords.join("|")})</b>)`,
                  "gi"
                  ),
                  (match, p1, p2) =>
                  `<span style="background-color: ${stringToColor(p2)}; font-weight: bold;">${p2}</span>`
                  ), $searchQuery)}
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
