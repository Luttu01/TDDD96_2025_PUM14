import { selectedNotes } from '$lib/stores';
import type { Note } from '$lib/models';

export const handleSelectNote = (note: Note): void => {
  try {
    if (!note?.CaseData || note.CaseData.includes("Not Found")) {
      const errorMessage = note.error || "Case note data not available or not found.";
      alert(errorMessage);
      return;
    }

    selectedNotes.update((current) => {
      const currentNotes = current || [];
      const foundIndex = currentNotes.findIndex(
        (n) => n.CompositionId === note.CompositionId
      );
      if (foundIndex >= 0) {
        // Deselect note
        return currentNotes.filter((_, i) => i !== foundIndex);
      } else {
        // Select note
        return [...currentNotes, note];
      }
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "Unknown error";
    alert(`Error selecting note: ${errorMessage}`);
  }
};