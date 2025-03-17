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

    let journalmallar: string[] = ["Läkaranteckning", "Case Report", "Research Article", "Clinical Study", "Review", "Guidelines"];
    let vardenheter: string[] = ["Kardiologiska kliniken", "Neurologiska avdelningen", "Onkologiska kliniken", "Kirurgen", "Medicinkliniken"];
    let yrkesroller: string[] = ["Läkare", "Specialistläkare", "Sjuksköterska", "Kirurg"];

    let journalmall: string = "Journalmall";
    let vardenhet: string = "Vårdenhet";
    let yrkesroll: string = "Yrkesroll";

    function update() {
        /***
         * Uppdaterar dynamiskt antalet dokument som uppnår filterkrav
        */
        const filteredDocs = documents.filter(
            (doc) => 
                (doc.unit == vardenhet || vardenhet == "Vårdenhet") && 
                (doc.professional == yrkesroll || yrkesroll == "Yrkesroll") && 
                (doc.type == journalmall || journalmall == "Journalmall")
        );
        matchingDocs = filteredDocs.length;
    }

    function handleButtonClick1(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        journalmall = button.name; 
        update();
    }
    function handleButtonClick2(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        vardenhet = button.name; 
        update();
    }
    function handleButtonClick3(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        yrkesroll = button.name; 
        update();
    }
    function reset(event: MouseEvent) {
        journalmall = "Journalmall";
        vardenhet = "Vårdenhet";
        yrkesroll = "Yrkesroll";
        const date1 = document.getElementById("DatumÄldst") as HTMLFormElement;
        const date2 = document.getElementById("DatumSenast") as HTMLFormElement;
        date1.value = "";
        date2.value = "";
        update();
    }
</script>

<div class="flex display-center h-[3em] outline-solid outline-gray-300 bg-gray-100">
    <h1 id="ProjektTitel" class="pl-[5vw] pr-[5vw] text-4xl"><a href="/" on:click={reset}>Better<span class="text-purple-700">Care</span></a></h1>
    <div id="Filtermenu" class="flex flex-row gap-[1vw] items-center text-[1.2em]">
        <div id="Sök" class="w-[15vw] overflow-hidden outline-3 outline-gray-300 rounded-xl bg-white">
            <input class="pl-[5%] w-[100%] bg-white outline-3 outline-gray-300 rounded-xl" type="text" placeholder="Sök:">
        </div>

        <div id="Journalmall" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <div id="dropdown_button">
                <button class="pl-[5%] w-[80%] overflow-hidden">
                    {journalmall}
                </button>
                <i class="fa fa-caret-down"></i>
            </div>
        
            <ul id="dropdown_1">
                {#each journalmallar as journal}
                    <li>
                        <button class="w-[100%] text-ellipsis" name={journal} on:click={handleButtonClick1}>{journal}</button>
                    </li>
                {/each}
            </ul>
        </div>
        <div id="Vårdenhet" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <div id="dropdown_button">
                <button class="pl-[5%] w-[80%] overflow-hidden">
                    {vardenhet}
                </button>
                <i class="fa fa-caret-down"></i>
            </div>
            <ul id="dropdown_2">
                {#each vardenheter as enhet}
                    <li>
                        <button class="w-[100%] text-ellipsis" name={enhet} on:click={handleButtonClick2}>{enhet}</button>
                    </li>
                {/each}
            </ul>
        </div>
        <div id="Yrkesroll" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <div id="dropdown_button">
                <button class="pl-[5%] w-[80%] overflow-hidden">
                    {yrkesroll}
                </button>
                <i class="fa fa-caret-down"></i>
            </div>
            <ul id="dropdown_3">
                {#each yrkesroller as yrke}
                    <li class="display: inline">
                        <button class="w-[100%]" name={yrke} on:click={handleButtonClick3}>{yrke}</button>
                    </li>
                {/each}
            </ul>
        </div>
        <style>
            #Journalmall, #Yrkesroll, #Vårdenhet {
                list-style: none;
                position: relative;
                transition: 0.5s;
                display: block;
                text-align: left;
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

            #Journalmall:hover ul, #Yrkesroll:hover ul, #Vårdenhet:hover ul {
                display: flex;
                position: absolute;
                flex-direction: column;
                font-size: 15px;
                background: white;
                width: 90%;
                margin-left: 5%;
                margin-right: 5%;
                box-shadow: 0px 20px 100px 0px rgba(0, 0, 0, 0.5);
            }
            #Journalmall:hover, #Yrkesroll:hover, #Vårdenhet:hover {
                background-color: #9470B0;
            }
        </style>
        <div id="DatumDiv" class="w-[21vw] h-[60%] outline-3 outline-gray-300 rounded-xl bg-white text-[80%] flex items-center">
            <div id="Datum1" class="flex flex-row gap-[1vw] items-center">
                <label for="DatumÄldst"></label>
                <input type="date" name="DatumÄldst" id="DatumÄldst">
            </div>
            <p class="pl-[1vw]">-</p>
            <div id="Datum2" class="flex flex-row gap-[1vw] items-center">
                <label for="DatumSenast"></label>
                <input type="date" name="DatumSenast" id="DatumSenast">
            </div>
        </div>
        <button id="Reset" class="hover:text-purple-500" on:click={reset}>Återställ</button>
    </div>
</div>