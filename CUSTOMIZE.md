# Make it your voice

The plugin ships empty on purpose. These steps take one session of about an
hour with Claude Code (or any agent that can read files and run Python).
The `voice-setup` skill does the work; this page tells you what to bring and
what to check.

## 1. Gather your writing

Put 5–15 pieces you wrote in one folder. Aim for 6,000+ words in total.

- **Pick pieces that are really yours.** For each one, know whether you wrote
  it alone, with editing help, or with AI help. Mixed pieces are still useful,
  but they get a lower trust tier.
- **Cover the genres you want help with.** Essays, op-eds, cover letters,
  speeches, emails. Two or more per genre is better than one.
- **Include old and new work** only if you say which is which; voices change.
- **Leave the typos in.** They are evidence; the plugin never reproduces them.

Optional: a short list of facts drafts may use (school, job, experiences),
phrases you overuse, and words you would never write.

## 2. Run the setup skill

Start Claude Code with the plugin loaded and say:

```
/writing-voice:voice-setup My samples are in <folder>. <Anything about which
pieces I wrote alone, which had help, and which are old.>
```

The agent will:

1. copy `templates/voice/` into `voice/`;
2. save each sample as `voice/corpus/NNN.txt` and record it in
   `voice/manifest.json` with genre, date, family and trust tier;
3. **stop and show you the manifest** (checkpoint 1) so you can fix tiers;
4. measure your rates (`tools/voice/measure.py`) and read every sample;
5. write `voice-profile.md`, `sentence-skeletons.md`, `exemplars/`,
   `imitation-tells.md`, `voice-exceptions.md`, `personal-facts.md` and
   `profile.json`, quoting your own sentences with doc IDs;
6. **test itself** (checkpoint 2): rewrite a paragraph of yours from a generic
   version and ask you what sounds wrong.

## 3. Check its work

Open these and correct anything that is not you:

- `voice/voice-profile.md` section 0: the habits that matter most. If it
  names a habit you do not recognize, ask which sentences it came from.
- `voice/personal-facts.md`: delete anything you do not want used.
- `voice/profile.json`: add your signature phrases to `signatures` (with a
  per-piece cap) and words you never use to `off_voice`.

Then run `python validate.py`. It should report 0 failures.

## 4. Use it

```
/writing-voice:voice Draft a 600-word op-ed arguing <position>. Facts: <...>
/writing-voice:voice Rewrite this in my voice, keeping every fact: <paste>
/writing-voice:academic-essay Write the paper in <prompt.docx>. Readings: <Readings.zip>.
  Course: <name>, Instructor: <name>, due <date>. Argue <side>.
```

Every time you tell it "that doesn't sound like me," the agent should add a
line to `voice/imitation-tells.md` or `voice/voice-exceptions.md`. The
profile gets better the more you correct it.

## 5. Keep it current

Add new pieces to your samples folder and say `/writing-voice:voice-setup
I added three new essays`; it re-runs steps 2–5 without starting over.

## Optional: train the classifier

If you want a numeric "how much like me" score, follow
[scorer-stylo/README.md](scorer-stylo/README.md). You will generate AI
imitations of your own assignments as negatives and train on your machine.
It needs numpy, scipy and scikit-learn, and at least two independent
assignment families. It is useful for ranking drafts of the same piece, not
for proving anything.

## Sharing your fork

`voice/` and generated training data are git-ignored, so you can fork and push
improvements to the code and skills without publishing your writing. Check
`git status` before every push anyway.
