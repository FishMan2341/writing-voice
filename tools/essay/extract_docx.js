// Print the paragraph text of a .docx (assignment prompts, rubrics). No dependencies.
// usage: node extract_docx.js prompt.docx
const fs = require('fs');
const zlib = require('zlib');

const buf = fs.readFileSync(process.argv[2]);
// Find the end-of-central-directory record, then walk the central directory.
let eocd = buf.lastIndexOf(Buffer.from([0x50, 0x4b, 0x05, 0x06]));
if (eocd < 0) throw new Error('not a zip/docx file');
const count = buf.readUInt16LE(eocd + 10);
let off = buf.readUInt32LE(eocd + 16);
let xml = null;
for (let i = 0; i < count; i++) {
  const method = buf.readUInt16LE(off + 10);
  const csize = buf.readUInt32LE(off + 20);
  const nlen = buf.readUInt16LE(off + 28), elen = buf.readUInt16LE(off + 30), clen = buf.readUInt16LE(off + 32);
  const local = buf.readUInt32LE(off + 42);
  const name = buf.toString('utf8', off + 46, off + 46 + nlen);
  if (name === 'word/document.xml') {
    const lnlen = buf.readUInt16LE(local + 26), lelen = buf.readUInt16LE(local + 28);
    const data = buf.subarray(local + 30 + lnlen + lelen, local + 30 + lnlen + lelen + csize);
    xml = (method === 8 ? zlib.inflateRawSync(data) : data).toString('utf8');
    break;
  }
  off += 46 + nlen + elen + clen;
}
if (!xml) throw new Error('word/document.xml not found');
const text = xml
  .replace(/<w:tab\/>/g, '\t')
  .replace(/<\/w:p>/g, '\n')
  .replace(/<[^>]+>/g, '')
  .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'");
console.log(text.split('\n').map(l => l.trim()).filter(Boolean).join('\n'));
