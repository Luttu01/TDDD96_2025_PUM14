import { browser } from '$app/environment';

/**
 * Tar ut all text som är markerad med <b> från samtiliga anteckningar.
 * Sorterar listan i alfabetisk ordning. 
 * @param html 
 * @returns 
 */
export function extractBoldTitlesFromHTML(html: string): string[] {
    if (!browser) return [];
    const container = document.createElement("div");
    container.innerHTML = html;

    const boldTags = Array.from(container.querySelectorAll("b"));
    const titles = boldTags
        .map(b => b.textContent?.trim() ?? "")
        .filter(Boolean);

    const uniqueTitles = Array.from(new Set(titles));
    return uniqueTitles.sort((a, b) => a.localeCompare(b, 'sv')); 
}

/**
 * Tar ut alla names från keywords och sorterar dem i alfabetisk ordning.
 * @param keywords 
 * @returns 
 */
export function getSortedUniqueKeywordNames(keywords: { Name: string }[]): string[] {
    const names = keywords
      .map(k => k.Name?.trim())
      .filter(Boolean);
  
    const uniqueNames = Array.from(new Set(names));
    return uniqueNames.sort((a, b) => a.localeCompare(b, 'sv'));
}