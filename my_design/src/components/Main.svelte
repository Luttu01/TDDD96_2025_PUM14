<script lang="ts">
    import Gridlayout from "../components/Gridlayout.svelte";
    import Tidslinje from "../components/Timeline.svelte";

   
    export let activeTab: string;
    export let isRows: boolean;
  </script>
  
<!-- Conditional rendering based on active tab -->
{#if activeTab === "Tidslinje"}
<Tidslinje {isRows} />

{:else}
<!-- Show Gridlayout for all other tabs -->
<Gridlayout {isRows} />
{/if}

