<script lang="ts">
  import type { Note } from '$lib/models';
  import { onDestroy } from 'svelte';
  import { allNotes, selectedNotes } from '$lib/stores';

  let localItems = $derived([...$allNotes]
      .map((item, index) => ({
        ...item,
        uniqueId: item.CompositionId || `${index}-${Date.now()}` 
      }))
      .sort((a, b) => new Date(b.DateTime).getTime() - new Date(a.DateTime).getTime())
  );

  let listContainerElement: HTMLDivElement;
  let lastClickedIndex = $state(-1);

  let listWidth = $state(300);
  let isDragging = $state(false);
  let initialX = $state(0);
  let initialWidth = $state(0);

  function formatDate(dateTimeString: string): string {
    return new Date(dateTimeString).toLocaleDateString('sv-SE');
  }

  function handleDocumentClick(clickedNote: Note, event: MouseEvent) {
    event.stopPropagation();

    const currentIndex = localItems.findIndex(item => item.CompositionId === clickedNote.CompositionId);
    if (currentIndex === -1) return;

    if (event.shiftKey && lastClickedIndex !== -1) {
      const start = Math.min(lastClickedIndex, currentIndex);
      const end = Math.max(lastClickedIndex, currentIndex);
      selectedNotes.set(localItems.slice(start, end + 1));
    } else {
      const isAlreadySelected = $selectedNotes.some(note => note.CompositionId === clickedNote.CompositionId);

      if (isAlreadySelected) {
        selectedNotes.update(current => current.filter(note => note.CompositionId !== clickedNote.CompositionId));
        if (lastClickedIndex === currentIndex) {
          lastClickedIndex = -1;
        }
      } else {
        selectedNotes.update(current => [...current, clickedNote]);
        lastClickedIndex = currentIndex;
      }
    }
  }

  function handleMouseDown(event: MouseEvent) {
    isDragging = true;
    initialX = event.clientX;
    initialWidth = listContainerElement.offsetWidth;
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  }

  function handleMouseMove(event: MouseEvent) {
    if (!isDragging) return;
    const currentX = event.clientX;
    const dx = currentX - initialX;
    const newWidth = initialWidth + dx;
    listWidth = Math.max(150, newWidth);
  }

  function handleMouseUp() {
    if (isDragging) {
      isDragging = false;
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    }
  }

  onDestroy(() => {
    if (isDragging) {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    }
  });
</script>

<div data-testid="list-view-container" class="list-container" bind:this={listContainerElement} style="width: {listWidth}px;">
  <ul data-testid="list-view" class="list-view" role="listbox">
    {#each localItems as item (item.CompositionId)}
      <li data-testid="list-item-{item.CompositionId}" role="option" aria-selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)} class="document-list-item">
        <button
          data-testid="list-item-button-{item.CompositionId}"
          type="button"
          class="document-button"
          class:selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)}
          onclick={(e) => handleDocumentClick(item, e)}
        >
          <div class="document-item">
            <h3>{item.Dokumentnamn}</h3>
            <div class="document-meta">
              <span class="type">{item.Dokumentationskod}</span>
              <span class="date">{formatDate(item.DateTime)}</span>
            </div>
            <div class="document-details">
              <span class="professional">{item.Dokument_skapad_av_yrkestitel_Namn}</span>
              <span class="unit">Unit: {item.Vårdenhet_Namn}</span>
            </div>
          </div>
        </button>
      </li>
    {/each}
  </ul>
  <button 
    data-testid="resize-handle" 
    class="resize-handle" 
    onmousedown={handleMouseDown}
    aria-label="Resize list width"
    type="button"
  ></button>
</div>

<style>
  .list-container {
    position: relative;
    overflow: hidden; 
    height: 100%; 
    min-width: 150px; 
    border: 1px solid #ccc; 
    background-color: white;
    border-radius: 4px;
  }

  .list-view {
    list-style: none;
    padding: 0;
    margin: 0;
   height: 100%; 
    overflow-y: auto; 
  }

  .document-list-item {
    margin: 0;
    border-bottom: 1px solid #e0e0e0;
  }

  .document-list-item:last-child {
    border-bottom: none;
  }

  .document-button {
    width: 100%;
    padding: 1rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s;
  }

  .document-button:hover {
    background-color: #f5f5f5;
  }

  .document-button.selected {
    background-color: #e3f2fd;
    border-left: 4px solid #3b82f6;
    padding-left: calc(1rem - 4px);
  }

  .document-button.selected:hover {
    background-color: #bbdefb;
  }

  .document-item h3 {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1rem;
    white-space: nowrap; 
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .document-meta,
  .document-details {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .document-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
    font-size: 0.85rem;
  }

  .document-details {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #666;
  }

  .unit {
    font-style: italic;
    color: #777;
  }

  .type {
    background-color: #f0f0f0;
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    font-weight: 500;
    font-size: 0.8rem;
  }

  .date, .professional {
    color: #555;
  }

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
