<script lang="ts">
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";
  import List from "$lib/components/List.svelte";
  import { writable } from "svelte/store";
  import type { Note } from "$lib/models/note";
  import { onMount } from "svelte";

  let expandTimeline = writable(false);
  let notes = $state<Note[]>([]);
  let selectedNotes = $state<Note[]>([]);

  function handleDocumentSelect(documents: Note[]) {
    console.log('Selected notes:', documents);
    selectedNotes = documents;
  }

  function toggleView() {
    expandTimeline.update((state) => !state);
  }

  onMount(async () => {
    try {
      const response = await fetch('/api/journals');
      const data = await response.json();
      notes = data;
    } catch (error) {
      console.error('Failed to fetch journal data:', error);
      notes = [];
    }
  });
</script>

<div class="flex flex-grow h-full">
  <aside
    class={$expandTimeline
      ? "w-0 flex-none transition-all duration-500 overflow-hidden"
      : "w-40 flex-none h-full transition-all duration-500 overflow-y-auto"}
  >
    <List
      items={notes}
      onselect={handleDocumentSelect}
    />
  </aside>

  <main class="flex flex-col flex-grow h-full overflow-hidden">
    <div class="flex-grow overflow-y-auto">
      <SelectedNotes />
    </div>
    <div
      class={$expandTimeline
        ? "h-6/8 transition-all duration-500"
        : "h-10 transition-all duration-500"}
    >
      <Timeline />
    </div>
  </main>
</div>

<button
  on:click={toggleView}
  class="fixed top-1 right-1 bg-black text-white p-1 rounded-md"
>
  {#if $expandTimeline}
    Hide Timeline
  {:else}
    Show Timeline
  {/if}
</button>
