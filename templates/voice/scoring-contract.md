# Scoring contract

No model ships with this plugin. Drafting and rewriting use the documented
profile and the tiered exemplars.

## Available without ML packages

- `scorer/score.py retrieve` and `overlap` read the manifest and corpus only.
  Inspect overlap matches in context: common phrases and attributed quotations
  are not automatically a problem.
- `tools/voice/measure.py` and `scorer-stylo/tools/profile.py` report
  descriptive rates. `fingerprint.py` compares a draft with your corpus, and
  with AI imitations of your assignments if you add them.
- `tools/essay/voice_gate.py` checks the targets in `voice/profile.json`.

## Optional classifier

`scorer-stylo/tools/train.py`, `ensemble.py`, `calibrate.py` and `escore.py`
train and run a topic-masked stylometric ensemble (numpy, scipy,
scikit-learn). It needs `voice/training_manifest.json`, AI negatives in
`scorer-stylo/negatives/`, and at least two independent assignment families.
`escore.py` refuses to run until you set `ensemble_ready` in
`scorer-stylo/availability.json`. With only a few families, treat its numbers
as rough. Record your held-out calibration here after training.

## Decisions

Facts, meaning, citations and requirements come first. Then specific critic
feedback, register fit, and the user's own judgment. Stop stylistic polish at
a plateau. Scores never certify authorship or predict external AI detectors.
