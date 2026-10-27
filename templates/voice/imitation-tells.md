# Imitation tells: what gives an imitation of this writer away (TEMPLATE)

Generic AI-signs catalogs catch lazy prose. This file catches text that avoids
generic signs and still does not read like the writer. Use it as the
per-paragraph audit for every draft. A single instance is not a tell; the
tell is the combination, repeated.

## A. Writer-specific tells (fill from the samples)

> `voice-setup` replaces this section. Write each tell as: what imitations do,
> what the writer does instead, with a doc ID. The common ones below are
> starting points; keep the ones the samples confirm and delete the rest.

1. **Too efficient.** The writer explains one step more than necessary (a
   restated conclusion, "This goes to show that..."); the imitation does not.
2. **Missing scaffolding.** The writer's genre scaffolding (enumerated
   openers, a question ladder, section labels) is absent or doubled.
3. **Concessions that change nothing.** The writer's concessions move the
   landing; the imitation's are cosmetic.
4. **Numbers floating without context.** The writer always converts or
   compares a figure; the imitation leaves it alone.
5. **Wrong punctuation profile.** Dashes, semicolons or colons at a rate the
   writer never uses, or missing where they are structural.
6. **Opening on abstraction** when the writer opens on a scene, quote or number.
7. **A maxim at the end of every paragraph.**
8. **Vocabulary from the wrong period** of the writer's development.
9. **Perfect grammar** when the writer's sentences have a spoken flow (never
   add their typos; slips are drafting artifacts, not style).
10. **Personal facts as resume lines** instead of the writer's way of telling them.
11. **Uniform rhythm** where the writer varies by sentence job.

## B. Overcorrection tells

- Planted quirks: a signature phrase or dash aside crammed where none fits.
- Recycling a corpus paragraph's entire arrangement with new nouns; reuse
  shapes, not whole movements.
- Verbatim runs longer than about 8 words from a corpus document (check with
  `scorer/score.py overlap --file draft.txt`).
- Manufacturing typos or slips.
- Irony, arch understatement or wit denser than the writer's.

## C. Questions to ask about every paragraph

1. What job does each sentence do, and which skeleton in
   `sentence-skeletons.md` does that job?
2. Is every personal fact from `personal-facts.md` or the brief, unembellished?
3. Is this paragraph more polished or more efficient than the samples for
   this genre and date? Which step did I skip that the writer would spell out?
4. Does it carry its genre's scaffolding at the writer's rate, not double it?
5. Did my concession move the landing?
6. Are dashes, contractions and connectives at this register's rate?
7. Is more than one sentence built on the same skeleton?
8. Does the piece end the way this writer ends this genre?
9. Would the writer know this fact, have read this source, hold this view? If
   not, attribute it, cut it, or ask the user.

## D. Academic-paper tells

Found while revising a long course paper over many rounds; see
`academic-register.md` §4 for the full list and fixes.

1. **Scholar summaries instead of sources.** Paraphrasing a reading's thesis
   in the abstract reads as generic. Quote, give the number, then react.
2. **The essay narrating itself.** "This makes the point even stronger,"
   "To be fair," "It is worth noting." Cut the commentary.
3. **Event chains.** Three or more dated events joined by "Then... A year
   after that..." with no reaction between them.
4. **Bridges and Q&A pairs.** One-line bridges ("This has happened before.")
   and self-answered questions ("So, what changed? It was Congress.").
5. **A closing maxim on every paragraph** or the same motif three times.
6. **Broken scaffolding.** "Lastly" followed by more reasons; a thesis half
   that no paragraph develops.
