<script lang="ts">
  import Header from "$lib/components/Header.svelte"
  import "../app.css";
</script>


<main class="flex flex-col gap-1 h-screen">
  <header>
    <Header />
  </header>
    <slot />
</main>
