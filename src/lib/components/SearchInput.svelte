<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { searchQuery } from '$lib/stores/searchStore';
    import { createEventDispatcher } from 'svelte';
  
    let searchInput: HTMLInputElement;
    const dispatch = createEventDispatcher();
  
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
        e.preventDefault();
        searchInput?.focus();
      } else if (e.key === 'Escape') {
        dispatch('close');
      }
    }
  
    onMount(() => {
      window.addEventListener('keydown', handleKeyDown);
    });
  
    onDestroy(() => {
      window.removeEventListener('keydown', handleKeyDown);
    });
  </script>
  
  <div class="relative">
    <input
      bind:this={searchInput}
      bind:value={$searchQuery}
      class="pl-3 w-full bg-white outline outline-1 outline-gray-300 rounded-md"
      placeholder="Sök..."
      type="text"
    />
  </div>