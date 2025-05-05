<script lang="ts">
  import {
    allNotes,
    filteredNotes,
    filter,
    powerMode,
    showTimeline,
    destructMode,
    selectedNotes,
    allKeywords,
  } from "$lib/stores";
  import { stringToColor } from "$lib/utils";

  import {
    extractBoldTitlesFromHTML,
    getSortedUniqueKeywordNames,
  } from "$lib/utils/keywordUtils";
  import type { filterSelect } from "$lib/models";

  let filteredTemplates = new Set<string>();
  let filteredUnits = new Set<string>();
  let filteredRoles = new Set<string>();
  let filteredKeywords = new Set<string>();

  $: templates = new Map(
    $allNotes.map((n) => [
      n.Dokumentnamn,
      { name: n.Dokumentnamn, selected: filteredTemplates.has(n.Dokumentnamn) },
    ])
  );
  $: units = new Map(
    $allNotes.map((n) => [
      n.Vårdenhet_Namn,
      { name: n.Vårdenhet_Namn, selected: filteredUnits.has(n.Vårdenhet_Namn) },
    ])
  );
  $: roles = new Map(
    $allNotes.map((n) => [
      n.Dokument_skapad_av_yrkestitel_Namn,
      {
        name: n.Dokument_skapad_av_yrkestitel_Namn,
        selected: filteredRoles.has(n.Dokument_skapad_av_yrkestitel_Namn),
      },
    ])
  );

  let minDate = "";
  let maxDate = "";
  let absMin = "";
  let absMax = "";

  let template = "Journalmall";
  let unit = "Vårdenhet";
  let role = "Yrkesroll";

  // Generate keyword map
  $: {
    const keywordNames = getSortedUniqueKeywordNames($allKeywords);
    const keywordTitles = $allNotes.flatMap((n) =>
      extractBoldTitlesFromHTML(n.CaseData)
    );
    const titleSet = new Set(keywordTitles);
    keywordsMap = new Map(
      keywordNames
        .filter((name) => titleSet.has(name))
        .map((name) => [name, { name, selected: filteredKeywords.has(name) }])
    );
  }

  let keywordsMap: Map<string, filterSelect> = new Map();

  // Automatically filter notes based on active filters
  $: {
    const result = $allNotes.filter((note) => {
      const date = note.DateTime.substring(0, 10);
      const titleMatches = Array.from(filteredKeywords).every((keyword) =>
        note.CaseData.includes(keyword)
      );
      return (
        (filteredTemplates.size === 0 ||
          filteredTemplates.has(note.Dokumentnamn)) &&
        (filteredUnits.size === 0 || filteredUnits.has(note.Vårdenhet_Namn)) &&
        (filteredRoles.size === 0 ||
          filteredRoles.has(note.Dokument_skapad_av_yrkestitel_Namn)) &&
        (minDate === "" || date >= minDate) &&
        (maxDate === "" || date <= maxDate) &&
        (filteredKeywords.size === 0 || titleMatches)
      );
    });
    filteredNotes.set(result);
    filter.set(
      new Map([
        [template, filteredTemplates],
        [unit, filteredUnits],
        [role, filteredRoles],
      ])
    );
  }

  $: {
    const updatedNotes = $allNotes.map((note) => {
      const noteKeywords = extractBoldTitlesFromHTML(note.CaseData);
      const matchingKeywords = Array.from(filteredKeywords).filter((keyword) =>
        noteKeywords.includes(keyword)
      );
      return { ...note, keywords: matchingKeywords };
    });
    allNotes.set(updatedNotes);

    const updatedSelectedNotes = $selectedNotes.map((note) => {
      const noteKeywords = extractBoldTitlesFromHTML(note.CaseData);
      const matchingKeywords = Array.from(filteredKeywords).filter((keyword) =>
        noteKeywords.includes(keyword)
      );
      return { ...note, keywords: matchingKeywords };
    });
    selectedNotes.set(updatedSelectedNotes);
  }

  function toggle(set: Set<string>, value: string) {
    const newSet = new Set(set);
    newSet.has(value) ? newSet.delete(value) : newSet.add(value);
    return newSet;
  }

  function handleClick(event: Event) {
    const name = (event.target as HTMLButtonElement).name;

    if (templates.has(name)) {
      filteredTemplates = toggle(filteredTemplates, name);
    } else if (units.has(name)) {
      filteredUnits = toggle(filteredUnits, name);
    } else if (roles.has(name)) {
      filteredRoles = toggle(filteredRoles, name);
    }
  }

  function handleKeywordClick(event: Event) {
    const name = (event.target as HTMLButtonElement).name;
    if (keywordsMap.has(name)) {
      filteredKeywords = toggle(filteredKeywords, name);
    }
  }

  function reset(filterName: string = "") {
    if (filterName === template || filterName === "") {
      filteredTemplates = new Set();
    }
    if (filterName === unit || filterName === "") {
      filteredUnits = new Set();
    }
    if (filterName === role || filterName === "") {
      filteredRoles = new Set();
    }
    if (filterName === "Sökord" || filterName === "") {
      filteredKeywords = new Set();
    }
    if (filterName === "") {
      minDate = absMin;
      maxDate = absMax;
    }
  }

  function closeDocs() {
    selectedNotes.set([]);
  }
