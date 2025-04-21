import type { Note } from './note';

export type Month = {
    month: number;
    notes: Note[];
    isCollapsed: boolean;
  };

export type Year = {
    year: number;
    months: Month[];
    isCollapsed: boolean;
};