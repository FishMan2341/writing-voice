"""One-shot voice gate for an essay in build_docx.js markup (plain prose also works).

usage: python voice_gate.py essay.txt

Strips footnotes, markup and quoted material, then:
  1. runs scorer-stylo/tools/fingerprint.py (FLAG count) and scorer/score.py overlap;
  2. checks the targets in voice/profile.json (your measured rates; see tools/voice/measure.py);
  3. lists off-voice phrases found, with the sentence they sit in.
Gates are re-read prompts, not quotas. Exit 1 if any FAIL (corpus overlap is the only hard gate).
Standard library only.
"""
import sys; sys.dont_write_bytecode = True
import os, re, subprocess, tempfile, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FINGERPRINT = os.path.join(ROOT, 'scorer-stylo', 'tools', 'fingerprint.py')
SCORE = os.path.join(ROOT, 'scorer', 'score.py')
PROFILE = os.path.join(ROOT, 'voice', 'profile.json')
TEMPLATE_PROFILE = os.path.join(ROOT, 'templates', 'voice', 'profile.json')


def load_profile():
    path = PROFILE
    if not os.path.exists(path):
        print('NOTE: voice/profile.json missing; using the generic template. Run the voice-setup skill.')
        path = TEMPLATE_PROFILE
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def clean(src):
    src = src.lstrip('﻿').replace('\r', '')
    main = re.split(r'(?m)^#BIB\s*$', src)[0]
    title = next((l[7:] for l in main.split('\n') if l.startswith('#TITLE ')), '')
    heads = [l for l in main.split('\n') if l.startswith('#HEAD ')]
    body = '\n\n'.join(l for l in main.split('\n') if l.strip() and not l.startswith('#'))
    body = re.sub(r'\{\{[^}]*\}\}', '', body).replace('*', '')
    return title, heads, body


def sentences(t):
    t = re.sub(r'\s+', ' ', t)
    parts = re.split(r'(?<=[.!?])["”\')]?\s+(?=[A-Z"“(])', t)
    out = []
    for p in parts:
        if out and re.search(r'(?:\b[A-Z]|v|U\.S|ex rel|Jr|No|St|Mr|Mrs|Dr)\.$', out[-1]):
            out[-1] += ' ' + p
        else:
            out.append(p)
    return [p for p in out if len(p.split()) >= 2]


def yours(v):
    return '' if v is None else f' (you {v})'


def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    prof = load_profile()
    title, heads, body = clean(open(sys.argv[1], encoding='utf-8').read())
    # Replace quoted material but keep its closing punctuation so sentence breaks survive.
    # The placeholder must not be a single capital letter, or "Q." reads as an initial and merges sentences.
    noq = re.sub(r'["“][^"“”]*?([.!?,;:]?)["”]', r'"Quote\1"', body)
    words = len(noq.split()); per = lambda n: 1000 * n / max(words, 1)
    ss = sentences(noq)
    opener = lambda w: 100 * sum(1 for s in ss if re.match(r'["“]?' + re.escape(w) + r'\b', s)) / max(len(ss), 1)

    results = []
    def gate(name, ok, detail, hard=False):
        results.append(('PASS' if ok else ('FAIL' if hard else 'WARN'), name, detail))

    with tempfile.TemporaryDirectory() as tmp:
        fb, fq = os.path.join(tmp, 'body.txt'), os.path.join(tmp, 'body_noq.txt')
        open(fb, 'w', encoding='utf-8').write(body); open(fq, 'w', encoding='utf-8').write(noq)
        fp = subprocess.run([sys.executable, '-I', FINGERPRINT, fq], capture_output=True, text=True)
        if fp.returncode == 0:
            flags = [l for l in fp.stdout.splitlines() if ' FLAG' in l and not l.startswith('NOTE')]
            gate('fingerprint flags', not flags, f'{len(flags)} flag(s)' + (': ' + '; '.join(f.split()[0] for f in flags) if flags else ''))
        else:
            gate('fingerprint', False, (fp.stderr or fp.stdout).strip()[-160:])
        ov = subprocess.run([sys.executable, '-I', SCORE, 'overlap', '--file', fb], capture_output=True, text=True)
        try: matches = json.loads(ov.stdout).get('matches', [])
        except ValueError: matches = None
        gate('corpus overlap (8+ words)', matches == [], 'none' if matches == [] else f'{matches}', hard=True)

    if not prof.get('title_colon_ok', True):
        gate('title has no colon', ':' not in title, title)
    if not prof.get('headings_ok', True):
        gate('no section headings', not heads, f'{len(heads)} heading(s)')
    for o in prof.get('openers', []):
        v = opener(o['word'])
        if 'max' in o: gate(f'"{o["word"]}" sentence openers <= {o["max"]}%', v <= o['max'], f'{v:.1f}%' + yours(o.get('yours')))
        if 'min' in o: gate(f'"{o["word"]}" sentence openers >= {o["min"]}%', v >= o['min'], f'{v:.1f}%' + yours(o.get('yours')))
    for r in prof.get('rates', []):
        v = per(len(re.findall(r['regex'], noq, re.I)))
        if 'max' in r: gate(f'{r["name"]} <= {r["max"]} per 1k words', v <= r['max'], f'{v:.1f}' + yours(r.get('yours')))
        if 'min' in r: gate(f'{r["name"]} >= {r["min"]} per 1k words', v >= r['min'], f'{v:.1f}' + yours(r.get('yours')))
    q = prof.get('questions')
    if q:
        n = body.count('?')
        gate(f'rhetorical questions {q["min"]}-{q["max"]}', q['min'] <= n <= q['max'], f'{n}')
    ls = prof.get('long_sentences')
    if ls:
        pct = 100 * sum(1 for s in ss if len(s.split()) >= ls['words']) / max(len(ss), 1)
        gate(f'sentences of {ls["words"]}+ words <= {ls["max_pct"]}%', pct <= ls['max_pct'], f'{pct:.0f}%' + yours(ls.get('yours')))
    if 'max_contractions' in prof:
        c = len(re.findall(r"\b\w+(?:n't|'re|'ll|'ve|'d)\b", noq))
        gate(f'contractions outside quotes <= {prof["max_contractions"]}', c <= prof['max_contractions'], f'{c}')
    for phrase, cap in prof.get('signatures', {}).items():
        n = body.count(phrase)
        if n > cap: gate(f'signature "{phrase}" <= {cap}', False, f'{n} uses')

    hits = []
    for pat in prof.get('off_voice', []):
        for s in sentences(body):
            if re.search(pat, s, re.I): hits.append((pat, s.strip()[:110]))
    gate('off-voice phrases', not hits, f'{len(hits)} found')

    for status, name, detail in results: print(f'{status:4}  {name}: {detail}')
    for pat, s in hits: print(f'      off-voice {pat!r}: {s}')
    print(f'      {words} words outside quotes, {len(ss)} sentences')
    return 1 if any(r[0] == 'FAIL' for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
