// lib/buttonData.ts

interface Link {
    href: string;
    text: string;
  }
  
  interface ButtonData {
    title: string;
    links: Link[];
  }
  
  export const buttonData: ButtonData[] = [
    {
      title: "Välj yrkesroll", 
      links: [
        { href: "#", text: "Läkare" }, 
        { href: "#", text: "Sjuksköterska" }, 
        { href: "#", text: "Fysioterapeut" }, 
      ]
    },
    {
      title: "Välj vårdenhet", 
      links: [
        { href: "#", text: "Akutmottagning" }, 
        { href: "#", text: "Barnavdelning" }, 
        { href: "#", text: "Intensivvård" }, 
      ]
    },
    {
      title: "Välj journalmall", 
      links: [
        { href: "#", text: "Allmän journal" }, 
        { href: "#", text: "Läkarjournal" }, 
        { href: "#", text: "Operationsjournal" }, 
      ]
    },
    {
      title: "Välj sökord", 
      links: [
        { href: "#", text: "Diagnos" }, 
        { href: "#", text: "Behandling" }, 
        { href: "#", text: "Symptom" }, 
      ]
    }
  ];