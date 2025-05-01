export function stringToColor(str: string): string {
    let hash = 0;

    // Generate a hash from the string
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    // Map hash to an HSL color
    const h = hash % 360;
    const s = 90;
    const l = 85;

    return `hsl(${h}, ${s}%, ${l}%)`;
  }