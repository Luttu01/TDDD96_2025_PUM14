<script lang="ts">
    // Array, representing events on the timeline
    let events = [
      { date: "2024-01-01", title: "Started Treatment" },
      { date: "2024-02-15", title: "Follow-up" },
      { date: "2024-03-10", title: "Changed Medication" },
    ];

    export let isRows: boolean = false;  // Accept isRows as a prop
  </script>
  
 <!-- Timeline Layout (0 or 1 row based on isRows) -->
<div class="w-full h-full bg-gray-100 p-6">
    <h1 class="text-2xl font-bold mb-4">Timeline</h1>

    <!-- Timeline (Only shown when isRows is true) -->
    <div class="relative border-l-4 border-purple-500 pl-6">
        {#if isRows}
            <!-- Loop through events and render when isRows is true -->
            {#each events as event}
                <div class="mb-6">
                    <!-- Circle at each event -->
                    <div class="absolute w-4 h-4 bg-purple-500 rounded-full -left-2.5"></div>
                    <!-- Date and Title of the event -->
                    <p class="text-sm text-gray-500">{event.date}</p>
                    <h2 class="text-lg font-semibold">{event.title}</h2>
                </div>
            {/each}
        {/if}
    </div>
</div>
  
  