<script lang="ts">
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";
  import SecondaryHeader from "$lib/components/SecondaryHeader.svelte";
  import List from "$lib/components/List.svelte";
  import { onDestroy } from "svelte";
  import { showTimeline } from "$lib/stores";

  const MIN_TIMELINE_HEIGHT = 40;
  const DEFAULT_TIMELINE_HEIGHT = 180;

  let timelineHeight = 0;
  let isDragging = false;
  let isCollapsed = true;

  let initialY = 0;
  let initialHeight = 0;

  // Toggle collapse/expand
  function toggleTimeline() {
    if (!isCollapsed) {
      timelineHeight = 0;
      isCollapsed = true;
    } else {
      timelineHeight = DEFAULT_TIMELINE_HEIGHT;
      isCollapsed = false;
    }
  }

    showTimeline.subscribe((value) => {
      if (value === isCollapsed) {
        toggleTimeline();
      }
    });

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
    class={!isCollapsed ? "flex-none h-full transition-all duration-500 overflow-y-auto w-0" : "flex-none h-full transition-all duration-500 overflow-y-auto border-r-1 border-gray-200"}
  >
    <List />
  </aside>

  <main class="flex flex-col flex-grow overflow-hidden">
    <SecondaryHeader />
    <div class="flex-grow flex flex-col transition-all duration-500 overflow-hidden relative">
      <SelectedNotes />
    </div>
    {#if !isCollapsed}
      <button
        class="w-full h-2 min-h-2 cursor-row-resize bg-gray-200 hover:bg-gray-300"
        onmousedown={handleMouseDown}
        aria-label="Resize timeline"
      ></button>
    {/if}
    <div
      style="height: {timelineHeight}px;"
      class="overflow-hidden flex-none relative max-h-[400px]"
    >
      <Timeline />
    </div>
  </main>
</div>
