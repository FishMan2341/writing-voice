"""Score drafts with the ensemble.
usage: escore.py draft.txt [more.txt ...]
Prints the whole-text score (mean over ~160-word windows) for the ensemble and
for the masked model used by calibrate.py, plus an ensemble score per
paragraph (paragraphs >= 25 words). Higher = more like the training author.

Guard: refuses to score unless scorer-stylo/availability.json sets
ensemble_ready true (set it only after you train on YOUR corpus with
tools/ensemble.py and check tools/calibrate.py). The guard runs BEFORE
pickle.load. Only load an ensemble.pkl you built yourself: pickle files can
run code when loaded."""
import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import sys, os, pickle, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ENSEMBLE, STYLO

AVAIL = os.path.join(STYLO, "availability.json")
_models = None


def _require_scoring():
    if not os.path.exists(AVAIL):
        sys.exit("REFUSED: scorer-stylo/availability.json is missing.")
    with open(AVAIL, encoding="utf-8") as fh:
        avail = json.load(fh)
    if not avail.get("ensemble_ready", False) or not os.path.exists(ENSEMBLE):
        sys.exit("REFUSED: no ensemble trained on your corpus yet. Train one "
                 "with tools/ensemble.py, check tools/calibrate.py, then set "
                 "ensemble_ready:true in scorer-stylo/availability.json.")


def es(texts):
    global _models
    if _models is None:
        _models = pickle.load(open(ENSEMBLE, "rb"))
    allm = np.array([m.margin(texts) for m in _models])
    return allm.mean(axis=0), allm


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Ensemble scorer (guarded until you train your own)")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()
    _require_scoring()
    import numpy as np
    from stylo import windows, clean
    if not args.files:
        sys.exit("no input files")
    for f in args.files:
        t = clean(open(f, encoding="utf-8").read())
        w, wall = es(windows(t, 160))
        ps = [p for p in t.split("\n\n") if len(p.split()) >= 25]
        pm, _ = es(ps) if ps else ([], None)
        print(f"{os.path.basename(f)}: whole-text ensemble {w.mean():+.2f} | masked model "
              f"{wall[0].mean():+.2f} | min window {w.min():+.2f}, {len(w)} windows")
        for i, (m, p) in enumerate(zip(pm, ps), 1):
            print(f"   p{i:<2d} {m:+.2f}  {p[:70]!r}")
