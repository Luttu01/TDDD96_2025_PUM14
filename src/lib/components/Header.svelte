<script lang="ts">
    let journalmall: string = "Journalmall";
    let vardenhet: string = "Vårdenhet";
    let yrkesroll: string = "Yrkesroll";

    function handleButtonClick1(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        journalmall = button.name; 
    }
    function handleButtonClick2(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        vardenhet = button.name; 
    }
    function handleButtonClick3(event: MouseEvent) {
        const button = event.target as HTMLButtonElement;
        yrkesroll = button.name; 
    }
    function reset(event: MouseEvent) {
        journalmall = "Journalmall";
        vardenhet = "Vårdenhet";
        yrkesroll = "Yrkesroll";
    }
</script>

<div class="flex display-center h-[3em] outline-solid outline-gray-300 bg-gray-100">
    <h1 id="ProjektTitel" class="pl-[5vw] pr-[5vw] text-4xl"><a href="/" on:click={reset}>Better<span class="text-purple-700">Care</span></a></h1>
    <div id="Filtermenu" class="flex flex-row gap-[1vw] items-center text-2xl">


        <div id="Sök" class="w-[10vw] overflow-hidden outline-3 outline-gray-300 rounded-xl bg-white">
            <input class="pl-[5%] w-[100%] bg-white outline-3 outline-gray-300 rounded-xl" type="text" placeholder="Sök:">
        </div>

        <div id="Journalmall" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <button id="dropdown_button" class="pl-[5%]">
                {journalmall} <i class="fa fa-caret-down"></i>
            </button>
            <div id="dropdown_1">
                <button name="Test11" on:click={handleButtonClick1}>Test1</button>
                <button name="Test12" on:click={handleButtonClick1}>Test2</button>
                <button name="Test13" on:click={handleButtonClick1}>Test3</button>
            </div>
        </div>
        <div id="Vårdenhet" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <button id="dropdown_button" class="pl-[5%]">
                {vardenhet} <i class="fa fa-caret-down"></i>
            </button>
            <div id="dropdown_2">
                <button name="Test21" on:click={handleButtonClick2}>Test1</button>
                <button name="Test22" on:click={handleButtonClick2}>Test2</button>
                <button name="Test23" on:click={handleButtonClick2}>Test3</button>
            </div>
        </div>
        <div id="Yrkesroll" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <button id="dropdown_button" class="pl-[5%]">
                {yrkesroll} <i class="fa fa-caret-down"></i>
            </button>
            <div id="dropdown_3">
                <button name="Test31" on:click={handleButtonClick3}>Test1</button>
                <button name="Test32" on:click={handleButtonClick3}>Test2</button>
                <button name="Test33" on:click={handleButtonClick3}>Test3</button>
            </div>
        </div>
        <style>
            #Journalmall, #Yrkesroll, #Vårdenhet {
                list-style: none;
                position: relative;
                transition: 0.5s;
                display: block;
                text-align: center;
            }
            #dropdown_button {
                color: #000;
                text-decoration: none;
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
            #dropdown_1 button:hover, #dropdown_2 button:hover, #dropdown_3 button:hover {background-color: #ddd;}

            #Journalmall:hover div, #Yrkesroll:hover div, #Vårdenhet:hover div {
                display: flex;
                position: absolute;
                flex-direction: column;
                background: white;
                width: 90%;
                margin-left: 5%;
                margin-right: 5%;
                box-shadow: 0px 20px 100px 0px rgba(0, 0, 0, 0.5);
            }
            #Journalmall:hover, #Yrkesroll:hover, #Vårdenhet:hover {
                size-adjust: fit-content;
                background-color: lightgray;
            }
        </style>

        <div id="Datum" class="flex flex-row gap-[6vw] w-[20vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <div class="pl-[5%]">Från:</div>
            <div>Till:</div>
        </div>
        <button id="Reset" class="hover:text-purple-500" on:click={reset}>Återställ</button>
    </div>
</div>