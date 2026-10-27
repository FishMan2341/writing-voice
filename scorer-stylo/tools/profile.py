import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import re, sys, statistics as st, collections
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
def prof(t):
    ss = sents(t); L = [len(s.split()) for s in ss]; W = re.findall(r"[A-Za-z’']+", t); n = len(W)
    per = lambda c: 1000 * c / n
    lw = [w.lower().replace('’', "'") for w in W]
    cnt = collections.Counter(lw)
    d = {}
    d['words'] = n; d['sents'] = len(ss)
    d['sl_med'] = st.median(L); d['sl_mean'] = round(st.mean(L), 1)
    d['sl_sd'] = round(st.pstdev(L), 1)
    d['pct<=10'] = round(100 * sum(l <= 10 for l in L) / len(L)); d['pct>=35'] = round(100 * sum(l >= 35 for l in L) / len(L))
    d['comma/sent'] = round(t.count(',') / len(ss), 2)
    for name, ch in [('semi', ';'), ('colon', ':'), ('paren', '('), ('quest', '?'), ('slash', '/')]:
        d[name] = round(per(t.count(ch)), 1)
    d['contr'] = round(per(len(re.findall(r"[A-Za-z][’'](s|d|ve|ll|re|t|m)\b", t))), 1)
    d['I/me/my'] = round(per(cnt['i'] + cnt['me'] + cnt['my']), 1)
    for w in ['the', 'of', 'and', 'that', 'which', 'to', 'a', 'it', 'this', 'is', 'be', 'as', 'in', 'their', 'they', 'one', 'not']:
        d[w] = round(per(cnt[w]), 1)
    d['-ly'] = round(per(sum(1 for w in lw if w.endswith('ly') and len(w) > 4)), 1)
    d['wlen'] = round(st.mean(len(w) for w in W), 2)
    caps = re.findall(r'(?<![.!?]\s)(?<!^)\b[A-Z][a-z]+', t)
    d['Caps/1k'] = round(per(len(caps)), 1)
    d['digits/1k'] = round(per(len(re.findall(r'\d+', t))), 1)
    return d, ss
if __name__ == '__main__':
  files = sys.argv[1:]
  rows = {}
  for f in files:
      t = open(f, encoding='utf-8').read()
      rows[f.split('/')[-1]], _ = prof(t)
  keys = list(next(iter(rows.values())).keys())
  print('feature'.ljust(11) + ''.join(k[:11].rjust(12) for k in rows))
  for k in keys:
      print(k.ljust(11) + ''.join(str(rows[r][k]).rjust(12) for r in rows))
