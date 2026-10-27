"""Train the 4-model ensemble on all data and save it to scorer-stylo/ensemble.pkl."""
import sys; sys.dont_write_bytecode = True  # keep the package free of __pycache__
import sys, os, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ENSEMBLE
from train import load, Model
X, y, grp, src = load()
cfgs = [dict(C=3.0, use_dense=False), dict(C=1.0, use_dense=False), dict(C=1.0, use_dense=True), dict(C=3.0, use_dense=False, raw=True)]
pickle.dump([Model(**c).fit(X, y) for c in cfgs], open(ENSEMBLE, 'wb'))
print('saved', ENSEMBLE)
