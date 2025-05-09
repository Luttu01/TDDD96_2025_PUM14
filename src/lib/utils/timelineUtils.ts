import type { Note } from "$lib/models";
import type { Year } from "$lib/models/dateHierarchy";

export function buildDateHierarchy(notes: Note[]): Year[] {
    const hierarchy: Year[] = [];
    notes.forEach((note) => {
        const noteDate = new Date(note.DateTime);
        const noteYear = noteDate.getFullYear();
        const noteMonth = noteDate.getMonth();

        let yearGroup = hierarchy.find((y) => y.year === noteYear);
        if (!yearGroup) {
            yearGroup = { year: noteYear, months: [], isCollapsed: true };
            hierarchy.push(yearGroup);
        }

        let monthGroup = yearGroup.months.find((m) => m.month === noteMonth);
        if (!monthGroup) {
            monthGroup = { month: noteMonth, notes: [], isCollapsed: true };
            yearGroup.months.push(monthGroup);
        }

        monthGroup.notes.push(note);
    });

    hierarchy.sort((year1, year2) => year2.year - year1.year);
    hierarchy.forEach((y) => y.months.sort((month1, month2) => month2.month - month1.month));
    hierarchy.forEach((y) =>
        y.months.forEach((m) =>
                m.notes.sort((note1, note2) => new Date(note2.DateTime).getTime() - new Date(note1.DateTime).getTime())
        )
    );

    return hierarchy;
}