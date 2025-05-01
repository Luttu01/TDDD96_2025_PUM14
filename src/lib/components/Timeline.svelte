<script lang="ts">
  import { writable } from "svelte/store";
  import { onMount, afterUpdate } from "svelte";
  import NotePreview from "./NotePreview.svelte";

  import type { Note, Year, Month } from "$lib/models";
  import { buildDateHierarchy } from "$lib/utils";
  import { allNotes, selectedNotes } from "$lib/stores";
  import { stringToColor } from "$lib/utils";

  const noteHierarchy = writable<Year[]>([]);

  $: {
    noteHierarchy.set(buildDateHierarchy($allNotes));
  }

  function toggleGroup(group: Year | Month) {
    group.isCollapsed = !group.isCollapsed;
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

  function getNoteSizeState(yearGroup: Year, monthGroup: Month) {
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
  let outOfViewNoteIds = new Set<string>();

  function updateOutOfViewNotes() {
    if (!scrollContainer) return;

    const containerRect = scrollContainer.getBoundingClientRect();
    const newOut = new Set<string>();

    for (const [id, el] of Object.entries(noteElements)) {
      const rect = el.getBoundingClientRect();
      if (rect.right > containerRect.right || rect.left < containerRect.left) {
        newOut.add(id);
      }
    }

    outOfViewNoteIds = newOut;
  }

  function scrollToNote(noteId: string) {
    const el = noteElements[noteId];
    if (el) {
      el.scrollIntoView({ behavior: "smooth", inline: "center" });
    }
  }

  onMount(() => {
    updateOutOfViewNotes();
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', updateOutOfViewNotes);
    }
    window.addEventListener('resize', updateOutOfViewNotes);
  });
</script>

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
          on:click={() => toggleGroup(yearGroup)}
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
                on:click={() => toggleGroup(monthGroup)}
                aria-label="Toggle month {monthGroup.month}"
              >
                <div
                  class="{yearGroup.isCollapsed
                    ? 'text-transparent'
                    : 'text-gray-900'} text-xs sticky left-1 px-1 w-8 font-semibold text-left"
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

                  {#if outOfViewNoteIds.has(note.Dokument_ID)}
                    <div
                      class="w-5 h-5 rounded-full"
                      style="position: absolute; top: 60%; left: 0; background-color: {stringToColor(note.keywords[0])}"
                    ></div>
                  {/if}


                    <button
                      class={`transition-all mt-2 duration-300 border rounded-md shadow-xs ${isInSelectedNotes(note) ? "bg-purple-50 border-purple-300 hover:bg-purple-100" : "bg-white border-gray-200 hover:bg-gray-50"} relative cursor-pointer ${
                        getNoteSizeState(yearGroup, monthGroup) === "compact"
                          ? "flex flex-col py-2 px-1 w-12 space-y-1"
                          : getNoteSizeState(yearGroup, monthGroup) === "medium"
                            ? "flex flex-col p-2 w-45 text-sm text-left"
                            : "flex justify-between p-2 w-100"
                      }`}
                      on:click={() => handleNoteClick(note)}
                      aria-label="Select note {note.Dokument_ID}"
                      bind:this={noteElements[note.Dokument_ID]}
                    >
                      <div
                        class="transition-all duration-300 absolute -top-2.5 left-1/2 -translate-x-1/2 w-0 h-0
              border-l-10 border-r-10 border-b-10 border-transparent {isInSelectedNotes(
                          note
                        )
                          ? 'border-b-purple-300'
                          : 'border-b-white'}"
                      ></div>
                      {#if getNoteSizeState(yearGroup, monthGroup) === "compact"}
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
                      {:else if getNoteSizeState(yearGroup, monthGroup) === "medium"}
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
                            <NotePreview {note} />
                          </div>
                          <!-- Temporary fix with max-h -->
                          <div class="overflow-y-auto w-full max-h-[280px]">
                            <div class="whitespace-pre-wrap text-xs">
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
