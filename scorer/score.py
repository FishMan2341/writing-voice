#!/usr/bin/env python3
"""Model-free corpus tools. Python 3 standard library only.

Commands:
  retrieve --genre g [--words 600]     pull real passages from your corpus for a genre
  overlap  --file draft.txt [--n 8]    longest shared word runs between a draft and each corpus file

Both read voice/manifest.json and voice/corpus/*.txt only; no model is loaded.
Use overlap before delivering anything: a run of 8+ words copied from your own
samples is a sign the draft is recycling, not writing.
"""
import argparse
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "voice", "corpus")
MANIFEST = os.path.join(ROOT, "voice", "manifest.json")
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def read_text(path):
    if path in (None, "-"):
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def load_manifest():
    if not os.path.exists(MANIFEST):
        sys.exit("voice/manifest.json is missing: run the voice-setup skill first.")
    with open(MANIFEST, encoding="utf-8") as fh:
        return [r for r in json.load(fh) if not r.get("excluded")]


def cmd_retrieve(args):
    recs = load_manifest()
    picked = [r for r in recs if r.get("genre") == args.genre] if args.genre else recs
    recs = picked or recs
    out, words = [], 0
    for r in recs:
        if words >= args.words:
            break
        path = os.path.join(CORPUS, f"{r['doc_id']}.txt")
        if not os.path.exists(path):
            continue
        paras = [p for p in read_text(path).split("\n\n") if len(p.split()) >= 40][:2]
        if not paras:
            continue
        out.append({"doc_id": r["doc_id"], "genre": r.get("genre"),
                    "source_tier": r.get("source_tier"), "text": "\n\n".join(paras)})
        words += sum(len(p.split()) for p in paras)
    print(json.dumps({"passages": out, "words": words}, indent=1))


def cmd_overlap(args):
    toks = [t.lower() for t in WORD_RE.findall(read_text(args.file))]
    matches = []
    names = sorted(n for n in os.listdir(CORPUS) if n.endswith(".txt")) if os.path.isdir(CORPUS) else []
    for name in names:
        doc = [t.lower() for t in WORD_RE.findall(read_text(os.path.join(CORPUS, name)))]
        sm = difflib.SequenceMatcher(None, toks, doc, autojunk=False)
        best = max(sm.get_matching_blocks(), key=lambda b: b.size, default=None)
        if best and best.size >= args.n:
            matches.append({"doc": name[:-4], "length": best.size,
                            "span": " ".join(toks[best.a:best.a + best.size])[:200]})
    matches.sort(key=lambda m: -m["length"])
    print(json.dumps({"matches": matches[:args.top], "threshold_words": args.n,
                      "corpus_files": len(names)}, indent=1))


def main():
    ap = argparse.ArgumentParser(description="Model-free corpus tools (stdlib only)")
    sub = ap.add_subparsers(required=True)
    q = sub.add_parser("retrieve")
    q.add_argument("--genre")
    q.add_argument("--words", type=int, default=600)
    q.set_defaults(func=cmd_retrieve)
    o = sub.add_parser("overlap")
    o.add_argument("--file")
    o.add_argument("--n", type=int, default=8)
    o.add_argument("--top", type=int, default=5)
    o.set_defaults(func=cmd_overlap)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
