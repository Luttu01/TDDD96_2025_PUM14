<script lang="ts">

let isOpen: boolean = false;
    
    function toggleAside() {
      isOpen = !isOpen;
    }

</script>

<!-- Sidebar -->
<aside class={`border-1 bg-gray-100 rounded-lg p-5 ${isOpen ? "w-60" : "w-20"}`}>
    <div class="inline-flex">
      
      <!-- Svelte Icon button with transparent background -->
      <button on:click={toggleAside}>
      <img 
      class="w-10 h-10 cursor-pointer block"
      src="/favicon.png" 
      alt="Svelte Icon">
    </button>

      </div>
  </aside>