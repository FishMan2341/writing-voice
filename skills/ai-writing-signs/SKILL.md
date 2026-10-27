---
name: ai-writing-signs
description: Diagnose AI-writing tells in drafts using the pinned Wikipedia Signs of AI writing catalog. Use when auditing or revising prose for artificial phrasing, formatting artifacts, or citation problems.
---

# AI writing signs

Audit prose for the signs catalogued from Wikipedia:Signs of AI writing
(revision 1375746757, 2026-09-19). This skill only diagnoses and explains; the
repair process lives in the `unslop` skill, and author-specific voice decisions
live in the `voice` skill.

## When to use

- A draft needs an "AI tells" audit before delivery.
- A revision or humanization pass must be checked against a stable list.
- Someone asks whether a passage shows signs of AI writing.

## When not to use

- Do not use it to accuse, score, or certify authorship. Signs are review cues.
- Do not use it as a detector benchmark; it is a checklist for editing.

## Process

1. Read the full catalog: `references/catalog.md`.
2. Read the draft once for meaning. Do not flag anything on the first pass.
3. On the second pass, flag spans, not documents. For each flag record: the
   span, the sign ID (e.g. C1, L1, S5), and a one-sentence reason.
4. Prefer clusters. One current sign is weak; three in one paragraph matter.
5. Repair with `unslop`; keep meaning, evidence, and citations intact.
6. If the draft is a voice task, apply
   `voice/voice-exceptions.md` (package root) before rewriting: documented author
   constructions may be preserved, including documented dash usage.
   This catalog only covers generic AI signs; for voice-imitation tells (too
   efficient, quotable endings, planted quirks, overused signature phrases) also
   run `voice/imitation-tells.md`.
7. Re-read the repaired draft. If a repair removed a verified voice trait,
   revert it and note the tradeoff.

## Status rules (do not flatten these)

- `current`: usable cue.
- `weakening`: still listed; check for clusters only.
- `historical`: weak evidence; mention only if clearly present.
- `ineffective`: never flag. The source explicitly says these are not
  diagnostic (perfect grammar, formal prose, transition words alone, etc.).

## Output format

```json
{
  "flags": [
    {"span": "text as written", "sign": "C1", "reason": "importance claim with no evidence"},
    {"span": "...", "sign": "S5", "reason": "spaced em dash used for emphasis"}
  ],
  "clusters": [{"paragraph": 2, "signs": ["C3", "L1", "L5"], "severity": 2}],
  "summary": "No severity-3 issues; two clusters to repair."
}
```

Severity: 0 absent, 1 isolated and harmless, 2 repeated or distracting,
3 structurally pervasive or misleading. Every material flag needs a span and a
reason. Never emit an "AI probability" from rule counts.

## Source discipline

- Only the pinned revision is authoritative for sign content.
- Do not add folk theories, forbidden-word lists from other sites, or claims
  that a sign proves AI authorship.
- Record the revision ID when reporting an audit that will be compared later.
