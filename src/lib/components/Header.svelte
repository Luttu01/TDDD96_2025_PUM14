<script lang="ts">
    import { allNotes, filteredNotes, filter } from "$lib/stores"
    import type { filterSelect } from "$lib/models";
    import { derived, get } from "svelte/store"

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

    let template: string = "Journalmall";
    let unit: string = "Vårdenhet";
    let role: string = "Yrkesroll";

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

    function updateFilter() {
        allNotes.subscribe(notes => {
            const filtered = notes.filter(
                (note) => {
                    return (minDate <= note.DateTime || minDate == "") && 
                    (minDate >= note.DateTime || maxDate == "");
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
        return;
    }

    function updateDocument(event: MouseEvent) {
        /***
         * Dynamically update selected filter options for templates, units and roles. 
        */
        const button = event.target as HTMLButtonElement;
        let selectedFilter = button.name; 
        let selectedFilterOption : filterSelect

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
        minDate = absMin;
        maxDate = absMax;
        
        templates = newTemplates;
        units = newUnits;
        roles = newRoles;
        updateFilter();
    }
</script>

<div id="Header" class="flex flex-row justify-between outline-solid outline-gray-300 p-2 space-x-4">
    <h1 id="ProjectTitle" class="hidden xl:flex text-2xl"><a href="/" onclick={(event) => reset(event, "")}>Better<span class="text-purple-700">Care</span></a></h1>
    <div id="Filtermenu" class="grid grid-flow-col grid-rows-2 lg:flex lg:flex-row lg:flex-grow text-md items-center justify-end gap-2">
            <div id="Search" class="max-w-[44em] rounded-md bg-white flex flex-grow">
                <input class="pl-3 w-[100%] bg-white outline-1 outline-gray-300 rounded-md" type="text" placeholder="Sök:">
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
                            <button class="w-[100%] {journal.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={journal.name} onclick={updateDocument}>{journal.name}</button>
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
                            <button class="w-[100%] {unit.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={unit.name} onclick={updateDocument}>{unit.name}</button>
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
                            <button class="w-[100%] {role.selected == true ? 'bg-blue-200 hover:bg-blue-300' : 'bg-white hover:bg-purple-100'}" name={role.name} onclick={updateDocument}>{role.name}</button>
                        </li>
                    {/each}
                </ul>
            </div>
            </div>
    </div>
    <button id="Reset" class="text-sm hover:text-purple-500 self-center" onclick={(event) => reset(event, "")}>Återställ</button>
</div>

<style>
    #template, #role, #Vårdenhet {
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
    #dropdown_1, #dropdown_2, #dropdown_3 {
        display: none;
        text-align: left;
    }
    #dropdown_1 button, #dropdown_2 button, #dropdown_3 button {
        color: black;
        text-decoration: none;
        padding: 5px;
    }

    #template:hover ul, #role:hover ul, #Vårdenhet:hover ul {
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
    #template:hover, #role:hover, #Vårdenhet:hover {
        background-color: lightskyblue;
    }
    #DateDiv {
        height: fit-content;
    }
</style>