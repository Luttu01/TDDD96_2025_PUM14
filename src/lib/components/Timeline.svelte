<script lang="ts">
  import { writable } from "svelte/store";
  import { onDestroy, onMount } from "svelte";
  import NotePreview from "./NotePreview.svelte";

  import type { Note, Year, Month } from "$lib/models";
  import { buildDateHierarchy } from "$lib/utils";
  import { allNotes, selectedNotes, destructMode, filter } from "$lib/stores";
  import { stringToColor } from "$lib/utils";

  const noteHierarchy = writable<Year[]>([]);

  $: {
    const currentHierarchy = $noteHierarchy;
    const updatedHierarchy = buildDateHierarchy($allNotes);

    // Preserve collapsed state for years and months
    for (const year of updatedHierarchy) {
      const existingYear = currentHierarchy.find((y) => y.year === year.year);
      if (existingYear) {
        year.isCollapsed = existingYear.isCollapsed;

        for (const month of year.months) {
          const existingMonth = existingYear.months.find(
            (m) => m.month === month.month
          );
          if (existingMonth) {
            month.isCollapsed = existingMonth.isCollapsed;
          }
        }
      }
    }

    noteHierarchy.set(updatedHierarchy);
  }

  function toggleGroup(group: Year | Month) {
    group.isCollapsed = !group.isCollapsed;
    noteHierarchy.set($noteHierarchy);
  }

  function toggleAllYearGroups() {
    const allCollapsed = $noteHierarchy.every((group) => group.isCollapsed);
    for (const group of $noteHierarchy) {
      group.isCollapsed = !allCollapsed;
    }
    noteHierarchy.set($noteHierarchy);
  }
  function toggleAllMonthGroups() {
    const allCollapsed = $noteHierarchy.every((group) =>
      group.months.every((month) => month.isCollapsed)
    );
    for (const group of $noteHierarchy) {
      for (const month of group.months) {
        month.isCollapsed = !allCollapsed;
      }
    }
    noteHierarchy.set($noteHierarchy);
  }

  function handleNoteClick(noteData: Note) {
    $selectedNotes = $selectedNotes || [];

    const foundIndex = $selectedNotes.findIndex(
      (n) => n.CaseData === noteData.CaseData
    );

    let newSelectedNotes = [...$selectedNotes];

    if (foundIndex >= 0) {
      newSelectedNotes.splice(foundIndex, 1);
    } else {
      newSelectedNotes.push(noteData);
    }

    selectedNotes.set(newSelectedNotes);
  }

  function matchesAnyFilter(note: Note) {
    for (const [key, activeValues] of $filter.entries()) {
      if (activeValues.size === 0) continue;

      let noteValue;

      // Map filter key to note property
      switch (key) {
        case "Yrkesroll":
          noteValue = note.Dokument_skapad_av_yrkestitel_Namn;
          break;
        case "Vårdenhet":
          noteValue = note.Vårdenhet_Namn;
          break;
        case "Journalmall":
          noteValue = note.Dokumentnamn;
          break;
        default:
          noteValue = note[key as keyof Note]; // fallback if any other key
      }

      if (typeof noteValue === "string" && activeValues.has(noteValue)) {
        return true; // found a match
      }
    }

    if (note.keywords.length > 0) {
      return true;
    }

    return false; // no matches
  }

  function matchesAllFilters(note: Note) {
  // Check all filter categories (AND logic across them)
  for (const [key, activeValues] of $filter.entries()) {
    if (activeValues.size === 0) continue;

    let noteValue: string | undefined;

    switch (key) {
      case "Yrkesroll":
        noteValue = note.Dokument_skapad_av_yrkestitel_Namn;
        break;
      case "Vårdenhet":
        noteValue = note.Vårdenhet_Namn;
        break;
      case "Journalmall":
        noteValue = note.Dokumentnamn;
        break;
      default:
        noteValue = note[key as keyof Note] as string;
    }

    if (!noteValue || !activeValues.has(noteValue)) {
      return false;
    }
  }

  // If keyword search is active, note.keywords must not be empty
  if (note.keywords.length === 0) {
    return false;
  }

  return true;
}



  function getNoteSizeState(yearGroup: Year, monthGroup: Month, note: Note) {
    if ($destructMode && !matchesAnyFilter(note)) return "hidden";
    if (yearGroup.isCollapsed) return "compact";
    if (monthGroup.isCollapsed) return "medium";
    return "expanded";
  }

  function isInSelectedNotes(note: Note) {
    return $selectedNotes.some((n) => n.CaseData === note.CaseData);
  }

  function getKeywordContext(caseData: string, keyword: string): string {
    const parser = new DOMParser();
    const parsedDocument = parser.parseFromString(caseData, "text/html");
    const boldElements = parsedDocument.querySelectorAll("b");

    for (const boldElement of boldElements) {
      if (boldElement.textContent?.toLowerCase() === keyword.toLowerCase()) {
        const siblingText = boldElement.nextSibling?.textContent?.trim();
        if (siblingText) {
          const maxLength = 60;
          const truncatedText =
            siblingText.length > maxLength
              ? siblingText.slice(0, maxLength) + "..."
              : siblingText;
          return `<strong style="font-weight: bold;">${keyword}</strong>${truncatedText}`;
        }
      }
    }
    return `<strong style="font-weight: bold;">${keyword}</strong>`;
  }

  let scrollContainer: HTMLElement | null = null;
  let noteElements: Record<string, HTMLElement> = {};

  const outOfViewKeywords = writable(new Map<string, number>());

