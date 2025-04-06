<script lang="ts">
    import type { Document } from "../models/note";
    //import { fetchData } from "../utils/fetchBot";
    import { onMount } from "svelte";

    let documents: Document[] = [];
    let matchingDocs: number = 0;

    onMount(async () => {
        //documents = await fetchData("documents");
        //matchingDocs = documents.length;
    });

</script>
