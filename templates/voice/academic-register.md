# Academic register: research papers and argumentative course essays

## Evidence status

Sections 1 and 4–7 are generic: they record what worked while drafting and
revising a 10-page argumentative paper over many feedback rounds. Sections 2
and 3 hold the writer's own academic patterns; `voice-setup` fills them from
academic samples (marked `TEMPLATE` until then). Never add an assisted paper
to `voice/corpus/` as style evidence.

## 1. Before drafting (skipping these cost most of the revision rounds)

1. **Read the assignment, not a summary of it.** Extract the prompt with
   `tools/essay/extract_docx.js`. Record: page count, font, spacing, margins,
   citation style (default Chicago notes-bibliography for history/politics),
   every grading criterion verbatim, and every topic the prompt "might
   consider." Each criterion becomes a check in §6.
2. **Get the course readings before writing a sentence.** Essays built on
   general knowledge were the weakest drafts; essays built on the assigned
   readings, with page numbers, were the strongest.
3. **Extract and verify.** `pdftotext -layout` each relevant reading, then
   `tools/essay/pgrep.js` to confirm every quote and number and find its
   printed page. Image-only scans yield no text: do not cite their content as
   verified; drop them or flag them to the user.
4. **Do not quote an author's hypothetical as the subject's words.** Note
   working-paper vs. published versions of articles.
5. **Ask once for what only the user knows:** course name, instructor, due
   date, any lecture or discussion point they want included.

## 2. Architecture (TEMPLATE: fill with the writer's own moves)

A structure that scored well. Replace each bracket with the writer's own
phrasing from their academic samples, with doc IDs.

- **Intro:** concrete anchor (a vote, a date, a quote) → both positions →
  where they agree and split → thesis in [the writer's thesis shape] →
  one-sentence roadmap.
- **Concession paragraph first:** [the writer's concession opener] ...
  [their turn word].
- **Enumerated reasons:** [their enumerators]. The last enumerator must be the
  last reason; every later paragraph belongs to a signposted
  counterargument or synthesis section.
- **Counterargument section:** opened with [their counterargument opener].
  Answer at least two counterarguments, including one course reading that
  cuts against the thesis, conceded honestly and answered with that reading's
  own explanation.
- **Synthesis paragraph:** if the thesis has two halves, give the second half
  its own developed paragraph with concrete evidence.
- **Conclusion:** [the writer's conclusion skeleton]. At most one closing
  metaphor.

## 3. Paragraph engine (TEMPLATE: fill with the writer's connectives)

1. Claim or enumerator sentence in the writer's scaffolding.
2. Anchor in a **direct quote** from a primary source or course reading, or a
   concrete case with a number. Prefer the source's own words over paraphrase.
3. Convert numbers ("a drop of about 99 percent in eight years").
4. React with one of the writer's connectives: [list].
5. Close on a restated judgment or a genuine question, at the writer's rate.

At most two events per paragraph, each followed by commentary. A run of
dated events reads as a summary.

## 4. Rewrite on sight (generic off-voice patterns)

- **Abstract paraphrase of a scholar's thesis.** Replace with a concrete
  example or quotation from the reading.
- **Meta-commentary about the essay's own moves:** "makes this point even
  stronger", "To be fair,", "It is worth noting".
- **Short bridge sentences:** "This has happened before." "The numbers tell a
  similar story."
- **Question-and-answer pairs:** "So, what changed things? It was Congress."
- **Aphoristic paragraph endings.**
- **Contrast frames** ("This is not X. It is Y.") more than once per paper.
- **Repeated motif:** the same point made three times. Make it once, where it
  is strongest.
- **Tidy closing generalization** after every paragraph.
- **Informal tone for a college paper:** "basically," "a big hole,"
  contractions outside quotations (unless the writer's register allows them).

## 5. Fingerprint aim points

`voice/profile.json` holds the numbers (`tools/voice/measure.py --write`
measures them from the writer's corpus). The voice gate reports each with the
writer's own rate beside it. Typical checks: "The" and "In" opener share,
"However" openers, "not" per 1,000 words, semicolons per 1,000 words, share of
35+ word sentences, contractions, signature-connective caps, and corpus
overlap of 8+ words (the only hard gate).

## 6. Submission checks

- **Rubric:** a written self-grade against every criterion copied in §1.1,
  naming the paragraph that satisfies it. The "class discussion" item can
  only come from the user; ask.
- **Citations:** `tools/essay/check_citations.js` must report 0 problems. Use
  full notes on first citation and short notes after; short notes are also
  the safest way to recover space when a page limit is tight.
- **Length:** build with `tools/essay/build_docx.js`, then measure with
  `tools/essay/page_check.js` (Word). The body should end in the bottom
  quarter of the last required page. Word's widow control moves two lines at
  a time; if a trim does not move the break, shorten a long footnote on that
  page instead. Trim order: redundant restatements, asides, long footnotes;
  never the thesis support or a counterargument. As a planning figure, about
  285–300 body words per page with Chicago footnotes at 12 pt, double-spaced.
- **Header:** name, instructor, course, date on separate lines, then the
  centered title. Never insert placeholders such as "[Course]"; leave lines
  out and tell the user.
- **Proofread** the whole body once after the last edit: splices from cuts,
  repeated words, dates, pronoun reference, short notes that appear before
  their full note.

## 7. Honesty and stopping

- External "AI detector" labels are noisy: they flip on unchanged text and
  flag bibliography fragments and the writer's own attested sentences. Use
  such labels at most as a pointer to passages that are abstract or
  paraphrase-heavy, revise once, and stop. Never promise or claim a detector
  outcome.
- After two revision passes that do not move a measure, change the approach
  (for example, rebuild around quotations) instead of rewording again.
- Remind the user once that the course's AI-use policy is theirs to check.
