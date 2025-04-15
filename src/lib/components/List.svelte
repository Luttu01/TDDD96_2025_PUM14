<script lang="ts">
  import type { Document } from '$lib/models/note';
  import { onMount, onDestroy } from 'svelte';

  const props = $props<{
    items?: Document[];
    onselect?: (selectedDocs: Document[]) => void;
  }>();

  let localItems = $state<Array<Document & { uniqueId: string }>>([]);
  let selectedDocuments = $state<Document[]>([]);
  let listViewElement: HTMLElement;
  let counter = 0; // Counter for unique IDs
  let lastClickedIndex = $state(-1); // Index of the last item clicked without Shift

  $effect(() => {
    if (props.items) {
      localItems = [...props.items]
        .map(item => ({
          ...item,
          uniqueId: `${item.id}-${counter++}`
        }))
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      // Reset last clicked index if items change
      lastClickedIndex = -1;
      // Also reset selection if items change? Optional, depends on desired UX.
      // selectedDocuments = [];
    }
  });

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('sv-SE');
  }

  function handleDocumentClick(clickedDocument: Document, event: MouseEvent) {
    event.stopPropagation();

    const currentIndex = localItems.findIndex(item => item.id === clickedDocument.id);
    if (currentIndex === -1) return; // Should not happen

    if (event.shiftKey && lastClickedIndex !== -1) {
      // Shift+Click logic for range selection
      const start = Math.min(lastClickedIndex, currentIndex);
      const end = Math.max(lastClickedIndex, currentIndex);
      // Select all items between lastClickedIndex and currentIndex, inclusive
      selectedDocuments = localItems.slice(start, end + 1);
      // Do not update lastClickedIndex on Shift+Click to keep the original anchor
    } else {
      // Normal click OR the first click in a potential shift-click sequence
      const isAlreadySelected = selectedDocuments.some(doc => doc.id === clickedDocument.id);

      if (isAlreadySelected) {
        // Item is already selected, remove it (toggle off)
        selectedDocuments = selectedDocuments.filter(doc => doc.id !== clickedDocument.id);
        // Reset lastClickedIndex if we just deselected the anchor point
        if (lastClickedIndex === currentIndex) {
          lastClickedIndex = -1;
        }
      } else {
        // Item is not selected, add it (toggle on)
        selectedDocuments = [...selectedDocuments, clickedDocument];
        // Set the anchor point for future Shift+Clicks
        lastClickedIndex = currentIndex;
      }
    }

    if (props.onselect) {
      props.onselect(selectedDocuments);
    }
  }

  /* Remove outside click handler
  function handleOutsideClick(event: MouseEvent) {
    if (listViewElement && !listViewElement.contains(event.target as Node)) {
      if (selectedDocuments.length > 0) {
        selectedDocuments = [];
        lastClickedIndex = -1; // Reset last clicked index on outside click
        if (props.onselect) {
          props.onselect([]);
        }
      }
    }
  }
  */

  onMount(() => {
    // Remove event listener for outside click
    /*
    if (typeof window !== 'undefined') {
      window.addEventListener('click', handleOutsideClick);
    }
    */
  });

  onDestroy(() => {
    // Remove event listener for outside click
    /*
    if (typeof window !== 'undefined') {
      window.removeEventListener('click', handleOutsideClick);
    }
    */
  });
</script>

<ul class="list-view" bind:this={listViewElement} role="listbox">
  {#each localItems as item (item.uniqueId)}
    <li role="option" aria-selected={selectedDocuments.some(doc => doc.id === item.id)} class="document-list-item">
      <button
        type="button"
        class="document-button"
        class:selected={selectedDocuments.some(doc => doc.id === item.id)}
        onclick={(e) => handleDocumentClick(item, e)}
      >
        <div class="document-item">
          <h3>{item.title}</h3>
          <div class="document-meta">
            <span class="type">{item.type}</span>
            <span class="category">{item.category}</span>
            <span class="date">{formatDate(item.date)}</span>
          </div>
          <div class="document-details">
            <span class="professional">{item.professional}</span>
            <span class="unit">Unit: {item.unit}</span>
          </div>
          <p class="abstract">{item.abstract}</p>
        </div>
      </button>
    </li>
  {/each}
</ul>

<style>
  .list-view {
    list-style: none;
    padding: 0;
    margin: 0;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
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

  .type, .category {
    background-color: #f0f0f0;
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    font-weight: 500;
    font-size: 0.8rem;
  }

  .date, .professional {
    color: #555;
  }

  .abstract {
    margin: 0.5rem 0 0 0;
    color: #444;
    font-size: 0.9rem;
    line-height: 1.4;
  }
</style>
