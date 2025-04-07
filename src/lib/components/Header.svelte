<script lang="ts">
    import type { Document } from "$lib/models/note"
    import { fetchData } from "../utils/fetchBot";
    import { onMount } from "svelte";

    let documents: Document[] = [];
    let matchingDocs: number = 0;

    onMount(async () => {
        documents = await fetchData("documents");
        matchingDocs = documents.length;
    });

    let templates: string[] = ["Läkaranteckning", "Case Report", "Research Article", "Clinical Study", "Review", "Guidelines"];
    let units: string[] = ["Kardiologiska kliniken", "Neurologiska avdelningen", "Onkologiska kliniken", "Kirurgen", "Medicinkliniken"];
    let roles: string[] = ["Läkare", "Specialistläkare", "Sjuksköterska", "Kirurg"];

    let template: string = "Journalmall";
    let unit: string = "Vårdenhet";
    let role: string = "Yrkesroll";

    function updateDocument() {
        /***
         * Uppdaterar dynamiskt antalet dokument som uppnår filterkrav
        */
        const filteredDocs = documents.filter(
            (doc) => 
                (doc.unit == unit || unit == "Vårdenhet") && 
                (doc.professional == role || role == "Yrkesroll") && 
                (doc.type == template || template == "Journalmall")
        );
        matchingDocs = filteredDocs.length;
    }

    function updateJournal(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        template = button.name; 
        updateDocument();
    }
    function updateUnit(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        unit = button.name; 
        updateDocument();
    }
    function updateRole(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        role = button.name; 
        updateDocument();
    }
    function reset(event: MouseEvent) {
        template = "Journalmall";
        unit = "Vårdenhet";
        role = "Yrkesroll";
        const date1 = document.getElementById("OldestDate") as HTMLFormElement;
        const date2 = document.getElementById("NewestDate") as HTMLFormElement;
        date1.value = "";
        date2.value = "";
        updateDocument();
    }
</script>

<div id="Header" class="flex flex-row justify-between outline-solid outline-gray-300 p-2 space-x-4">
    <h1 id="ProjectTitle" class="hidden xl:flex text-2xl"><a href="/" on:click={reset}>Better<span class="text-purple-700">Care</span></a></h1>
    <div id="Filtermenu" class="grid grid-flow-col grid-rows-2 lg:flex lg:flex-row lg:flex-grow text-md items-center justify-end gap-2">
            <div id="Search" class="rounded-md bg-white flex flex-grow">
                <input class="pl-3 w-[100%] bg-white outline-1 outline-gray-300 rounded-md" type="text" placeholder="Sök:">
            </div>
            <div id="DateDiv" class="outline-1 outline-gray-300 rounded-md bg-white flex flex-row space-x-4 px-3">
                <input type="date" name="OldestDate" id="OldestDate">
                <p>-</p>
                <input type="date" name="NewestDate" id="NewestDate">
            </div>
            <div id="template" class="outline-1 outline-gray-300 rounded-md bg-white">
                <div id="dropdown_button" class="px-3 flex flex-row justify-between">
                    <button>
                        {template}
                    </button>
                    <i class="fa fa-caret-down pt-1"></i>
                </div>
                
                <div class="w-full flex justify-center">
                <ul id="dropdown_1">
                    {#each templates as journal}
                        <li>
                            <button class="w-[100%]" name={journal} on:click={updateJournal}>{journal}</button>
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
                    <i class="fa fa-caret-down pt-1"></i>
                </div>
                <div class="w-full flex justify-center">
                <ul id="dropdown_2">
                    {#each units as unit}
                        <li>
                            <button class="w-[100%]" name={unit} on:click={updateUnit}>{unit}</button>
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
                    <i class="fa fa-caret-down pt-1"></i>
                </div>
                <div class="w-full flex justify-center">
                <ul id="dropdown_3">
                    {#each roles as role}
                        <li class="display: inline">
                            <button class="w-[100%]" name={role} on:click={updateRole}>{role}</button>
                        </li>
                    {/each}
                </ul>
            </div>
            </div>
    </div>
    <button id="Reset" class="text-sm hover:text-purple-500 self-center" on:click={reset}>Återställ</button>
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
    #dropdown_1 button:hover, #dropdown_2 button:hover, #dropdown_3 button:hover {background-color: #c495fc;}

    #template:hover ul, #role:hover ul, #Vårdenhet:hover ul {
        display: flex;
        position: absolute;
        flex-direction: column;
        font-size: 15px;
        background: white;
        width: 90%;
        min-width: fit-content;
        box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.2);
    }
    #template:hover, #role:hover, #Vårdenhet:hover {
        background-color: #c495fc;
    }
    #DateDiv {
        height: fit-content;
    }
</style>