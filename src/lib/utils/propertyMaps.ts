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
  "Karolinska ÖV": "bg-orange-500",
  "Privat ÖV": "bg-lime-500",
  "Karolinska SV": "bg-emerald-500",
  "SLSO ÖV": "bg-sky-500",
  "Visby  ÖV": "bg-yellow-500",
  "Öppenvårdsmott. Urologi": "bg-cyan-500",
},
Journalmall: {
  "Levnadsvanor": "text-rose-500",
  "Nybesök Vårdcentral": "text-blue-500",
  "Utskrivning-omvårdnad": "text-green-500",
  "Inskrivningsanteckning SSK": "text-yellow-500",
  "Intagningsanteckning": "text-purple-500",
  "Mottagningsanteckning diabetes barn": "text-pink-500",
  "Nybesöksanteckning": "text-orange-500",
  "Remissbedömning": "text-indigo-500",
},
Yrkesroll: {
  "Läkare": "bg-purple-500",
  "Sjuksköterska": "bg-pink-500",
},
};