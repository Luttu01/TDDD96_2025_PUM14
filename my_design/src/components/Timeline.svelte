<script lang="ts">
    // Array, representing events on the timeline
    let events = [
      { date: "2024-01-01", title: "Started Treatment" },
      { date: "2024-02-15", title: "Follow-up" },
      { date: "2024-03-10", title: "Changed Medication" },
    ];

    export let isRows: boolean = false;  // Accep isRows as a prop
  </script>
  

<div class={`w-full h-full ${isRows ? "grid grid-rows-1" : "grid grid-rows-2"} gap-2`}>

    {#if !isRows}
        <div class="grid grid-cols-3 gap-2">
            <div class="border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center">col 1 row 0</div>
            <div class="border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center">col 2 row 0</div>
            <div class="border bg-white rounded-sm text-center text-gray-400 flex items-center justify-center">col 3 row 0</div>
        </div>
    {/if}

    

    <ul class="border-s border-neutral-300 dark:border-neutral-500 md:flex md:justify-center md:gap-6 md:border-s-0 md:border-t">
        <!--First item-->
        <li>
          <div class="flex-start flex items-center pt-2 md:block md:pt-0">
            <div
              class="-ms-[5px] me-3 h-[9px] w-[9px] rounded-full bg-neutral-300 dark:bg-neutral-500 md:-mt-[5px] md:me-0 md:ms-0"></div>
            <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-300">
              01.07.2021
            </p>
          </div>
          <div class="ms-4 mt-2 pb-5 md:ms-0">
            <h4 class="mb-1.5 text-xl font-semibold">Title of section 1</h4>
            <p class="mb-3 text-neutral-500 dark:text-neutral-300">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque
              scelerisque diam non nisi semper, et elementum lorem ornare.
              Maecenas placerat facilisis mollis. Duis sagittis ligula in
              sodales vehicula.
            </p>
          </div>
        </li>
      
        <!--Second item-->
        <li>
          <div class="flex-start flex items-center pt-2 md:block md:pt-0">
            <div
              class="-ms-[5px] me-3 h-[9px] w-[9px] rounded-full bg-neutral-300 dark:bg-neutral-500 md:-mt-[5px] md:me-0 md:ms-0"></div>
            <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-300">
              13.09.2021
            </p>
          </div>
          <div class="ms-4 mt-2 pb-5 md:ms-0">
            <h4 class="mb-1.5 text-xl font-semibold">Title of section 2</h4>
            <p class="mb-3 text-neutral-500 dark:text-neutral-300">
              Libero expedita explicabo eius fugiat quia aspernatur autem
              laudantium error architecto recusandae natus sapiente sit nam
              eaque, consectetur porro molestiae ipsam an deleniti.
            </p>
          </div>
        </li>
      
        <!--Third item-->
        <li>
          <div class="flex-start flex items-center pt-2 md:block md:pt-0">
            <div
              class="-ms-[5px] me-3 h-[9px] w-[9px] rounded-full bg-neutral-300 dark:bg-neutral-500 md:-mt-[5px] md:me-0 md:ms-0"></div>
            <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-300">
              25.11.2021
            </p>
          </div>
          <div class="ms-4 mt-2 pb-5 md:ms-0">
            <h4 class="mb-1.5 text-xl font-semibold">Title of section 3</h4>
            <p class="mb-3 text-neutral-500 dark:text-neutral-300">
              Voluptatibus temporibus esse illum eum aspernatur, fugiat suscipit
              natus! Eum corporis illum nihil officiis tempore. Excepturi illo
              natus libero sit doloremque, laborum molestias rerum pariatur quam
              ipsam necessitatibus incidunt, explicabo.
            </p>
          </div>
        </li>
  
    </ul>
        <!--
        <div class="relative border-l-4 border-purple-500 pl-6">
            {#each events as event}
                <div class="mb-6">
                    <div class="absolute w-4 h-4 bg-purple-500 rounded-full -left-2.5"></div>
                    <p class="text-sm text-gray-400">{event.date}</p>
                    <h2 class="text-lg font-semibold text-gray-400">{event.title}</h2>
                </div>
            {/each}
        </div> -->
    </div>









  