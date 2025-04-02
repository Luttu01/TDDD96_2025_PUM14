<script lang="ts">
  import type { Document } from '$lib/types';

  const props = $props<{
    items?: Document[];
    keyBy?: string | ((item: Document) => string | number);
    selectedDocument?: Document | null;
    onselect?: (document: Document) => void;
  }>();

  // Create mutable state for values that need to be updated
  let localItems = $state<Document[]>([]);
  let localSelectedDocument = $state<Document | null>(null);
  let expandedUnits = $state<string[]>([]);
  
  // Update local state when props change
  $effect(() => {
    if (props.items) {
      localItems = [...props.items];
    }
  });

  $effect(() => {
    localSelectedDocument = props.selectedDocument || null;
  });
  


  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('sv-SE');
  }

  // Group items by unit - make it a regular function for better control
  function getGroupedItems() {
    const groups: Record<string, Array<Document & { uniqueId: string }>> = {};
    let counter = 0;
    
    for (const item of localItems) {
      const unit = item.unit;
      if (!groups[unit]) {
        groups[unit] = [];
      }
      // Add a uniqueId to each item
      groups[unit].push({
        ...item,
        uniqueId: `${unit}-${item.id}-${counter++}`
      });
    }
    
    // Sort items within each group by date
    for (const unit in groups) {
      groups[unit].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    }
    
    return groups;
  }

  // Make groupedItems reactive
  let groupedItems = $derived(getGroupedItems());

  // Toggle a unit's expanded state
  function toggleUnit(unit: string) {
    expandedUnits = expandedUnits.includes(unit)
      ? expandedUnits.filter(u => u !== unit)
      : [...expandedUnits, unit];
  }

  function handleDocumentClick(document: Document) {
    // Update local state
    localSelectedDocument = document;
    
    // Call the onselect handler if provided
    if (props.onselect) {
      props.onselect(document);
    }
    
    // Log for debugging
    console.log('Document clicked:', document.title, 'Event handled');
  }
</script>

<ul class="list-view">
  {#each Object.entries(groupedItems) as [unit, unitItems] (unit)}
    <li class="unit-group">
      <button 
        type="button"
        class="unit-header" 
        onclick={() => toggleUnit(unit)}
        aria-expanded={expandedUnits.includes(unit)}
      >
        <span class="unit-name">{unit}</span>
        <span class="item-count">({unitItems.length})</span>
      </button>
      {#if expandedUnits.includes(unit)}
        <ul class="unit-items">
          {#each unitItems as item (item.uniqueId)}
            <li>
              <button 
                type="button"
                class="document-button" 
                class:selected={localSelectedDocument?.id === item.id}
                onclick={() => handleDocumentClick(item)}
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
  }

  .document-button.selected:hover {
    background-color: #bbdefb;
  }

  .document-item h3 {
    margin: 0 0 0.5rem 0;
    color: #333;
  }

  .document-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }

  .document-details {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #666;
  }

  .type, .category {
    background-color: #f0f0f0;
    padding: 0.2rem 0.5rem;
    border-radius: 3px;
    font-weight: 500;
  }

  .date {
    color: #666;
  }

  .abstract {
    margin: 0.5rem 0 0 0;
    color: #444;
    font-size: 0.95rem;
    line-height: 1.4;
  }
</style>
