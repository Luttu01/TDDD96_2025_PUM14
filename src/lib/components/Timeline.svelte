<script lang="ts">
  import { onMount } from "svelte";

  let journalNotes = [
    { date: new Date("2021-01-01"), content: "Anteckning 1" },
    { date: new Date("2021-01-02"), content: "Anteckning 2" },
    { date: new Date("2021-01-03"), content: "Anteckning 3" },
    { date: new Date("2021-01-04"), content: "Anteckning 4" },
    { date: new Date("2021-01-05"), content: "Anteckning 5" },
    { date: new Date("2021-01-06"), content: "Anteckning 6" },
    { date: new Date("2021-01-07"), content: "Anteckning 7" },
    { date: new Date("2021-01-08"), content: "Anteckning 8" },
    { date: new Date("2021-01-09"), content: "Anteckning 9" },
    { date: new Date("2021-01-10"), content: "Anteckning 10" },
    { date: new Date("2021-01-11"), content: "Anteckning 11" },
    { date: new Date("2021-01-12"), content: "Anteckning 12" },
    { date: new Date("2021-01-13"), content: "Anteckning 13" },
    { date: new Date("2021-01-14"), content: "Anteckning 14" },
    { date: new Date("2021-01-15"), content: "Anteckning 15" },
    { date: new Date("2021-01-16"), content: "Anteckning 16" },
    { date: new Date("2021-01-17"), content: "Anteckning 17" },
    { date: new Date("2021-01-18"), content: "Anteckning 18" },
    { date: new Date("2021-01-19"), content: "Anteckning 19" },
  ];

  let scale: number = 1;
  let speed: number = 0.01;
  const minScale: number = 0.38;
  const maxScale: number = 1.5;
  const baseWidth: number = 320;

  function handleZoom(event: WheelEvent): void {
    if (event.ctrlKey) {
      event.preventDefault();
      scale -= event.deltaY * speed;
      scale = Math.min(maxScale, Math.max(minScale, scale));
    }
  }

  onMount(() => {
    window.addEventListener("wheel", handleZoom, { passive: false });

    return () => {
      window.removeEventListener("wheel", handleZoom);
    };
  });
</script>

<div
  class="h-full bg-gray-100 relative flex flex-col overflow-x-auto p-2 space-y-2"
>
  <div class="flex space-x-1">
    {#each journalNotes as note, index}
      <div class="relative flex-none h-3" style="width: {baseWidth * scale}px;">
        <div
          class="absolute top-0 left-1/2 h-3 w-3 bg-black rounded-full"
        ></div>
      </div>
    {/each}
  </div>

  <div class="flex flex-grow space-x-1">
    {#each journalNotes as note}
      <div
        class="bg-white flex-none p-1 rounded-md shadow-sm"
        style="width: {baseWidth * scale}px;"
      >
        <div class="text-left text-sm text-gray-500">
          {note.date.toDateString()}
        </div>
        {note.content}
      </div>
    {/each}
  </div>
</div>
