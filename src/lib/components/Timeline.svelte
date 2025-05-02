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
    noteHierarchy.set(buildDateHierarchy($allNotes));
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

  const outOfViewKeywords = writable(
    new Map<string, { direction: string; count: number }>()
  );

  function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function updateOutOfViewNotes() {
    if (!scrollContainer) return;
    sleep(400);
    const containerRect = scrollContainer.getBoundingClientRect();
    outOfViewKeywords.set(new Map());

    for (const [noteId, el] of Object.entries(noteElements)) {
      const rect = el.getBoundingClientRect();
      if (rect.right > containerRect.right || rect.left < containerRect.left) {
        const note = $allNotes.find((n) => n.Dokument_ID === noteId);
        if (note) {
          for (const keyword of note.keywords) {
            const existingEntry = $outOfViewKeywords.get(keyword);
            const direction =
              rect.right > containerRect.right ? "right" : "left";
            const count = existingEntry?.count || 0;
            const updatedMap = new Map($outOfViewKeywords);
            updatedMap.set(keyword, { direction, count: count + 1 });
            outOfViewKeywords.set(updatedMap);
          }
        }
      }
    }
  }

  onMount(() => {
    updateOutOfViewNotes();
    if (scrollContainer) {
      scrollContainer.addEventListener("scroll", updateOutOfViewNotes);
      scrollContainer.addEventListener("resize", updateOutOfViewNotes);
    }
  });

  onDestroy(() => {
    if (scrollContainer) {
      scrollContainer.removeEventListener("scroll", updateOutOfViewNotes);
      scrollContainer.removeEventListener("resize", updateOutOfViewNotes);
    }
  });
</script>

