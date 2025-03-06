


<div class="flex display-center h-[3em] outline-solid outline-gray-300 bg-gray-100">
    <h1 id="ProjektTitel" class="pl-[5vw] pr-[5vw] text-4xl">Better<span class="text-purple-700">Care</span></h1>
    <div id="Filtermenu" class="flex flex-row gap-[1vw] items-center text-2xl">


        <div id="Sök" class="w-[10vw] overflow-hidden outline-3 outline-gray-300 rounded-xl bg-white">
            <input class="pl-[5%] w-[100%] bg-white outline-3 outline-gray-300 rounded-xl" type="text" placeholder="Sök:">
        </div>

        <div id="Journalmall" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <button id="dropdown_button" class="pl-[5%]">Journalmall</button>
            <div id="dropdown_1">
                <a href="/">Test1</a>
                <a href="/">Test2</a>
                <a href="/">Test3</a>
            </div>
        </div>
        <div id="Journalmall" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <button id="dropdown_button" class="pl-[5%]">Vårdenhet</button>
            <div id="dropdown_1">
                <a href="/">Test1</a>
                <a href="/">Test2</a>
                <a href="/">Test3</a>
            </div>
        </div>
        <div id="Journalmall" class="w-[10vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <button id="dropdown_button" class="pl-[5%]">Yrkesroll</button>
            <div id="dropdown_1">
                <a href="/">Test1</a>
                <a href="/">Test2</a>
                <a href="/">Test3</a>
            </div>
        </div>
        <style>
            #Journalmall {
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
            #dropdown_1 {
                display: none;
                text-align: left;
            }
            #dropdown_1 a {
                color: black;
                text-decoration: none;
                padding: 5px;
            }
            #dropdown_1 a:hover {background-color: #ddd;}

            #Journalmall:hover #dropdown_1 {
                display: flex;
                position: absolute;
                flex-direction: column;
                background: white;
                width: 90%;
                margin-left: 5%;
                margin-right: 5%;
                box-shadow: 0px 20px 100px 0px rgba(0, 0, 0, 0.5);
            }
            #Journalmall:hover {
                size-adjust: fit-content;
            }
            #Journalmall:hover {background-color: lightgray;}
        </style>

        <div id="Datum" class="flex flex-row gap-[6vw] w-[20vw] outline-3 outline-gray-300 rounded-xl bg-white">
            <div class="pl-[5%]">Från:</div>
            <div>Till:</div>
        </div>
        <div id="Reset">Återställ</div>
    </div>
</div>