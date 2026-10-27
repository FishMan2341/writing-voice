# AI-writing signs catalog (essay edition)

Source: Wikipedia:Signs of AI writing, pinned revision 1375746757 (edited
2026-09-19, read 2026-09-20):
https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1375746757

The source page is advice, not policy, and carries an update notice for recent
models. Status labels below preserve the source's own distinctions:

- **current**: observed in current model output; useful as a review cue.
- **weakening**: still listed but noted as less common in newer output.
- **historical**: characteristic of older models; weak evidence today.
- **ineffective**: explicitly listed by the source as not diagnostic.

A sign is a reason to look closer, never proof of AI authorship. One sign alone
means little; clusters of current signs in the same passage are the signal.
False positives are common in formal, technical, or non-native English writing.
Adaptations for essays are marked "essay adaptation"; everything else is
paraphrased from the source. No sign from other websites or the unslop skill is
added here.

## Content

| ID | Sign | Status | Essay check and repair |
|---|---|---|---|
| C1 | Undue emphasis on significance, legacy, broader trends ("stands as", "testament to", "pivotal moment", "evolving landscape", "indelible mark") | current | Find importance claims with no analysis; replace with a specific consequence the evidence supports. |
| C2 | Canned emphasis on notability, attribution, media coverage ("profiled in", "recognized by", name-dropping outlets without context) | current | Pick one source, state what it actually says, or cut. |
| C3 | Superficial analyses via trailing "-ing" phrases ("highlighting", "underscoring", "reflecting", "ensuring", "fostering", "contributing to") | current | Delete the participle or expand it into a claim with evidence. |
| C4 | Promotional or advertisement-like language ("vibrant", "nestled", "breathtaking", "groundbreaking", "renowned", "must-visit") | current | Replace with neutral description. |
| C5 | Vague attributions and overgeneralization ("experts argue", "industry reports suggest", "some critics", "several sources" with one citation) | current | Name the source and its actual claim, or remove. |
| C6 | Outline-like conclusions about challenges and future prospects ("Despite these challenges... continues to thrive", "the future looks bright") | current | End on the specific argument or evidence instead of a template resolution. |
| C7 | Essay adaptation: teacher-prompt residue. The answer restates or answers the assignment question in the opening instead of starting from the argument. | essay adaptation | Open with the claim or scene; let the prompt be implied. |

## Language and grammar

| ID | Sign | Status | Essay check and repair |
|---|---|---|---|
| L1 | High density of "AI vocabulary": align with, boasts, bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adj), landscape (abstract), meticulous, pivotal, showcase, tapestry, testament, underscore, vibrant | current | Keep at most one if it is the precise word; otherwise use the plain word. Density matters more than any single word. |
| L2 | Avoidance of basic copulatives: "serves as", "stands as", "represents", "functions as", "boasts", "features", "offers" instead of is/has | current | Prefer "is" or "has" unless the substitute adds meaning. |
| L3 | Vague expression of connection or association: "in connection with", "associated with", "connected to" instead of stating the relationship | current | State who did what: "X taught at Y", not "X was connected with Y". |
| L4 | Negative parallelisms: "not just X, but Y", "not only... but also", "it is not X, it is Y" | current | State the point directly without the contrast frame. |
| L5 | Rule of three: adjective triplets, three-item lists used as a flourish rather than because there are three things | current | Use the natural number; two or four is fine. |
| L6 | Essay adaptation: formulaic transitions at sentence start ("Additionally", "Moreover", "Furthermore", "Consequently", "Notably") in clusters. | weakening / weak tell | The source lists transition words in isolation as ineffective. Only treat a dense cluster of them as a cue, and check the writer's own habits first (check the author's documented habits in voice/voice-profile.md first). |

## Style and formatting

