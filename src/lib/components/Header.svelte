<script lang="ts">
    import { allNotes, filteredNotes, filter } from "$lib/stores"
    import type { filterSelect } from "$lib/models";
    import { derived, get } from "svelte/store"
    import { getPropertyForFilter } from "$lib/models"
    import { allKeywords } from "$lib/stores";
    import { extractBoldTitlesFromHTML, getSortedUniqueKeywordNames } from '$lib/utils/keywordHelper';

    /**
     * TODO Sprint 2-3
     * 1. Vid fler än X alternativ i en drop-down: lägg till overflow-scroll ist för oändligt lång lista (DONE)
     * 2. Flera filteralternativ ska kunna vara aktiva samtidigt från samma kategori, färgmarkerade (DONE)
     * 3. Varje kategori ska vara återställbar utan att påverka de andra kategorierna (DONE)
     * 4. Filtrering ska ske vid val av filter (just nu genom färgläggning av dok) (DONE)
     * 5. Datum -> FilteredDocuments (Ska faktiskt ta bort) (DONE)
     * 6. Annan filtrering -> Sätt till "Filter" (DONE)
     * 7. Sätt min och max datum från början (sådant att det inkapslar alla dokument för patienten)
     */
    
    let selectedFilters : Map<string, Set<filterSelect>> = new Map;
    selectedFilters.set("Vårdenhet", new Set<filterSelect>);
    selectedFilters.set("Journalmall", new Set<filterSelect>);
    selectedFilters.set("Yrkesroll", new Set<filterSelect>);
    selectedFilters.set("Sökord", new Set<filterSelect>);

    let template: string = "Journalmall";
    let unit: string = "Vårdenhet";
    let role: string = "Yrkesroll";
    let search: string = "Sökord";

    /**
     * Skapa map till keywords.
     * Sortera set i alfabetiskordring med funktionen getSortedUniqueKeywordNames.
     * Lägger endast till keywords som faktiskt finns i notes. Alla sökord träffar minst en anteckning nu. 
     */
    let keywordsMap: Map<string, filterSelect> = new Map();
    let filteredKeywords: Set<string> = new Set();
    
        $: if (keywordsMap.size === 0) {
            const keywordNames = getSortedUniqueKeywordNames(get(allKeywords));
            const keywordTitles = get(allNotes)
                .flatMap(note => extractBoldTitlesFromHTML(note.CaseData));

            const titleSet = new Set(keywordTitles);

            keywordNames
                .filter(name => titleSet.has(name))
                .forEach(name => {
                    keywordsMap.set(name, { name, selected: false });
                });
        }

    const filterNotes = derived(allNotes, $allNotes => {
        /**
         * Derives a map of sets of filter options from all notes for select patient
         */
        let notes : Map<string, Map<string, filterSelect>> = new Map
        notes.set("Vårdenhet", new Map<string, filterSelect>);
        notes.set("Journalmall", new Map<string, filterSelect>);
        notes.set("Yrkesroll", new Map<string, filterSelect>);
        notes.set("Äldsta dokument", new Map<string, filterSelect>);
        notes.set("Nyaste dokument", new Map<string, filterSelect>);
        $allNotes.forEach(note => {
            notes.get("Vårdenhet")!.set(
                note.Vårdenhet_Namn, 
                {name: note.Vårdenhet_Namn, selected : false}
            );
            notes.get("Journalmall")!.set(
                note.Dokumentnamn, 
                {name: note.Dokumentnamn, selected : false}
            );
            notes.get("Yrkesroll")!.set(
                note.Dokument_skapad_av_yrkestitel_Namn, 
                {name: note.Dokument_skapad_av_yrkestitel_Namn, selected : false}
            );

            // Set min and max date for notes
            if(notes.get("Nyaste dokument")!.size == 0 && notes.get("Äldsta dokument")!.size == 0) {
                notes.get("Nyaste dokument")!.set(
                    "Nyast", 
                    {
                        name: note.DateTime,
                        selected : false
                    }
                );
                notes.get("Äldsta dokument")!.set(
                    "Äldst", 
                    {
                        name: note.DateTime,
                        selected : false
                    }
                );
            } else {
                if(notes.get("Nyaste dokument")!.get("Nyast")!.name < note.DateTime) {
                    notes.get("Nyaste dokument")!.set(
                        "Nyast",
                        {
                            name: note.DateTime,
                            selected : false
                        }
                    );
                }
                if(notes.get("Äldsta dokument")!.get("Äldst")!.name > note.DateTime) {
                    notes.get("Äldsta dokument")!.set(
                        "Äldst",
                        {
                            name: note.DateTime,
                            selected : false
                        }
                    );
                }
            }
        });
        return notes;
    });

    const readNotes = get(filterNotes);
    let templates: Map<string, filterSelect> = readNotes.get("Journalmall")!;
    let units: Map<string, filterSelect> = readNotes.get("Vårdenhet")!;
    let roles: Map<string, filterSelect> = readNotes.get("Yrkesroll")!;
    let minDate: string = readNotes.get("Äldsta dokument")!.get("Äldst")!.name.substring(0, 10);
    let maxDate: string = readNotes.get("Nyaste dokument")!.get("Nyast")!.name.substring(0, 10);
    const absMax = maxDate; // Reset value
    const absMin = minDate; // Reset value
    let filteredTemplates : Set<string> = new Set;
    let filteredUnits : Set<string> = new Set;
    let filteredRoles : Set<string> = new Set;

    allNotes.subscribe(notes => {
        filteredNotes.set(notes);
    })();

    function updateFilter() {
        allNotes.subscribe(notes => {
            const filtered = notes.filter(
                (note) => {
                    const titleMatches = Array.from(filteredKeywords).every(keyword => note.CaseData.includes(keyword));
                    return (minDate <= note.DateTime.substring(0, 10) || minDate === "") && 
                    (maxDate >= note.DateTime.substring(0, 10) || maxDate === "") &&
                    (filteredKeywords.size === 0 || titleMatches);
                    /*(templates.get(note.Dokumentnamn)!.selected || filteredTemplates.size == 0) &&
                    (units.get(note.Vårdenhet_Namn)!.selected || filteredUnits.size == 0) &&
                    (roles.get(note.Dokument_skapad_av_yrkestitel_Namn)!.selected || filteredRoles.size == 0) &&*/
                }
            );
            filteredNotes.set(filtered);
        })();
        let activeFilters : Map<string, Set<string>> = new Map;
        activeFilters.set(template, filteredTemplates);
        activeFilters.set(unit, filteredUnits);
        activeFilters.set(role, filteredRoles);
        filter.set(activeFilters);
        
        console.log(filteredNotes);
        return;
    }

    function updateDocument(event: MouseEvent) {
        /***
         * Dynamically update selected filter options for templates, units and roles. 
        */
        const button = event.target as HTMLButtonElement;
        let selectedFilter = button.name; 
        let selectedFilterOption : filterSelect

        console.log(selectedFilter)

        // Check if selected filter is a template filter 
        if(templates.has(selectedFilter)) {
            const newTemplates = new Map(templates); // create temporary placeholder for templates
            selectedFilterOption = templates.get(selectedFilter) as filterSelect; // Get value from key
            newTemplates.set(selectedFilter, {name : selectedFilter, selected : !selectedFilterOption.selected}); // set new value in temporary map
            templates = newTemplates; // replace existing map with new one
            if(!selectedFilterOption.selected) { 
                filteredTemplates.add(selectedFilter); // Add to "keep track" list
            } else {
                filteredTemplates.delete(selectedFilter); // Remove from "keep track" list
            }
            filteredTemplates = new Set(filteredTemplates);
        }
        // Repeat (look at template for brief)
        else if(units.has(selectedFilter)) {
            const newUnits = new Map(units);
            selectedFilterOption = units.get(selectedFilter) as filterSelect;
            newUnits.set(selectedFilter, {name : selectedFilter, selected : !selectedFilterOption.selected});
            units = newUnits;
            if(!selectedFilterOption.selected) {
                filteredUnits.add(selectedFilter);
            } else {
                filteredUnits.delete(selectedFilter);
            }
            filteredUnits = new Set(filteredUnits);
        }
        // Repeat (look at template for brief)
        else if(roles.has(selectedFilter)) {
            const newRoles = new Map(roles);
            selectedFilterOption = roles.get(selectedFilter) as filterSelect;
            newRoles.set(selectedFilter, {name : selectedFilter, selected : !selectedFilterOption.selected});
            roles = newRoles;
            if(!selectedFilterOption.selected) {
                filteredRoles.add(selectedFilter);
            } else {
                filteredRoles.delete(selectedFilter);
            }
            filteredRoles = new Set(filteredRoles);
        } 

        else if (keywordsMap.has(selectedFilter)) {
            const newKeywords = new Map(keywordsMap);
            const prev = newKeywords.get(selectedFilter);
            if (prev) {
                const updated = { ...prev, selected: !prev.selected };
                newKeywords.set(selectedFilter, updated);

                if (updated.selected) {
                    filteredKeywords.add(selectedFilter);
                } else {
                    filteredKeywords.delete(selectedFilter);
                }

                keywordsMap = newKeywords; // 🔁 This triggers reactivity
                filteredKeywords = new Set(filteredKeywords); // 🔁 Re-trigger here too
            }
        } else { // If function called from somewhere not associated with filter
            return;
        }
        
        // Filter all notes by filter criteria 
        updateFilter()
    }

    function reset(event : MouseEvent, arg : string) {
        const newTemplates = new Map(templates);
        const newUnits = new Map(units);
        const newRoles = new Map(roles);
        if(arg == template || arg == "") {
            newTemplates.forEach(element => {
                element.selected = false;
            });
            filteredTemplates.clear()
            filteredTemplates = new Set(filteredTemplates);
        }
        if(arg == unit || arg == "") {
            newUnits.forEach(element => {
                element.selected = false;
            });
            filteredUnits.clear();
            filteredUnits = new Set(filteredUnits);
        }
        if(arg == role || arg == "") {
            newRoles.forEach(element => {
                element.selected = false;
            });
            filteredRoles.clear();
            filteredRoles = new Set(filteredRoles);
        } 
        if(arg == "") {
            minDate = absMin;
            maxDate = absMax;
        }
        if (arg == "Sökord" || arg == "") {
            const newKeywords = new Map(keywordsMap);
            newKeywords.forEach((element) => {
                element.selected = false
            });
            keywordsMap = newKeywords;
            filteredKeywords.clear();
            filteredKeywords = new Set(filteredKeywords);
        }
        
        templates = newTemplates;
        units = newUnits;
        roles = newRoles;
        updateFilter();
    }
