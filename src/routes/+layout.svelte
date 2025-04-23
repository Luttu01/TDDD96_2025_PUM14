<script lang="ts">
  import Header from "$lib/components/Header.svelte"
  import SecondaryHeader from "$lib/components/secondaryHeader.svelte";
  import "../app.css";
</script>


<main class="flex flex-col h-screen">
  <header class="border-b-1 border-gray-200">
    <Header />
    <SecondaryHeader />
  </header>
    <slot />
</main>
