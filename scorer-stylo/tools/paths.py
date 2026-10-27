import os
TOOLS = os.path.dirname(os.path.abspath(__file__))
STYLO = os.path.dirname(TOOLS)                 # scorer-stylo/
PKG = os.path.dirname(STYLO)                   # plugin root
CORPUS = os.path.join(PKG, 'voice', 'corpus')
MANIFEST = os.path.join(PKG, 'voice', 'manifest.json')
NEGATIVES = os.path.join(STYLO, 'negatives')
ENSEMBLE = os.path.join(STYLO, 'ensemble.pkl')
