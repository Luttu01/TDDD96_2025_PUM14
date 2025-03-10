<script lang="ts">
    import type { document } from "../utils/fetchBot";
    import { fetchData } from "../utils/fetchBot";
    import { onMount } from "svelte";

    let documents: document[] = [];
    let matchingDocs: number = 0;

    onMount(async () => {
        documents = await fetchData("documents");
        matchingDocs = documents.length;
    });

</script>
