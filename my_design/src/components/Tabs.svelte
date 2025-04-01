<script lang="ts">

    import { tabsData } from '$lib/tabsData'; // Import from the lib directory

    //let activeLink: string = 'Journaltexter'; // Default active tab
    //function setActiveLink(link: string) {
    //  activeLink = link;
    //}
    export let activeTab: string; // ⭐ Receive activeTab from parent

  function setActiveLink(link: string) {
    activeTab = link; // ⭐ Update activeTab (this will reflect in page.svelte)
  }
</script>

<ul class="flex border-b border-gray-500 text-center font-medium text-gray-400 mb-2">
  {#each tabsData as tab}
    <li class="me-2 w-32 flex justify-center relative">
      <a
        href={tab.href}
        class="p-4 inline-block cursor-pointer w-full text-center"
        class:text-purple-500={activeTab === tab.name}
        class:hover:text-gray-600={activeTab !== tab.name}
        on:click={() => setActiveLink(tab.name)}
      >
        {tab.name}
      </a>
      {#if activeTab === tab.name}
        <div class="absolute bottom-0 left-0 w-full h-1 bg-purple-500"></div>
      {/if}
    </li>
  {/each}
</ul>




<!--
<ul class="flex border-b border-gray-500 text-center font-medium text-gray-400 mb-2">

    {#each tabsData as tab }
    <li class="me-2 w-32 flex justify-center relative">
        <a
        href={tab.href}
        class="p-4 inline-block cursor-pointer w-full text-center"
        class:text-purple-500={activeLink === tab.name}
        class:hover:text-gray-600={activeLink !== tab.name}
        on:click={() => setActiveLink(tab.name)}>
          {tab.name}
        </a>
        {#if activeLink === tab.name}
          <div class="absolute bottom-0 left-0 w-full h-1 bg-purple-500"></div>
        {/if}
      </li>
    {/each}
    
  </ul> 
-->