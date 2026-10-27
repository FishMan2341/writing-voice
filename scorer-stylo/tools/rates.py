import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import sys, glob, re, collections, math
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import mask, clean
from paths import STYLO as W
from paths import PKG
def grams(files, n):
    c = collections.Counter(); tot = 0
    for f in files:
        toks = mask(clean(open(f, encoding="utf-8").read())).split()
        tot += len(toks)
        for i in range(len(toks) - n + 1):
            c[' '.join(toks[i:i + n])] += 1
    return c, tot
author = sorted(glob.glob(f'{PKG}/voice/corpus/*.txt'))
imit = sorted(glob.glob(f'{W}/negatives/*/*.txt'))
for n in (1, 2, 3):
    a, ta = grams(author, n); b, tb = grams(imit, n)
    rows = []
    for g in set(a) | set(b):
        if a[g] + b[g] < (25 if n == 1 else 15): continue
        ra = (a[g] + 0.5) / ta * 1000; rb = (b[g] + 0.5) / tb * 1000
        rows.append((math.log(ra / rb), g, ra, rb))
    rows.sort()
    print(f'== n={n}  IMITATORS OVERUSE (author rate / imitator rate per 1k tokens)')
    print('   ' + ' | '.join(f'{g} {ra:.1f}/{rb:.1f}' for _, g, ra, rb in rows[:28]))
    print(f'== n={n}  AUTHOR USES MORE')
    print('   ' + ' | '.join(f'{g} {ra:.1f}/{rb:.1f}' for _, g, ra, rb in rows[::-1][:28]))
