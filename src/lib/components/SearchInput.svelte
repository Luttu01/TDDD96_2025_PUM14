<script lang="ts">
    import { onMount } from 'svelte';
    import { searchQuery } from '$lib/stores/searchStore';
  
    let searchInput: HTMLInputElement;
  
    onMount(() => {
      window.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
          e.preventDefault();
          searchInput?.focus();
        }
      });
    });
  </script>
  
  <input
    bind:this={searchInput}
    bind:value={$searchQuery}
    class="pl-3 w-full bg-white outline outline-1 outline-gray-300 rounded-md"
    placeholder="Sök..."
    type="text"
  />