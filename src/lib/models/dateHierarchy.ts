import type { Note } from './note';

export type Day = {
    day: number;
    notes: Note[];
    isCollapsed: boolean;
  };

export type Month = {
    month: number;
    days: Day[];
    isCollapsed: boolean;
  };

export type Year = {
    year: number;
    months: Month[];
    isCollapsed: boolean;
};