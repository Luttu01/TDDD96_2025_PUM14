import { browser } from '$app/environment';

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