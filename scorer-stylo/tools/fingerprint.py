"""Compare a draft's surface fingerprint with your corpus (voice/corpus/) and, if present,
with AI imitations of your assignments (scorer-stylo/negatives/<source>/*.txt).
usage: python3 fingerprint.py [draft.txt ...]      (stdlib only)
Rates are per 1,000 words. FLAG marks a draft rate that sits on the imitator side of your rate
(well above you where imitators overuse it, or well below where you use it more). Without
negatives there are no FLAGs; you only get your rates next to the draft's.
Treat flags as prompts to re-read a passage, never as quotas to hit."""
import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import sys, os, glob, re, collections, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import CORPUS, NEGATIVES
def norm(t): return t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
author_files = sorted(glob.glob(os.path.join(CORPUS, '*.txt')))
if not author_files:
    sys.exit('voice/corpus/ is empty: add your writing samples first (see skills/voice-setup).')
imit_files = sorted(glob.glob(os.path.join(NEGATIVES, '*', '*.txt')))
PATS = [
 ('this', r'\bthis\b'), ('in', r'\bin\b'), ('as', r'\bas\b'), (', as (causal)', r', as\b'), ('such', r'\bsuch\b'), ('the fact that', r'\bthe fact that\b'),
 ('we/us/our', r'\b(we|us|our)\b'), ('my', r'\bmy\b'), ('ultimately', r'\bultimately\b'), ('despite', r'\bdespite\b'), ('certainly', r'\bcertainly\b'),
 ('particularly', r'\bparticularly\b'), ("I'd / I'm", r"\bi'(d|m)\b"), ('( parenthesis', r'\('), ('; semicolon', r';'), ('hyphenated word', r'[a-z]-[a-z]'),
 ('I find', r'\bi find\b'), ('in my own experience', r'\bin my own experience\b'), ('I am of the belief/opinion', r'\bi am of the (belief|opinion)\b'),
 ('all in all', r'\ball in all\b'), ('in other words', r'\bin other words\b'), ('simply', r'\bsimply\b'), (', however (splice)', r', however\b'),
 ('because', r'\bbecause\b'), ('since', r'\bsince\b'), ('whether', r'\bwhether\b'), ('rather than', r'\brather than\b'), ('which is', r'\bwhich is\b'),
 ('can', r'\bcan\b'), ('could', r'\bcould\b'), ('should', r'\bshould\b'), ('may', r'\bmay\b'), ('not', r'\bnot\b'), ('do/does not', r'\b(do|does) not\b'),
 ('I think', r'\bi think\b'), ('someone', r'\bsomeone\b'), ('who', r'\bwho\b'), ('without', r'\bwithout\b'), ('when', r'\bwhen\b'), ('what', r'\bwhat\b'),
 ('is', r'\bis\b'), ('that', r'\bthat\b'),
]
def rates(t):
    n = max(len(t.split()), 1); return {k: 1000 * len(re.findall(p, t, flags=re.I)) / n for k, p in PATS}
ABBR = r"(?:\b[A-Z]|Mr|Mrs|Ms|Dr|St|vs|etc|e\.g|i\.e|U\.S|No|Vol|pp?)\.$"
def sents(t):
    """Sentence split that does not break on initials ("T. Harv") or common abbreviations."""
    t = re.sub(r'\s+', ' ', t)
    parts = re.split(r'(?<=[.!?])["\'”’)]?\s+(?=[A-Z"“(])', t)
    out = []
    for p in parts:
        if out and re.search(ABBR, out[-1]):
            out[-1] += ' ' + p
        else:
            out.append(p)
    return [p for p in out if len(p.split()) >= 2]
def openers(t):
    ss = sents(t); c = collections.Counter(re.findall(r"[A-Za-z']+", s)[0] for s in ss if re.findall(r"[A-Za-z']+", s))
    return c, max(len(ss), 1)
A = norm(' '.join(open(f, encoding="utf-8").read() for f in author_files)); I = norm(' '.join(open(f, encoding="utf-8").read() for f in imit_files))
HAVE_NEG = bool(I.strip())
ra, ri = rates(A), rates(I)
print('NOTE: provisional feature list; not a calibrated classifier.' + ('' if HAVE_NEG else ' No negatives found, so nothing is flagged.'))

drafts = [(os.path.basename(f), norm(open(f, encoding="utf-8").read())) for f in sys.argv[1:]]
rd = [rates(t) for _, t in drafts]
print(f"{'feature':28s} {'author':>6s} {'imit':>6s}" + ''.join(f' {n[:10]:>10s}' for n, _ in drafts))
for k, _ in PATS:
    cells = ''
    for r in rd:
        v = r[k]; a, i = ra[k], ri[k]
        flag = HAVE_NEG and ((i > a and v > max(2 * a, a + 0.5) and v > 0) or (a > i and v < min(0.5 * a, a - 0.5)))
        cells += f" {v:7.2f}{' FLAG' if flag else '    '}"[:11].rjust(11)
    print(f'{k:28s} {ra[k]:6.2f} {ri[k]:6.2f}{cells}')
ca, na = openers(A); ci, ni = openers(I)
print('\nsentence openers (% of sentences)')
keys = ['This', 'In', 'I', 'As', 'While', 'However', 'If', 'It', 'That', 'When', 'Ultimately', 'The']
for k in keys:
    row = f'{k:12s} author {100*ca[k]/na:4.1f}  imit {100*ci[k]/ni:4.1f}'
    for (n, t) in drafts:
        c, m = openers(t); row += f'  {n[:10]}: {100*c[k]/m:4.1f}'
    print(row)
for n, t in drafts:
    L = [len(s.split()) for s in sents(t)]
    print(f'\n{n}: sentences {len(L)}, median length {st.median(L):.0f}, mean {st.mean(L):.1f}, sd {st.pstdev(L):.1f}, commas/sentence {t.count(",")/len(L):.2f}')