function makeKey(keyword: string, direction: string): string {
  return `${keyword}::${direction}`;
}

function updateOutOfViewNotes() {
  if (!scrollContainer) return;
  const containerRect = scrollContainer.getBoundingClientRect();
  const updatedMap = new Map<string, number>();

  for (const [noteId, el] of Object.entries(noteElements)) {
    const rect = el.getBoundingClientRect();
    const note = $allNotes.find((n) => n.Dokument_ID === noteId);
    if (!note) continue;

    for (const keyword of note.keywords) {
      const isOutOfRight = rect.right > containerRect.right;
      const isOutOfLeft = rect.left < containerRect.left;

      if (isOutOfRight) {
        const key = makeKey(keyword, "right");
        const count = updatedMap.get(key) || 0;
        updatedMap.set(key, count + 1);
      }

      if (isOutOfLeft) {
        const key = makeKey(keyword, "left");
        const count = updatedMap.get(key) || 0;
        updatedMap.set(key, count + 1);
      }
    }
  }

  outOfViewKeywords.set(updatedMap);
}

function scrollToKeywordInDirection(keyword: string, direction: string) {
  if (!scrollContainer) return;

  const containerRect = scrollContainer.getBoundingClientRect();
  const notesWithKeyword = Object.entries(noteElements)
    .map(([noteId, el]) => {
      const note = $allNotes.find((n) => n.Dokument_ID === noteId);
      if (note && note.keywords.includes(keyword)) {
        return { el, rect: el.getBoundingClientRect(), note };
      }
      return null;
    })
    .filter((item): item is { el: HTMLElement; rect: DOMRect; note: Note } => item !== null);

  const outOfViewNotes = notesWithKeyword.filter(({ rect }) =>
    direction === "right"
      ? rect.right > containerRect.right
      : rect.left < containerRect.left
  );

  if (outOfViewNotes.length === 0) return;

  const nearest = outOfViewNotes.reduce((closest, current) => {
    const distance = direction === "right"
      ? current.rect.left - containerRect.right
      : containerRect.left - current.rect.right;

    const closestDistance = direction === "right"
      ? closest.rect.left - containerRect.right
      : containerRect.left - closest.rect.right;

    return distance < closestDistance ? current : closest;
  }, outOfViewNotes[0]);

  if (nearest) {
    const offset = (containerRect.width - nearest.rect.width) / 2;
    scrollContainer.scrollTo({
      left: nearest.rect.left - containerRect.left + scrollContainer.scrollLeft - offset,
      behavior: "smooth",
    });
  }
}



  onMount(() => {
    updateOutOfViewNotes();
    if (scrollContainer) {
      scrollContainer.addEventListener("scroll", updateOutOfViewNotes);
    }
    if (noteElements) {
      for (const el of Object.values(noteElements)) {
        el.addEventListener("transitionend", updateOutOfViewNotes);
      }
    }
  });

  onDestroy(() => {
    if (scrollContainer) {
      scrollContainer.removeEventListener("scroll", updateOutOfViewNotes);
    }
    if (noteElements) {
      for (const el of Object.values(noteElements)) {
        el.removeEventListener("transitionend", updateOutOfViewNotes);
      }
    }
  });
