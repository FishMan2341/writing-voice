// Measure a built .docx in Microsoft Word (Windows) and optionally export a PDF.
// Reports total pages, the page and height where the body ends (the last words
// of the conclusion, given as --end), and which footnotes sit on that page.
// Runs Word through an inline PowerShell command, so no .ps1 file is needed.
// usage: node page_check.js --docx Essay.docx --end "rather than a" [--pdf]
const { execFileSync } = require('child_process');
const path = require('path');

const args = {};
process.argv.slice(2).forEach((a, i, all) => { if (a.startsWith('--')) args[a.slice(2)] = all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true; });
if (!args.docx || !args.end) { console.error('usage: node page_check.js --docx Essay.docx --end "last words of the body" [--pdf]'); process.exit(2); }
if (process.platform !== 'win32') { console.error('page_check needs Microsoft Word on Windows; estimate length from word count instead.'); process.exit(3); }

const q = s => "'" + String(s).replace(/'/g, "''") + "'";
const docx = path.resolve(args.docx);
const pdf = args.pdf ? docx.replace(/\.docx$/i, '.pdf') : '';
// Distinct variable names: PowerShell names ignore case, so $w and $W collide.
const ps = `
$word = New-Object -ComObject Word.Application; $word.Visible = $false
try {
  $doc = $word.Documents.Open(${q(docx)}, $false, $true)
  "total pages: " + $doc.ComputeStatistics(2)
  $range = $doc.Content; $endPage = $null; $endY = $null
  # Keep the LAST match so an earlier sentence with the same words cannot fool the check.
  while ($range.Find.Execute(${q(args.end)})) { $endPage = $range.Information(3); $endY = $range.Information(6); $range.Collapse(0) }
  if ($endPage) {
    "body ends on page " + $endPage + " at " + [math]::Round($endY / 72, 2) + " in from the top (text area ends at 10.0 in)"
    $notes = @(foreach ($f in $doc.Footnotes) { if ($f.Reference.Information(3) -eq $endPage) { $f.Index } })
    "footnotes on that page: " + ($notes -join ', ')
  } else { "end text not found (search a phrase without quotation marks)" }
  ${pdf ? `$doc.ExportAsFixedFormat(${q(pdf)}, 17); "pdf: ${pdf.replace(/"/g, '')}"` : ''}
  $doc.Close($false)
} finally { $word.Quit() }`;
process.stdout.write(execFileSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', ps], { encoding: 'utf8' }));
