//import { selectedNotes } from '$lib/stores';
//import type { Note } from '$lib/models';

//export const handleSelectNote = (note: Note): { error?: string } => {
//  try {
//    if (!note?.CaseData || note.CaseData.includes("Not Found")) {
//      const errorMessage = note.error || "Case note data not available or not found.";
//      return { error: errorMessage };
//    }

//    selectedNotes.set(note);
//    return {};
//  } catch (error) {
//    const errorMessage = error instanceof Error ? error.message : "Unknown error";
//    return { error: `Error selecting note: ${errorMessage}` };
//  }
//};

import { selectedNotes } from '$lib/stores';
import type { Note } from '$lib/models';

export const handleSelectNote = (note: Note): void => {
  try {
    if (!note?.CaseData || note.CaseData.includes("Not Found")) {
      const errorMessage = note.error || "Case note data not available or not found.";
      alert(errorMessage); // Visa felmeddelande i en popup
      return;
    }

    selectedNotes.set(note);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "Unknown error";
    alert(`Error selecting note: ${errorMessage}`); // Visa felmeddelande i en popup
  }
};