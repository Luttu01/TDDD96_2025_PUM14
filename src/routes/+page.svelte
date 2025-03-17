<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    import List from "$lib/components/List.svelte";
    import SelectedNotes from "$lib/components/SelectedNotes.svelte";
    import Timeline from "$lib/components/Timeline.svelte";
</script>

<aside>
  <List />
</aside>

<main>
  <div class="welcome-message">
    <h1>Welcome to BetterCare</h1>
    <p>Interactive Visualization of Patient Journals</p>
  </div>
  <SelectedNotes />
  <Timeline />
</main>

<style>
  .welcome-message {
    background-color: #f0f9ff;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #3b82f6;
  }
  
  h1 {
    font-size: 1.5rem;
    margin: 0 0 0.5rem 0;
    color: #1e40af;
  }
  
  p {
    margin: 0;
    color: #4b5563;
  }
</style>