{#if $outOfViewKeywords.size > 0}
  <div
    class="absolute right-0 top-18 flex flex-col space-y-1 bg-white p-2 rounded-l-md shadow-md"
    style="z-index: 100;"
  >
    {#each Array.from($outOfViewKeywords.entries()).filter(([_, { direction }]) => direction === "right") as [key, { count }]}
      <div
        class="w-5 h-5 rounded-md text-xs flex items-center justify-center relative"
        style="background-color: {stringToColor(key)}"
      >
        {count}
        <div
          class="absolute right-[-12px] top-1/2 -translate-y-1/2 w-0 h-0 border-l-[6px] border-r-transparent border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-r-[6px]"
          style="border-left-color: {stringToColor(key)}"
        ></div>
      </div>
    {/each}
  </div>
  <div
    class="absolute left-0 top-18 flex flex-col space-y-1 bg-white p-2 rounded-r-md shadow-md"
    style="z-index: 100;"
  >
    {#each Array.from($outOfViewKeywords.entries()).filter(([_, { direction }]) => direction === "left") as [key, { count }]}
      <div
        class="w-5 h-5 rounded-md text-xs flex items-center justify-center relative"
        style="background-color: {stringToColor(key)}"
      >
        {count}
        <div
          class="absolute left-[-12px] top-1/2 -translate-y-1/2 w-0 h-0 border-r-[6px] border-l-transparent border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-l-[6px]"
          style="border-right-color: {stringToColor(key)}"
        ></div>
      </div>
    {/each}
  </div>
{/if}

<div
  class="flex h-full bg-gray-100 overflow-x-auto overflow-y-hidden"
  bind:this={scrollContainer}
>
  <div class="flex flex-row w-max h-full space-x-[2px]">
    {#each $noteHierarchy as yearGroup (yearGroup.year)}
      <div class="h-full flex flex-col">
        <button
          class="flex bg-purple-200 py-1 text-left text-sm px-2 w-full shadow-xs justify-between {yearGroup.isCollapsed
            ? 'cursor-zoom-in'
            : 'cursor-zoom-out'}"
            onclick={() => ($destructMode ? toggleAllYearGroups() : toggleGroup(yearGroup))}
          aria-label="Toggle year {yearGroup.year}"
        >
          <div class="text-sm sticky left-1 w-8 font-bold text-gray-900">
            {yearGroup.year}
          </div>
        </button>
        <div class="flex flex-row space-x-[2px]">
          {#each yearGroup.months as monthGroup}
            <div class="flex flex-col">
              <button
                class="{yearGroup.isCollapsed
                  ? 'h-0 py-0'
                  : 'h-6 py-1'} flex bg-purple-300 px-1 justify-between w-full shadow-xs transition-all duration-300 {monthGroup.isCollapsed
                  ? 'cursor-zoom-in'
                  : 'cursor-zoom-out'}"
                onclick={() => ($destructMode ? toggleAllMonthGroups() : toggleGroup(monthGroup))}
                aria-label="Toggle month {monthGroup.month}"
              >
                <div
                  class="{yearGroup.isCollapsed
                    ? 'text-transparent'
                    : 'text-gray-900'} text-xs sticky left-1 px-1 w-6 font-semibold text-left"
                >
                  {new Date(0, monthGroup.month).toLocaleString("sv-SE", {
                    month: "short",
                  })}
                </div>
              </button>
              <div
                class="flex flex-row overflow-hidden p-[2px] space-x-[4px] items-start"
              >
                {#each monthGroup.notes as note}
                  {#key note.Dokument_ID}
                    <button
                      class={`transition-all mt-2 duration-300 border rounded-md shadow-xs ${isInSelectedNotes(note) ? "bg-purple-50 border-purple-300 hover:bg-purple-100" : "bg-white border-gray-200 hover:bg-gray-50"} relative cursor-pointer ${
                        getNoteSizeState(yearGroup, monthGroup, note) ===
                        "compact"
                          ? "flex flex-col py-2 px-1 w-12 space-y-1"
                          : getNoteSizeState(yearGroup, monthGroup, note) ===
                              "medium"
                            ? "flex flex-col p-2 w-45 text-sm text-left"
                            : getNoteSizeState(yearGroup, monthGroup, note) ===
                                "hidden"
                              ? "w-6 flex flex-col"
                              : "flex justify-between p-2 w-100"
                      }`}
                      onclick={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                      bind:this={noteElements[note.Dokument_ID]}
                    >
                      <div
                        class="transition-all duration-300 absolute -top-2.5 left-1/2 -translate-x-1/2 w-0 h-0 border-b-10
               {getNoteSizeState(yearGroup, monthGroup, note) === "hidden" ? 'border-l-4 border-r-4' : 'border-l-10 border-r-10'} border-transparent {isInSelectedNotes(
                          note
                        )
                          ? 'border-b-purple-300'
                          : 'border-b-white'}"
                      ></div>
                      {#if getNoteSizeState(yearGroup, monthGroup, note) === "hidden"}
                        <div class="h-12 bg-white rounded-md"></div>
                      {:else if getNoteSizeState(yearGroup, monthGroup, note) === "compact"}
                        <span class="text-[10px] text-gray-500">
                          {new Date(note.DateTime).toLocaleDateString("sv-SE", {
                            month: "2-digit",
                            day: "2-digit",
                          })}
                        </span>
                        <NotePreview {note} direction="flex-col" />
                        <span class="flex flex-col">
                          {#each note.keywords as keyword}
                            <div
                              class="h-2"
                              style="background-color: {stringToColor(keyword)}"
                            ></div>
                          {/each}
                        </span>
                      {:else if getNoteSizeState(yearGroup, monthGroup, note) === "medium"}
                        <div
                          class="text-gray-500 text-xs flex justify-between border-b-1 border-gray-200 pb-1"
                        >
                          {new Date(note.DateTime).toLocaleDateString("sv-SE")}
                          <NotePreview {note} />
                        </div>
                        <div class="">
                          <div
                            class="text-gray-900 text-xs font-bold flex justify-between h-10"
                          >
                            {note.Dokumentnamn}
                          </div>
                        </div>
                        <span
                          class="text-sm font-medium border-gray-200 flex flex-col"
                        >
                          {#each note.keywords as keyword, index}
                            {#if index < 4 || note.keywords.length <= 5}
                              <span
                                class="text-xs font-light px-1"
                                style="background-color: {stringToColor(
                                  keyword
                                )}"
                              >
                                {@html getKeywordContext(
                                  note.CaseData,
                                  keyword
                                )}
                              </span>
                            {:else if index === 4}
                              <span
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
                          class="text-gray-900 text-left text-xs w-full flex flex-col"
                        >
                          <div
                            class="text-gray-500 text-xs flex justify-between border-b-1 border-gray-200 pb-1"
                          >
                            {new Date(note.DateTime).toLocaleDateString(
                              "sv-SE"
                            )}
                            <div class="flex flex-row">
                            {#each note.keywords as keyword}
                              <span
                                class="text-xs font-light px-1"
                                style="background-color: {stringToColor(
                                  keyword
                                )}"
                              >
                              </span>
                            {/each}
                          </div>
                            <NotePreview {note} />
                          </div>
                          <!-- Temporary fix with max-h -->
                          <div class="overflow-y-auto w-full max-h-[280px]">
                            <div class="whitespace-pre-wrap text-xs">
                              {console.log(note.CaseData)}
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
</div>