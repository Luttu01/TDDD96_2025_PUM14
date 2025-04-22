import {colorMap} from "$lib/utils"

export function getPropertyForFilter(category : string, type : string) : string {
    return colorMap[category as "Vårdenhet" || "Journalmall" || "Yrkesroll"][type];
  }