| ID | Sign | Status | Essay check and repair |
|---|---|---|---|
| S1 | Title Case headings | current | Use sentence case. |
| S2 | Headings that only contain other headings; skipped heading levels | current | Restructure; in essays, remove headings entirely unless the assignment wants them. |
| S3 | Overuse of boldface for emphasis or "key takeaway" labels | current | Remove bold from prose; bold only genuinely new terms if the format requires it. |
| S4 | Inline-header vertical lists: a bold label and colon that restates the line ("**Performance:** Performance improved...") | current | Convert to prose; a bold lead-in is acceptable only when it names the item and the rest is new detail. |
| S5 | Overuse of em dashes, especially spaced em dashes used to punch up clauses | weakening (source note: less common in recent output) | Preserve the author's documented dash usage where it serves the sentence; match the requested register. |
| S6 | Emoji as formatting, including in headings and bullets | current | Remove. |
| S7 | Unusual use of tables for what should be prose | current | Use prose for arguments. |
| S8 | Curly quotation marks and apostrophes in plain text | current | Curly quotes alone prove nothing (word processors auto-convert). Match the document's convention and keep it consistent. |
| S9 | Thematic breaks (`----`, `***`) between sections in prose output | current | Remove in essays. |
| S10 | Markdown formatting leaking into a document that should be plain prose (heading hashes, bold markers, bullet syntax) | current | Strip all markup; deliver plain prose. |

## Communication artifacts

| ID | Sign | Status | Essay check and repair |
|---|---|---|---|
| M1 | Collaborative/chatbot phrasing: "I hope this helps", "Of course!", "Certainly!", "Let me know if...", "Here is a...", "Would you like..." | current | Delete; it is conversation, not essay text. |
| M2 | Knowledge-cutoff disclaimers and speculation about missing sources ("While specific details are limited...", "As of my last update") | current | Find the source or drop the claim. |
| M3 | Phrasal templates and placeholder text ("[Describe the specific section]", "I hope this message finds you well") | current | Fill or delete; check for leftover brackets. |
| M4 | Prompt refusal residue ("As an AI language model, I cannot...") | historical | Remove; rewrite the passage. |

## Citations and markup

| ID | Sign | Status | Essay check and repair |
|---|---|---|---|
| R1 | Broken or dead external links, especially several at once | current | Verify every URL; replace or remove. |
| R2 | Invalid DOIs/ISBNs, DOIs pointing at unrelated work | current | Verify identifiers resolve to the cited work. |
| R3 | Book citations without page numbers or URLs | current | Add locators or drop the citation. |
| R4 | Incorrect or unconventional reference style: re-use syntax wrong, sources that do not support the sentence, formatting unlike the rest of the document | current | Fix style; check that each source supports its claim. |
| R5 | `utm_source=` and other tracking parameters in URLs | current | Strip tracking parameters. |

## Historical indicators (weak evidence today)

- Didactic disclaimers: "it's important to note/remember/consider", "worth noting", "may vary" (2022-2024 models).
- Section summaries: "In summary", "In conclusion", "Overall" closing every section.
- Prompt refusals and abrupt cut-offs mid-generation.
- Outdated access-date parameters in citations.
- Lexical diversity/elegant variation: avoiding repeating a word by cycling synonyms (protagonist, main character, central figure). Older models with repetition penalties did this.

## Ineffective indicators (source says these do NOT indicate AI)

Perfect grammar; mixed casual and formal register; "bland" or "robotic" prose;
formal or academic prose; transition words in isolation; unsourced content;
correct markup; bizarre markup that looks like editor bugs.

## Human-writing signs to preserve

- Text that predates November 2022 cannot be AI-generated.
- A writer can explain their editorial choices and mistakes.
- Human syntax: simple "is/has" phrases, plain verbs (wrote, moved, used,
  tried, died), superlatives and definitive statements, hedging, and
  inconsistency where a person would naturally vary. The source notes these
  are more common in human writing than in AI text.

## How to audit a draft

1. Read once for meaning and argument; do not count signs yet.
2. Flag spans, not documents: each flag needs the span, the sign ID, and why.
3. Repair the smallest span that removes the sign without changing meaning.
4. Never output an "AI probability" from rule counts.
5. Re-read after repair: removing signs must not flatten the author's documented voice
   (see voice/voice-exceptions.md at the package root; em dashes stay banned).
