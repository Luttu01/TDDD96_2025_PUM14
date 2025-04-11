import type { Note } from "$lib/models";
import type { Year, Month, Day } from "$lib/models/dateHierarchy";

export function buildDateHierarchy(notes: Note[]): Year[] {
    const hierarchy: Year[] = [];
    notes.forEach((note) => {
        const noteDate = new Date(note.DateTime);
        const noteYear = noteDate.getFullYear();
        const noteMonth = noteDate.getMonth();
        const noteDay = noteDate.getDay();

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

    hierarchy.sort((year1, year2) => year2.year - year1.year);
    hierarchy.forEach((y) => y.months.sort((month1, month2) => month2.month - month1.month));
    hierarchy.forEach((y) =>
        y.months.forEach((m) => m.days.sort((day1, day2) => day2.day - day1.day))
    );

    return hierarchy;
}

type VisibleItem = {
    id: string;
    type: "summary" | "note";
    text: string;
    date?: string;
    context: any;
};


export function buildVisibleNotes(noteHierarchy: Year[]): VisibleItem[] {
    const output: VisibleItem[] = [];

    for (const year of noteHierarchy) {
        if (year.isCollapsed) {
            output.push(buildYearSummary(year));
            continue;
        }

        for (const month of year.months) {
            if (month.isCollapsed) {
                output.push(buildMonthSummary(year.year, month));
                continue;
            }

            for (const day of month.days) {
                if (day.isCollapsed) {
                    output.push(buildDaySummary(day));
                } else {
                    output.push(...buildNotes(day));
                }
            }
        }
    }

    return output;
}

function buildYearSummary(year: Year): VisibleItem {
    const count = year.months.reduce(
        (sum, month) =>
            sum + month.days.reduce((daySum, day) => daySum + day.notes.length, 0),
        0
    );

    return {
        id: `summary-year-${year.year}`,
        type: "summary",
        text: `${year.year} (${count} anteckningar dolda)`,
        context: year,
        date: `${year.year}`,
    };
}

function buildMonthSummary(yearNumber: number, month: Month): VisibleItem {
    const count = month.days.reduce((sum, day) => sum + day.notes.length, 0);
    const date = new Date(yearNumber, month.month).toLocaleDateString("sv-SE", {
        year: "numeric",
        month: "numeric",
    });

    return {
        id: `summary-month-${yearNumber}-${month.month}`,
        type: "summary",
        text: `${date} (${count} anteckningar dolda)`,
        context: month,
        date,
    };
}

function buildDaySummary(day: Day): VisibleItem {
    const date = day.notes[0]?.DateTime ?? "Okänd dag";

    return {
        id: `summary-day-${day.notes[0]?.DateTime}`,
        type: "summary",
        text: `${date} (${day.notes.length} anteckningar dolda)`,
        context: day,
        date,
    };
}

function buildNotes(day: Day): VisibleItem[] {
    return day.notes.map((note) => ({
        id: `note-${note.Dokument_ID}`,
        type: "note",
        text: "",
        context: note,
        date: note.DateTime,
    }));
}


export function countVisibleNotesWithinGroup(groups: (Year | Month | Day)[]): number {
    // Tree traversal to count visible notes
    let count = 0;
    for (const group of groups) {       // for each year node
      if ("notes" in group) {           // if the group is a day node, add all it's notes
        count += group.isCollapsed ? 1 : group.notes.length;
      } else if ("days" in group) {     // if the group is a month node, traverse
        count += group.isCollapsed ? 1 : countVisibleNotesWithinGroup(group.days);
      } else if ("months" in group) {   // if the group is a year node, traverse
        count += group.isCollapsed ? 1 : countVisibleNotesWithinGroup(group.months);
      }
    }
    return count;
  }