import type { Note } from "$lib/models";
import type { Year, Month, Day } from "$lib/models/dateHierarchy";

export function buildDateHierarchy(notes: Note[]): Year[] {
    const hierarchy: Year[] = [];

    notes.forEach((note) => {
        const noteYear = note.date.getFullYear();
        const noteMonth = note.date.getMonth();
        const noteDay = note.date.getDay();

        let yearGroup = hierarchy.find((y) => y.year === noteYear);
        if (!yearGroup) {
            yearGroup = { year: noteYear, months: [], isCollapsed: false };
            hierarchy.push(yearGroup);
        }

        let monthGroup = yearGroup.months.find((m) => m.month === noteMonth);
        if (!monthGroup) {
            monthGroup = { month: noteMonth, days: [], isCollapsed: false };
            yearGroup.months.push(monthGroup);
        }

        let dayGroup = monthGroup.days.find((d) => d.day === noteDay);
        if (!dayGroup) {
            dayGroup = { day: noteDay, notes: [], isCollapsed: false };
            monthGroup.days.push(dayGroup);
        }

        dayGroup.notes.push(note);
    });

    hierarchy.sort((a, b) => b.year - a.year);
    hierarchy.forEach((y) => y.months.sort((a, b) => b.month - a.month));
    hierarchy.forEach((y) =>
        y.months.forEach((m) => m.days.sort((a, b) => b.day - a.day))
    );

    return hierarchy;
}

export function buildVisibleNotes(noteHierarchy: Year[]) {
    let output = [];

    for (const year of noteHierarchy) {
        if (year.isCollapsed) {
            const count = year.months.reduce(
                (sum, month) =>
                    sum +
                    month.days.reduce((daySum, day) => daySum + day.notes.length, 0),
                0
            );
            output.push({
                type: "summary",
                text: `${year.year} (${count} anteckningar dolda)`,
                year,
            });
        } else {
            for (const month of year.months) {
                if (month.isCollapsed) {
                    const count = month.days.reduce(
                        (sum, day) => sum + day.notes.length,
                        0
                    );
                    output.push({
                        type: "summary",
                        text: `${new Date(year.year, month.month).toLocaleDateString(
                            "sv-SE",
                            {
                                year: "numeric",
                                month: "numeric",
                            }
                        )} (${count} anteckningar dolda)`,
                        month,
                    });
                } else {
                    for (const day of month.days) {
                        if (day.isCollapsed) {
                            output.push({
                                type: "summary",
                                text: `${day.notes[0]?.date.toLocaleDateString("sv-SE")} (${day.notes.length} anteckningar dolda)`,
                                day,
                            });
                        } else {
                            for (const note of day.notes) {
                                output.push({ type: "note", note });
                            }
                        }
                    }
                }
            }
        }
    }

    return output;
}

export function countVisibleNotesWithinGroup(groups: (Year | Month | Day)[]): number {
    let count = 0;
    for (const group of groups) {
      if ("notes" in group) {
        count += group.isCollapsed ? 1 : group.notes.length;
      } else if ("days" in group) {
        count += group.isCollapsed ? 1 : countVisibleNotesWithinGroup(group.days);
      } else if ("months" in group) {
        count += group.isCollapsed ? 1 : countVisibleNotesWithinGroup(group.months);
      }
    }
    return count;
  }