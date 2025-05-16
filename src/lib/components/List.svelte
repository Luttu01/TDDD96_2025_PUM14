<script lang="ts">
  import type { Note } from '$lib/models';
  import { onDestroy, onMount } from 'svelte';
  import { selectedNotes, filteredNotes, showTimeline, allNotes, filter, selectedKeywords } from '$lib/stores';

  // Get notes from global store and sort them by date 
  let localFilteredItems: Note[] = $derived([...$filteredNotes]
      .map((item, index) => ({
        ...item,
        uniqueId: item.CompositionId || `${index}-${Date.now()}`
      }))
      .sort((a, b) => new Date(b.DateTime).getTime() - new Date(a.DateTime).getTime())
  );

  // Get all non-filtered items
  let localNonFilteredItems: Note[] = $derived([...$allNotes]
      .filter(item => !$filteredNotes.some(filteredItem => filteredItem.CompositionId === item.CompositionId))
      .map((item, index) => ({
        ...item,
        uniqueId: item.CompositionId || `${index}-${Date.now()}`
      }))
      .sort((a, b) => new Date(b.DateTime).getTime() - new Date(a.DateTime).getTime())
  );

  // Get active filter descriptions using proper runes mode
  let activeFilterText = $derived(getActiveFilterText(localNonFilteredItems));

  function getActiveFilterText(filtered : Note[]): string {
    let filterText = [];
    
    if(filtered.length > 0) {
      filterText[0] = "Filtrerade Journaler";
    }
    
    // Return filter text or default
    return filterText.length > 0 ? filterText.join(', ') : 'Alla Journaler';
  }

  // Reference to DOM element for the list container and list views
  let listContainerElement: HTMLDivElement;
  let filteredListElement: HTMLUListElement;
  let nonFilteredListElement: HTMLUListElement;

  let lastClickedIndex = $state(-1);

  // State for resizable list width functionality
  const MIN_LIST_WIDTH = 110; 
  const DEFAULT_LIST_WIDTH = 280; 
  const COMPACT_THRESHOLD = 200;  // Threshold for compact mode
  const EXPANDED_THRESHOLD = 400; // Threshold for expanded mode (lowered from 380)
  
  let listWidth = $state(DEFAULT_LIST_WIDTH);
  let isDragging = $state(false);
  let initialX = $state(0);
  let initialWidth = $state(0);

  // Function to determine layout mode based on width
  function getLayoutMode(width: number): 'compact' | 'normal' | 'expanded' {
    if (width < COMPACT_THRESHOLD) return 'compact';
    if (width > EXPANDED_THRESHOLD) return 'expanded';
    return 'normal';
  }

  // Reactive layout modes based on width using $derived instead of $:
  let layoutMode = $derived(getLayoutMode(listWidth));

  showTimeline.subscribe((value) => {
    if (value) {
      listWidth = 0;
    } else {
      listWidth = DEFAULT_LIST_WIDTH;
    }
  });

  function formatDate(dateTimeString: string): string {
    return new Date(dateTimeString).toLocaleDateString('sv-SE', {
      year: '2-digit',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  // Format date with different levels of detail based on layout mode
  function formatDateByMode(dateTimeString: string, mode: string): string {
    const date = new Date(dateTimeString);
    
    if (mode === 'compact') {
      return date.toLocaleDateString('sv-SE', {
        month: '2-digit',
        day: '2-digit',
      });
    } else if (mode === 'normal') {
      return date.toLocaleDateString('sv-SE', {
        year: '2-digit',
        month: '2-digit',
        day: '2-digit',
      });
    } else {
      return date.toLocaleDateString('sv-SE', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      });
    }
  }

  function handleDocumentClick(clickedNote: Note, event: MouseEvent) {
    event.stopPropagation();

    // Find the index of the clicked note in our local array - check both filtered and non-filtered items
    const filteredIndex = localFilteredItems.findIndex(item => item.CompositionId === clickedNote.CompositionId);
    const nonFilteredIndex = localNonFilteredItems.findIndex(item => item.CompositionId === clickedNote.CompositionId);
    
    // Set currentIndex based on which array the note was found in
    let currentIndex = -1;
    let items = localFilteredItems;
    
    if (filteredIndex !== -1) {
      currentIndex = filteredIndex;
    } else if (nonFilteredIndex !== -1) {
      currentIndex = nonFilteredIndex;
      items = localNonFilteredItems;
    }
    
    if (currentIndex === -1) return;

    // Handle shift+click for multi-select range
    if (event.shiftKey && lastClickedIndex !== -1) {
      // Select all notes between last clicked and current
      const start = Math.min(lastClickedIndex, currentIndex);
      const end = Math.max(lastClickedIndex, currentIndex);
      selectedNotes.set(items.slice(start, end + 1));
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
<div 
  data-testid="list-view-container" 
  class="list-container" 
  class:transition-all={isDragging === false} 
  class:duration-300={isDragging === false}
  class:list-compact={layoutMode === 'compact'}
  class:list-normal={layoutMode === 'normal'}
  class:list-expanded={layoutMode === 'expanded'}
  bind:this={listContainerElement} 
  style="width: {listWidth}px;"
>
  <!-- Top section with filtered items -->
   <div id="filtered-header" aria-hidden="true">
    <div id="filtered-header-text">{activeFilterText}</div>
  </div>
  <div id="top-section">
    {#if localFilteredItems.length > 0}
      
      <ul data-testid="filtered-list-view" id="filtered-list-view" role="listbox" aria-multiselectable="true" aria-label="Filtered clinical notes list">
        <!-- Iterate through filtered notes using CompositionId as unique key -->
        {#each localFilteredItems as item}
          <!-- List item-->
          <li data-testid="list-item-{item.CompositionId}" role="option" aria-selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)} class="document-list-item">
            <button
              data-testid="list-item-button-{item.CompositionId}"
              type="button"
              class="document-button"
              class:selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)}
              onclick={(e) => handleDocumentClick(item, e)}
            >
              <div id="document-item">
                <!-- Dynamic layout based on width -->
                {#if layoutMode === 'compact'}
                  <!-- Compact layout -->
                  <div id="compact-container" class="flex flex-col">
                    <h3>{item.Dokumentnamn}</h3>
                    <div id="document-meta">
                      <span class="font-mono">{item.Vårdenhet_Namn}</span>
                    </div>
                    <div id="document-meta" class="space-x-1">
                      <span class="font-mono">{formatDateByMode(item.DateTime, 'normal')}</span>
                      <span class="font-mono">{item.Dokument_skapad_av_yrkestitel_Namn === 'Sjuksköterska' ? 'Ssk' : 'Läk'}</span>
                    </div>
                  </div>
                {:else if layoutMode === 'normal'}
                  <!-- Normal layout -->
                  <div id="normal-container" class="flex flex-col">
                    <h3>{item.Dokumentnamn}</h3>
                    <div id="document-meta" class="space-x-1">
                      <span class="font-mono">{item.Vårdenhet_Namn}</span>
                      <span class="font-mono">{formatDateByMode(item.DateTime, 'normal')}</span>
                      <span class="font-mono">{item.Dokument_skapad_av_yrkestitel_Namn === 'Sjuksköterska' ? 'Ssk' : 'Läk'}</span>
                    </div>
                  </div>
                {:else}
                  <!-- Expanded layout -->
                  <div id="expanded-container" class="flex justify-between items-center">
                    <h3>{item.Dokumentnamn}</h3>
                    <div id="document-meta" class="space-x-1">
                      <span class="font-mono">{item.Vårdenhet_Namn}</span>
                      <span class="font-mono">{item.Dokument_skapad_av_yrkestitel_Namn === 'Sjuksköterska' ? 'Ssk' : 'Läk'}</span>
                      <span class="font-mono">{formatDateByMode(item.DateTime, 'normal')}</span>
                    </div>
                  </div>
                {/if}
              </div>
            </button>
          </li>
        {/each}
      </ul>
    {/if}
  </div>

  <!-- Bottom section with non-filtered items -->
  {#if localNonFilteredItems.length > 0}
    <div id="filtered-header" aria-hidden="true">
      <div id="filtered-header-text">Ofiltrerade journaler</div>
    </div>
    <div id="bottom-section">
      <!-- Separator for non-filtered items with no text -->
      
      <ul data-testid="non-filtered-list-view" id="non-filtered-list-view" role="listbox" aria-multiselectable="true" aria-label="Non-filtered clinical notes list">
        <!-- Iterate through non-filtered notes -->
        {#each localNonFilteredItems as item}
          <!-- List item with muted styling -->
          <li data-testid="list-item-non-filtered-{item.CompositionId}" role="option" aria-selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)} class="document-list-item document-list-item-muted">
            <button
              data-testid="list-item-button-{item.CompositionId}"
              type="button"
              class="document-button document-button-muted"
              class:selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)}
              onclick={(e) => handleDocumentClick(item, e)}
            >
              <div id="document-item">
                <!-- Dynamic layout based on width, same as above but with muted styling -->
                {#if layoutMode === 'compact'}
                  <!-- Compact layout -->
                  <div id="compact-container" class="flex flex-col">
                    <h3>{item.Dokumentnamn}</h3>
                    <div id="document-meta">
                      <span class="font-mono">{item.Vårdenhet_Namn}</span>
                    </div>
                    <div id="document-meta" class="space-x-1">
                      <span class="font-mono">{formatDateByMode(item.DateTime, 'normal')}</span>
                      <span class="font-mono">{item.Dokument_skapad_av_yrkestitel_Namn === 'Sjuksköterska' ? 'Ssk' : 'Läk'}</span>
                    </div>
                  </div>
                {:else if layoutMode === 'normal'}
                  <!-- Normal layout -->
                  <div id="normal-container" class="flex flex-col">
                    <h3>{item.Dokumentnamn}</h3>
                    <div id="document-meta" class="space-x-1">
                      <span class="font-mono">{item.Vårdenhet_Namn}</span>
                      <span class="font-mono">{formatDateByMode(item.DateTime, 'normal')}</span>
                      <span class="font-mono">{item.Dokument_skapad_av_yrkestitel_Namn === 'Sjuksköterska' ? 'Ssk' : 'Läk'}</span>
                    </div>
                  </div>
                {:else}
                  <!-- Expanded layout -->
                  <div id="expanded-container" class="flex justify-between items-center">
                    <h3>{item.Dokumentnamn}</h3>
                    <div id="document-meta" class="space-x-1">
                      <span class="font-mono">{item.Vårdenhet_Namn}</span>
                      <span class="font-mono">{item.Dokument_skapad_av_yrkestitel_Namn === 'Sjuksköterska' ? 'Ssk' : 'Läk'}</span>
                      <span class="font-mono">{formatDateByMode(item.DateTime, 'normal')}</span>
                    </div>
                  </div>
                {/if}
              </div>
            </button>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  <!-- Resize handle for adjusting list width -->
  <button 
    data-testid="resize-handle" 
    id="resize-handle" 
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
    max-width: 500px;
    border: 1px solid #ccc; 
    background-color: white;
    display: flex;
    flex-direction: column;
  }

  /* Top and bottom sections */
  #top-section {
    flex-grow: 1;
    overflow-y: auto;
    border-bottom: 1px solid #eaeaea;
    display: flex;
    flex-direction: column;
    min-height: 100px;
    max-height: calc(100% - 50px);
  }

  #bottom-section {
    max-height: 50%;
    min-height: 10%;
    overflow-y: auto;
    background-color: #fafafa;
  }

  /* Scrollable lists of documents */
  #filtered-list-view, #non-filtered-list-view {
    list-style: none;
    padding: 0;
    margin: 0;
    width: 100%;
  }

  /* Individual list items with border between them */
  .document-list-item {
    margin: 0;
    border-bottom: 2px solid #e0e0e0;
  }

  .document-list-item:last-child {
    border-bottom: none;
  }

  /* Muted styling for non-filtered items */
  .document-list-item-muted {
    background-color: #f8f8f8;
  }

  /* Button styling for each document in the list */
  .document-button {
    width: 100%;
    padding: 0.4rem 0.5rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s;
  }

  .document-button:hover {
    background-color: #f5f5f5;
  }

  /* Muted button styling */
  .document-button-muted {
    opacity: 0.7;
    padding: 0.2rem 0.2rem;
  }

  .document-button-muted:hover {
    background-color: #f0f0f0;
    opacity: 0.9;
  }

  /* Selected document styling with left border accent */
  .document-button.selected {
    background-color: oklch(97.7% 0.014 308.299);
    border-left: 4px solid #b83bf6;
  }

  .document-button.selected:hover {
    background-color: oklch(94.6% 0.033 307.174);
  }

  /* Document title styling with text overflow handling */
  #document-item h3 {
    margin: 0 0 0.1rem 0;
    color: #333;
    font-size: 0.70rem;
    font-weight: 600;
    white-space: nowrap; 
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Responsive styling based on list width */
  .list-compact #document-item h3 {
    font-size: 0.7rem;
  }

  .list-expanded #document-item h3 {
    font-size: 0.7rem;
  }

  /* Metadata sections with overflow handling */
  #document-meta {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Document metadata (type and date) */
  #document-meta {
    display: flex;
    flex-wrap: row;
    font-size: 0.70rem;
    font-weight: 300;
    color: #6d6d6d;
  }

  /* Responsive font sizes based on layout */
  .list-compact #document-meta {
    font-size: 0.7rem;
  }

  .list-expanded #document-meta {
    font-size: 0.7rem;
  }

  /* Resize handle on the right side of the list */
  #resize-handle {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 5px; 
    cursor: col-resize;
    background-color: rgba(0, 0, 0, 0.1); 
  }

  #resize-handle:hover {
    background-color: rgba(0, 0, 0, 0.3);
  }

  /* Filtered header styling */
  #filtered-header {
    display: flex;
    justify-content: center;
    padding: 0.4rem 0.2rem 0.1rem 0.2rem;
    background-color: #f5f8ff;
  }

  #filtered-header-text {
    font-size: 0.8rem;
    font-weight: 600;
    color: #4a5568;
  }
</style>
