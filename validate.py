"""Standard-library checks for the plugin. Never modifies anything.

usage: python validate.py

Checks syntax of every .py and .json file, skill frontmatter, template
presence, that the model-free tools run, and (when voice/ is set up) that every
manifest record has a corpus file. Exit 1 on any FAIL.
"""
import sys; sys.dont_write_bytecode = True
import ast, json, os, re, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ['voice', 'voice-setup', 'academic-essay', 'unslop', 'ai-writing-signs']
TEMPLATES = ['voice-profile.md', 'sentence-skeletons.md', 'imitation-tells.md', 'personal-facts.md',
             'voice-exceptions.md', 'scoring-contract.md', 'academic-register.md', 'profile.json',
             'manifest.json', 'training_manifest.json', 'exclusions.json', 'exemplars/README.md']
FAILS = []


def report(name, ok, detail=''):
    status = 'SKIP' if ok is None else ('PASS' if ok else 'FAIL')
    if ok is False:
        FAILS.append(name)
    print(f'[{status}] {name}' + (': ' + detail if detail else ''))


def run(*args):
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, env=env,
                          capture_output=True, text=True, encoding='utf-8', timeout=60)


def main():
    skip = {'venv', '.git', 'node_modules'}
    for p in sorted(ROOT.rglob('*.py')):
        if skip & set(p.parts): continue
        try: ast.parse(p.read_text(encoding='utf-8')); report('syntax:' + p.relative_to(ROOT).as_posix(), True)
        except SyntaxError as e: report('syntax:' + p.relative_to(ROOT).as_posix(), False, str(e))
    for p in sorted(ROOT.rglob('*.json')):
        if skip & set(p.parts): continue
        try: json.loads(p.read_text(encoding='utf-8')); report('json:' + p.relative_to(ROOT).as_posix(), True)
        except ValueError as e: report('json:' + p.relative_to(ROOT).as_posix(), False, str(e))
    report('plugin-manifest', json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8')).get('name') == 'writing-voice')
    for s in SKILLS:
        t = (ROOT / 'skills' / s / 'SKILL.md').read_text(encoding='utf-8')
        front = t.split('---', 2)[1] if t.startswith('---') else ''
        report('frontmatter:' + s, bool(re.search(r'^name: ' + re.escape(s) + r'\s*$', front, re.M)
                                        and re.search(r'^description:\s*\S', front, re.M)))
    for f in TEMPLATES:
        report('template:' + f, (ROOT / 'templates' / 'voice' / f).is_file())

    with tempfile.TemporaryDirectory() as td:
        sample = Path(td) / 'draft.txt'
        sample.write_text('#TITLE A test\nIt is true that this is a test. However, it is short.\n', encoding='utf-8')
        r = run('scorer/score.py', 'overlap', '--file', sample)
        report('overlap-runs', r.returncode == 0 and '"matches"' in r.stdout, r.stderr.strip()[-200:])
        r = run('tools/essay/voice_gate.py', sample)
        report('voice-gate-runs', r.returncode in (0, 1) and 'off-voice phrases' in r.stdout, r.stderr.strip()[-200:])
    r = run('scorer-stylo/tools/escore.py', 'x.txt')
    report('ensemble-guard', r.returncode != 0 and 'REFUSED' in (r.stderr + r.stdout))

    man = ROOT / 'voice' / 'manifest.json'
    if man.is_file():
        recs = json.loads(man.read_text(encoding='utf-8'))
        missing = [r['doc_id'] for r in recs if not (ROOT / 'voice' / 'corpus' / f"{r['doc_id']}.txt").is_file()]
        report('corpus-files', not missing, f'missing {missing}' if missing else f'{len(recs)} documents')
        tiers = {r.get('source_tier') for r in recs}
        report('tiers-valid', tiers <= {'primary', 'review', 'review_ai_edit_reported'}, str(sorted(map(str, tiers))))
    else:
        report('voice-setup', None, 'voice/ not set up yet (run the voice-setup skill)')
    print(f'\n{len(FAILS)} failure(s)')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
