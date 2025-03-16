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
    let groups: Record<GroupType, number[][]> = {
      day: [],
      month: [],
      year: [],
    };
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

  let groupedNotes = derived(journalNotes, ($journalNotes) =>
    groupNotes($journalNotes)
  );

  function handleZoom(event: WheelEvent): void {
    if (event.ctrlKey) {
      event.preventDefault();
      scale -= event.deltaY * speed;
      scale = Math.min(maxScale, Math.max(minScale, scale));
    }
  }

  let collapsedYears = writable(new Set<number>());
  let collapsedMonths = writable(new Set<number>());
  let collapsedDays = writable(new Set<number>());

  function toggleCollapse(
    setStore: typeof collapsedYears,
    index: number,
    parentStore?: typeof collapsedYears,
    parentIndex?: number
  ) {
    setStore.update((set) => {
      if (set.has(index)) {
        set.delete(index);
      } else {
        set.add(index);
        if (parentStore && parentIndex !== undefined) {
          parentStore.update((pSet) => {
            pSet.delete(parentIndex);
            return new Set(pSet);
          });
        }
      }
      return new Set(set);
    });
  }

  function isCollapsed(
    index: number,
    groups: number[][],
    collapsedSet: Set<number>
  ): boolean {
    return groups.some(
      (group, groupIndex) =>
        collapsedSet.has(groupIndex) && group.includes(index)
    );
  }

  function getCollapsedSummary(groups: number[][], collapsedSet: Set<number>) {
    return groups
      .map((group, groupIndex) => ({
        index: groupIndex,
        start: $journalNotes[group[0]].date,
        end: $journalNotes[group[group.length - 1]].date,
        count: group.length,
      }))
      .filter(({ index }) => collapsedSet.has(index));
  }

  function getCollapsedCountBefore(
    index: number,
    collapsedSets: Set<number>[],
    groupedNotes: number[][][]
  ): number {
    return groupedNotes
      .flatMap((groups, level) =>
        groups.slice(0, index).reduce((count, group, groupIndex) => {
          if (
            level > 0 &&
            collapsedSets[level - 1].has(
              groupedNotes[level - 1].findIndex((g) => g.includes(group[0]))
            )
          ) {
            return count;
          }
          return collapsedSets[level].has(groupIndex)
            ? count + (group.length - 1)
            : count;
        }, 0)
      )
      .reduce((a, b) => a + b, 0);
  }

  function getCollapsedCount(
    index: number,
    collapsedSets: Set<number>[],
    groupedNotes: number[][][]
  ): number {
    return groupedNotes
      .flatMap((groups, level) =>
        groups.slice(index).reduce((count, group, groupIndex) => {
          if (
            level > 0 &&
            collapsedSets[level - 1].has(
              groupedNotes[level - 1].findIndex((g) => g.includes(group[0]))
            )
          ) {
            return count;
          }
          return collapsedSets[level].has(groupIndex)
            ? count + (group.length - 1)
            : count;
        }, 0)
      )
      .reduce((a, b) => a + b, 0);
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

    {#each $groupedNotes.year as yearGroup, yearIndex}
      <button
        on:click={() => toggleCollapse(collapsedYears, yearIndex)}
        class="absolute top-0 h-3 bg-gray-300 rounded-md border-2 border-white"
        style="
        left: {(yearGroup[0] -
          getCollapsedCountBefore(
            yearIndex,
            [$collapsedYears, $collapsedMonths, $collapsedDays],
            [$groupedNotes.year, $groupedNotes.month, $groupedNotes.day]
          )) *
          baseWidth *
          scale +
          (yearGroup[0] -
            getCollapsedCountBefore(
              yearIndex,
              [$collapsedYears, $collapsedMonths, $collapsedDays],
              [$groupedNotes.year, $groupedNotes.month, $groupedNotes.day]
            ) -
            1) *
            4 +
          40 * scale}px;
        width: {!$collapsedYears.has(yearIndex)
          ? (yearGroup.length -
              getCollapsedCount(
                yearIndex,
                [$collapsedMonths, $collapsedDays],
                [$groupedNotes.month, $groupedNotes.day]
              )) *
              baseWidth *
              scale +
            (yearGroup.length -
              getCollapsedCount(
                yearIndex,
                [$collapsedMonths, $collapsedDays],
                [$groupedNotes.month, $groupedNotes.day]
              ) +
              1) *
              4 -
            80 * scale
          : baseWidth * scale - 80 * scale + 8}px;
      "
        aria-label="Toggle year group"
      ></button>
    {/each}

    {#each $groupedNotes.month as monthGroup, monthIndex}
      {#if !$collapsedYears.has($groupedNotes.year.findIndex( (g) => g.includes(monthGroup[0]) ))}
        <button
          on:click={() => toggleCollapse(collapsedMonths, monthIndex)}
          class="absolute top-0 h-3 bg-gray-500 rounded-md border-2 border-white"
          style="
          left: {(monthGroup[0] -
            getCollapsedCountBefore(
              monthIndex,
              [$collapsedYears, $collapsedMonths, $collapsedDays],
              [$groupedNotes.year, $groupedNotes.month, $groupedNotes.day]
            )) *
            baseWidth *
            scale +
            (monthGroup[0] -
              getCollapsedCountBefore(
                monthIndex,
                [$collapsedYears, $collapsedMonths, $collapsedDays],
                [$groupedNotes.year, $groupedNotes.month, $groupedNotes.day]
              ) -
              1) *
              4 +
            80 * scale}px;
          width: {!$collapsedMonths.has(monthIndex)
            ? (monthGroup.length -
                getCollapsedCount(
                  monthIndex,
                  [$collapsedDays],
                  [$groupedNotes.day]
                )) *
                baseWidth *
                scale +
              (monthGroup.length -
                getCollapsedCount(
                  monthIndex,
                  [$collapsedDays],
                  [$groupedNotes.day]
                ) +
                1) *
                4 -
              160 * scale
            : baseWidth * scale - 160 * scale + 8}px;
        "
          aria-label="Toggle month group"
        ></button>
      {/if}
    {/each}

    {#each $groupedNotes.day as dayGroup, dayIndex}
      {#if !$collapsedYears.has($groupedNotes.year.findIndex( (g) => g.includes(dayGroup[0]) )) && !$collapsedMonths.has($groupedNotes.month.findIndex( (g) => g.includes(dayGroup[0]) ))}
        <button
          on:click={() => toggleCollapse(collapsedDays, dayIndex)}
          class="absolute top-0 h-3 bg-gray-700 rounded-md border-2 border-white"
          style="
          left: {(dayGroup[0] -
            getCollapsedCountBefore(
              dayIndex,
              [$collapsedYears, $collapsedMonths, $collapsedDays],
              [$groupedNotes.year, $groupedNotes.month, $groupedNotes.day]
            )) * baseWidth * scale +
            (dayGroup[0] -
              getCollapsedCountBefore(
                dayIndex,
                [$collapsedYears, $collapsedMonths, $collapsedDays],
                [$groupedNotes.year, $groupedNotes.month, $groupedNotes.day]
              ) - 1) * 4 + 120 * scale}px;
          width: {!$collapsedDays.has(dayIndex)
            ? dayGroup.length * baseWidth * scale + (dayGroup.length + 1) * 4 - 240 * scale
            : baseWidth * scale - 240 * scale + 8}px;
          "
          aria-label="Toggle day group"
        ></button>
      {/if}
    {/each}

    <!-- TODO: fixa så en prick finns för en kollapsad enhet också, nu tas alla prickar bort -->
    {#each $journalNotes as _, index}
      {#if !isCollapsed(index, $groupedNotes.year, $collapsedYears) && !isCollapsed(index, $groupedNotes.month, $collapsedMonths) && !isCollapsed(index, $groupedNotes.day, $collapsedDays)}
        <div
          class="flex flex-none items-center justify-center"
          style="width: {baseWidth * scale}px;"
        >
          <div
            class="relative h-3 w-3 bg-black rounded-full border-2 border-white"
          ></div>
        </div>
      {/if}
    {/each}
  </div>

  <!-- TODO: fixa hela denna så allt är i ordning och under rätt prick vid kollaps, också att om förälderkollaps så behövs inte summary av barn -->
  <div class="flex flex-grow space-x-1">
    {#each getCollapsedSummary($groupedNotes.year, $collapsedYears) as summary}
      <button
        class="bg-gray-200 flex-none p-1 rounded-md shadow-sm text-gray-700"
        style="width: {baseWidth * scale}px;"
        on:click={() => toggleCollapse(collapsedYears, summary.index)}
      >
        <div class="text-sm text-gray-600">
          År {summary.start.getFullYear()}
        </div>
        <div>{summary.count} anteckningar dolda</div>
      </button>
    {/each}

    {#each getCollapsedSummary($groupedNotes.month, $collapsedMonths) as summary}
      <button
        class="bg-gray-300 flex-none p-1 rounded-md shadow-sm text-gray-700"
        style="width: {baseWidth * scale}px;"
        on:click={() => toggleCollapse(collapsedMonths, summary.index)}
      >
        <div class="text-sm text-gray-600">
          Månad {summary.start.toLocaleString("default", { month: "long" })}
        </div>
        <div>{summary.count} anteckningar dolda</div>
      </button>
    {/each}

    {#each getCollapsedSummary($groupedNotes.day, $collapsedDays) as summary}
      <button
        class="bg-gray-400 flex-none p-1 rounded-md shadow-sm text-gray-700"
        style="width: {baseWidth * scale}px;"
        on:click={() => toggleCollapse(collapsedDays, summary.index)}
      >
        <div class="text-sm text-gray-600">{summary.start.toDateString()}</div>
        <div>{summary.count} anteckningar dolda</div>
      </button>
    {/each}

    {#each $journalNotes as note, index}
      {#if !isCollapsed(index, $groupedNotes.year, $collapsedYears) && !isCollapsed(index, $groupedNotes.month, $collapsedMonths) && !isCollapsed(index, $groupedNotes.day, $collapsedDays)}
        <div
          class="bg-white flex-none p-1 rounded-md shadow-sm"
          style="width: {baseWidth * scale}px;"
        >
          <div class="text-left text-sm text-gray-500">
            {note.date.toDateString()}
          </div>
          {note.content}
        </div>
      {/if}
    {/each}
  </div>
</div>
