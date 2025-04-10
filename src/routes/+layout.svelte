<script lang="ts">
  import Header from "$lib/components/Header.svelte"
  import "../app.css";
</script>


<main class="flex flex-col h-screen">
  <header class="border-b-1 border-gray-200">
    <Header />
  </header>
    <slot />
</main>