</script>

<div id="Header" class="flex flex-row justify-between outline-solid outline-gray-300 p-2 space-x-4">
    <h1 id="ProjectTitle" class="hidden xl:flex text-2xl"><a href="/" onclick={(event) => reset(event, "")}>Demo<span class="text-purple-700"> 2</span></a></h1>
    <div id="Filtermenu" class="grid grid-flow-col grid-rows-2 lg:flex lg:flex-row lg:flex-grow text-md items-center justify-end gap-2">
            <!-- Keywords dropdown -->
            <div id="keywords" class="outline-1 outline-gray-300 rounded-md bg-white justify-center">
                <div id="dropdown_button" class="px-3 flex flex-row justify-between">
                    <button>Sökord</button>
                    {#if filteredKeywords.size != 0}
                        <button onclick={(event) => reset(event, 'Sökord')} class="text-red-600 text-1xl">X</button>
                    {:else}
                        <i class="fa fa-caret-down pt-1"></i>
                    {/if}
                </div>
                <div class="w-full flex justify-center">
                    <ul id="dropdown_keywords">
                        {#each Array.from(keywordsMap) as [key, kw]}
                            <li>
                                <button class="w-[100%] flex row justify-between {kw.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={kw.name} onclick={updateDocument}>
                                    {kw.name}
                                </button>
                                
                            </li>
                        {/each}
                    </ul>
                </div>
            </div>

            <div id="DateDiv" class="outline-1 outline-gray-300 rounded-md bg-white flex flex-row space-x-4 px-3">
                <input type="date" name="OldestDate" id="OldestDate" min={absMin} max={maxDate} oninput={updateFilter} bind:value={minDate}/>
                <p>-</p>
                <input type="date" name="NewestDate" id="NewestDate" min={minDate} max={absMax} oninput={updateFilter} bind:value={maxDate}>
            </div>
            <div id="template" class="outline-1 outline-gray-300 rounded-md bg-white">
                <div id="dropdown_button" class="px-3 flex flex-row justify-between">
                    <button>
                        {template}
                    </button>
                    {#if filteredTemplates.size != 0}
                        <button onclick={(event) => reset(event, template)} class="text-red-600 text-1xl">X</button>
                    {:else}
                    <i class="fa fa-caret-down pt-1"></i>
                    {/if}
                </div>
                
                <div class="w-full flex justify-center">
                <ul id="dropdown_1">
                    {#each Array.from(templates) as [key, journal]}
                        <li>
                            <button class="w-[100%] flex row justify-between {journal.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={journal.name} onclick={updateDocument}>{journal.name}
                                <div class={`w-0 h-0 border-l-6 border-r-6 border-b-12 border-transparent border-b-current ${getPropertyForFilter("Journalmall", journal.name)}`}></div>
                            </button>
                        </li>
                    {/each}
                </ul>
                </div>
            </div>
            <div id="Vårdenhet" class="outline-1 outline-gray-300 rounded-md bg-white justify-center">
                <div id="dropdown_button" class="px-3 flex flex-row justify-between">
                    <button>
                        {unit}
                    </button>
                    {#if filteredUnits.size != 0}
                        <button onclick={(event) => reset(event, unit)} class="text-red-600 text-1xl">X</button>
                    {:else}
                    <i class="fa fa-caret-down pt-1"></i>
                    {/if}
                </div>
                <div class="w-full flex justify-center">
                <ul id="dropdown_2">
                    {#each Array.from(units) as [key, unit]}
                        <li>
                            <button class="w-[100%] flex row justify-between {unit.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={unit.name} onclick={updateDocument}>{unit.name}
                                <div class={`w-3 h-3 rounded-full ${getPropertyForFilter("Vårdenhet", unit.name)}`}></div>
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
            </div>
            <div id="role" class="outline-1 outline-gray-300 rounded-md bg-white justify-center">
                <div id="dropdown_button" class="px-3 flex flex-row justify-between">
                    <button>
                        {role}
                    </button>
                    {#if filteredRoles.size != 0}
                        <button onclick={(event) => reset(event, role)} class="text-red-600 text-1xl">X</button>
                    {:else}
                    <i class="fa fa-caret-down pt-1"></i>
                    {/if}
                </div>
                <div class="w-full flex justify-center">
                <ul id="dropdown_3">
                    {#each Array.from(roles) as [key, role]}
                        <li>
                            <button class="w-[100%] flex row justify-between {role.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={role.name} onclick={updateDocument}>{role.name}
                                <div class={`w-3 h-3 ${getPropertyForFilter("Yrkesroll", role.name)}`}></div>
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
            </div>
    </div>
    <button id="Reset" class="text-sm hover:text-purple-500 self-center" onclick={(event) => reset(event, "")}>Återställ</button>
</div>

<style>
    #template, #role, #Vårdenhet, #keywords {
        list-style: none;
        position: relative;
        display: block;
        text-align: left;
        height: fit-content;
        width: 11em;
    }
    #dropdown_button {
        color: #000;
        text-decoration: none;
        white-space: nowrap;
        overflow: hidden;
    }
    #dropdown_1, #dropdown_2, #dropdown_3, #dropdown_keywords {
        display: none;
        text-align: left;
    }
    #dropdown_1 button, #dropdown_2 button, #dropdown_3 button, #dropdown_keywords button {
        color: black;
        text-decoration: none;
        padding: 5px;
    }

    #template:hover ul, #role:hover ul, #Vårdenhet:hover ul, #keywords:hover ul {
        display: flex;
        position: absolute;
        flex-direction: column;
        font-size: 15px;
        background: white;
        width: 90%;
        min-width: fit-content;
        box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.2);
        z-index: 50;
        overflow-y: auto;
        max-height: 20em;
    }
    #template:hover, #role:hover, #Vårdenhet:hover, #keywords:hover {
        background-color: lightskyblue;
    }
    #DateDiv {
        height: fit-content;
    }
</style>