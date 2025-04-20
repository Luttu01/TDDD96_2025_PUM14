export function extractBoldTitlesFromHTML(html: string): string[] {
  const container = document.createElement("div");
  container.innerHTML = html;

  const boldTags = Array.from(container.querySelectorAll("b"));
  const titles = boldTags
    .map(b => b.textContent?.trim() ?? "")
    .filter(Boolean);

  // Deduplicate and sort
  const uniqueTitles = Array.from(new Set(titles));
  return uniqueTitles.sort((a, b) => a.localeCompare(b, 'sv')); // 'sv' for Swedish sorting
}