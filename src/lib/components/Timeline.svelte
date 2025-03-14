<script lang="ts">
    import { onMount } from "svelte";
  
    let journalNotes: { date: Date; content: string }[] = [];
  
    onMount(() => {
      journalNotes = [
        { date: new Date("2021-01-01"), content: "First note" },
        { date: new Date("2021-01-02"), content: "Second note" },
        { date: new Date("2021-01-03"), content: "Third note" },
        { date: new Date("2021-01-04"), content: "Fourth note" },
        { date: new Date("2021-01-05"), content: "Fifth note" },
        { date: new Date("2021-01-06"), content: "Sixth note" },
        { date: new Date("2021-01-07"), content: "Seventh note" },
        { date: new Date("2021-01-08"), content: "Eighth note" },
        { date: new Date("2021-01-09"), content: "Ninth note" },
        { date: new Date("2021-01-10"), content: "Tenth note" },
      ];
    });
  </script>
  
  <div class="h-full bg-gray-100 relative flex flex-col overflow-x-auto p-2 space-y-2">
    <div class="flex">
      {#each journalNotes as note, index}
        <div class="relative flex-none w-[calc(20rem+0.25rem)] h-3">
          <div
            class="absolute top-0 left-1/2 h-3 w-3 bg-black rounded-full"
          ></div>
        </div>
      {/each}
    </div>
  
    <div class="flex flex-grow space-x-1">
      {#each journalNotes as note}
        <div class="bg-white flex-none p-1 rounded-md shadow-sm w-80">
          <div class="text-left text-sm text-gray-500">
            {note.date.toDateString()}
          </div>
          {note.content}
        </div>
      {/each}
    </div>
  </div>
  