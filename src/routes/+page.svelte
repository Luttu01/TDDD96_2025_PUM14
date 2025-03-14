<script lang="ts">
  import List from "$lib/components/List.svelte";
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";
</script>

<aside>
  <List />
</aside>

<main class="h-screen">
  <SelectedNotes />
  <Timeline />
</main>
