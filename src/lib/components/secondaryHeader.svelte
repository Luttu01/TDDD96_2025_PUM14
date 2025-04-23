<script lang="ts">

import { powerMode } from "$lib/stores";
</script>

<div class="p-2 flex items-center gap-2">
    <label for="powerModeToggle" class="text-sm font-medium"
      >PowerPoint Mode</label
    >
    <input
      id="powerModeToggle"
      type="checkbox"
      bind:checked={$powerMode}
      class="toggle"
    />
  </div>