export const shapeMap: Record<
"Vårdenhet" | "Journalmall" | "Yrkesroll",
"Circle" | "Triangle" | "Square"
> = {
Vårdenhet: "Circle",
Journalmall: "Triangle",
Yrkesroll: "Square",
};

export const colorMap: Record<
"Vårdenhet" | "Journalmall" | "Yrkesroll",
Record<string, string>
> = {
Vårdenhet: {
  "Karolinska ÖV": "bg-red-500",
  "Privat ÖV": "bg-amber-500",
  "Karolinska SV": "bg-lime-500",
  "SLSO ÖV": "bg-emerald-500",
  "Visby  ÖV": "bg-cyan-500",
  "Öppenvårdsmott. Urologi": "bg-blue-500",
},
Journalmall: {
  "Levnadsvanor": "bg-red-500",
  "Nybesök Vårdcentral": "bg-amber-500",
  "Utskrivning-omvårdnad": "bg-lime-500",
  "Inskrivningsanteckning SSK": "bg-emerald-500",
  "Intagningsanteckning": "bg-cyan-500",
  "Mottagningsanteckning diabetes barn": "bg-blue-500",
  "Nybesöksanteckning": "bg-violet-500",
  "Remissbedömning": "bg-fuchsia-500",
  "Besöksanteckning": "bg-rose-500",
  "Operationsberättelse": "bg-red-500",
  "Läkarbesök": "bg-gray-500",
  "Daganteckning": "bg-neutral-500",
  "Telefonkontakt utan besök": "bg-orange-500",
  "Läkemedelsgenomgång": "bg-yellow-500"
},
Yrkesroll: {
  "Läkare": "bg-lime-500",
  "Sjuksköterska": "bg-red-500",
},
};