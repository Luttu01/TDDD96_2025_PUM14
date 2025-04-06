<script lang="ts">
  import Filter from "$lib/components/Filter.svelte";
  import "../app.css";
</script>

<main class="flex flex-col h-screen">
  <header class="h-10">
    <Filter />
  </header>

  <slot />
</main>
