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
  "Levnadsvanor": "text-red-500",
  "Nybesök Vårdcentral": "text-amber-500",
  "Utskrivning-omvårdnad": "text-lime-500",
  "Inskrivningsanteckning SSK": "text-emerald-500",
  "Intagningsanteckning": "text-cyan-500",
  "Mottagningsanteckning diabetes barn": "text-blue-500",
  "Nybesöksanteckning": "text-violet-500",
  "Remissbedömning": "text-fuchsia-500",
  "Besöksanteckning": "text-rose-500",
  "Operationsberättelse": "text-red-500",
  "Läkarbesök": "text-gray-500",
  "Daganteckning": "text-neutral-400",
  "Telefonkontakt utan besök": "text-orange-500",
  "Läkemedelsgenomgång": "text-yellow-500"
},
Yrkesroll: {
  "Läkare": "bg-lime-500",
  "Sjuksköterska": "bg-red-500",
},
};