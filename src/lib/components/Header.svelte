<script lang="ts">
    import type { document } from "../models/note"
    import { fetchData } from "../utils/fetchBot";
    import { onMount } from "svelte";

    let documents: document[] = [];
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

<div id="Header" class="flex display-center h-[3em] outline-solid outline-gray-300 bg-gray-100">
    <h1 id="ProjectTitle" class="pl-[5vw] text-4xl"><a href="/" on:click={reset}>Better<span class="text-purple-700">Care</span></a></h1>
    <div id="Filtermenu" class="flex flex-row gap-[1em] items-center text-[1.2em] pl-[5em]">
        <div id="SearchAndDate" class="flex flex-row gap-[1em]">
            <div id="Search" class="w-[15vw] min-w-[10.5em] outline-3 outline-gray-300 rounded-xl bg-white">
                <input class="pl-[5%] w-[100%] bg-white outline-3 outline-gray-300 rounded-xl" type="text" placeholder="Sök:">
            </div>
            <div id="DateDiv" class="w-[21em] outline-3 outline-gray-300 rounded-xl bg-white flex items-center">
                <div id="Date1" class="flex flex-row gap-[1em] items-center">
                    <label for="OldestDate"></label>
                    <input type="date" name="OldestDate" id="OldestDate">
                </div>
                <p class="pl-[1em]">-</p>
                <div id="Date2" class="flex flex-row gap-[1em] items-center">
                    <label for="NewestDate"></label>
                    <input type="date" name="NewestDate" id="NewestDate">
                </div>
            </div>
        </div>
        <div id="Filter" class="flex flex-row gap-[1em]">
            <div id="template" class="w-[10em] outline-3 outline-gray-300 rounded-xl bg-white">
                <div id="dropdown_button">
                    <button class="pl-[5%]">
                        {template}
                    </button>
                    <i class="fa fa-caret-down absolute pt-[2.5%] right-[5%]"></i>
                </div>
            
                <ul id="dropdown_1">
                    {#each templates as journal}
                        <li>
                            <button class="w-[100%] text-ellipsis" name={journal} on:click={updateJournal}>{journal}</button>
                        </li>
                    {/each}
                </ul>
            </div>
            <div id="Vårdenhet" class="w-[10em] outline-3 outline-gray-300 rounded-xl bg-white">
                <div id="dropdown_button">
                    <button class="pl-[5%]">
                        {unit}
                    </button>
                    <i class="fa fa-caret-down absolute pt-[2.5%] right-[5%]"></i>
                </div>
                <ul id="dropdown_2">
                    {#each units as unit}
                        <li>
                            <button class="w-[100%] text-ellipsis" name={unit} on:click={updateUnit}>{unit}</button>
                        </li>
                    {/each}
                </ul>
            </div>
            <div id="role" class="w-[10em] outline-3 outline-gray-300 rounded-xl bg-white">
                <div id="dropdown_button">
                    <button class="pl-[5%]">
                        {role}
                    </button>
                    <i class="fa fa-caret-down absolute pt-[2.5%] right-[5%]"></i>
                </div>
                <ul id="dropdown_3">
                    {#each roles as role}
                        <li class="display: inline">
                            <button class="w-[100%]" name={role} on:click={updateRole}>{role}</button>
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
        <style>
            #template, #role, #Vårdenhet {
                list-style: none;
                position: relative;
                display: block;
                text-align: left;
                padding-right: 3%;
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
            #dropdown_1 button:hover, #dropdown_2 button:hover, #dropdown_3 button:hover {background-color: #9E7BB3;}

            #template:hover ul, #role:hover ul, #Vårdenhet:hover ul {
                display: flex;
                position: absolute;
                flex-direction: column;
                font-size: 15px;
                background: white;
                width: 90%;
                min-width: fit-content;
                margin-left: 5%;
                margin-right: 5%;
                box-shadow: 0px 20px 100px 0px rgba(0, 0, 0, 0.5);
            }
            #template:hover, #role:hover, #Vårdenhet:hover {
                background-color: #9470B0;
            }
        </style>
    </div>
    <button id="Reset" class="absolute text-[1.2em] hover:text-purple-500 right-[2em] top-[0.5em]" on:click={reset}>Återställ</button>
    <style>
        #DateDiv {
            width: fit-content;
            padding-right: 1%;
        }
        /** ADJUSTING PROPERTIES TO FIT SCREENS OF DIFFERENT RESOLUTION */
        @Media (1400px < width < 1775px) {
            #ProjectTitle {
                display: none;
            }
            #Filtermenu {
                padding-left: 2.5%;
            }
        }
        @Media (width < 1400px) {
            #Header {
                height: 6em;
            }
            #Filtermenu {
                padding-top: 1vh;
                flex-direction: column;
            }
            #Reset {
                top: 1.75em;
            }
        }
        /** IPAD MINI */
        @Media (width < 869px) {
            #Header {
                height: fit-content;
                flex-direction: column;
            }
            #ProjectTitle {
                display: flex;
                width: 20%;
                outline: dotted red 1px;
                margin: auto;
                padding: 0;
                padding-top: 0.5em;
            }
            #Filtermenu {
                width: 100%;
                padding: 0;
            }
            #SearchAndDate {
                flex-direction: column;
                width: 100%;
                padding-right: 5%;
                padding-left: 5%;
                padding-top: 1em;
            }
            #Search {
                width: 100%;
            }
            #DateDiv {
                width: 100%;
            }
            #Filter {
                width: 100%;
                padding: 5%;
                padding-top: 0;
            }
            #Reset {
                top: 9em;
                right: 3em;
            }
        }
    </style>
</div>