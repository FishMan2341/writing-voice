---
name: academic-essay
description: Write a complete academic essay or research paper in the user's documented voice from an assignment prompt and course readings, in one or two prompts. Use when the user gives a prompt file (.docx/.pdf/pasted), a page or word count, a rubric, or a readings folder/zip and asks for a full essay with citations. Produces a .docx and .pdf with Chicago footnotes, verified quotes, and voice and citation checks.
---

# academic-essay

A one-pass pipeline for course essays. Follow it in order; each step exists
because skipping it cost a revision round in testing. It extends the `voice`
skill; that skill's provenance, personal-facts and honesty rules all apply.

**Setup check:** if `voice/voice-profile.md` is missing or still contains
`TEMPLATE`, the voice has not been set up. Tell the user, and
offer to run the `voice-setup` skill first. You may still run the pipeline;
say in delivery that the prose follows generic academic style, not their voice.

## Plugin paths

Resolve `${CLAUDE_PLUGIN_ROOT}` (or the folder two levels above this file).
Tools live in `tools/essay/`; voice resources in `voice/`. Keep scratch files
in the scratchpad or a working folder, never inside the plugin.

## Read first

1. `voice/academic-register.md` (this pipeline's rules, aim points and checks;
   falls back to `templates/voice/academic-register.md` before setup).
2. `voice/voice-profile.md` (register table), `voice/sentence-skeletons.md`
   (the conceding, enumerating and concluding sections), and the academic
   exemplars listed in `voice/exemplars/README.md`.
3. `voice/imitation-tells.md`, including section D.

## Step 0: intake in the first reply (one round trip)

Extract the prompt: `node tools/essay/extract_docx.js <prompt.docx>`. Then,
in a single message, ask only for what is missing and needed:
- course readings (folder or zip) and syllabus, if not attached;
- course name, instructor and due date for the header;
- any lecture or class-discussion point to include;
- the side the user wants to argue, only if the prompt is two-sided and the
  user has not said.
If the user has already supplied these, skip straight to step 1. If they
decline, proceed and note the gap in delivery.

## Step 1: sources

- Unzip readings into a new empty folder; run `pdftotext -layout` on each
  relevant PDF (poppler). On Windows, very long working-directory paths can
  stop native tools from starting: work from a short folder if that happens.
  Word COM PDF conversion can hang; avoid it.
- Two-column scans read better without `-layout`; keep both versions and
  search either.
- Choose readings that address the prompt's listed topics. Prefer assigned
  readings over outside sources; use primary sources (cases, speeches,
  constitutional text) as anchors.
- Verify every quote and number with `node tools/essay/pgrep.js <txt> "<regex>"`
  and record the printed page. Image-only scans give 0 words: do not cite
  their content as verified.
- Do not quote an author's imagined dialogue as the subject's own words.
- Verify recent cases or events with a web search and say which ones came
  from secondary coverage.

## Step 2: plan (plain notes, no styling)

Thesis that picks a side; roadmap; concession; three to five enumerated
reasons with their anchoring quotes; a counterargument section with two or
more counterarguments, including one reading that cuts against the thesis;
a synthesis paragraph for the thesis's second half; conclusion. Map every
rubric criterion to the paragraph that satisfies it.

## Step 3: draft once, in build markup

Write `essay.txt` in the markup that `tools/essay/build_docx.js` documents
(`#TITLE`, paragraphs with `{{footnote}}` and `*italics*`, `#BIB`). Build
each paragraph with the engine in `academic-register.md` §3. Avoid every
pattern in §4. Size the draft from the planning figure in §6 (about 285–300
body words per page with footnotes).

## Step 4: gates (run all; fix, then re-run)

```
python  tools/essay/voice_gate.py      essay.txt
node    tools/essay/check_citations.js essay.txt
node    tools/essay/build_docx.js --in essay.txt --out <Name>_Essay.docx --name "<Name>" --date "<Date>" [--course ... --instructor ...]
node    tools/essay/page_check.js --docx <Name>_Essay.docx --end "<last words of conclusion>" --pdf
```

- `voice_gate.py`: FAIL is blocking (corpus overlap). WARNs are prompts to
  re-read those sentences; fix them where a fix keeps the meaning.
- `check_citations.js` must report 0 problems.
- `page_check.js`: the body should end in the bottom quarter of the last
  required page. Adjust as in `academic-register.md` §6. Without Word, report
  the length as an estimate.
- Proofread the full body once after the final edit.

## Step 5: deliver

Send the .docx and .pdf. In the reply: the thesis in one line; a rubric
self-grade (criterion → where it is met → any residual risk); sources used,
which were verified against the reading text and which were not; anything
the user must add (course and instructor lines, class-discussion point); and
a one-line reminder that the course's AI-use policy is theirs to check. Do
not claim or predict detector outcomes.

## Step 6: if the user asks for another round

Apply targeted revision only to the passages they flag (`voice` skill,
"Targeted revision" mode), re-run step 4, and stop after two passes that do
not change the result: say so and change the approach rather than
rewording again.
