"""Measure your corpus and suggest voice/profile.json targets.

usage: python measure.py [--write] [--genre g]

Reads voice/manifest.json and voice/corpus/*.txt (or only one genre) and prints
the rates the voice gate checks: sentence openers, "not" and semicolon rates,
long sentences, questions and contractions, plus your 15 most common sentence
openers. With --write it merges suggested targets into voice/profile.json,
keeping any off_voice and signatures lists you already wrote.

Targets are your rate plus headroom (openers and "not" may run about 30% above
you; minimums sit at about half of your rate). They are aim points for
re-reading, not quotas. Standard library only.
"""
import sys; sys.dont_write_bytecode = True
import argparse, collections, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CORPUS = os.path.join(ROOT, 'voice', 'corpus')
MANIFEST = os.path.join(ROOT, 'voice', 'manifest.json')
PROFILE = os.path.join(ROOT, 'voice', 'profile.json')
TEMPLATE_PROFILE = os.path.join(ROOT, 'templates', 'voice', 'profile.json')


def sentences(t):
    t = re.sub(r'\s+', ' ', t)
    parts = re.split(r'(?<=[.!?])["”\')]?\s+(?=[A-Z"“(])', t)
    out = []
    for p in parts:
        if out and re.search(r'(?:\b[A-Z]|U\.S|Jr|No|St|Mr|Mrs|Ms|Dr)\.$', out[-1]):
            out[-1] += ' ' + p
        else:
            out.append(p)
    return [p for p in out if len(p.split()) >= 2]


def load_texts(genre):
    if not os.path.exists(MANIFEST):
        sys.exit('voice/manifest.json is missing: run the voice-setup skill first.')
    recs = [r for r in json.load(open(MANIFEST, encoding='utf-8')) if not r.get('excluded')]
    if genre:
        recs = [r for r in recs if r.get('genre') == genre]
    texts = []
    for r in recs:
        p = os.path.join(CORPUS, r['doc_id'] + '.txt')
        if os.path.exists(p):
            texts.append(open(p, encoding='utf-8').read())
    if not texts:
        sys.exit('no corpus files matched; check voice/corpus/ and the manifest.')
    return texts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--genre')
    args = ap.parse_args()
    raw = '\n\n'.join(load_texts(args.genre))
    noq = re.sub(r'["“][^"“”]*?([.!?,;:]?)["”]', r'"Quote\1"', raw.replace('’', "'"))
    words = max(len(noq.split()), 1)
    ss = sentences(noq)
    n = max(len(ss), 1)
    per = lambda c: round(1000 * c / words, 1)
    first = collections.Counter(m.group(0) for s in ss for m in [re.match(r"[A-Za-z']+", s.lstrip('"“'))] if m)
    op = lambda w: round(100 * first[w] / n, 1)
    long35 = round(100 * sum(1 for s in ss if len(s.split()) >= 35) / n)
    m = {
        'words': words, 'sentences': len(ss),
        'openers_pct': {w: op(w) for w in ['The', 'In', 'This', 'However', 'It', 'I']},
        'not_per_1k': per(len(re.findall(r'\bnot\b', noq, re.I))),
        'semicolons_per_1k': per(noq.count(';')),
        'dashes_per_1k': per(len(re.findall(r' [–—-] ', noq))),
        'questions_per_1k': per(raw.count('?')),
        'contractions_per_1k': per(len(re.findall(r"\b\w+(?:n't|'re|'ll|'ve|'d|'m)\b", noq))),
        'long35_pct': long35,
        'top_openers': first.most_common(15),
    }
    print(json.dumps(m, indent=1))
    if words < 3000:
        print(f'NOTE: only {words} words measured; rates from under ~3,000 words are noisy.')
    if not args.write:
        return 0
    src = PROFILE if os.path.exists(PROFILE) else TEMPLATE_PROFILE
    prof = json.load(open(src, encoding='utf-8'))
    prof.pop('_comment', None)
    o = m['openers_pct']
    prof['openers'] = [
        {'word': 'The', 'max': max(round(o['The'] * 1.3, 1), 5.0), 'yours': o['The']},
        {'word': 'In', 'max': max(round(o['In'] * 1.5, 1), 4.0), 'yours': o['In']},
    ] + ([{'word': 'However', 'min': round(o['However'] / 2, 1), 'yours': o['However']}] if o['However'] >= 2 else [])
    prof['rates'] = [{'name': '"not"', 'regex': r'\bnot\b', 'max': max(round(m['not_per_1k'] * 1.3, 1), 3.0), 'yours': m['not_per_1k']}]
    if m['semicolons_per_1k'] >= 1:
        prof['rates'].append({'name': 'semicolons', 'regex': ';', 'min': round(m['semicolons_per_1k'] / 2, 1), 'yours': m['semicolons_per_1k']})
    prof['long_sentences'] = {'words': 35, 'max_pct': max(long35 + 5, 10), 'yours': f'{long35}%'}
    prof.setdefault('off_voice', [])
    prof.setdefault('signatures', {})
    prof['_measured'] = {k: v for k, v in m.items() if k != 'top_openers'}
    json.dump(prof, open(PROFILE, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('wrote', PROFILE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
