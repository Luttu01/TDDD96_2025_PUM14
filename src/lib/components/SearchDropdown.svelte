<script lang="ts">
    import { allNotes, allKeywords } from '$lib/stores';
    import { extractBoldTitlesFromHTML, getSortedUniqueKeywordNames } from '$lib/utils/keywordHelper';
    import { searchQuery } from '$lib/stores/searchStore';
    import { get } from 'svelte/store';
  
    let selectedTitle = "Sökord";

    const sortedNames = getSortedUniqueKeywordNames(get(allKeywords));
  
    $: allTitles = get(allNotes).flatMap(note =>
      extractBoldTitlesFromHTML(note.CaseData)
    );
  
    $: sortedTitles = Array.from(new Set(allTitles)).sort((a, b) =>
      a.localeCompare(b, 'sv')
    );
  
    function updateTitle(event: MouseEvent) {
      const button = event.target as HTMLButtonElement;
      selectedTitle = button.name;
      searchQuery.set(button.name);
    }
  </script>
  
  <div id="SearchDropdown" class="outline-1 outline-gray-300 rounded-md bg-white justify-center">
    <div id="dropdown_button" class="px-3 flex flex-row justify-between">
      <button>{selectedTitle}</button>
      <i class="fa fa-caret-down pt-1"></i>
    </div>
  
    <div class="w-full flex justify-center">
      <ul id="dropdown_search_titles">
        {#each sortedNames as title}
          <li>
            <button class="w-[100%] text-left" name={title} on:click={updateTitle}>
              {title}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  </div>
  
  <style>
    #SearchDropdown {
        list-style: none;
        position: relative;
        display: block;
        text-align: left;
        height: fit-content;
        width: 15em;
    }
  
    #dropdown_search_titles {
        display: none;
        text-align: left;
    }
  
    #SearchDropdown:hover ul {
        display: flex;
        position: absolute;
        flex-direction: column;
        font-size: 15px;
        background: white;
        width: 90%;
        min-width: fit-content;
        box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.2);
        z-index: 50;
        max-height: 400px;
        overflow-y: auto; 
    }
  
    #SearchDropdown:hover {
        background-color: oklch(94.6% 0.033 307.174);
    }
  
    #dropdown_search_titles button {
        color: black;
        text-decoration: none;
        padding: 5px;
    }
  
    #dropdown_search_titles button:hover {
        background-color: oklch(94.6% 0.033 307.174);
    }
  </style>