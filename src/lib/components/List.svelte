<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { allNotes, selectedNotes } from '$lib/stores';
  import type { Note } from '$lib/models/note';

  let listViewElement: HTMLElement;
  let expandedUnits: string[] = [];

  function formatDate(dateString: string): string {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('sv-SE');
  }

  function groupByUnit(notes: Note[]): Record<string, Note[]> {
    const groups: Record<string, Note[]> = {};

    for (const note of notes) {
      // Use "Unknown" or some fallback if Vårdenhet_Namn is missing
      const unit = note.Vårdenhet_Namn || 'Okänd enhet';
      if (!groups[unit]) {
        groups[unit] = [];
      }
      groups[unit].push(note);
    }

    for (const unit in groups) {
      groups[unit].sort((a, b) => {
        return new Date(b.DateTime).getTime() - new Date(a.DateTime).getTime();
      });
    }

    return groups;
  }

  $: groupedNotes = groupByUnit($allNotes);

  function toggleUnit(unit: string) {
    if (expandedUnits.includes(unit)) {
      expandedUnits = expandedUnits.filter(u => u !== unit);
    } else {
      expandedUnits = [...expandedUnits, unit];
    }
  }

  function handleNoteClick(note: Note, event: MouseEvent) {
    event.stopPropagation();
    const ctrlOrCmd = event.ctrlKey || event.metaKey;

    selectedNotes.update((current) => {
      const alreadySelected = current.some(n => n.Dokument_ID === note.Dokument_ID);
        // Multi-select logic
        if (alreadySelected) {
          // Remove from selected
          return current.filter(n => n.Dokument_ID !== note.Dokument_ID);
        } else {
          // Add to selected
          return [...current, note];
        }
    });
  }

  function handleOutsideClick(event: MouseEvent) {
    if (
      listViewElement &&
      !listViewElement.contains(event.target as Node)
    ) {
      selectedNotes.update((current) => {
        if (current.length > 0) {
          return [];
        }
        return current;
      });
    }
  }
</script>

<ul class="list-view" bind:this={listViewElement} role="listbox">
  {#each Object.entries(groupedNotes) as [unitName, notes] (unitName)}
    <li
      class="unit-group"
      role="group"
      aria-labelledby={`unit-header-${unitName}`}
    >
      <button
        type="button"
        class="unit-header"
        on:click={() => toggleUnit(unitName)}
        aria-expanded={expandedUnits.includes(unitName)}
        id={`unit-header-${unitName}`}
      >
        <span class="unit-name">{unitName}</span>
        <span class="item-count">({notes.length})</span>
      </button>

      {#if expandedUnits.includes(unitName)}
        <ul class="unit-items" role="presentation">
          {#each notes as note (note.Dokument_ID)}
            <li
              role="option"
              aria-selected={$selectedNotes.some(n => n.Dokument_ID === note.Dokument_ID)}
            >
              <button
                type="button"
                class="document-button"
                class:selected={$selectedNotes.some(n => n.Dokument_ID === note.Dokument_ID)}
                on:click={(e) => handleNoteClick(note, e)}
              >
                <div class="document-item">
                  <h3>{note.Dokumentnamn}</h3>
                  <div class="document-meta">
                    <span class="date">{formatDate(note.DateTime)}</span>
                    <span class="professional">{note.Dokument_skapad_av_yrkestitel_Namn}</span>
                  </div>
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
    border: 1px solid #e0e0e0;
    background-color: white;
    overflow: hidden; 
  }

  .unit-header {
    width: 100%;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    font-size: 0.9rem;
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
    font-size: 0.8rem;
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
    padding: 0.5rem;
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
    background-color: oklch(94.6% 0.033 307.174); 
    border-left: 4px solid oklch(62.7% 0.265 303.9); 
    padding-left: calc(1rem - 4px); 
  }

  .document-button.selected:hover {
    background-color: #bbdefb; 
  }

  .document-item h3 {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 0.9rem;
  }

  .document-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem; 
    font-size: 0.8rem; 
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
    font-size: 0.8rem;
    line-height: 1.4;
  }
</style>
