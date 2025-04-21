<script lang="ts">
  import { filter } from "$lib/stores";
  import type { Note } from "$lib/models";
  export let note;

  const shapeMap: Record<
    "Vårdenhet" | "Journalmall" | "Yrkesroll",
    "Circle" | "Triangle" | "Square"
  > = {
    Vårdenhet: "Circle",
    Journalmall: "Triangle",
    Yrkesroll: "Square",
  };

  const colorMap: Record<
    "Vårdenhet" | "Journalmall" | "Yrkesroll",
    Record<string, string>
  > = {
    Vårdenhet: {
      "Karolinska ÖV": "bg-orange-500",
      "Privat ÖV": "bg-lime-500",
      "Karolinska SV": "bg-emerald-500",
      "SLSO ÖV": "bg-sky-500",
      "Visby ÖV": "bg-fuchsia-500",
      "Öppenvårdsmott. Urologi": "bg-cyan-500",
    },
    Journalmall: {
      "Levnadsvanor": "text-rose-500",
      "Nybesök Vårdcentral": "text-blue-500",
      "Utskrivning-omvårdnad": "text-green-500",
      "Inskrivningsanteckning SSK": "text-yellow-500",
      "Intagningsanteckning": "text-purple-500",
      "Mottagningsanteckning diabetes barn": "text-pink-500",
      "Nybesöksanteckning": "text-orange-500",
      "Remissbedömning": "text-indigo-500",
    },
    Yrkesroll: {
      "Läkare": "bg-purple-500",
      "Sjuksköterska": "bg-pink-500",
    },
  };

  function getNoteProperty(note: Note, key: string) {
    switch (key) {
      case "Vårdenhet":
        return note.Vårdenhet_Namn;
      case "Journalmall":
        return note.Dokumentnamn;
      case "Yrkesroll":
        return note.Dokument_skapad_av_yrkestitel_Namn;
      default:
        return null;
    }
  }

  let matchingIndicators: Array<{
    key: string;
    shape: "Circle" | "Triangle" | "Square";
    color: string;
  }> = [];
  $: matchingIndicators = [];

  $: if ($filter) {
    matchingIndicators = [];

    for (const [key, activeValues] of $filter.entries()) {
      if (activeValues.size === 0) continue;

      const noteValue = getNoteProperty(note, key);
      if (noteValue !== null && activeValues.has(noteValue)) {
        matchingIndicators.push({
          key,
          shape: shapeMap[key as "Vårdenhet" | "Journalmall" | "Yrkesroll"],
          color:
            colorMap[key as "Vårdenhet" | "Journalmall" | "Yrkesroll"]?.[
              noteValue
            ] || "bg-gray-400",
        });
      }
    }
  }
</script>


<div class="flex items-center space-x-1">
{#each matchingIndicators as indicator}
    {#if indicator.shape === "Circle"}
    <div class={`w-3 h-3 rounded-full ${indicator.color}`}></div>
    {:else if indicator.shape === "Triangle"}
    <div
        class={`w-0 h-0 border-l-6 border-r-6 border-b-12 border-transparent border-b-current ${indicator.color}`}
    ></div>
    {:else if indicator.shape === "Square"}
    <div class={`w-3 h-3 ${indicator.color}`}></div>
    {/if}
{/each}
</div>

