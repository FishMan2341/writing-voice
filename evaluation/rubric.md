# Evaluation rubric and blind critic protocol

Scores rank; they do not certify. This rubric is the decisive gate.

## Ship criteria (all must hold)

1. **Requirements:** prompt, genre, length, citation format, required content.
2. **Facts:** claims traceable to the brief, sources, or confirmed personal
   facts; no invented anecdotes or numbers.
3. **Meaning:** rewrites preserve the source's claims, facts, and citations.
4. **Voice:** `voice/imitation-tells.md` audit per paragraph, resolved.
5. **Originality:** review overlaps of eight or more corpus words in context.
   Keep appropriate attributed quotations and requested source wording; do
   not silently copy unrelated distinctive expression.
6. **Checks honestly reported:** any unavailable scorer or reviewer named,
   not implied.

## Iteration and failure (binding rule)

Iteration limits bind only stylistic polish. They never excuse an unresolved
factual, citation, or meaning-preservation failure: fix it, flag it to the
user, or hold the piece.

## Blind critic (judge the writing, never authorship)

A reviewer from a different model family than the drafter, given the draft
plus the genre's `voice/exemplars/` file (primary-tier exemplars preferred;
label AI-edited exemplars as such). Diagnosis only; cite exact spans; no
rewriting in the critic's voice. Prompt, with confirmed personal facts and
required labels listed separately:

> Compare the candidate with these labeled, genre-matched samples by the same
> writer. Diagnose differences in syntax, rhythm, paragraph movement, register
> and reasoning. Quote exact candidate spans with reasons and, where useful, a
> comparable sample construction. Distinguish defects from optional
> preferences and uncertain style evidence. Report quality and voice fit
> without inferring authorship or detector performance. Diagnosis only; do not
> rewrite in your own voice.

Two rounds at most unless the user asks; severity-2+ findings force another pass.

## Quick record

| Draft | Voice fit | Structure | Defects | Assignment | Overlap | Verdict |
|---|---|---|---|---|---|---|
