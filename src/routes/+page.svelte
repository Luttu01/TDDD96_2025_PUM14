<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    import Listview from "$lib/components/listview.svelte";
    import SelectedNotes from "$lib/components/SelectedNotes.svelte";
    import Timeline from "$lib/components/Timeline.svelte";
    import type { document } from "$lib/models/note";
    import type { Document } from "$lib/types";
    import { mockJournals } from "$lib/data/mockJournals";

    // Cast mockJournals to Document type
    const typedJournals = mockJournals as unknown as Document[];

    // Function to handle document selection
    function handleDocumentSelect(event: CustomEvent<Document>) {
        const doc = event.detail;
        console.log('Document selected:', doc.id, doc.title);
    }
    
    // Selected document state
    let selectedDocument = $state<Document | null>(null);
</script>

<div class="app-container">
  <aside class="sidebar">
    <!-- Use listview component instead of List -->
    <Listview
      items={typedJournals}
      selectedDocument={selectedDocument}
      on:select={handleDocumentSelect}
    />
  </aside>

  <main class="main-content">
    <div class="welcome-message">
      <h1>Welcome to BetterCare</h1>
      <p>Interactive Visualization of Patient Journals</p>
      <div class="success-message">
        ✓ Using {typedJournals.length} mock journal entries
      </div>
    </div>
    <SelectedNotes />
    <Timeline />
  </main>
</div>

<style>
  .app-container {
    display: flex;
    min-height: 100vh;
  }
  
  .sidebar {
    width: 30%;
    min-width: 300px;
    border-right: 1px solid #e5e7eb;
  }
  
  .main-content {
    flex: 1;
    padding: 1rem;
  }
  
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
  
  .success-message {
    margin-top: 0.5rem;
    padding: 0.5rem;
    background-color: #d1fae5;
    border-radius: 0.25rem;
    color: #065f46;
    font-weight: 500;
  }
</style>
