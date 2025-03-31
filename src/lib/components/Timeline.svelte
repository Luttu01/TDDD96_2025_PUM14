<script lang="ts">
  import { onMount } from "svelte";
  import { derived, writable } from "svelte/store";
  import { flip } from "svelte/animate";
  import { fade } from "svelte/transition";

  type Note = {
    date: Date;
    content: string;
  };

  type Day = {
    day: number;
    notes: Note[];
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

  let notes = writable([
    { date: new Date("2021-01-01"), content: "Anteckning 1" },
    { date: new Date("2021-01-01"), content: "Anteckning 2" },
    { date: new Date("2021-01-03"), content: "Anteckning 3" },
    { date: new Date("2021-02-01"), content: "Anteckning 4" },
    { date: new Date("2021-02-01"), content: "Anteckning 5" },
    { date: new Date("2021-03-10"), content: "Anteckning 6" },
    { date: new Date("2021-03-10"), content: "Anteckning 7" },
    { date: new Date("2021-03-10"), content: "Anteckning 8" },
    { date: new Date("2021-04-01"), content: "Anteckning 9" },
    { date: new Date("2021-05-05"), content: "Anteckning 10" },
    { date: new Date("2021-05-05"), content: "Anteckning 11" },
    { date: new Date("2021-08-23"), content: "Anteckning 12" },
    { date: new Date("2021-08-23"), content: "Anteckning 13" },
    { date: new Date("2021-10-11"), content: "Anteckning 14" },
    { date: new Date("2021-12-24"), content: "Anteckning 15" },
    { date: new Date("2022-01-05"), content: "Anteckning 16" },
    { date: new Date("2022-01-05"), content: "Anteckning 17" },
    { date: new Date("2022-03-17"), content: "Anteckning 18" },
    { date: new Date("2022-04-25"), content: "Anteckning 19" },
    { date: new Date("2022-04-25"), content: "Anteckning 20" },
    { date: new Date("2022-04-25"), content: "Anteckning 21" },
    { date: new Date("2022-07-20"), content: "Anteckning 22" },
    { date: new Date("2022-08-30"), content: "Anteckning 23" },
    { date: new Date("2022-09-15"), content: "Anteckning 24" },
    { date: new Date("2022-12-31"), content: "Anteckning 25" },
    { date: new Date("2023-01-01"), content: "Anteckning 26" },
    { date: new Date("2023-01-01"), content: "Anteckning 27" },
    { date: new Date("2023-02-14"), content: "Anteckning 28" },
    { date: new Date("2023-02-14"), content: "Anteckning 29" },
    { date: new Date("2023-02-14"), content: "Anteckning 30" },
  ]);

  let scale: number = 1;
  let speed: number = 0.01;
  const minScale: number = 0.5;
  const maxScale: number = 1.5;
  const baseWidth: number = 320;
  const buttonPaddingX: number = 20;

  let enableTransition = writable(false);
  $: scale, enableTransition.set(false);

  function buildHierarchy(notes: Note[]): Year[] {
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

    hierarchy.sort((a, b) => b.year - a.year);
    hierarchy.forEach((y) => y.months.sort((a, b) => b.month - a.month));
    hierarchy.forEach((y) =>
      y.months.forEach((m) => m.days.sort((a, b) => b.day - a.day))
    );

    return hierarchy;
  }

  const noteHierarchy = writable<Year[]>(buildHierarchy($notes));

  function toggleCollapse(
    group: { isCollapsed: boolean },
    event?: Event
  ): void {
    if (event) event.stopPropagation();
    setTimeout(() => enableTransition.set(true), 300);
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

  function calculateWidth(group: Year | Month | Day) {
    return (
      baseWidth * countVisibleNotes([group]) * scale +
      4 * countVisibleNotes([group]) -
      buttonPaddingX * 2 * ("month" in group ? 2 : "day" in group ? 3 : 1)
    );
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
              text: `${new Date(year.year, month.month).toLocaleDateString(
                "sv-SE",
                {
                  year: "numeric",
                  month: "numeric",
                }
              )} (${count} anteckningar dolda)`,
              month,
            });
          } else {
            for (const day of month.days) {
              if (day.isCollapsed) {
                output.push({
                  type: "summary",
                  text: `${day.notes[0]?.date.toLocaleDateString("sv-SE")} (${day.notes.length} anteckningar dolda)`,
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
    <div
      class="flex relative min-w-max px-[{buttonPaddingX}px] justify-between"
      transition:fade={{ duration: 150 }}
    >
      {#each $noteHierarchy as yearGroup}
        <button
          on:click={(event) => toggleCollapse(yearGroup, event)}
          class="h-2 bg-purple-300 rounded-full"
          class:transition-width={$enableTransition}
          style="width: {calculateWidth(yearGroup)}px;"
          aria-label="Toggle year group"
        >
          {#if !yearGroup.isCollapsed}
            <div
              class="flex justify-between px-[{buttonPaddingX}px]"
              transition:fade={{ duration: 150 }}
            >
              {#each yearGroup.months as monthGroup}
                <!-- svelte-ignore node_invalid_placement_ssr -->
                <button
                  on:click={(event) => toggleCollapse(monthGroup, event)}
                  class="h-2 bg-purple-500 rounded-full"
                  class:transition-width={$enableTransition}
                  style="width: {calculateWidth(monthGroup)}px;"
                  aria-label="Toggle month group"
                >
                  {#if !monthGroup.isCollapsed}
                    <div
                      class="flex justify-between px-[{buttonPaddingX}px]"
                      transition:fade={{ duration: 150 }}
                    >
                      {#each monthGroup.days as dayGroup}
                        <button
                          on:click={(event) => toggleCollapse(dayGroup, event)}
                          class="h-2 bg-purple-700 rounded-full"
                          class:transition-width={$enableTransition}
                          style="width: {calculateWidth(dayGroup)}px;"
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
      {#each $visibleNotes as item (item.type === "note" ? item.note?.date : item.text)}
        <div class="flex flex-grow" animate:flip={{ duration: 250 }}>
          {#if item.type === "summary"}
            <button
              transition:fade={{ duration: 150 }}
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
              transition:fade={{ duration: 150 }}
              class="bg-white flex-none p-1 rounded-md shadow-sm"
              style="width: {baseWidth * scale}px;"
            >
              <div class="text-left text-sm text-gray-500">
                {item.note?.date.toLocaleDateString("sv-SE")}
              </div>
              {item.note?.content}
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .transition-width {
    transition: width 250ms ease-in-out;
  }
</style>
