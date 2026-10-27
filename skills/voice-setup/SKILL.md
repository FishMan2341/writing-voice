---
name: voice-setup
description: Build or update this plugin's voice profile from the user's own writing samples. Collects and vets samples, fills voice/corpus and voice/manifest.json, measures the user's rates, and writes voice-profile.md, sentence-skeletons.md, exemplars, personal-facts.md and profile.json from evidence. Use when the user first installs the plugin, says "set up my voice", adds new samples, or the voice skill reports that setup has not been done.
---

# voice-setup

Turns a folder of someone's real writing into the files the `voice` and
`academic-essay` skills read. Everything written here must be traceable to
the samples. Work through the steps in order and show the user what you found
at the two checkpoints.

Resolve the plugin root as `${CLAUDE_PLUGIN_ROOT}` or two folders above this
file.

## Step 0: copy the templates

Copy everything in `templates/voice/` into `voice/` that is not there yet
(never overwrite an existing file). Files that still contain `TEMPLATE` are
placeholders to replace. `voice/` is git-ignored apart from its README, so
nothing the user adds there is published by accident.

## Step 1: collect samples (one message)

Ask the user for:
- **5–15 pieces they wrote themselves**, ideally 6,000+ words in total, across
  the genres they want help with (essays, op-eds, application statements,
  emails, speeches). More genres need more pieces.
- For each piece: rough date, course or purpose, and whether they wrote it
  **alone**, **with editing help** (a tutor, a friend, Grammarly), or **with AI
  assistance**. This sets the trust tier; do not guess it.
- Any facts about themselves they are happy for drafts to use (school, job,
  hometown, experiences). Optional.
- Phrases they know they overuse, or never use.

Accept .docx, .pdf, .txt, .md, or pasted text. Read files with
`tools/essay/extract_docx.js`, `pdftotext`, or directly.

## Step 2: build the corpus

For each sample:
1. Save the text as `voice/corpus/NNN.txt` (001, 002, ...), body text only.
   Drop headers with name, student ID, teacher or address; keep the prose
   unchanged otherwise, typos included (they are evidence, not style to copy).
2. Add a record to `voice/manifest.json`:
   ```json
   {"doc_id": "001", "family_id": "short_assignment_name", "genre": "argumentative_essay",
    "written_approx": "2025-03", "source_tier": "primary", "authorship": "self-reported",
    "raw_body_words": null, "training_eligible": false, "notes": "..."}
   ```
   - `source_tier`: `primary` (wrote it alone), `review` (edited or unsure),
     `review_ai_edit_reported` (AI touched it).
   - `family_id`: drafts and revisions of the same assignment share one
     family, so they are never split between training and testing.
3. If a sample contains long third-party quotations or prompt labels, record
   them in `voice/exclusions.json` (see `voice/README.md`) and run
   `python extract_authored.py` to make the quote-free copies in
   `voice/corpus_authored/`. Otherwise copy the files across unchanged.

**Checkpoint 1:** show the user the manifest as a short table (id, genre, date,
tier, words) and confirm the tiers before going on.

## Step 3: measure

```
python tools/voice/measure.py            # whole corpus
python tools/voice/measure.py --genre <g>
python scorer-stylo/tools/profile.py voice/corpus/*.txt
```

Note sentence length, opener habits, punctuation (dashes, semicolons, colons),
contractions, questions, "I"/"we" rates, and how these differ by genre and
year. Then read every sample in full. Numbers find habits; reading explains them.

## Step 4: write the profile files (replace each TEMPLATE)

Write in the user's terms, quoting their own sentences with doc IDs. Each file's
template lists the sections to fill.

1. `voice/voice-profile.md`: the most important habits first (scaffolding,
   how they open, concede, ground numbers, conclude), a register table by
   genre, word-level habits (use often / avoid), sentence openers,
   punctuation, and how the voice changed over time. Mark rates as estimates.
2. `voice/sentence-skeletons.md`: 10–15 job-based sections (opening, conceding,
   grounding a number, enumerating, concluding, ...). Each skeleton is a
   bracketed pattern plus the real sentence it came from, with its doc ID.
3. `voice/exemplars/`: one file per main genre, holding 1–3 verbatim paragraphs
   from the corpus, headed with source, date and tier. Update
   `voice/exemplars/README.md` to route genres to files.
4. `voice/imitation-tells.md`: keep sections B–D; rewrite section A for this
   person (what an imitation of *them* gets wrong). Base it on step 5 if you
   do it, otherwise on reading.
5. `voice/voice-exceptions.md`: the constructions they use that generic editing
   rules would remove (a dash habit, "due to the fact that", a signature
   opener), so `unslop` leaves them alone.
6. `voice/personal-facts.md`: only facts the user gave or a sample states,
   each with its source. Mark anything older than a year as "confirm before use".
7. `voice/academic-register.md`: fill §2 and §3 with their academic patterns,
   if they have academic samples; otherwise leave the generic version.
8. `voice/profile.json`: run `python tools/voice/measure.py --write`, then add
   `signatures` (their pet connectives, capped at about 2 uses per piece) and
   `off_voice` phrases (words they never use). Set `title_colon_ok` and
   `headings_ok` from their samples.

## Step 5 (optional): blind imitation test

Write two short pieces imitating the user on topics from their samples, then
compare them with real paragraphs. Every difference you can name is a line
for `imitation-tells.md` section A. If the user wants the stylometric
classifier, save AI attempts at their own assignment prompts under
`scorer-stylo/negatives/<model>_<plain|style>/<family_id>.txt`, list the
eligible documents in `voice/training_manifest.json`, install numpy, scipy and
scikit-learn, run `scorer-stylo/tools/ensemble.py` and `calibrate.py`, and only
then set `ensemble_ready` in `scorer-stylo/availability.json`. Never put
drafts of a task being judged into `negatives/`.

## Step 6: test and hand over

1. Pick a sample the user did not use in any skeleton. Ask Claude (via the
   `voice` skill) to rewrite a generic version of its first paragraph, and
   show the user the result next to their original.
2. Run `python tools/essay/voice_gate.py` on the result and
   `python validate.py`.

**Checkpoint 2:** ask the user what sounds wrong. Each answer becomes a line in
`imitation-tells.md` or `voice-exceptions.md`.

## Privacy note to give the user

Their samples, profile and facts now live in `voice/` inside the plugin
folder. `.gitignore` excludes `voice/` (except its README) and
`scorer-stylo/negatives/`, so a fork can be pushed without them, but anyone
who zips or copies the folder shares their writing. Tell them to run
`git status` before every push and never `git add -f` inside `voice/`.

## Rules

- Never invent a habit, fact, or quotation. Every claim cites a doc ID.
- Never copy whole sample paragraphs into skeletons; keep the shape only.
- Do not upgrade a sample's tier without the user's word.
- Re-run this skill (steps 2–4) whenever the user adds samples.
