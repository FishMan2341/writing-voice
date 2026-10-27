---
name: voice
description: Draft new material, rewrite existing drafts (including rough notes and AI-assisted drafts), and revise flagged passages in the user's own documented writing voice, based on their genuine writing samples in voice/. Also analyzes how well a passage fits their style and reports concrete mismatches. Use when the user asks for writing or rewriting "in my voice", matching their samples, or analysis of a passage's fit to their style.
---

# voice

## Plugin paths

All resource paths below are relative to the installed plugin root, not the
user's project or this SKILL.md directory. Resolve `${CLAUDE_PLUGIN_ROOT}` when
available, or discover the plugin root two directories above this skill folder.
Read resources and invoke scripts by absolute paths; pass an absolute draft path.
Do not install dependencies or train models automatically.

## Setup check (first)

If `voice/voice-profile.md` is missing or still contains the word `TEMPLATE`,
or `voice/manifest.json` is missing or empty, the voice has not been built yet. Say so and
offer to run the `voice-setup` skill. Do not pretend to write in a voice that
has no samples behind it.

## Provenance and trust tiers

Every corpus document in `voice/manifest.json` carries a `source_tier`:

- `primary`: the user confirmed they wrote it alone.
- `review`: probably theirs, but edited, co-written, or uncertain.
- `review_ai_edit_reported`: known to have passed through AI editing.

Consequences:
- Style evidence: all documents inform the profile; weight primary over
  review; treat AI-edited polish cautiously.
- Training (optional stylometry): only documents listed in
  `voice/training_manifest.json` are eligible; the loader fails without it.
  Never promote a review-tier document without the user's confirmation.
- Personal facts: only those in `voice/personal-facts.md` or the brief.
  Confirm with the user before using one in a new draft. Never invent.

## Read order

1. This file.
2. `voice/voice-profile.md` (registers, word habits, targets).
3. `voice/sentence-skeletons.md` (the drafting tool).
4. `voice/exemplars/README.md` (route to the closest 2-3 genuine excerpts).
5. `voice/personal-facts.md` before using any personal detail.
6. `voice/voice-exceptions.md` where a general editing rule may conflict.
7. `voice/academic-register.md` for any course essay or cited academic writing.

## Modes

- **Academic essay** (a full paper from a prompt and readings): use this
  plugin's `academic-essay` skill.
- **Draft**: from the user's brief. Plan content first (claims, evidence,
  order, open factual questions), then build sentences on skeletons. Do not
  invent personal experiences or attribute views to the user beyond supplied facts.
- **Rewrite**: preserve intended meaning, facts, numbers, and citations;
  note material changes.
- **Targeted revision**: revise only flagged spans; adjust neighbors only for
  coherence.

## Workflow

1. Intake: purpose, audience, genre, length, intended position, factual
   inputs, sources, requirements. New genre: route by proximity and say so.
2. Content plan (plain notes; no styling yet).
3. Register: pick the genre row in `voice-profile.md`; weight recent samples
   over old ones if the profile says the voice changed over time.
4. Draft/rewrite on skeletons: keep the user's scaffolding habits at their
   observed rates (never double them).
5. Self-review per paragraph against `imitation-tells.md`; name concrete
   mismatches. Optional aids: `scorer-stylo/tools/profile.py`,
   `scorer-stylo/tools/fingerprint.py` (flags are re-read prompts).
6. Variant comparison: 2-3 variants for difficult passages; rank by
   editorial judgment plus the audit (or by `escore.py` if the user has
   trained their own ensemble).
7. Independent review (optional): a blind critic from a different model
   family using `evaluation/rubric.md`; it judges fit and quality, never
   authorship. If unavailable, say so and continue.
8. Final checks: facts, citations, required content, no unintended meaning
   change; `python3 scorer/score.py overlap --file draft.txt`. Generic-tell
   audit with `unslop` and `ai-writing-signs`, with `voice-exceptions.md`
   applied.
9. Deliver: prose plus a short note on personal facts used (doc IDs),
   material uncertainties, and any checks not performed.

## Stopping rules

- Stylistic iteration stops on plateau or about three passes for routine
  tasks. An iteration limit never overrides an unresolved factual, citation,
  or meaning-preservation failure: fix it, flag it, or hold the piece.
- Any user-flagged span is wrong regardless of scores or critic opinion.

## Honesty rules

Scores are comparative style signals. Do not claim authorship, absence of
assistance, undetectability, or detector results. When asked, describe
accurately what this skill did and did not check.
