<script lang="ts">

    export let isRows: boolean = false;  // Accept isRows as a prop
    export let activeTab: string = '';   // To detect if we're in the "Timeline" tab

</script>


<div class={` ${isRows ? "grid grid-cols-3 grid-rows-2 gap-2 flex-grow" : "grid grid-cols-3 grid-rows-1 gap-2 flex-grow" }`}>

<div class="border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center">col 1 row 0</div>
<div class="border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center">col 2 row 0</div>
<div class="border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center">col 3 row 0</div>

<div class={`border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center ${isRows ? "" : "hidden"}`}>col 1 row 1</div>
<div class={`border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center ${isRows ? "" : "hidden"}`}>col 2 row 1</div>
<div class={`border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center ${isRows ? "" : "hidden"}`}>col 3 row 1</div>
</div> 

 