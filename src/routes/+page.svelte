<script lang="ts">
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";
  import List from "$lib/components/List.svelte";
  import { onDestroy } from "svelte";

  const MIN_TIMELINE_HEIGHT = 150;
  const DEFAULT_TIMELINE_HEIGHT = 300;

  let timelineHeight = $state(DEFAULT_TIMELINE_HEIGHT);
  let lastExpandedHeight = $state(DEFAULT_TIMELINE_HEIGHT); // to restore on expand
  let isDragging = $state(false);
  let isCollapsed = $state(false);

  let initialY = $state(0);
  let initialHeight = $state(0);

  // Toggle collapse/expand
  function toggleTimeline() {
    if (!isCollapsed) {
      lastExpandedHeight = timelineHeight;
      timelineHeight = 0;
      isCollapsed = true;
    } else {
      timelineHeight = Math.max(lastExpandedHeight, MIN_TIMELINE_HEIGHT);
      isCollapsed = false;
    }
  }

  // Start resize
  function handleMouseDown(event: MouseEvent) {
    if (isCollapsed) return; // Skip dragging when collapsed
    isDragging = true;
    initialY = event.clientY;
    initialHeight = timelineHeight;
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
  }

  // Resizing logic
  function handleMouseMove(event: MouseEvent) {
    if (!isDragging || isCollapsed) return;
    const currentY = event.clientY;
    const dy = initialY - currentY;
    const newHeight = initialHeight + dy;
    timelineHeight = Math.max(MIN_TIMELINE_HEIGHT, newHeight);
    lastExpandedHeight = timelineHeight;
  }

  function handleMouseUp() {
    if (isDragging) {
      isDragging = false;
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    }
  }

  onDestroy(() => {
    if (isDragging) {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    }
  });
</script>

<div class="flex flex-grow overflow-hidden">
  <aside
    class={!isCollapsed
      ? "w-0 flex-none transition-all duration-500 overflow-hidden border-r-1 border-gray-200"
      : "flex-none h-full transition-all duration-500 overflow-y-auto border-r-1 border-gray-200"}
  >
    <List />
  </aside>

  <main class="flex flex-col flex-grow overflow-hidden">
    <div class="flex-grow transition-all duration-500 overflow-hidden">
      <SelectedNotes />
    </div>
    <button
      onclick={toggleTimeline}
      class="w-full border-t border-b border-gray-200 bg-white text-center"
      aria-label="Toggle timeline view"
    >
      <i class="fa {isCollapsed ? 'fa-caret-up' : 'fa-caret-down'}"></i>
    </button>
    <div
      style="height: {timelineHeight}px;"
      class="overflow-hidden flex-none relative border-t border-gray-200"
    >
    {#if !isCollapsed}
      <div
        class="w-full h-1 cursor-row-resize bg-gray-200 hover:bg-gray-300"
        onmousedown={handleMouseDown}
      />
    {/if}
      <Timeline />
    </div>
  </main>
</div>
