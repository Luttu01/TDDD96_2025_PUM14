<script lang="ts">

    // Import components
	import Aside from "../components/Aside.svelte";
    import Navbar from "../components/Navbar.svelte";  
	import Tabs from "../components/Tabs.svelte";
    import Main from "../components/Main.svelte"; // Handles switching between tabs (Gridlayout & Tidslinje)
    
    let isRows: boolean = false;    // Tracks Gridlayout 
  function toggleGrid() {           // Toggles between row & grid view for Gridlayout
    isRows = !isRows;
  }

  let activeTab: string = "Journaltexter"; // Default active tab (Basvy view)
    
</script>
    
<!-- Canvas -->
<div class="w-screen h-screen bg-gray-500 p-1">
    <div class="w-full h-full p-1 rounded-lg bg-white flex flex-col gap-1">
        
        <Navbar {toggleGrid} /> <!-- Pass isRows and toggleGrid to Navbar -->
    
        <!-- Sidebar + Main Content Layout -->
        <div class="flex flex-grow gap-1">
            <Aside /> <!-- Sidebar navigation -->
            <main class="flex-grow border rounded-lg p-2 bg-gray-100 flex flex-col">
                <Tabs bind:activeTab /> <!-- Tabs for switching between views -->
                <Main {activeTab} {isRows} /> <!-- Displays Gridlayout or Tidslinje based on activeTab -->
            </main>
        </div>
    </div>
</div>
            
        
    
    
    
    
    