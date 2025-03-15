<script lang="ts">
  import { onMount } from "svelte";
  import { derived, writable } from "svelte/store";

  type JournalNote = {
    date: Date;
    content: string;
  };

  let journalNotes = writable<JournalNote[]>([
    { date: new Date("2021-01-01"), content: "Anteckning 1" },
    { date: new Date("2021-01-01"), content: "Anteckning 1" },
    { date: new Date("2021-01-01"), content: "Anteckning 1" },
    { date: new Date("2021-01-02"), content: "Anteckning 2" },
    { date: new Date("2021-02-03"), content: "Anteckning 3" },
    { date: new Date("2021-02-04"), content: "Anteckning 4" },
    { date: new Date("2021-03-05"), content: "Anteckning 5" },
    { date: new Date("2021-04-06"), content: "Anteckning 6" },
    { date: new Date("2021-05-07"), content: "Anteckning 7" },
    { date: new Date("2021-05-08"), content: "Anteckning 8" },
    { date: new Date("2022-01-09"), content: "Anteckning 9" },
    { date: new Date("2022-04-10"), content: "Anteckning 10" },
    { date: new Date("2023-05-11"), content: "Anteckning 11" },
    { date: new Date("2023-05-12"), content: "Anteckning 12" },
    { date: new Date("2023-06-13"), content: "Anteckning 13" },
    { date: new Date("2023-06-14"), content: "Anteckning 14" },
    { date: new Date("2024-01-15"), content: "Anteckning 15" },
    { date: new Date("2024-01-16"), content: "Anteckning 16" },
    { date: new Date("2024-02-17"), content: "Anteckning 17" },
    { date: new Date("2024-03-18"), content: "Anteckning 18" },
    { date: new Date("2024-04-19"), content: "Anteckning 19" },
  ]);

  let scale: number = 1;
  let speed: number = 0.01;
  const minScale: number = 0.38;
  const maxScale: number = 1.5;
  const baseWidth: number = 320;
  const space: number = 4;

  type GroupType = "day" | "month" | "year";

  function groupNotes(notes: JournalNote[]) {
    let groups: Record<GroupType, number[][]> = { day: [], month: [], year: [] };
    let dayMap = new Map<string, number[]>();
    let monthMap = new Map<string, number[]>();
    let yearMap = new Map<string, number[]>();

    notes.forEach((note, index) => {
      const dayStr = note.date.toISOString().split("T")[0];
      const monthStr = `${note.date.getFullYear()}-${note.date.getMonth() + 1}`;
      const yearStr = `${note.date.getFullYear()}`;

      // Group by day
      if (!dayMap.has(dayStr)) dayMap.set(dayStr, []);
      dayMap.get(dayStr)?.push(index);

      // Group by month
      if (!monthMap.has(monthStr)) monthMap.set(monthStr, []);
      monthMap.get(monthStr)?.push(index);

      // Group by year
      if (!yearMap.has(yearStr)) yearMap.set(yearStr, []);
      yearMap.get(yearStr)?.push(index);
    });

    groups.day = Array.from(dayMap.values()).filter((g) => g.length > 1);
    groups.month = Array.from(monthMap.values()).filter((g) => g.length > 1);
    groups.year = Array.from(yearMap.values()).filter((g) => g.length > 1);

    return groups;
  }

  // Derived store to update grouped data dynamically
  let groupedNotes = derived(journalNotes, ($journalNotes) => groupNotes($journalNotes));

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
  
<div class="relative flex min-w-max space-x-1">
  <div class="absolute top-1 left-0 right-0 h-1 bg-gray-300"></div>

  {#each $groupedNotes.year as yearGroup}
    <div
      class="absolute top-0 h-3 bg-gray-300 rounded-md border-2 border-white"
      style="
        left: {yearGroup[0] * baseWidth * scale + yearGroup[0]*space +40*scale}px;
        width: {yearGroup.length * baseWidth * scale +((yearGroup.length-1)*4) -80*scale}px;
      "
    ></div>
  {/each}

  {#each $groupedNotes.month as monthGroup}
    <div
      class="absolute top-0 h-3 bg-gray-500 rounded-md border-2 border-white"
      style="
        left: {monthGroup[0] * baseWidth * scale + monthGroup[0]*space +80*scale}px;
        width: {monthGroup.length * baseWidth * scale +((monthGroup.length-1)*4) -160*scale}px;
      "
    ></div>
  {/each}

  {#each $groupedNotes.day as dayGroup}
    <div
      class="absolute top-0 h-3 bg-gray-700 rounded-md border-2 border-white"
      style="
        left: {dayGroup[0] * baseWidth * scale + dayGroup[0]*space +120*scale}px;
        width: {dayGroup.length * baseWidth * scale +((dayGroup.length-1)*4) -240*scale}px;
      "
    ></div>
  {/each}

  {#each $journalNotes as _}
    <div class="relative flex-none" style="width: {baseWidth * scale}px;">
      <div class="relative top-0 left-1/2 h-3 w-3 bg-black rounded-full border-2 border-white"></div>
    </div>
  {/each}
</div>

  <div class="flex flex-grow space-x-1">
    {#each $journalNotes as note}
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
