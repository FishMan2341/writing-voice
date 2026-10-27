"""Topic-masked stylometric features for the author-vs-imitator classifier."""
import re, glob, os, json, sys, statistics as st
import numpy as np

FUNC = set("""a about above across after afterwards again against all almost alone along already also although always am among amongst an and another any anybody anyhow anyone anything anyway anywhere are around as at back be became because become becomes becoming been before beforehand behind being below beside besides between beyond both but by can cannot could did do does doing done down due during each either else elsewhere enough even ever every everybody everyone everything everywhere except few first for former formerly from further furthermore had has have having he hence her here hereafter hereby herein hers herself him himself his how however i if in indeed into is it its itself just last latter latterly least less many may me meanwhile might mine more moreover most mostly much must my myself namely neither never nevertheless next no nobody none noone nor not nothing now nowhere of off often on once one only onto or other others otherwise our ours ourselves out over own per perhaps please quite rather really same several she should since so some somebody somehow someone something sometime sometimes somewhere still such than that the their theirs them themselves then thence there thereafter thereby therefore therein thereupon these they this those though through throughout thus to together too toward towards under until up upon us very via was we well were what whatever when whence whenever where whereafter whereas whereby wherein whereupon wherever whether which while whither who whoever whole whom whose why will with within without would yet you your yours yourself yourselves
i'm i'd i've i'll it's that's don't doesn't didn't isn't aren't wasn't weren't won't wouldn't couldn't shouldn't can't there's they're we're you're he's she's let's what's who's
ultimately simply actually certainly particularly especially essentially truly definitely obviously clearly mainly mostly largely likely unlikely merely fully generally typically usually ideally personally initially eventually subsequently previously currently recently fundamentally admittedly notably consequently additionally nonetheless albeit hypothetically ironically arguably undoubtedly seemingly potentially relatively extremely highly somewhat fairly pretty incredibly deeply directly entirely completely
said such like instead despite spite regard regarding opinion belief view experience realm fact case sense terms way extent example instance order able unable thing things people somebody someone anything nothing everything lot kind sort part
believe think feel find agree argue would imagine say suppose suggest seem seems seemed""".split())

TOK = re.compile(r"[A-Za-z]+(?:[’'][A-Za-z]+)?|\d+|[.,;:!?()\"“”/%&-]")

def mask(text):
    out = []
    prev_end = True
    for m in TOK.finditer(text):
        w = m.group(0)
        lw = w.lower().replace('’', "'")
        if re.match(r"[A-Za-z]", w):
            if lw in FUNC:
                out.append(lw)
            elif w[0].isupper() and not prev_end:
                out.append('C')
            else:
                out.append('w' if len(w) <= 4 else ('W' if len(w) <= 8 else 'L'))
            prev_end = False
        elif w.isdigit():
            out.append('0'); prev_end = False
        else:
            out.append({'“': '"', '”': '"'}.get(w, w))
            prev_end = w in '.!?'
    return ' '.join(out)

def sents(t):
    t = re.sub(r'\s+', ' ', t)
    parts = re.split(r'(?<=[.!?])["”’)]?\s+(?=[A-Z“"(])', t)
    return [p for p in parts if len(p.split()) >= 2]

def dense(text):
    ss = sents(text) or [text]
    L = np.array([len(s.split()) for s in ss], float)
    W = re.findall(r"[A-Za-z’']+", text); n = max(len(W), 1)
    lw = [w.lower() for w in W]
    f = [L.mean(), L.std(), np.median(L), (L <= 10).mean(), (L >= 35).mean(),
         text.count(',') / len(ss), 1000 * text.count(';') / n, 1000 * text.count(':') / n,
         1000 * text.count('(') / n, 1000 * text.count('?') / n, 1000 * text.count('/') / n,
         1000 * len(re.findall(r"[A-Za-z][’'](s|d|ve|ll|re|t|m)\b", text)) / n,
         np.mean([len(w) for w in W]) if W else 0, np.mean([len(w) >= 9 for w in W]) if W else 0,
         len(set(lw)) / n]
    return f

def windows(text, target=160, min_words=60):
    ss = sents(text); out, buf, k = [], [], 0
    for s in ss:
        buf.append(s); k += len(s.split())
        if k >= target:
            out.append(' '.join(buf)); buf, k = [], 0
    if buf:
        if out and k < min_words: out[-1] += ' ' + ' '.join(buf)
        else: out.append(' '.join(buf))
    return [w for w in out if len(w.split()) >= min_words]

def clean(text):
    """Strip short field labels at the start of a line (e.g. 'Goals:', 'Broad Topic:') and markdown remnants,
    so worksheet/form labels are not scored as prose."""
    text = re.sub(r'(?m)^(?:\[[^\]\n]{1,60}\]\s*|[A-Z][A-Za-z/&\- ]{1,40}(?:\([^)\n]{0,40}\))?:\s+)', '', text)
    text = re.sub(r'[#*_`>]', '', text)
    return text
