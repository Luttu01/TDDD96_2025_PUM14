<script lang="ts">
  import type { Note } from '$lib/models';
  import { onDestroy } from 'svelte';
  import { allNotes, selectedNotes, filteredNotes, filter } from '$lib/stores';

  // Get notes from global store and sort them by date 
  let localItems = $derived([...$filteredNotes]
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
  const DEFAULT_LIST_WIDTH = 300; 
  let listWidth = $state(DEFAULT_LIST_WIDTH);
  let isDragging = $state(false);
  let initialX = $state(0);
  let initialWidth = $state(0);

  // Check if note matches any filter criteria
  function matchesFilter(note: Note) {
    // Check if there are any filters selected
    const templateFilters = $filter.get("Journalmall");
    const unitFilters = $filter.get("Vårdenhet");
    const roleFilters = $filter.get("Yrkesroll");
    
    // If no filters are active, don't highlight anything
    const hasTemplateFilters = templateFilters && templateFilters.size > 0;
    const hasUnitFilters = unitFilters && unitFilters.size > 0;
    const hasRoleFilters = roleFilters && roleFilters.size > 0;
    
    if (!hasTemplateFilters && !hasUnitFilters && !hasRoleFilters) {
      return false;
    }
    
    // Check if note matches template filter
    const matchesTemplate = hasTemplateFilters ? 
      templateFilters!.has(note.Dokumentnamn) : false;
    
    // Check if note matches unit filter
    const matchesUnit = hasUnitFilters ? 
      unitFilters!.has(note.Vårdenhet_Namn) : false;
    
    // Check if note matches role filter
    const matchesRole = hasRoleFilters ? 
      roleFilters!.has(note.Dokument_skapad_av_yrkestitel_Namn) : false;
    
    return (hasTemplateFilters && matchesTemplate) || 
           (hasUnitFilters && matchesUnit) ||
           (hasRoleFilters && matchesRole);
  }

  // Determine specific filter match type for color highlighting
  function getFilterMatchType(note: Note) {
    // Check if there are any filters selected
    const templateFilters = $filter.get("Journalmall");
    const unitFilters = $filter.get("Vårdenhet");
    const roleFilters = $filter.get("Yrkesroll");
    
    // Check for active filters
    const hasTemplateFilters = templateFilters && templateFilters.size > 0;
    const hasUnitFilters = unitFilters && unitFilters.size > 0;
    const hasRoleFilters = roleFilters && roleFilters.size > 0;
    
    // Match specific filter types
    const matchesTemplate = hasTemplateFilters ? 
      templateFilters!.has(note.Dokumentnamn) : false;
    
    const matchesUnit = hasUnitFilters ? 
      unitFilters!.has(note.Vårdenhet_Namn) : false;
    
    const matchesRole = hasRoleFilters ? 
      roleFilters!.has(note.Dokument_skapad_av_yrkestitel_Namn) : false;
    
    // Priority: template > unit > role (if matches multiple filters)
    if (matchesTemplate) return 'template-match';
    if (matchesUnit) return 'unit-match';
    if (matchesRole) return 'role-match';
    
    return '';
  }

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
    {#each localItems as item (item.CompositionId)}
      <!-- List item-->
      <li data-testid="list-item-{item.CompositionId}" role="option" aria-selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)} class="document-list-item">
        <button
          data-testid="list-item-button-{item.CompositionId}"
          type="button"
          class="document-button"
          class:selected={$selectedNotes.some(note => note.CompositionId === item.CompositionId)}
          class:template-match={getFilterMatchType(item) === 'template-match'}
          class:unit-match={getFilterMatchType(item) === 'unit-match'}
          class:role-match={getFilterMatchType(item) === 'role-match'}
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
    border: 1px solid #ccc; 
    background-color: white;
    border-radius: 4px;
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
    border-bottom: 1px solid #e0e0e0;
  }

  .document-list-item:last-child {
    border-bottom: none;
  }

  /* Button styling for each document in the list */
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

  /* Selected document styling with left border accent */
  .document-button.selected {
    background-color: #e3f2fd;
    border-left: 4px solid #3b82f6;
    padding-left: calc(1rem - 4px);
  }

  .document-button.selected:hover {
    background-color: #bbdefb;
  }
  
  /* Template filter match styling (yellow) */
  .document-button.template-match {
    background-color: #ffecb3;
    border-left: 4px solid #ffc107;
    padding-left: calc(1rem - 4px);
  }

  .document-button.template-match:hover {
    background-color: #ffe082;
  }

  /* Unit filter match styling (green) */
  .document-button.unit-match {
    background-color: #c8e6c9;
    border-left: 4px solid #4caf50;
    padding-left: calc(1rem - 4px);
  }

  .document-button.unit-match:hover {
    background-color: #a5d6a7;
  }

  /* Role filter match styling (purple) */
  .document-button.role-match {
    background-color: #e1bee7;
    border-left: 4px solid #9c27b0;
    padding-left: calc(1rem - 4px);
  }

  .document-button.role-match:hover {
    background-color: #ce93d8;
  }

  /* Document title styling with text overflow handling */
  .document-item h3 {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1rem;
    white-space: nowrap; 
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Metadata sections with overflow handling */
  .document-meta,
  .document-details {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Document metadata (type and date) */
  .document-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
    font-size: 0.85rem;
  }

  /* Document details (professional and unit) */
  .document-details {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #666;
  }

  /* Style for unit name */
  .unit {
    font-style: italic;
    color: #555;
  }

  /* Document type badge styling */
  .type {
    background-color: #f0f0f0;
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    font-weight: 500;
    font-size: 0.8rem;
  }

  /* Date and professional styling */
  .date, .professional {
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
