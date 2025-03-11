<script lang="ts">

import { buttonData } from '$lib/buttonData'; // Import from the lib directory

export let toggleGrid: () => void;   // Define the type for toggleGrid function

  let fromDate: string = "";
  let toDate: string = "";
    
  function handleDateChange() {
  console.log("Från:", fromDate, "Till:", toDate);
  }


</script>

<!-- Navbar -->
<nav class="bg-gray-100 border-1 p-1 h-20 rounded-lg">
    
    <div class="flex items-center gap-2">
      <!-- Datepickers -->
      <input 
        type="date" 
        bind:value={fromDate} 
        class="appearance-none z-10 border-1 border-gray-300 bg-white text-gray-500 
               text-lg px-3 py-1 rounded cursor-pointer"
        on:change={handleDateChange}>
      
      <input 
        type="date" 
        bind:value={toDate} 
        class="appearance-none z-10 border-1 border-gray-300 bg-white text-gray-500 
               text-lg px-3 py-1 rounded cursor-pointer"
        on:change={handleDateChange}>
  
      {#each buttonData as button}
        <button class="z-10 w-43 group relative focus:bg-black/20 border-1 border-gray-300 bg-white text-gray-500 text-medium px-3 py-1 rounded flex items-center justify-between">
          {button.title}
          <img src="/down-arrow-icon.svg" alt="Down-Arrow" class="w-3 h-3 ml-3">
          <div class="absolute bg-white top-full left-0 w-full rounded-lg p-1 mt-1 shadow-md scale-y-0 group-focus:scale-y-100 origin-top duration-200">
            {#each button.links as link}
            <a href={link.href} class="hover:bg-black/20 rounded block w-full py-1">{link.text}</a>
            {/each}
          </div>
        </button>
      {/each}
          
      <button class="group w-43 relative focus:bg-black/20 border-1 border-gray-300 bg-white text-gray-500 
          text-medium px-3 py-1 rounded" on:click={toggleGrid}>
            Gridsystem
        </button>
      </div>
        <h1 class="text-center text-lg font-semibold">Navbar</h1>
    </nav>