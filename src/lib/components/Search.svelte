<script lang="ts">
    import { searchQuery } from '$lib/stores/searchStore';
    import { onMount } from 'svelte';
  
    let searchInput: HTMLInputElement;
    
    /*
     * Ctrl + f funktionalitet för senare.
    */
    onMount(() => {
      window.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
          e.preventDefault();
          searchInput?.focus();
        }
      });
    });
  </script>
  
  <!-- Sök komponent till header. -->
  <input
    bind:this={searchInput}
    class="pl-3 w-[100%] bg-white outline-1 outline-gray-300 rounded-md"
    type="text"
    placeholder="Sök:"
    bind:value={$searchQuery}
  />