<script lang="ts">
  import Filter from "../lib/components/Filter.svelte";
  import Header from "../lib/components/Header.svelte";
  import "../app.css";
</script>

<main class="flex flex-col h-screen">
  <header class="h-10">
    <Header />
    <Filter />
  </header>

  <slot />
</main>
