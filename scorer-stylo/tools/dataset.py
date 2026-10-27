"""Dependency-free eligibility enforcement for the author dataset."""
import os, json
from paths import PKG, MANIFEST
TRAINING_MANIFEST = os.path.join(PKG, "voice", "training_manifest.json")
CORPUS_AUTHORED = os.path.join(PKG, "voice", "corpus_authored")

def _positive_files():
    """Returns list of (doc_id, family_id, path). Every eligible record must
    exist on disk, appear in voice/manifest.json, and agree on family."""
    if not os.path.exists(TRAINING_MANIFEST):
        raise RuntimeError(
            "voice/training_manifest.json is missing. Training requires "
            "an explicit eligibility manifest; refusing to fall back to the raw corpus.")
    with open(TRAINING_MANIFEST, encoding="utf-8") as fh:
        recs = json.load(fh)
    if not isinstance(recs, list):
        raise RuntimeError("voice/training_manifest.json is invalid: not a JSON list")
    if any(not isinstance(r, dict) for r in recs):
        raise RuntimeError("training manifest records must be objects")
    elig = [r for r in recs if r.get("training_eligible") is True]
    if not elig:
        raise RuntimeError(
            "voice/training_manifest.json marks no document as training_eligible")
    with open(MANIFEST, encoding="utf-8") as fh:
        main_man = {d["doc_id"]: d for d in json.load(fh)}
    files = []
    seen = set()
    for r in elig:
        for key in ("doc_id", "family_id", "file"):
            if key not in r:
                raise RuntimeError(f"training manifest record missing {key!r}: {r!r}")
        did = r["doc_id"]
        if did in seen:
            raise RuntimeError(f"duplicate training document: {did}")
        seen.add(did)
        if not main_man.get(did, {}).get("training_eligible", False):
            raise RuntimeError(f"document {did} is not eligible in voice/manifest.json")
        path = r["file"]
        if not os.path.isabs(path):
            path = os.path.join(PKG, path)
        expected = os.path.realpath(os.path.join(CORPUS_AUTHORED, did + ".txt"))
        if os.path.realpath(path) != expected:
            raise RuntimeError(f"training file for {did} must be its authored corpus file")
        if not os.path.exists(path):
            raise RuntimeError(f"training manifest references missing file: {path}")
        if did not in main_man:
            raise RuntimeError(f"training manifest doc {did} absent from voice/manifest.json")
        if main_man[did].get("family_id") != r["family_id"]:
            raise RuntimeError(
                f"training manifest family for {did} ({r['family_id']!r}) disagrees "
                f"with voice/manifest.json ({main_man[did].get('family_id')!r})")
        files.append((did, r["family_id"], path))
    return files

