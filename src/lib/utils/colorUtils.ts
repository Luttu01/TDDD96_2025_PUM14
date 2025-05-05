export function stringToColor(str: string): string {
    let hash = 0;

    // Generate a hash from the string
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    // Map hash to an HSL color
    const h = hash % 360;
    const s = 90;
    const l = 80;

    return `hsl(${h}, ${s}%, ${l}%)`;
  }

export function darkenHSL(hslStr: string, factor = 0.8) {
    const match = hslStr.match(/hsl\((\d+),\s*(\d+)%?,\s*(\d+)%?\)/);
    if (!match) return hslStr; // fallback

    const h = parseInt(match[1], 10);
    const s = parseInt(match[2], 10);
    const l = parseInt(match[3], 10);
  
    const darkerL = Math.max(0, l * factor);
    return `hsl(${h}, ${s}%, ${darkerL}%)`;
  }
  