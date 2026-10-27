# voice/: your voice, as data

This folder is git-ignored (except this README). The `voice-setup` skill
copies the templates from `templates/voice/` here and fills them from your
own writing. Files that still contain `TEMPLATE` are placeholders.

| File | What it holds |
|---|---|
| `corpus/NNN.txt` | Your samples, body text only |
| `corpus_authored/NNN.txt` | Same, minus long quotations and prompt labels (`extract_authored.py`) |
| `manifest.json` | One record per sample: genre, date, trust tier, family |
| `exclusions.json` | Lines to drop when making `corpus_authored/` |
| `training_manifest.json` | Samples eligible for the optional classifier |
| `profile.json` | Rates and phrase lists the voice gate checks (`tools/voice/measure.py --write`) |
| `voice-profile.md` | Your habits, by register, with quoted evidence |
| `sentence-skeletons.md` | Sentence patterns by job, each taken from a real sentence |
| `exemplars/*.md` | 1–3 verbatim paragraphs per genre, plus a routing README |
| `imitation-tells.md` | What imitations of you get wrong |
| `voice-exceptions.md` | Your habits that generic editing rules must leave alone |
| `personal-facts.md` | Facts drafts may use, each with a source |
| `academic-register.md` | Rules for course essays (generic until you fill §2–3) |
| `scoring-contract.md` | What the scores mean and do not mean |

## manifest.json record

```json
{"doc_id": "001", "family_id": "outliers_essay", "genre": "argumentative_essay",
 "written_approx": "2025-03", "source_tier": "primary", "authorship": "self-reported",
 "raw_body_words": null, "training_eligible": false, "notes": "Revision of 002."}
```

`source_tier` is `primary` (written alone), `review` (edited, co-written or
unsure) or `review_ai_edit_reported`. Drafts of one assignment share a
`family_id`. `raw_body_words` may stay null; `extract_authored.py` checks it
when set.

## exclusions.json

`docs` maps a doc ID to `operations`: `drop_line_exact` (`text`) or
`drop_line_prefix` (`prefix`), each with the `expected_count` of lines it
must match. The run aborts if a count disagrees, so an exclusion can never
silently drop the wrong text.
