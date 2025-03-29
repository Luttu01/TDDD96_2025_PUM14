<script lang="ts">
  import { onMount } from "svelte";
  import { derived, writable } from "svelte/store";

  type JournalNote = {
    date: Date;
    content: string;
  };

  type Day = {
    day: number;
    notes: JournalNote[];
    isCollapsed: boolean;
  };

  type Month = {
    month: number;
    days: Day[];
    isCollapsed: boolean;
  };

  type Year = {
    year: number;
    months: Month[];
    isCollapsed: boolean;
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

  function buildHierarchy(notes: JournalNote[]): Year[] {
    const hierarchy: Year[] = [];

    notes.forEach((note) => {
      const noteYear = note.date.getFullYear();
      const noteMonth = note.date.getMonth();
      const noteDay = note.date.getDay();

      let yearGroup = hierarchy.find((y) => y.year === noteYear);
      if (!yearGroup) {
        yearGroup = { year: noteYear, months: [], isCollapsed: false };
        hierarchy.push(yearGroup);
      }

      let monthGroup = yearGroup.months.find((m) => m.month === noteMonth);
      if (!monthGroup) {
        monthGroup = { month: noteMonth, days: [], isCollapsed: false };
        yearGroup.months.push(monthGroup);
      }

      let dayGroup = monthGroup.days.find((d) => d.day === noteDay);
      if (!dayGroup) {
        dayGroup = { day: noteDay, notes: [], isCollapsed: false };
        monthGroup.days.push(dayGroup);
      }

      dayGroup.notes.push(note);
    });

    hierarchy.sort((a, b) => a.year - b.year);
    hierarchy.forEach((y) => y.months.sort((a, b) => a.month - b.month));
    hierarchy.forEach((y) =>
      y.months.forEach((m) => m.days.sort((a, b) => a.day - b.day))
    );

    return hierarchy;
  }

  const noteHierarchy = writable<Year[]>(buildHierarchy($journalNotes));

  function toggleCollapse(
    group: { isCollapsed: boolean },
    event?: Event
  ): void {
    if (event) event.stopPropagation();
    group.isCollapsed = !group.isCollapsed;
    noteHierarchy.update((n) => [...n]);
  }

  function countVisibleNotes(groups: (Year | Month | Day)[]): number {
    let count = 0;
    for (const group of groups) {
      if ("notes" in group) {
        count += group.isCollapsed ? 1 : group.notes.length;
      } else if ("days" in group) {
        count += group.isCollapsed ? 1 : countVisibleNotes(group.days);
      } else if ("months" in group) {
        count += group.isCollapsed ? 1 : countVisibleNotes(group.months);
      }
    }
    return count;
  }

  const visibleNotes = derived(noteHierarchy, ($noteHierarchy) => {
    let output = [];

    for (const year of $noteHierarchy) {
      if (year.isCollapsed) {
        const count = year.months.reduce(
          (sum, month) =>
            sum +
            month.days.reduce((daySum, day) => daySum + day.notes.length, 0),
          0
        );
        output.push({
          type: "summary",
          text: `${year.year} (${count} anteckningar dolda)`,
          year,
        });
      } else {
        for (const month of year.months) {
          if (month.isCollapsed) {
            const count = month.days.reduce(
              (sum, day) => sum + day.notes.length,
              0
            );
            output.push({
              type: "summary",
                text: `${new Date(year.year, month.month).toLocaleDateString("sv-SE", {
                  year: "numeric",
                  month: "long",
                  })} (${count} anteckningar dolda)`,
              month,
            });
          } else {
            for (const day of month.days) {
              if (day.isCollapsed) {
                output.push({
                  type: "summary",
                  text: `${day.notes[0]?.date.toLocaleDateString("sv-SE", {
                    weekday: "long",
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                    })} (${day.notes.length} anteckningar dolda)`,
                  day,
                });
              } else {
                for (const note of day.notes) {
                  output.push({ type: "note", note });
                }
              }
            }
          }
        }
      }
    }

    return output;
  });

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

<div class="h-full bg-gray-100 flex overflow-x-auto">
  <div class="w-max flex-col flex p-2 space-y-2">
    <div class="flex relative min-w-max px-[10px] justify-between">
      {#each $noteHierarchy as yearGroup}
        <button
          on:click={(event) => toggleCollapse(yearGroup, event)}
          class="h-4 bg-purple-300 rounded-full"
          style="width: {baseWidth * countVisibleNotes([yearGroup]) * scale +
            4 * countVisibleNotes([yearGroup]) -
            25}px;"
          aria-label="Toggle year group"
        >
          {#if !yearGroup.isCollapsed}
            <div class="flex justify-between px-[30px]">
              {#each yearGroup.months as monthGroup}
                <!-- svelte-ignore node_invalid_placement_ssr -->
                <button
                  on:click={(event) => toggleCollapse(monthGroup, event)}
                  class="h-4 bg-purple-500 rounded-full "
                  style="width: {baseWidth *
                    countVisibleNotes([monthGroup]) *
                    scale +
                    4 * countVisibleNotes([monthGroup]) -
                    85}px;"
                  aria-label="Toggle month group"
                >
                  {#if !monthGroup.isCollapsed}
                    <div class="flex justify-between px-[30px]">
                      {#each monthGroup.days as dayGroup}
                        <button
                          on:click={(event) => toggleCollapse(dayGroup, event)}
                          class="h-4 bg-purple-700 rounded-full "
                          style="width: {baseWidth *
                            countVisibleNotes([dayGroup]) *
                            scale +
                            4 * countVisibleNotes([dayGroup]) -
                            145}px;"
                          aria-label="Toggle day group"
                        >
                        </button>
                      {/each}
                    </div>
                  {/if}
                </button>
              {/each}
            </div>
          {/if}
        </button>
      {/each}
    </div>
    <div class="flex flex-grow space-x-1">
      {#each $visibleNotes as item}
        {#if item.type === "summary"}
          <button
            class="bg-gray-200 flex-none p-1 rounded-md shadow-sm text-gray-700"
            style="width: {baseWidth * scale}px;"
            on:click={() => {
              if (item.year) toggleCollapse(item.year);
              else if (item.month) toggleCollapse(item.month);
              else if (item.day) toggleCollapse(item.day);
            }}
          >
            {item.text}
          </button>
        {:else}
          <div
            class="bg-white flex-none p-1 rounded-md shadow-sm"
            style="width: {baseWidth * scale}px;"
          >
            <div class="text-left text-sm text-gray-500">
                {item.note?.date.toLocaleDateString("sv-SE", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
                })}
            </div>
            {item.note?.content}
          </div>
        {/if}
      {/each}
    </div>
  </div>
</div>
