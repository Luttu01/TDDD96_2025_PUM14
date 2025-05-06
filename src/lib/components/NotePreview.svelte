<script lang="ts">
  import { filter } from "$lib/stores";
  import type { Note } from "$lib/models";
  import { stringToColor } from "$lib/utils";
  export let note: Note;
  export let direction: "flex-col" | "flex-row" = "flex-row";
</script>

<div
  id="note-preview"
  class="flex items-center"
  class:flex-col={direction === "flex-col"}
  class:flex-row={direction === "flex-row"}
  class:space-x-1={direction === "flex-row"}
  class:space-y-1={direction === "flex-col"}
>
  <div id="vårdenhet-preview" title={note.Vårdenhet_Namn}>
  <svg
    class={`w-5 h-5 p-[2px] ${$filter.get("Vårdenhet")?.has(note.Vårdenhet_Namn) ? `bg-[color:var(--tw-color)]` : "bg-gray-400"} text-white rounded-full`}
    style="--tw-color: {stringToColor(note.Vårdenhet_Namn)};"
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      fill-rule="evenodd"
      d="M11.293 3.293a1 1 0 0 1 1.414 0l6 6 2 2a1 1 0 0 1-1.414 1.414L19 12.414V19a2 2 0 0 1-2 2h-3a1 1 0 0 1-1-1v-3h-2v3a1 1 0 0 1-1 1H7a2 2 0 0 1-2-2v-6.586l-.293.293a1 1 0 0 1-1.414-1.414l2-2 6-6Z"
      clip-rule="evenodd"
    />
  </svg>
</div>
  <div id="journalmall-preview" title={note.Dokumentnamn}>
  <svg
    class={`w-5 h-5 p-[2px] ${$filter.get("Journalmall")?.has(note.Dokumentnamn) ? `bg-[color:var(--tw-color)]` : "bg-gray-400"} text-white rounded-full`}
    style="--tw-color: {stringToColor(note.Dokumentnamn)};"
    name={note.Dokumentnamn}
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      fill-rule="evenodd"
      d="M9 2.221V7H4.221a2 2 0 0 1 .365-.5L8.5 2.586A2 2 0 0 1 9 2.22ZM11 2v5a2 2 0 0 1-2 2H4v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-7ZM8 16a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2H9a1 1 0 0 1-1-1Zm1-5a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2H9Z"
      clip-rule="evenodd"
    />
  </svg>
</div>
  <div id="yrkesroll-preview" title={note.Dokument_skapad_av_yrkestitel_Namn}>
  <svg
    class={`w-5 h-5 p-[2px] ${$filter.get("Yrkesroll")?.has(note.Dokument_skapad_av_yrkestitel_Namn) ? `bg-[color:var(--tw-color)]` : "bg-gray-400"} text-white rounded-full`}
    style="--tw-color: {stringToColor(note.Dokument_skapad_av_yrkestitel_Namn)};"
    name={note.Dokument_skapad_av_yrkestitel_Namn}
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      fill-rule="evenodd"
      d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z"
      clip-rule="evenodd"
    />
  </svg>
  </div>
</div>
