<script lang="ts">
    import type { Note } from "../models/note";
    //import { fetchData } from "../utils/fetchBot";
    import { onMount } from "svelte";

    let documents: Note[] = [];
    let matchingDocs: number = 0;

    onMount(async () => {
        //documents = await fetchData("documents");
        //matchingDocs = documents.length;
    });

</script>
