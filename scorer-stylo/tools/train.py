"""Dataset loading, model definition and family-grouped cross-validation.

Positives: ONLY documents marked training_eligible in voice/training_manifest.json,
loaded from voice/corpus_authored/ (authored-only views). A missing, invalid,
non-list, empty, or inconsistent manifest raises a clear RuntimeError. There is
NO fallback to the raw corpus. Negatives: scorer-stylo/negatives/<source>/<family>.txt
that you generate (see skills/voice-setup)."""
import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import sys, glob, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from paths import PKG, CORPUS, MANIFEST, NEGATIVES
from stylo import mask, dense, windows, clean
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from scipy.sparse import hstack, csr_matrix

TRAINING_MANIFEST = os.path.join(PKG, "voice", "training_manifest.json")
CORPUS_AUTHORED = os.path.join(PKG, "voice", "corpus_authored")


from dataset import _positive_files


def load(max_windows=10):
    X, y, grp, src = [], [], [], []
    for did, fam, path in _positive_files():
        with open(path, encoding="utf-8") as fh:
            for w in windows(clean(fh.read()))[:max_windows]:
                X.append(w); y.append(1); grp.append(fam); src.append("author:" + did)
    for f in sorted(glob.glob(os.path.join(NEGATIVES, "*", "*.txt"))):
        source = f.split(os.sep)[-2]; fam = os.path.basename(f)[:-4]
        for w in windows(clean(open(f, encoding="utf-8").read()))[:max_windows]:
            X.append(w); y.append(0); grp.append(fam); src.append(source)
    y = np.array(y)
    if len(X) == 0 or y.sum() == 0 or (1 - y).sum() == 0:
        raise RuntimeError("training data must contain both positives and negatives")
    return X, y, np.array(grp), np.array(src)


class Model:
    def __init__(self, C=1.0, use_dense=True, raw=False):
        self.C, self.use_dense, self.raw = C, use_dense, raw
    def _feats(self, X, fit=False):
        M = [x if self.raw else mask(x) for x in X]
        if fit:
            self.vw = TfidfVectorizer(analyzer="word", token_pattern=r"\S+", ngram_range=(1, 3), min_df=2, sublinear_tf=True, lowercase=False)
            self.vc = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=2, sublinear_tf=True, lowercase=False, max_features=60000)
            A = self.vw.fit_transform(M); B = self.vc.fit_transform(M)
        else:
            A = self.vw.transform(M); B = self.vc.transform(M)
        parts = [A, B]
        if self.use_dense:
            D = np.array([dense(x) for x in X])
            if fit: self.sc = StandardScaler().fit(D)
            parts.append(csr_matrix(np.clip(self.sc.transform(D), -4, 4) * 0.3))
        return hstack(parts).tocsr()
    def fit(self, X, y, w=None):
        F = self._feats(X, fit=True)
        self.lr = LogisticRegression(C=self.C, class_weight="balanced", max_iter=4000)
        self.lr.fit(F, y, sample_weight=w); return self
    def margin(self, X):
        return self.lr.decision_function(self._feats(X))


def cv(X, y, grp, src, k=6, **kw):
    """Out-of-fold margins with whole assignment families held out. k is
    clamped to the number of families so thin datasets cannot create empty folds."""
    fams = sorted(set(grp))
    if len(fams) < 2:
        raise RuntimeError("validation needs at least two independent families")
    k = max(2, min(k, len(fams)))
    rng = np.random.RandomState(0); rng.shuffle(fams)
    out = np.zeros(len(y))
    for fo in [fams[i::k] for i in range(k)]:
        te = np.isin(grp, fo); tr = ~te
        if len(set(y[tr])) != 2 or not te.any():
            raise RuntimeError("validation fold lacks both training classes or test data")
        m = Model(**kw).fit([X[i] for i in np.where(tr)[0]], y[tr])
        out[te] = m.margin([X[i] for i in np.where(te)[0]])
    return out


if __name__ == "__main__":
    X, y, grp, src = load()
    print("windows", len(X), "author", int(y.sum()), "negatives", int((1 - y).sum()))
    o = cv(X, y, grp, src, C=3.0, use_dense=False)
    res = {"ALL": roc_auc_score(y, o)}
    for s in sorted(set(src)):
        if not s.startswith("author"):
            m = (y == 1) | (src == s); res[s] = roc_auc_score(y[m], o[m])
    print("held-out-family AUC", {kk: round(v, 3) for kk, v in res.items()})
