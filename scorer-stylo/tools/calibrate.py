"""Held-out calibration: score every training-eligible document with its whole
assignment family held out. Uses train.load(), so it requires
voice/training_manifest.json (no fallback). Run after retraining and update
voice/scoring-contract.md with the observed numbers."""
import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from paths import MANIFEST
from train import load, cv
from sklearn.metrics import roc_auc_score
X, y, grp, src = load()
o = cv(X, y, grp, src, C=3.0, use_dense=False)
man = {d["doc_id"]: d for d in json.load(open(MANIFEST, encoding="utf-8"))}
per_doc = collections.defaultdict(list)
for m, s in zip(o, src):
    if s.startswith("author:"): per_doc[s[5:]].append(m)
by_genre = collections.defaultdict(list)
for d, ms in per_doc.items(): by_genre[man[d]["genre"]].append(np.mean(ms))
print("held-out AUC", round(roc_auc_score(y, o), 3))
print("imitator windows: median %+.2f  p90 %+.2f" % (np.median(o[y == 0]), np.percentile(o[y == 0], 90)))
for g, v in sorted(by_genre.items(), key=lambda kv: np.mean(kv[1])):
    print(f"{g:20s} author held-out doc mean {np.mean(v):+.2f}  (range {min(v):+.2f} .. {max(v):+.2f}, n={len(v)})")
