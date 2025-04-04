<script lang="ts">
  import type { Document } from '$lib/models/note';
  import { onMount, onDestroy } from 'svelte';

  const props = $props<{
    items?: Document[];
    onselect?: (selectedDocs: Document[]) => void;
  }>();

  let localItems = $state<Document[]>([]);
  let selectedDocuments = $state<Document[]>([]);
  let expandedUnits = $state<string[]>([]);
  let listViewElement: HTMLElement;

  $effect(() => {
    if (props.items) {
      localItems = [...props.items];
    }
  });

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('sv-SE');
  }
// groups the items by unit
  function getGroupedItems() {
    const groups: Record<string, Array<Document & { uniqueId: string }>> = {};
    let counter = 0;

    for (const item of localItems) {
      const unit = item.unit;
      if (!groups[unit]) {
        groups[unit] = [];
      }
      // uniqueId helps Svelte efficiently update the list when items change order or content
      groups[unit].push({
        ...item,
        uniqueId: `${unit}-${item.id}-${counter++}`
      });
    }

    for (const unit in groups) {
      groups[unit].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    }

    return groups;
  }

  let groupedItems = $derived(getGroupedItems());

  // expands or collapses the unit group
  function toggleUnit(unit: string) {
    expandedUnits = expandedUnits.includes(unit)
      ? expandedUnits.filter(u => u !== unit)
      : [...expandedUnits, unit];
  }

  function handleDocumentClick(document: Document, event: MouseEvent) {
    event.stopPropagation();

    const ctrlOrCmdPressed = event.ctrlKey || event.metaKey;

    if (ctrlOrCmdPressed) {
      const isAlreadySelected = selectedDocuments.some(doc => doc.id === document.id);
      if (isAlreadySelected) {
        selectedDocuments = selectedDocuments.filter(doc => doc.id !== document.id);
      } else {
        selectedDocuments = [...selectedDocuments, document];
      }
    } else {
      if (selectedDocuments.length === 1 && selectedDocuments[0].id === document.id) {
        selectedDocuments = [];
      } else {
        selectedDocuments = [document];
      }
    }

    if (props.onselect) {
      props.onselect(selectedDocuments);
    }
  }

  function handleOutsideClick(event: MouseEvent) {
    if (listViewElement && !listViewElement.contains(event.target as Node)) {
      if (selectedDocuments.length > 0) {
        selectedDocuments = [];
        if (props.onselect) {
          props.onselect([]);
        }
      }
    }
  }

  // listens for clicks outside the list-view
  onMount(() => {
    if (typeof window !== 'undefined') {
      window.addEventListener('click', handleOutsideClick);
    }
  });

  // removes the listener when the component is destroyed
  onDestroy(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('click', handleOutsideClick);
    }
  });
</script>

<ul class="list-view" bind:this={listViewElement} role="listbox">
  {#each Object.entries(groupedItems) as [unit, unitItems] (unit)}
    <li class="unit-group" role="group" aria-labelledby={`unit-header-${unit.replace(/\s+/g, '-')}`}>
      <button
        type="button"
        class="unit-header"
        onclick={() => toggleUnit(unit)}
        aria-expanded={expandedUnits.includes(unit)}
        id={`unit-header-${unit.replace(/\s+/g, '-')}`}
      >
        <span class="unit-name">{unit}</span>
        <span class="item-count">({unitItems.length})</span>
        <span class="toggle-icon" aria-hidden="true">{expandedUnits.includes(unit) ? '−' : '+'}</span>
      </button>

      {#if expandedUnits.includes(unit)}
        <ul class="unit-items" role="presentation">
          {#each unitItems as item (item.uniqueId)}
            <li role="option" aria-selected={selectedDocuments.some(doc => doc.id === item.id)}>
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
                  </div>
                  <p class="abstract">{item.abstract}</p>
                </div>
              </button>
            </li>
          {/each}
        </ul>
      {/if}
    </li>
  {/each}
</ul>

<style>
  .list-view {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .unit-group {
    margin-bottom: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: white;
    overflow: hidden; 
  }

  .unit-header {
    width: 100%;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    font-size: 1.1rem;
    font-weight: 500;
    color: #333;
    border-bottom: 1px solid transparent; 
    transition: background-color 0.2s;
  }

  .unit-header:hover {
    background-color: #f5f5f5;
  }

  .unit-header[aria-expanded="true"] {
    border-bottom-color: #e0e0e0;
  }

  .unit-name {
    flex: 1; 
  }
  .item-count {
    color: #666;
    font-size: 0.9rem;
  }

  .toggle-icon {
    font-weight: bold;
    margin-left: auto; 
  }

  .unit-items {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .unit-items li {
    margin: 0;
    border-bottom: 1px solid #e0e0e0; 
  }

  .unit-items li:last-child {
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
