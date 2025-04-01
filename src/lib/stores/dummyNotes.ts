import { writable } from 'svelte/store';

export let dummyNotes = writable([
    { date: new Date("2021-01-01"), content: "Anteckning 1" },
    { date: new Date("2021-01-01"), content: "Anteckning 2" },
    { date: new Date("2021-01-03"), content: "Anteckning 3" },
    { date: new Date("2021-02-01"), content: "Anteckning 4" },
    { date: new Date("2021-02-01"), content: "Anteckning 5" },
    { date: new Date("2021-03-10"), content: "Anteckning 6" },
    { date: new Date("2021-03-10"), content: "Anteckning 7" },
    { date: new Date("2021-03-10"), content: "Anteckning 8" },
    { date: new Date("2021-04-01"), content: "Anteckning 9" },
    { date: new Date("2021-05-05"), content: "Anteckning 10" },
    { date: new Date("2021-05-05"), content: "Anteckning 11" },
    { date: new Date("2021-08-23"), content: "Anteckning 12" },
    { date: new Date("2021-08-23"), content: "Anteckning 13" },
    { date: new Date("2021-10-11"), content: "Anteckning 14" },
    { date: new Date("2021-12-24"), content: "Anteckning 15" },
    { date: new Date("2022-01-05"), content: "Anteckning 16" },
    { date: new Date("2022-01-05"), content: "Anteckning 17" },
    { date: new Date("2022-03-17"), content: "Anteckning 18" },
    { date: new Date("2022-04-25"), content: "Anteckning 19" },
    { date: new Date("2022-04-25"), content: "Anteckning 20" },
    { date: new Date("2022-04-25"), content: "Anteckning 21" },
    { date: new Date("2022-07-20"), content: "Anteckning 22" },
    { date: new Date("2022-08-30"), content: "Anteckning 23" },
    { date: new Date("2022-09-15"), content: "Anteckning 24" },
    { date: new Date("2022-12-31"), content: "Anteckning 25" },
    { date: new Date("2023-01-01"), content: "Anteckning 26" },
    { date: new Date("2023-01-01"), content: "Anteckning 27" },
    { date: new Date("2023-02-14"), content: "Anteckning 28" },
    { date: new Date("2023-02-14"), content: "Anteckning 29" },
    { date: new Date("2023-02-14"), content: "Anteckning 30" },
  ]);