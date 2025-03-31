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
  <aside
    class={$expandTimeline
      ? "w-0 flex-none transition-all duration-500 overflow-hidden"
      : "w-40 flex-none h-full transition-all duration-500 overflow-hidden"}
  >
    <List />
  </aside>

  <main class="flex flex-col flex-grow overflow-hidden">
    <div class="flex-grow transition-all duration-500 overflow-hidden">
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
