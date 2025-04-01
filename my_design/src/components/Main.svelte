<script lang="ts">
    import Gridlayout from "../components/Gridlayout.svelte";
    import Tidslinje from "../components/Timeline.svelte";
   
    export let activeTab: string;
    export let isRows: boolean;
  </script>
  
  {#if activeTab === "Tidslinje"}
    <!-- Show Timeline view -->
    <Tidslinje {isRows}/>
  {:else}
    <!-- Show Gridlayout for all other tabs -->
    <Gridlayout {activeTab} {isRows} />
  {/if}

