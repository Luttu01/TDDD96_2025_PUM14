<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    import List from "$lib/components/List.svelte";
    import SelectedNotes from "$lib/components/SelectedNotes.svelte";
    import Timeline from "$lib/components/Timeline.svelte";
    import type { Document } from "$lib/models/note";
    import { mockJournals } from "$lib/data/mockJournals";
    
    // Using mocked journals until we have a real API
    const typedJournals = mockJournals as unknown as Document[];

    // Temporary states for notification popup
    let showNotification = $state(false);
    let notificationMessage = $state("");
    let notificationTimeout: ReturnType<typeof setTimeout>;

    // Selected documents state
    let selectedDocuments = $state<Document[]>([]);

    // Temporary function to test document selection
    function handleDocumentSelect(selectedDocs: Document[]) {
        // Update the selected documents
        selectedDocuments = selectedDocs;
        
        // Update notification message based on selection count
        if (selectedDocs.length > 1) {
            notificationMessage = `Selected ${selectedDocs.length} documents`;
        } else if (selectedDocs.length === 1) {
            notificationMessage = `Selected: ${selectedDocs[0].title}`;
        } else {
            notificationMessage = 'No documents selected';
        }
        
        showNotification = true;
        
        // Clear previous timeout if exists
        if (notificationTimeout) clearTimeout(notificationTimeout);
        
        // Auto-hide after 3 seconds
        notificationTimeout = setTimeout(() => {
            showNotification = false;
        }, 3000);
    }
</script>

<div class="app-container">
  <aside class="sidebar">
    <List
      items={typedJournals}
      onselect={handleDocumentSelect}
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

  {#if showNotification}
    <div class="notification">
      <div class="notification-content">
        <span>{notificationMessage}</span>
        <button 
          class="close-button" 
          onclick={() => showNotification = false}
          aria-label="Close notification"
        >
          ×
        </button>
      </div>
    </div>
  {/if}
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
  
  .notification {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    z-index: 100;
    animation: slideIn 0.3s ease-out;
  }
  
  .notification-content {
    background-color: #3b82f6;
    color: white;
    padding: 0.75rem 1.25rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 400px;
  }
  
  .close-button {
    background: none;
    border: none;
    color: white;
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0;
    line-height: 1;
  }
  
  @keyframes slideIn {
    from {
      transform: translateY(100%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>
