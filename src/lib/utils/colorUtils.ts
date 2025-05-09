export function stringToColor(str: string, l: number = 85): string {
    let hash = 0;

    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    const h = hash % 360;
    const s = 100;

    return `hsl(${h}, ${s}%, ${l}%)`;
  }
  