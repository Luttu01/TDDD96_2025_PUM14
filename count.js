import { readFileSync, readdirSync } from "fs";
import { join } from "path";

const directoryPath = "./src/lib/components";

let totalIdCount = 0;
let totalDivCount = 0;
let totalFilesChecked = 0;

function countDivsInSvelteFile(filePath) {
    const content = readFileSync(filePath, "utf-8");

    // Match only <div> tags
    const divRegex = /<\s*div(?:\s[^>]*)?>/gi;

    // Match <div> tags with id attributes
    const divWithIdRegex = /<\s*div[^>]*\sid\s*=\s*["'{]/gi;

    const divs = content.match(divRegex) || [];
    const divsWithId = content.match(divWithIdRegex) || [];

    return {
        totalDivs: divs.length,
        divsWithId: divsWithId.length,
    };
}

function traverseDir(dir) {
    const entries = readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = join(dir, entry.name);
        if (entry.isDirectory()) {
            traverseDir(fullPath);
        } else if (entry.isFile() && entry.name.endsWith(".svelte")) {
            const { totalDivs, divsWithId } = countDivsInSvelteFile(fullPath);
            totalDivCount += totalDivs;
            totalIdCount += divsWithId;
            totalFilesChecked++;
            console.log(`${entry.name}: ${divsWithId} IDs / ${totalDivs} divs`);
        }
    }
}

traverseDir(directoryPath);

const percentage = totalDivCount
    ? ((totalIdCount / totalDivCount) * 100).toFixed(2)
    : "0.00";

console.log("\nSummary:");
console.log(`Total Svelte files checked: ${totalFilesChecked}`);
console.log(`Total <div> elements: ${totalDivCount}`);
console.log(`Total <div> elements with id attributes: ${totalIdCount}`);
console.log(`Percentage of <div> elements with id: ${percentage}%`);
