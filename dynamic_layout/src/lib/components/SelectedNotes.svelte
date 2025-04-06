<script lang="ts">
    export let data: any = {}; // Expecting an object with a 'data' property

    console.log("selectednotes", data);
  </script>
  
  <div class="h-full bg-white p-4">
    <h1 class="text-2xl font-bold mb-4">Case Notes</h1>
  
    {#if data.data && data.data.length > 0} <!-- Check if data.data exists and is not empty -->
      <div>
        {#each data.data as note (note.CompositionId)}
          <div class="mb-4"> <!-- Adds space between each note -->
            <p class="text-lg text-blue-600">
              <strong>CompositionId:</strong> {note.CompositionId}
            </p>
            <p class="text-lg text-green-600">
              <strong>DateTime:</strong> {note.DateTime}
            </p>
            <p class="text-lg text-green-500">
              <strong>DisplayDateTime:</strong> {note.DisplayDateTime}
            </p>
            <p class="text-lg text-purple-600">
              <strong>Dokument_ID:</strong> {note.Dokument_ID}
            </p>
            <p class="text-lg text-orange-600">
              <strong>Dokument_skapad_av_yrkestitel_ID:</strong> {note.Dokument_skapad_av_yrkestitel_ID}
            </p>
            <p class="text-lg text-orange-500">
              <strong>Dokument_skapad_av_yrkestitel_Namn:</strong> {note.Dokument_skapad_av_yrkestitel_Namn}
            </p>
            <p class="text-lg text-red-500">
              <strong>Dokumentationskod:</strong> {note.Dokumentationskod}
            </p>
            <p class="text-lg text-red-600">
              <strong>Dokumentnamn:</strong> {note.Dokumentnamn}
            </p>
            <p class="text-lg text-yellow-600">
              <strong>Tidsstämpel_för_sparat_dokument:</strong> {note.Tidsstämpel_för_sparat_dokument}
            </p>
            <p class="text-lg text-teal-600">
              <strong>Vårdenhet_Identifierare:</strong> {note.Vårdenhet_Identifierare}
            </p>
            <p class="text-lg text-teal-500">
              <strong>Vårdenhet_Namn:</strong> {note.Vårdenhet_Namn}
            </p>
          </div>
        {/each}
      </div>
    {:else}
      <p class="text-gray-500">No case notes available.</p>
    {/if}
  </div>