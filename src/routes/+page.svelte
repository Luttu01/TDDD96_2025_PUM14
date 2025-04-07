<script lang="ts">
  import List from "$lib/components/List.svelte";
  import SelectedNotes from "$lib/components/SelectedNotes.svelte";
  import Timeline from "$lib/components/Timeline.svelte";
</script>

<div class="flex flex-col w-full h-screen p-4 bg-gray-100">
  <aside class="mb-4">
    <List />
  </aside>

  <main class="flex-1 min-h-0"> 
    <div class="w-full h-full flex flex-col"> 
      <div class="flex-1 w-full h-full p-4 bg-white rounded-lg shadow-lg overflow-y-auto"> 
        <SelectedNotes />
        <Timeline/>
      </div>
    </div>
  </main>
</div>