</script>

<div id="Header" class="flex flex-row justify-between p-1 space-x-4">
  <div
    id="settingsJournal"
    class="flex flex-row flex-grow text-sm items-center justify-beginning space-x-1 border-r border-gray-300"
  >
    <span class="text-xs font-bold">Journalvy:</span>

    <div id="ToggleCanvas" class="p-1 flex">
      <label for="toggleCanvas" class="text-xs items-center flex gap-1">
        Canvas
        <div class="relative inline-block w-8 h-4 items-center">
          <input
            id="toggleCanvas"
            type="checkbox"
            bind:checked={$powerMode}
            class="sr-only peer"
          />
          <div
            class="w-full h-full bg-gray-300 rounded-full peer-checked:bg-purple-500 transition-colors"
          ></div>
          <div
            class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow-md transition-all peer-checked:translate-x-4"
          ></div>
        </div>
      </label>
    </div>

    <div id="CloseDocs" class="p-1 flex items-center">
      <button
        id="Close"
        class="hover:text-purple-500 self-center text-xs"
        onclick={closeDocs}>Återställ Journalvy</button
      >
    </div>
  </div>
  <div
    id="settingsTimeline"
    class="flex flex-row flex-grow text-sm items-center justify-beginning space-x-1 border-r border-gray-300"
  >
    <span class="text-xs font-bold">Tidslinje:</span>

    <div id="ToggleTimeline" class="p-1 flex">
      <label for="toggleTimeline" class="text-xs items-center flex gap-1">
        Tidslinje
        <div class="relative inline-block w-8 h-4 items-center">
          <input
            id="toggleTimeline"
            type="checkbox"
            bind:checked={$showTimeline}
            class="sr-only peer"
          />
          <div
            class="w-full h-full bg-gray-300 rounded-full peer-checked:bg-purple-500 transition-colors"
          ></div>
          <div
            class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow-md transition-all peer-checked:translate-x-4"
          ></div>
        </div>
      </label>
    </div>

    <div id="ToggleDestruct" class="p-1 flex">
      <label for="toggleDestruct" class="text-xs items-center flex gap-1">
        Gömma
        <div class="relative inline-block w-8 h-4 items-center">
          <input
            id="toggleDestruct"
            type="checkbox"
            bind:checked={$destructMode}
            class="sr-only peer"
          />
          <div
            class="w-full h-full bg-gray-300 rounded-full peer-checked:bg-purple-500 transition-colors"
          ></div>
          <div
            class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow-md transition-all peer-checked:translate-x-4"
          ></div>
        </div>
      </label>
    </div>
  </div>
  <div
    id="Filtermenu"
    class="grid grid-flow-col grid-rows-2 xl:flex xl:flex-row xl:flex-grow text-sm items-center justify-end gap-1"
  >
    <div
      id="DateDiv"
      class="outline-1 outline-gray-300 rounded-md bg-white flex flex-row space-x-2 px-2 text-sm"
    >
      <input
        type="date"
        name="OldestDate"
        id="OldestDate"
        min={absMin}
        max={maxDate}
        oninput={handleClick}
        bind:value={minDate}
      />
      <p>-</p>
      <input
        type="date"
        name="NewestDate"
        id="NewestDate"
        min={minDate}
        max={absMax}
        oninput={handleClick}
        bind:value={maxDate}
      />
    </div>
    <!-- Keywords dropdown -->
    <div
      id="keywords"
      class="outline-1 outline-gray-300 rounded-md bg-white justify-center"
    >
      <div
        id="dropdown_button"
        class="px-2 flex flex-row justify-between text-sm"
      >
        <button>Sökord</button>
        {#if filteredKeywords.size != 0}
          <button
            onclick={(event) => reset("Sökord")}
            class="text-red-500 text-sm font-bold">X</button
          >
        {:else}
          <i class="fa fa-caret-down pt-1"></i>
        {/if}
      </div>
      <div class="w-full flex justify-center">
        <ul id="dropdown_keywords">
          {#each Array.from(keywordsMap) as [key, kw]}
            <li>
              <button
                class="w-[100%] flex row justify-between text-left text-sm {kw.selected
                  ? 'bg-[color:var(--tw-color)]'
                  : 'bg-white hover:bg-gray-100'}"
                style="--tw-color: {stringToColor(kw.name)};"
                name={kw.name}
                onclick={handleKeywordClick}
              >
                {kw.name}
              </button>
            </li>
          {/each}
        </ul>
      </div>
    </div>
    <div id="template" class="outline-1 outline-gray-300 rounded-md bg-white">
      <div
        id="dropdown_button"
        class="px-2 flex flex-row justify-between text-sm"
      >
        <button>
          {template}
        </button>
        {#if filteredTemplates.size != 0}
          <button
            onclick={(event) => reset(template)}
            class="text-red-500 text-sm font-bold">X</button
          >
        {:else}
          <i class="fa fa-caret-down pt-1"></i>
        {/if}
      </div>

      <div class="w-full flex justify-center">
        <ul id="dropdown_1">
          {#each Array.from(templates) as [key, journal]}
            <li>
              <button
                class="w-[100%] flex row justify-between text-left text-sm {journal.selected ==
                true
                  ? 'bg-purple-200 hover:bg-purple-300'
                  : 'bg-white hover:bg-purple-100'}"
                name={journal.name}
                onclick={handleClick}
                >{journal.name}
                <svg
                  class="w-5 h-5 p-[2px] flex-none bg-[color:var(--tw-color)] text-white rounded-full"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  style="--tw-color: {stringToColor(journal.name)};"
                >
                  <path
                    fill-rule="evenodd"
                    d="M9 2.221V7H4.221a2 2 0 0 1 .365-.5L8.5 2.586A2 2 0 0 1 9 2.22ZM11 2v5a2 2 0 0 1-2 2H4v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-7ZM8 16a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2H9a1 1 0 0 1-1-1Zm1-5a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2H9Z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </li>
          {/each}
        </ul>
      </div>
    </div>
    <div
      id="Vårdenhet"
      class="outline-1 outline-gray-300 rounded-md bg-white justify-center"
    >
      <div
        id="dropdown_button"
        class="px-2 flex flex-row justify-between text-sm"
      >
        <button>
          {unit}
        </button>
        {#if filteredUnits.size != 0}
          <button
            onclick={() => reset(unit)}
            class="text-red-500 text-sm font-bold">X</button
          >
        {:else}
          <i class="fa fa-caret-down pt-1"></i>
        {/if}
      </div>
      <div class="w-full flex justify-center">
        <ul id="dropdown_2">
          {#each Array.from(units) as [key, unit]}
            <li>
              <button
                class="w-[100%] flex row justify-between text-left text-sm {unit.selected ==
                true
                  ? 'bg-purple-200 hover:bg-purple-300'
                  : 'bg-white hover:bg-purple-100'}"
                name={unit.name}
                onclick={handleClick}
                >{unit.name}
                <svg
                  class="w-5 h-5 p-[2px] flex-none bg-[color:var(--tw-color)] text-white rounded-full"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  style="--tw-color: {stringToColor(unit.name)};"
                >
                  <path
                    fill-rule="evenodd"
                    d="M11.293 3.293a1 1 0 0 1 1.414 0l6 6 2 2a1 1 0 0 1-1.414 1.414L19 12.414V19a2 2 0 0 1-2 2h-3a1 1 0 0 1-1-1v-3h-2v3a1 1 0 0 1-1 1H7a2 2 0 0 1-2-2v-6.586l-.293.293a1 1 0 0 1-1.414-1.414l2-2 6-6Z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </li>
          {/each}
        </ul>
      </div>
    </div>
    <div
      id="role"
      class="outline-1 outline-gray-300 rounded-md bg-white justify-center"
    >
      <div
        id="dropdown_button"
        class="px-2 flex flex-row justify-between text-sm"
      >
        <button>
          {role}
        </button>
        {#if filteredRoles.size != 0}
          <button
            onclick={() => reset(role)}
            class="text-red-500 text-sm font-bold">X</button
          >
        {:else}
          <i class="fa fa-caret-down pt-1"></i>
        {/if}
      </div>
      <div class="w-full flex justify-center">
        <ul id="dropdown_3">
          {#each Array.from(roles) as [_, role]}
            <li>
              <button
                class="w-[100%] flex row justify-between text-left text-sm {role.selected ==
                true
                  ? 'bg-purple-200 hover:bg-purple-300'
                  : 'bg-white hover:bg-purple-100'}"
                name={role.name}
                onclick={handleClick}
                >{role.name}
                <svg
                  class="w-5 h-5 p-[1px] flex-none bg-[color:var(--tw-color)] text-white rounded-full"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  style="--tw-color: {stringToColor(role.name)};"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </li>
          {/each}
        </ul>
      </div>
    </div>
    <div id="ResetFilters" class="p-1 flex items-center">
      <button
        id="Reset"
        class="hover:text-purple-500 self-center text-xs"
        onclick={() => reset("")}>Återställ Filter</button
      >
    </div>
  </div>
</div>

<style>
  #template,
  #role,
  #Vårdenhet,
  #keywords {
    list-style: none;
    position: relative;
    display: block;
    text-align: left;
    height: fit-content;
    width: 8em;
  }
  #dropdown_button {
    color: #000;
    text-decoration: none;
    white-space: nowrap;
    overflow: hidden;
  }
  #dropdown_1,
  #dropdown_2,
  #dropdown_3,
  #dropdown_keywords {
    display: none;
    text-align: left;
  }
  #dropdown_1 button,
  #dropdown_2 button,
  #dropdown_3 button,
  #dropdown_keywords button {
    color: black;
    text-decoration: none;
    padding: 5px;
  }

  #template:hover ul,
  #role:hover ul,
  #Vårdenhet:hover ul,
  #keywords:hover ul {
    display: flex;
    position: absolute;
    flex-direction: column;
    font-size: 15px;
    background: white;
    width: 100%;
    min-width: fit-content;
    box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.2);
    z-index: 50;
    overflow-y: auto;
    max-height: 20em;
  }
  #template:hover,
  #role:hover,
  #Vårdenhet:hover,
  #keywords:hover {
    background-color: rgb(233, 233, 233);
  }
  #DateDiv {
    height: fit-content;
  }
</style>
