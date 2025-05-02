<script lang="ts">
    import { selectedNotes } from "$lib/stores/storedNotes";
    import { derived, writable } from "svelte/store";
    import type { Note } from "$lib/models";
    import { searchQuery } from '$lib/stores/searchStore';
    import SearchInput from "./SearchInput.svelte";
    import { onMount } from "svelte";
    import interact from "interactjs";
    import { powerMode } from "$lib/stores";
    
    let interactInstance: any;
    let initialPositions = new Map<string, { x: number; y: number }>();
    let showSearchInput = false;

    function handleNoteClick(noteData: Note) {
    $selectedNotes = $selectedNotes || []; 

    const foundIndex = $selectedNotes.findIndex(n => n.CaseData === noteData.CaseData);


    let newSelectedNotes = [...$selectedNotes]; // Copy array

    if (foundIndex >= 0) {
      newSelectedNotes.splice(foundIndex, 1);
    }
    selectedNotes.set(newSelectedNotes);
  }

  /*
   * Markerar sökord i anteckningar baserat på input.
   * För att behålla strukturen på anteckningen skapas en temporär kopia med highlightad text
   * som sedan byter ut orginalet. Detta görs för samtliga valda anteckningar. 
   */
  function highlightMatches(html: string, query: string): string {
    if (!query) return html;

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

  onMount(() => {
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


<div class="h-full bg-gray-100 flex">
  {#if showSearchInput}
    <div id="SearchInput" class="fixed top-10 left-1/2 transform -translate-x-1/2 z-50 bg-white rounded-md shadow-lg max-w-md w-[90%] p-2">
      <SearchInput on:close={() => showSearchInput = false} />
    </div>
  {/if}
    <div class="flex-1 overflow-x-auto p-2">
      <div class="flex space-x-2 h-full min-w-full">
        {#each $selectedNotes as note (note.CaseData)}
          <div class="w-[100vw] bg-white p-4 rounded-lg shadow-md">
            <div class="text-left text-sm text-gray-500 flex justify-between">
              {note?.DateTime}
              <button class="h-6 w-6 bg-red-500 rounded-md fa fa-caret-down text-white"
                on:click={() => note?.CaseData && handleNoteClick(note)} 
                class:selected={$selectedNotes?.find(n => n.CaseData === note?.CaseData)}
                aria-label="deselect note"
              ></button>
            </div>
            <div class="h-full overflow-y-auto">
              {@html highlightMatches(note.CaseData, $searchQuery)}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>