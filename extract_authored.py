#!/usr/bin/env python3
"""Materialize the authored-only training view (voice/corpus_authored/) from
the raw sources (voice/corpus/) using the exact source-span exclusion records
in voice/exclusions.json, then write exact authored word counts to
voice/authored_counts.json.

- Raw sources are read-only; they are never modified.
- Authored word counts are computed ONLY at execution time. Until this script
  runs successfully, authored counts stay pending; no estimates are performed.
- Any disagreement between an exclusion record and the raw source aborts the
  run with a clear error before the counts file is written.

Usage: python3 extract_authored.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(ROOT, "voice", "corpus")
OUT_DIR = os.path.join(ROOT, "voice", "corpus_authored")
EXCL_PATH = os.path.join(ROOT, "voice", "exclusions.json")
MANIFEST_PATH = os.path.join(ROOT, "voice", "manifest.json")
COUNTS_PATH = os.path.join(ROOT, "voice", "authored_counts.json")

# Word token definition used for every count in the package.
WORD_RE = re.compile(r"[^\W_]+(?:['\u2019][^\W_]+)*", re.UNICODE)


def count_words(text):
    return len(WORD_RE.findall(text))


def apply_operations(raw_text, ops, doc_id):
    """Line-level exclusion. Each operation must match exactly its
    expected_count line(s) in the raw source, or the run aborts."""
    lines = raw_text.splitlines()
    for op in ops:
        kind = op.get("op")
        if kind == "drop_line_exact":
            hits = [i for i, ln in enumerate(lines) if ln.strip() == op["text"]]
        elif kind == "drop_line_prefix":
            hits = [i for i, ln in enumerate(lines)
                    if ln.strip().startswith(op["prefix"])]
        else:
            raise ValueError("%s: unknown op %r" % (doc_id, kind))
        if len(hits) != op["expected_count"]:
            raise AssertionError(
                "%s: op %s %r matched %d line(s), expected %d; raw source and "
                "exclusions.json disagree - refusing to write authored view"
                % (doc_id, kind, op.get("text") or op.get("prefix"),
                   len(hits), op["expected_count"]))
        op["_dropped_lines"] = [lines[i] for i in hits]
        drop = set(hits)
        lines = [ln for i, ln in enumerate(lines) if i not in drop]
    body = "\n".join(lines)
    if raw_text.endswith("\n"):
        body += "\n"
    return body


def main():
    exclusions = {}
    if os.path.exists(EXCL_PATH):
        with open(EXCL_PATH, encoding="utf-8") as fh:
            exclusions = json.load(fh)
    with open(MANIFEST_PATH, encoding="utf-8") as fh:
        manifest = json.load(fh)
    os.makedirs(OUT_DIR, exist_ok=True)
    counts = {
        "counting_regex": "[^\\W_]+(?:['\u2019'][^\\W_]+)*",
        "generated_by": "extract_authored.py",
        "status": "counts available; computed at execution time by this script",
        "docs": {},
    }
    for rec in manifest:
        doc_id = rec["doc_id"]
        raw_path = os.path.join(CORPUS, doc_id + ".txt")
        if not os.path.exists(raw_path):
            sys.exit("missing raw source: %s" % raw_path)
        with open(raw_path, encoding="utf-8") as fh:
            raw_text = fh.read()
        ops = exclusions.get("docs", {}).get(doc_id, {}).get("operations", [])
        if ops:
            authored_text = apply_operations(raw_text, ops, doc_id)
        else:
            authored_text = raw_text
        raw_words = count_words(raw_text)
        if rec.get("raw_body_words") is not None and raw_words != rec["raw_body_words"]:
            sys.exit("%s: raw word count %d != manifest raw_body_words %d; "
                     "counting method mismatch - aborting"
                     % (doc_id, raw_words, rec["raw_body_words"]))
        out_path = os.path.join(OUT_DIR, doc_id + ".txt")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(authored_text)
        authored_words = count_words(authored_text)
        counts["docs"][doc_id] = {
            "raw_body_words": raw_words,
            "authored_words": authored_words,
            "ops_applied": [{"op": o["op"],
                             "text": o.get("text") or o.get("prefix"),
                             "dropped_lines": o.get("_dropped_lines", [])}
                            for o in ops],
            "training_eligible": bool(rec.get("training_eligible")),
        }
        print("%s: raw %d -> authored %d words, %d exclusion op(s)"
              % (doc_id, raw_words, authored_words, len(ops)))
    with open(COUNTS_PATH, "w", encoding="utf-8") as fh:
        json.dump(counts, fh, indent=1, ensure_ascii=False)
    print("wrote %s and %d authored-only files (raw sources untouched)"
          % (COUNTS_PATH, len(manifest)))


if __name__ == "__main__":
    main()
