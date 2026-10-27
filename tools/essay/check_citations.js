// Cross-check an essay source (build_docx.js markup) against its bibliography:
//  - every bibliography entry must be cited somewhere in the footnotes or text
//  - every source named first in a footnote must appear in the bibliography
//  - flags quotes that sit in a sentence with no footnote in that paragraph
// usage: node check_citations.js essay.txt
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8').replace(/^﻿/, '').replace(/\r/g, '');
const [main, bib = ''] = src.split(/^#BIB\s*$/m);
const notes = [...main.matchAll(/\{\{([^}]*)\}\}/g)].map(m => m[1]);
const bibLines = bib.split('\n').map(l => l.trim()).filter(Boolean);
const strip = s => s.replace(/\*/g, '').replace(/[“”"]/g, '').trim();

// Key for a bibliography line: case name ("Plessy v. Ferguson") or author surname ("Keyssar").
const bibKey = l => {
  const s = strip(l);
  const m = s.match(/^(?:The )?([^,.]+?)(?:,|\.| \d)/);
  return (m ? m[1] : s).trim();
};
const keys = bibLines.map(bibKey);
const allNotes = notes.map(strip).join(' || ');
const body = strip(main.replace(/\{\{[^}]*\}\}/g, ''));
let problems = 0;

for (const [i, k] of keys.entries()) {
  const word = k.split(/\s+v\.\s+|\s+/)[0];
  if (!allNotes.includes(word) && !body.includes(word)) { console.log(`UNCITED bibliography entry: ${bibLines[i].slice(0, 80)}`); problems++; }
}

const skip = /^(ibid|id\.|see also|see|quoted|cf\.|u\.s\. const|amend\.|art\.|the declaration)/i;
for (const [i, n] of notes.entries()) {
  for (const part of strip(n).split(/;\s*/)) {
    const p = part.replace(/^(see also|see|cf\.)\s+/i, '').trim();
    if (!p || skip.test(p)) continue;
    const lead = p.split(/[,(]/)[0].replace(/\s+v\.\s+.*/, '').trim();
    const surname = lead.split(/\s+and\s+|\s+/).filter(w => /^[A-Z]/.test(w)).slice(-1)[0] || lead;
    const caseName = p.match(/^([A-Z][^,]*? v\. [^,]+)/);
    const needle = caseName ? caseName[1].split(' v. ')[0] : (lead.includes(' ') && !/^[A-Z][a-z]+, /.test(p) ? surname : lead);
    if (needle.length > 2 && !bibLines.some(b => strip(b).includes(needle))) { console.log(`NOT IN BIBLIOGRAPHY (note ${i + 1}): ${p.slice(0, 80)}`); problems++; }
  }
}

main.split('\n').filter(l => l.trim() && !l.startsWith('#')).forEach((para, i) => {
  const outside = para.replace(/\{\{[^}]*\}\}/g, '');
  const longQuote = [...outside.matchAll(/"([^"]*)"/g)].some(m => m[1].length >= 25);
  if (longQuote && !para.includes('{{')) { console.log(`QUOTE WITHOUT NOTE in paragraph ${i + 1}: ${para.slice(0, 70)}...`); problems++; }
});

console.log(`${notes.length} footnotes, ${bibLines.length} bibliography entries, ${problems} problem(s)`);
process.exit(problems ? 1 : 0);
