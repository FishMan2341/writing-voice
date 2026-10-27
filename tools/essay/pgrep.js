// Page-aware search of text extracted with `pdftotext -layout file.pdf out.txt`
// (pages are separated by form feeds). Use it to verify every quote and number and
// to find the printed page number for a footnote.
// usage: node pgrep.js reading.txt "regex" [contextLines]
const fs = require('fs');
const [file, pat, ctxArg] = process.argv.slice(2);
if (!file || !pat) { console.error('usage: node pgrep.js reading.txt "regex" [contextLines]'); process.exit(2); }
const ctx = Number(ctxArg || 1);
const re = new RegExp(pat, 'i');
let hits = 0;
fs.readFileSync(file, 'utf8').split('\f').forEach((page, i) => {
  const lines = page.split('\n');
  // Printed page numbers usually sit alone on a line or at the edge of a running head.
  const nums = lines.map(l => l.trim())
    .filter(l => /^\d{1,4}$/.test(l) || /^\d{1,4}\s{3,}\S|\S\s{3,}\d{1,4}$/.test(l) || /\bI \d{1,4}$|^\d{1,4} I\b/.test(l))
    .map(l => (l.match(/^\d{1,4}|\d{1,4}$/) || [''])[0]);
  lines.forEach((l, j) => {
    if (!re.test(l)) return;
    hits++;
    console.log(`[pdf p${i + 1} | printed ${[...new Set(nums)].slice(0, 3).join(',') || '?'}]`);
    console.log(lines.slice(Math.max(0, j - ctx), j + ctx + 1).map(x => '   ' + x.trim()).join('\n'));
  });
});
if (!hits) { console.log('no match'); process.exit(1); }
