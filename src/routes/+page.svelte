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

<div class="flex flex-grow overflow-hidden">
  <aside
    class={$expandTimeline
      ? "w-0 flex-none transition-all duration-500 overflow-hidden border-r-1 border-gray-200"
      : "flex-none h-full transition-all duration-500 overflow-y-auto border-r-1 border-gray-200"}
  >
    <List/>
  </aside>

  <main class="flex flex-col flex-grow overflow-hidden">
    <div class="flex-grow transition-all duration-500 overflow-hidden">
      <SelectedNotes />
    </div>
    <button onclick={toggleView} class="w-full border-t-1 border-b-1 border-gray-200 bg-white fa {$expandTimeline ? 'fa-caret-down' : 'fa-caret-up' }" aria-label="Toggle timeline view">
    </button>
    <div
      class={$expandTimeline
        ? "h-2/5 transition-all duration-500 flex-none"
        : "h-0 transition-all duration-500 flex-none"}
    >
      <Timeline />
    </div>
  </main>
</div>
