<script lang="ts">
  import type { Note } from '$lib/models';
  import { onDestroy } from 'svelte';
  import { selectedNotes, filteredNotes, filter } from '$lib/stores';
  import NotePreview from './NotePreview.svelte';

  // Get notes from global store and sort them by date 
  let localItems : Note[] = $derived([...$filteredNotes]
      .map((item, index) => ({
        ...item,
        uniqueId: item.CompositionId || `${index}-${Date.now()}` 
      }))
      .sort((a, b) => new Date(b.DateTime).getTime() - new Date(a.DateTime).getTime())
  );

  // Reference to DOM element for the list container that is used to resize the list
  let listContainerElement: HTMLDivElement;

  let lastClickedIndex = $state(-1);

  // State for resizable list width functionality
  const MIN_LIST_WIDTH = 150; 
  const DEFAULT_LIST_WIDTH = 280; 
  let listWidth = $state(DEFAULT_LIST_WIDTH);
  let isDragging = $state(false);
  let initialX = $state(0);
  let initialWidth = $state(0);

  function formatDate(dateTimeString: string): string {
    return new Date(dateTimeString).toLocaleDateString('sv-SE');
  }

  function handleDocumentClick(clickedNote: Note, event: MouseEvent) {
    event.stopPropagation();

    // Find the index of the clicked note in our local array
    const currentIndex = localItems.findIndex(item => item.CompositionId === clickedNote.CompositionId);
    if (currentIndex === -1) return;

    // Handle shift+click for multi-select range
    if (event.shiftKey && lastClickedIndex !== -1) {
      // Select all notes between last clicked and current
      const start = Math.min(lastClickedIndex, currentIndex);
      const end = Math.max(lastClickedIndex, currentIndex);
      selectedNotes.set(localItems.slice(start, end + 1));
    } else {
      // Toggle selection for individual note
      const isAlreadySelected = $selectedNotes.some(note => note.CompositionId === clickedNote.CompositionId);

      if (isAlreadySelected) {
        // Deselect the note
        selectedNotes.update(current => current.filter(note => note.CompositionId !== clickedNote.CompositionId));
        if (lastClickedIndex === currentIndex) {
          lastClickedIndex = -1; // Reset last clicked if we deselected it
        }
      } else {
        // Add note to selection
        selectedNotes.update(current => [...current, clickedNote]);
        lastClickedIndex = currentIndex;
      }
    }
  }

  
  // Start resizing when mouse down on resize handle
  function handleMouseDown(event: MouseEvent) {
    isDragging = true;
    initialX = event.clientX;
    initialWidth = listContainerElement.offsetWidth;
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  }

  // Update width as mouse moves when dragging
  function handleMouseMove(event: MouseEvent) {
    if (!isDragging) return;
    const currentX = event.clientX;
    const dx = currentX - initialX;
    const newWidth = initialWidth + dx;
    listWidth = Math.max(MIN_LIST_WIDTH, newWidth); 
  }

  // Clean up event listeners when mouse released
  function handleMouseUp() {
    if (isDragging) {
      isDragging = false;
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    }
  }

  // Clean up any event listeners when component is destroyed
  onDestroy(() => {
    if (isDragging) {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    }
  });
</script>

<!-- List container -->
<div data-testid="list-view-container" class="list-container" bind:this={listContainerElement} style="width: {listWidth}px;">
  <ul data-testid="list-view" class="list-view" role="listbox" aria-multiselectable="true" aria-label="Clinical notes list">
    <!-- Iterate through sorted notes using CompositionId as unique key -->
    {#each localItems as item}
      <!-- List item-->
      <li data-testid="list-item-{item.CompositionId}" role="option" aria-selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)} class="document-list-item">
        <button
          data-testid="list-item-button-{item.CompositionId}"
          type="button"
          class="document-button"
          class:selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)}
          onclick={(e) => handleDocumentClick(item, e)}
        >
          <div class="document-item">
            <div id="document-header">
              <h3>{item.Dokumentnamn}</h3>
              <NotePreview note={ item }/>
            </div>
            <div class="document-meta">
              <span>{formatDate(item.DateTime)} -</span>
              <span>{item.Dokument_skapad_av_yrkestitel_Namn} -</span>
              <span>{item.Vårdenhet_Namn}</span>
            </div>
          </div>
        </button>
      </li>
    {/each}
  </ul>
  <!-- Resize handle for adjusting list width -->
  <button 
    data-testid="resize-handle" 
    class="resize-handle" 
    onmousedown={handleMouseDown}
    aria-label="Resize list width"
    type="button"
  ></button>
</div>

<style>
  /* Main container for the list with resizable width */
  .list-container {
    position: relative;
    overflow: hidden; 
    height: 100%; 
    min-width: 150px; 
    max-width: 500px;
    border: 1px solid #ccc; 
    background-color: white;
  }

  /* Scrollable list of documents */
  .list-view {
    list-style: none;
    padding: 0;
    margin: 0;
    height: 100%; 
    overflow-y: auto; 
  }

  /* Individual list items with border between them */
  .document-list-item {
    margin: 0;
    border-bottom: 2px solid #e0e0e0;
  }

  .document-list-item:last-child {
    border-bottom: none;
  }

  /* Button styling for each document in the list */
  .document-button {
    width: 100%;
    padding: 0.2rem 1rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s;
  }

  .document-button:hover {
    background-color: #f5f5f5;
  }

  /* Selected document styling with left border accent */
  .document-button.selected {
    background-color: #e3f2fd;
    border-left: 4px solid #3b82f6;
    padding-left: calc(1rem - 4px);
  }

  .document-button.selected:hover {
    background-color: #bbdefb;
  }

  /* Document title styling with text overflow handling */
  .document-item h3 {
    margin: 0 0 0.1rem 0;
    color: #333;
    font-size: 0.85rem;
    font-weight: 700;
    white-space: nowrap; 
    overflow: hidden;
    text-overflow: ellipsis;
  }

  #document-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  /* Metadata sections with overflow handling */
  .document-meta {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Document metadata (type and date) */
  .document-meta {
    display: flex;
    flex-wrap: row;
    font-size: 0.75rem;
    font-weight: 400;
    color: #555;
  }

  /* Resize handle on the right side of the list */
  .resize-handle {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 5px; 
    cursor: col-resize;
    background-color: rgba(0, 0, 0, 0.1); 
  }

  .resize-handle:hover {
    background-color: rgba(0, 0, 0, 0.3);
  }
</style>
