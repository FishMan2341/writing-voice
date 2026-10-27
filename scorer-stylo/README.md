# scorer-stylo: optional topic-masked stylometry

Judges how you write, not what you write about. Content words are replaced by
shape tokens (w / W / L by length, C for a mid-sentence capital, 0 for digits);
function words, discourse markers, contractions and punctuation are kept.
Four logistic-regression models (masked word 1-3 grams + character 2-5 grams at
two regularization strengths, one with sentence-length statistics, one on raw
text) are averaged.

Nothing here is trained when you install the plugin. Everything except
`fingerprint.py` and `profile.py` needs numpy, scipy and scikit-learn.

## Training your own

1. Fill `voice/` with the `voice-setup` skill and list eligible documents in
   `voice/training_manifest.json` (records: `doc_id`, `family_id`,
   `training_eligible: true`, `file: "voice/corpus_authored/<id>.txt"`).
2. Generate negatives: have one or more models answer each of your corpus
   prompts, once plainly and once told to imitate you, into
   `negatives/<model>_<plain|style>/<family_id>.txt`.
3. ```bash
   python -m venv venv && venv/bin/pip install numpy scipy scikit-learn
   venv/bin/python tools/train.py       # held-out-family AUC per source
   venv/bin/python tools/ensemble.py    # saves ensemble.pkl (git-ignored)
   venv/bin/python tools/calibrate.py   # your held-out range per genre
   ```
4. Record the calibration in `voice/scoring-contract.md`, then set
   `ensemble_ready: true` in `availability.json`.

Only load an `ensemble.pkl` you built yourself: pickle files can run code.

## Tools

| Command | What it does |
|---|---|
| `tools/escore.py draft.txt [...]` | Whole-text and per-paragraph score (refuses until `ensemble_ready`) |
| `tools/fingerprint.py draft.txt` | Stdlib only. Per-1,000-word rates and openers vs your corpus (and imitators, if present) |
| `tools/profile.py a.txt b.txt` | Stdlib only. Side-by-side profile (sentence length, punctuation, function words) |
| `tools/train.py` | Held-out AUC per imitator source |
| `tools/ensemble.py` | Trains and saves `ensemble.pkl` |
| `tools/calibrate.py` | Held-out score for every eligible document, by genre |
| `tools/rates.py` | Masked n-gram rates, you vs imitators (research, not drafting) |

## Reading the numbers

Rank variants of the same content, compare against same-task controls, aim
for your own held-out range for the register, and do not chase scores above
it. With few assignment families the numbers are rough. Scores never prove
authorship or predict external AI detectors.
