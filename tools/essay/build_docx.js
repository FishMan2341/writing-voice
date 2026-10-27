// Build a submission-ready .docx (Times New Roman 12, double-spaced, 1" margins,
// Chicago footnotes, page numbers, bibliography on its own page) from a plain-text
// essay source. No dependencies; zipping uses PowerShell on Windows or `zip` elsewhere.
//
// usage: node build_docx.js --in essay.txt --out Essay.docx --name "Your Name"
//          [--date "October 27, 2026"] [--course "..."] [--instructor "..."]
//
// Source markup:
//   #TITLE Title text          (first line)
//   #HEAD Heading text         (optional; essays normally have none)
//   Paragraph text with {{footnote text}} and *italics*.
//   #BIB                       (everything after is one bibliography entry per line)
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const args = {};
process.argv.slice(2).forEach((a, i, all) => { if (a.startsWith('--')) args[a.slice(2)] = all[i + 1]; });
if (!args.in || !args.out) { console.error('usage: node build_docx.js --in essay.txt --out Essay.docx --name "Name" [--date ...] [--course ...] [--instructor ...]'); process.exit(2); }

// Strip a UTF-8 BOM: PowerShell's Set-Content -Encoding utf8 adds one, and it hides the #TITLE marker.
const src = fs.readFileSync(args.in, 'utf8').replace(/^﻿/, '').replace(/\r/g, '');

function curly(s) {
  return s
    .replace(/(^|[\s(\[—–-])"/g, '$1“')
    .replace(/"/g, '”')
    .replace(/(^|[\s(\[“—–-])'/g, '$1‘')
    .replace(/'/g, '’');
}
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function runs(text, rpr = '') {
  return text.split(/(\*[^*]+\*)/).filter(Boolean).map(part => {
    const it = part.startsWith('*') && part.endsWith('*');
    const t = it ? part.slice(1, -1) : part;
    return `<w:r><w:rPr>${it ? '<w:i/>' : ''}${rpr}</w:rPr><w:t xml:space="preserve">${esc(curly(t))}</w:t></w:r>`;
  }).join('');
}

const footnotes = [];
function bodyPara(text, ppr) {
  let xml = '';
  for (const p of text.split(/(\{\{[^}]*\}\})/)) {
    if (p.startsWith('{{')) {
      footnotes.push(p.slice(2, -2));
      xml += `<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="${footnotes.length}"/></w:r>`;
    } else if (p) xml += runs(p);
  }
  return `<w:p><w:pPr>${ppr}</w:pPr>${xml}</w:p>`;
}

const [main, bib = ''] = src.split(/^#BIB\s*$/m);
let body = '';
let sawTitle = false;
for (const line of main.split('\n')) {
  if (!line.trim()) continue;
  if (line.startsWith('#TITLE ')) {
    sawTitle = true;
    for (const h of [args.name, args.instructor, args.course, args.date].filter(Boolean)) body += `<w:p>${runs(h)}</w:p>`;
    body += `<w:p><w:pPr><w:jc w:val="center"/></w:pPr>${runs(line.slice(7).trim())}</w:p>`;
  } else if (line.startsWith('#HEAD ')) {
    body += `<w:p><w:pPr><w:keepNext/></w:pPr>${runs(line.slice(6), '<w:b/>')}</w:p>`;
  } else if (line.startsWith('#')) {
    throw new Error('Unknown marker line: ' + line.slice(0, 40));
  } else {
    body += bodyPara(line, '<w:ind w:firstLine="720"/>');
  }
}
if (!sawTitle) throw new Error('No #TITLE line found (check for a stray character before it).');
const bibLines = bib.split('\n').filter(l => l.trim());
if (bibLines.length) {
  body += `<w:p><w:pPr><w:pageBreakBefore/><w:jc w:val="center"/></w:pPr>${runs('Bibliography')}</w:p>`;
  for (const line of bibLines) body += `<w:p><w:pPr><w:spacing w:line="240" w:lineRule="auto" w:after="240"/><w:ind w:left="720" w:hanging="720"/></w:pPr>${runs(line)}</w:p>`;
}

const NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
const files = {
  '[Content_Types].xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>`,
  '_rels/.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`,
  'word/_rels/document.xml.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>`,
  'word/document.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document ${NS}><w:body>${body}<w:sectPr><w:footerReference w:type="default" r:id="rId4"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>`,
  'word/styles.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles ${NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="FootnoteText"><w:name w:val="footnote text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:line="240" w:lineRule="auto"/></w:pPr></w:style>
</w:styles>`,
  'word/settings.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings ${NS}><w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr></w:settings>`,
  'word/footnotes.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:footnotes ${NS}>
<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>
<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>
${footnotes.map((t, i) => `<w:footnote w:id="${i + 1}"><w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr><w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>${runs(' ' + t)}</w:p></w:footnote>`).join('\n')}
</w:footnotes>`,
  'word/footer1.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr ${NS}><w:p><w:pPr><w:pStyle w:val="Footer"/><w:jc w:val="center"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>`,
};

const stage = fs.mkdtempSync(path.join(os.tmpdir(), 'essaydocx-'));
for (const [name, content] of Object.entries(files)) {
  const p = path.join(stage, name);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, content);
}
const out = path.resolve(args.out);
if (fs.existsSync(out)) fs.unlinkSync(out);
if (process.platform === 'win32') {
  const ps = `Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::CreateFromDirectory('${stage.replace(/'/g, "''")}', '${out.replace(/'/g, "''")}')`;
  execFileSync('powershell.exe', ['-NoProfile', '-Command', ps], { stdio: 'inherit' });
} else {
  execFileSync('zip', ['-qr', '-X', out, '.'], { cwd: stage, stdio: 'inherit' });
}
fs.rmSync(stage, { recursive: true, force: true });
console.log(`wrote ${out} (${footnotes.length} footnotes, ${bibLines.length} bibliography entries)`);
