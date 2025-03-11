<script lang="ts">

	import Aside from "../components/Aside.svelte";
	import Gridlayout from "../components/Gridlayout.svelte";
    import Navbar from "../components/Navbar.svelte";  
	import Tabs from "../components/Tabs.svelte";
    
    let isRows: boolean = false;    // State for grid layout
    function toggleGrid(){          // Function to toggle grid rows
      isRows = !isRows;
    }
    
</script>
    
<!-- Canvas -->
<div class="w-screen h-screen bg-gray-500 p-1">
    <div class="w-full h-full p-1 rounded-lg bg-white flex flex-col gap-1">
        <Navbar {toggleGrid} /> <!-- Pass isRows and toggleGrid to Navbar -->
    
        <!-- Sidebar + Main Content Layout -->
        <div class="flex flex-grow gap-1">
            <Aside />
            <main class="flex-grow border rounded-lg p-2 bg-gray-100 flex flex-col">
              <Tabs />
              <Gridlayout {isRows} /> <!-- Pass isRows to Gridlayout -->
            </main>
        </div>
    </div>
</div>
            
        
    
    
    
    
    