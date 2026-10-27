# writing-voice

A Claude Code plugin that learns **your** writing voice from your own
samples, then drafts, rewrites and revises in it. It ships with no one's
voice: you build yours in one guided session (see [CUSTOMIZE.md](CUSTOMIZE.md)).

## What's inside

| Skill | Use it to |
|---|---|
| `/writing-voice:voice-setup` | Turn 5–15 of your own pieces into a voice profile (run this first) |
| `/writing-voice:voice` | Draft, rewrite or revise in your voice; check how well a passage fits it |
| `/writing-voice:academic-essay` | Write a full course paper from a prompt and readings: verified quotes with page numbers, Chicago footnotes, .docx and .pdf |
| `/writing-voice:unslop` | Remove generic AI patterns while keeping your documented habits |
| `/writing-voice:ai-writing-signs` | Audit a draft against a pinned catalog of AI-writing signs |

Tools (all standard library unless noted):

| Tool | Purpose |
|---|---|
| `tools/voice/measure.py` | Measure your corpus and write `voice/profile.json` targets |
| `tools/essay/voice_gate.py` | Check a draft against your profile and for 8+ word copying from your samples |
| `tools/essay/extract_docx.js` | Print the text of a .docx (Node.js) |
| `tools/essay/pgrep.js` | Page-aware search of `pdftotext -layout` output to verify quotes and pages (Node.js) |
| `tools/essay/build_docx.js` | Times New Roman 12, double-spaced, Chicago footnotes, bibliography (Node.js) |
| `tools/essay/check_citations.js` | Footnotes vs bibliography cross-check (Node.js) |
| `tools/essay/page_check.js` | Page count, where the body ends, PDF export (Windows + Microsoft Word) |
| `scorer/score.py` | `retrieve` passages by genre, `overlap` with your corpus |
| `scorer-stylo/` | Optional stylometric classifier you train on your own data (numpy, scipy, scikit-learn) |
| `validate.py` | Self-check of the package |

## Install

```bash
git clone https://github.com/FishMan2341/writing-voice
claude --plugin-dir ./writing-voice
```

Or add it as a marketplace inside Claude Code:

```
/plugin marketplace add FishMan2341/writing-voice
/plugin install writing-voice@writing-voice
```

Then run `/writing-voice:voice-setup` and follow [CUSTOMIZE.md](CUSTOMIZE.md).

Requirements: Python 3, Node.js. For essays from PDF readings, `pdftotext`
(poppler). `page_check.js` needs Microsoft Word on Windows; elsewhere, page
length is reported as an estimate.

## Your data stays yours

Everything personal lives in `voice/`, which is git-ignored except for its
README. Generated training data (`scorer-stylo/negatives/`) and models are
ignored too. Run `git status` before every push, and never `git add -f`
anything inside `voice/`.

## Honesty

The plugin never claims authorship, undetectability or detector results.
Scores are comparative style signals. The academic-essay skill reminds you
that your course's AI-use policy is yours to check, so check it.

## Credits and licenses

- Code and docs: MIT ([LICENSE](LICENSE)).
- `skills/ai-writing-signs/references/catalog.md` paraphrases
  [Wikipedia:Signs of AI writing](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1375746757)
  (pinned revision), which is CC BY-SA 4.0; see [NOTICE](NOTICE).
