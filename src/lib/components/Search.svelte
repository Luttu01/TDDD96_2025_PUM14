<script lang="ts">
  import { searchQuery } from '$lib/stores/searchStore';
  import { onMount } from 'svelte';
  import { extractBoldTitlesFromHTML } from '$lib/utils/keywordHelper';
  import { selectedNotes } from '$lib/stores/storedNotes';

  let searchInput: HTMLInputElement;
  let selectedTitle = '';

  /**
   * Ctrl + f funktionalitet
   */
  onMount(() => {
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
        e.preventDefault();
        searchInput?.focus();
      }
    });
  });

  // Extract and sort bold titles
  $: allTitles = $selectedNotes.flatMap(note =>
    extractBoldTitlesFromHTML(note.CaseData)
  );
  $: sortedTitles = Array.from(new Set(allTitles)).sort((a, b) =>
    a.localeCompare(b, 'sv')
  );

  // When user picks a title from dropdown, update searchQuery
  $: if (selectedTitle) {
    searchQuery.set(selectedTitle);
  }
</script>

<!-- Search input -->
<input
  bind:this={searchInput}
  class="pl-3 w-full bg-white outline-1 outline-gray-300 rounded-md mb-2"
  type="text"
  placeholder="Sök..."
  bind:value={$searchQuery}
/>

<!-- Dropdown with bold titles -->
<div class="mb-4">
  <label for="titleDropdown" class="block text-sm font-medium mb-1">Rubriker i anteckningar:</label>
  <select
    id="titleDropdown"
    bind:value={selectedTitle}
    class="w-full p-2 border border-gray-300 rounded-md text-sm"
  >
    <option value="">Välj en rubrik...</option>
    {#each sortedTitles as title}
      <option value={title}>{title}</option>
    {/each}
  </select>
</div>