</script>

{#if $outOfViewKeywords.entries().filter(([key]) => key.split("::")[1] === "right").toArray().length > 0}
  <div
    id="out-of-view-keywords-right"
    class="absolute right-0 top-18 flex flex-col space-y-1 bg-white p-2 rounded-l-md shadow-md"
    style="z-index: 100;"
  >
    {#each Array.from($outOfViewKeywords.entries()).filter(([key]) => key.split("::")[1] === "right") as [key, count]}
      {#key key}
        {#if key.split("::").length === 2}
          <button
            id="keyword-bubble-right-{key.split('::')[0].replace(/\s+/g, '-')}"
            class="w-5 h-5 rounded-md text-xs flex items-center justify-center relative"
            style="background-color: {stringToColor(key.split('::')[0])}"
            onclick={() => scrollToKeywordInDirection(key.split("::")[0], "right")}
            aria-label="Scroll to keyword {key.split('::')[0]}"
            title="Scroll to keyword {key.split('::')[0]}"
          >
            {count}
            <div
              id="keyword-pointer-right-{key.split('::')[0].replace(/\s+/g, '-')}"
              class="absolute right-[-12px] top-1/2 -translate-y-1/2 w-0 h-0 border-l-[6px] border-r-transparent border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-r-[6px]"
              style="border-left-color: {stringToColor(key.split('::')[0])}"
            ></div>
          </button>
        {/if}
      {/key}
    {/each}
  </div>
{/if}

{#if $outOfViewKeywords.entries().filter(([key]) => key.split("::")[1] === "left").toArray().length > 0}
  <div
    id="out-of-view-keywords-left"
    class="absolute left-0 top-18 flex flex-col space-y-1 bg-white p-2 rounded-r-md shadow-md"
    style="z-index: 100;"
  >
    {#each Array.from($outOfViewKeywords.entries()).filter(([key]) => key.split("::")[1] === "left") as [key, count]}
      {#key key}
        {#if key.split("::").length === 2}
          <button
            id="keyword-bubble-left-{key.split('::')[0].replace(/\s+/g, '-')}"
            class="w-5 h-5 rounded-md text-xs flex items-center justify-center relative"
            style="background-color: {stringToColor(key.split('::')[0])}"
            onclick={() => scrollToKeywordInDirection(key.split("::")[0], "left")}
            aria-label="Scroll to keyword {key.split('::')[0]}"
            title="Scroll to keyword {key.split('::')[0]}"
          >
            {count}
            <div
              id="keyword-pointer-left-{key.split('::')[0].replace(/\s+/g, '-')}"
              class="absolute left-[-12px] top-1/2 -translate-y-1/2 w-0 h-0 border-r-[6px] border-l-transparent border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-l-[6px]"
              style="border-right-color: {stringToColor(key.split('::')[0])}"
            ></div>
          </button>
        {/if}
      {/key}
    {/each}
  </div>
{/if}



<div
  id="scroll-container"
  class="flex bg-gray-100 overflow-x-auto h-full"
  bind:this={scrollContainer}
>
  <div id="years-container" class="flex flex-row space-x-[8px] h-full min-h-0">
    {#each $noteHierarchy as yearGroup (yearGroup.year)}
      <div id="year-{yearGroup.year}" class="flex flex-col h-full min-h-0">
        <button
          id="toggle-year-{yearGroup.year}"
          class="flex bg-purple-100 py-1 text-left text-sm px-1 w-full shadow-sm justify-between {yearGroup.isCollapsed ? 'cursor-zoom-in' : 'cursor-zoom-out'}"
          onclick={() => (toggleAllYearGroups())}
          aria-label="Toggle year {yearGroup.year}"
        >
          <div id="year-label-{yearGroup.year}" class="text-xs sticky left-1 w-7 font-bold text-gray-900">
            {yearGroup.year}
          </div>
        </button>
        <div id="months-container-year-{yearGroup.year}" class="flex flex-row space-x-[8px] h-full min-h-0">
          {#each yearGroup.months as monthGroup}
            <div id="month-{yearGroup.year}-{monthGroup.month}" class="flex flex-col h-full min-h-0">
              <button
                id="toggle-month-{yearGroup.year}-{monthGroup.month}"
                class="{yearGroup.isCollapsed ? 'h-0 py-0 w-6' : 'h-6 py-1 w-full'} flex bg-purple-200 justify-between px-1 shadow-xs transition-all duration-300 shadow-md {monthGroup.isCollapsed ? 'cursor-zoom-in' : 'cursor-zoom-out'}"
                onclick={() => (toggleAllMonthGroups())}
                aria-label="Toggle month {monthGroup.month}"
              >
                <div
                  id="month-label-{yearGroup.year}-{monthGroup.month}"
                  class="{yearGroup.isCollapsed ? 'text-transparent' : 'text-gray-900'} text-xs sticky left-1 w-7 font-semibold text-left"
                >
                  {new Date(0, monthGroup.month).toLocaleString("sv-SE", {
                    month: "short",
                  })}
                </div>
              </button>
              <div
                id="notes-container-{yearGroup.year}-{monthGroup.month}"
                class="flex flex-row space-x-[8px] items-start h-full min-h-0 mb-4"
              >
                {#each monthGroup.notes as note}
                  {#key note.Dokument_ID}
                    <button
                      id="note-{note.Dokument_ID}"
                      class={`transition-all mt-2 duration-300 border rounded-md shadow-xs ${isInSelectedNotes(note) ? "bg-purple-50 border-purple-300 hover:bg-purple-100" : "bg-white border-gray-200 hover:bg-gray-50"} relative cursor-pointer ${
                        getNoteSizeState(yearGroup, monthGroup, note) === "compact"
                          ? "flex flex-col py-2 px-1 w-12 space-y-1"
                          : getNoteSizeState(yearGroup, monthGroup, note) === "medium"
                            ? "flex flex-col p-2 w-42 text-sm text-left"
                            : getNoteSizeState(yearGroup, monthGroup, note) === "hidden"
                              ? "w-6 flex flex-col"
                              : "flex flex-col p-2 w-100 h-full min-h-0"
                      }`}
                      onclick={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                      bind:this={noteElements[note.Dokument_ID]}
                    >
                      <div
                        id="note-pointer-{note.Dokument_ID}"
                        class="transition-all duration-300 absolute -top-2 left-1/2 -translate-x-1/2 w-0 h-0 border-b-10
                 {getNoteSizeState(yearGroup, monthGroup, note) === "hidden" ? 'border-l-4 border-r-4' : 'border-l-10 border-r-10'} border-transparent {isInSelectedNotes(
                          note
                        )
                          ? 'border-b-purple-300'
                          : 'border-b-white'}"
                      ></div>
                      {#if getNoteSizeState(yearGroup, monthGroup, note) === "hidden"}
                        <div id="note-hidden-placeholder-{note.Dokument_ID}" class="h-12 bg-white rounded-md"></div>
                      {:else if getNoteSizeState(yearGroup, monthGroup, note) === "compact"}
                        <span id="note-date-{note.Dokument_ID}" class="text-[10px] text-gray-500 font-mono">
                          {new Date(note.DateTime).toLocaleDateString("sv-SE", {
                            month: "2-digit",
                            day: "2-digit",
                          })}
                        </span>
                        <NotePreview {note} direction="flex-col" />
                        <span id="note-keywords-{note.Dokument_ID}" class="flex flex-col">
                          {#each note.keywords as keyword}
                            <div
                              id="note-keyword-{note.Dokument_ID}-{keyword}"
                              class="h-2"
                              style="background-color: {stringToColor(keyword)}"
                              title={keyword}
                            ></div>
                          {/each}
                        </span>
                      {:else if getNoteSizeState(yearGroup, monthGroup, note) === "medium"}
                        <div
                          id="note-metadata-{note.Dokument_ID}"
                          class="text-gray-500 text-xs flex justify-between items-center border-b-1 border-gray-200 pb-1 font-mono"
                        >
                          {new Date(note.DateTime).toLocaleDateString("sv-SE")}
                          <NotePreview {note} />
                        </div>
                        <div
                          id="note-title-container-{note.Dokument_ID}"
                          class="text-gray-900 text-xs font-bold flex justify-between h-5 text-ellipsis whitespace-nowrap overflow-hidden"
                        >
                          {note.Dokumentnamn}
                        </div>
                        <span
                          id="note-keywords-list-{note.Dokument_ID}"
                          class="text-sm font-medium flex flex-col"
                        >
                          {#each note.keywords as keyword, index}
                            {#if index < 4 || note.keywords.length <= 5}
                              <span
                                id="note-keyword-context-{note.Dokument_ID}-{keyword}"
                                class="text-xs font-light px-1"
                                style="background-color: {stringToColor(keyword)}"
                              >
                                {@html getKeywordContext(
                                  note.CaseData,
                                  keyword
                                )}
                              </span>
                            {:else if index === 4}
                              <span
                                id="note-keyword-more-{note.Dokument_ID}"
                                class="text-xs font-light px-1 bg-gray-200 cursor-pointer"
                                title="Show more keywords"
                              >
                                + {note.keywords.length - 4}
                              </span>
                            {/if}
                          {/each}
                        </span>
                      {:else}
                        <div
                          id="note-detailed-view-{note.Dokument_ID}"
                          class="text-gray-900 text-left text-xs w-full flex flex-col h-full min-h-0"
                        >
                          <div
                            id="note-detailed-header-{note.Dokument_ID}"
                            class="text-gray-500 text-xs flex justify-between items-center border-b-1 border-gray-200 pb-1 font-mono"
                          >
                            {new Date(note.DateTime).toLocaleDateString(
                              "sv-SE",
                              {
                                year: "numeric",
                                month: "2-digit",
                                day: "2-digit",
                                hour: "2-digit",
                                minute: "2-digit",
                              }
                            )}
                            <div class="flex flex-row">
                              {#each note.keywords as keyword}
                                <span
                                  id="note-detailed-keyword-{note.Dokument_ID}-{keyword}"
                                  class="text-xs font-light px-1"
                                  style="background-color: {stringToColor(
                                    keyword
                                  )}"
                                ></span>
                              {/each}
                            </div>
                            <NotePreview {note} />
                          </div>
                          <div
                            id="note-detailed-text-{note.Dokument_ID}"
                            class="overflow-y-auto w-full whitespace-pre-wrap text-xs flex-grow min-h-0"
                          >
                            {@html note.CaseData.replace(
                              new RegExp(
                                `(<b>(${note.keywords.join("|")})</b>)`,
                                "gi"
                              ),
                              (match, p1, p2) =>
                                `<span style="background-color: ${stringToColor(p2)}; font-weight: bold;">${p2}</span>`
                            )}
                          </div>
                        </div>
                      {/if}
                    </button>
                  {/key}
                {/each}
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
  <div class="flex-grow flex items-center justify-left text-gray-500 text-xs shadow-sm font-medium h-6 bg-gray-200 overflow-hidden pl-1 ml-[8px]">
    Inga äldre anteckningar
  </div>
</div>