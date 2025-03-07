<script lang="ts">
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";
  import List from "$lib/components/List.svelte";
  import { writable } from "svelte/store";

  let expandTimeline = writable(false);

  function toggleView() {
    expandTimeline.update((state) => !state);
  }
</script>

<div class="flex flex-grow">
  <aside class="w-40 h-full">
    <List />
  </aside>

  <main class="flex flex-col flex-grow">
    <div class="flex flex-grow transition-all duration-500">
      <SelectedNotes />
    </div>
    <div
      class={$expandTimeline
        ? "flex h-16 transition-all duration-500"
        : "flex h-6/8 transition-all duration-500"}
    >
      <Timeline />
    </div>
  </main>
</div>

<button
  on:click={toggleView}
  class="fixed bottom-4 right-4 bg-black text-white p-2 rounded-full"
>
  {#if $expandTimeline}
    Hide Timeline
  {:else}
    Show Timeline
  {/if}
</button>
