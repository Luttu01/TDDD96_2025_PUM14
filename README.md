# Interaktiv Visualisering av Patientjournaler

> Ett kandidatarbete vid Linköpings universitet, 2025

---

## Om projektet

**IVPJ** är en webbaserad applikation för interaktiv visualisering av patientjournaler. Systemet är byggt med fokus på snabbhet, tillgänglighet och flexibilitet, med ett gränssnitt som kan anpassas till olika arbetsflöden inom vården.

Projektet är utvecklat som ett kandidatarbete på uppdrag av Karolinska Universitetssjukhuset, med syftet att inspirera till ett nytt, mer användarvänligt journalsystem.

---

## Funktionalitet

* **Basvy** som efterliknar det nuvarande TakeCare-gränssnittet
* **Canvas-läge** – dra och släpp-ytor för att anpassa visningen av journalanteckningar
* **Tidslinjevy** – visualisera patientens historik över tid
* **Filter & sökord** – hitta relevanta journalanteckningar snabbt
* **Touch-anpassad vy** – stöd för surfplattor
* **Snabb laddningstid** - under 1.5s mätt med Lighthouse

---

## Teknisk information

| Teknologi        | Beskrivning                                              |
| ---------------- | -------------------------------------------------------- |
| **SvelteKit**    | Frontend-ramverk (kompilerar till JS)                    |
| **Tailwind CSS** | Utility-first CSS för responsiv och tillgänglig design   |
| **TypeScript**   | Statisk typning för robust utveckling                    |
| **REST API**     | Asynkrona anrop mot patientjournal-data i OpenEHR-format |
| **Playwright**   | End-to-end-testning av användargränssnitt                |
| **Lighthouse**   | Mätning av prestanda och tillgänglighet                  |

---

## Installation

För att köra projektet lokalt, följ dessa steg:

### 1. Klona projektet

```bash
git clone https://github.com/Luttu01/TDDD96_2025_PUM14.git
cd TDDD96_2025_PUM14
```

### 2. Installera beroenden

```bash
npm install
```

### 3. Starta utvecklingsservern

```bash
npm run dev
```

---

## Köra release-versionen

Om du vill köra en färdig release-version utan att bygga själv:

1. Gå till [Releases]([https://github.com/<ditt-org>/<repo-namn>/releases](https://github.com/Luttu01/TDDD96_2025_PUM14/releases))
2. Ladda ner den senaste zip-filen
3. Packa upp den och öppna `index.html` i en webbläsare

---

## Projektgruppen

| Namn             | Roll                   |
| ---------------- | ---------------------- |
| Philip Batan     | Teamledare             |
| Gustav Boberg    | Testledare             |
| Marcus Hedquist  | Analysansvarig         |
| William Janowsky | Utvecklingsledare      |
| Lucas Lindahl    | Arkitekt               |
| Erik Luttu       | Konfigurationsansvarig |
| Gabriel Matsson  | Kvalitetssamordnare    |
| Michael Werner   | Dokumentansvarig       |

---

## Licens och användning

Detta projekt är licensierat under **Apache License 2.0**.

Se hela licenstexten i filen [`LICENSE`](https://github.com/Luttu01/TDDD96_2025_PUM14/blob/main/LICENSE) eller läs mer här:  
[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

## Läs mer

Rapporten (PDF): `diva/länk`

---

## Kontakt

För frågor eller intresse kring projektet, vänligen kontakta någon av projektmedlemmarna via e-post.
