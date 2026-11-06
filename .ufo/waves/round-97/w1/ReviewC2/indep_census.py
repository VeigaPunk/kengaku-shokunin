#!/usr/bin/env python3
"""ReviewC2 independent census — no instrument code imported; parser, detector and
diff logic re-derived. Prints the facts cited in .ufo/waves/round-97/w1/ReviewC2.md."""
import subprocess, re, collections

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
T = "f1083da60e7ff6b88f7420aae7424f7762d14700"

def blob(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None

SPLIT = re.compile(r"(?<!\\)\|")
def registry(rev):
    lines = blob(rev, "SKILL.md").decode(errors="replace").split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith("## Gate/probe registry")]
    rows = []
    for line in lines[starts[0] + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("| `"):
            rows.append([c.strip() for c in SPLIT.split(line.strip())[1:-1]])
    return rows

b, t = registry(BASE), registry(T)
bt, tt = {r[0]: r for r in b}, {r[0]: r for r in t}
kb, kt = collections.Counter(r[1] for r in b), collections.Counter(r[1] for r in t)
removed = [n for n in bt if n not in tt]
added = [n for n in tt if n not in bt]
kind_only, other = [], []
for n, r in bt.items():
    if n in tt:
        rr = tt[n]
        d = [i for i in range(max(len(r), len(rr))) if (r[i] if i < len(r) else None) != (rr[i] if i < len(rr) else None)]
        (kind_only if d == [1] and r[1] == "gate" and rr[1] == "probe" else other).append((n, d) if other is not None else n)
# (recompute cleanly to avoid aliasing)
kind_only = [n for n, r in bt.items() if n in tt and
             [i for i in range(max(len(r), len(tt[n]))) if (r[i] if i < len(r) else None) != (tt[n][i] if i < len(tt[n]) else None)] == [1]
             and r[1] == "gate" and tt[n][1] == "probe"]
other = [(n, [i for i in range(max(len(r), len(tt[n]))) if (r[i] if i < len(r) else None) != (tt[n][i] if i < len(tt[n]) else None)], r[1], tt[n][1])
         for n, r in bt.items() if n in tt and n not in kind_only and
         [i for i in range(max(len(r), len(tt[n]))) if (r[i] if i < len(r) else None) != (tt[n][i] if i < len(tt[n]) else None)]]
print(f"rows BASE={len(b)} T={len(t)} kinds BASE={dict(kb)} T={dict(kt)}")
print(f"removed={removed} added={added}")
print(f"kind_only gate->probe n={len(kind_only)}")
print(f"other_cell_diffs n={len(other)} {other[:5]}")
SPELL = [re.compile(p) for p in (
    r"add_argument\(\s*[\"']--self-?test[\"']", r"add_parser\(\s*[\"']self-?test[\"']",
    r"[\"']--self-?test[\"']\s*(?:in|==|not in)\b", r"(?:\bin|==)\s*\(?[\"']--self-?test[\"']",
    r"def run_selftest\b", r"(?:==|\bin)\s*\(?[\"']self-?test[\"']")]
BROAD = re.compile(r"self.?test", re.I)
SCRIPT = re.compile(r"([\w./-]+\.(?:py|sh|mjs))")
def scan(rev, s):
    body = blob(rev, s)
    if body is None:
        return None, [], []
    txt = body.decode(errors="replace").split("\n")
    return body, [(i, ln) for i, ln in enumerate(txt, 1) if any(p.search(ln) for p in SPELL)], \
           [(i, ln) for i, ln in enumerate(txt, 1) if BROAD.search(ln)]
tg = [r for r in t if r[1] == "gate"]
bad = []
for r in tg:
    m = SCRIPT.search(r[2]) if len(r) > 2 else None
    s = m.group(1) if m else None
    body, hits, _ = scan(T, s) if s else (None, [], [])
    if body is None or not hits:
        bad.append((r[0], s, "absent" if body is None else "no-code-hit"))
print(f"T gates={len(tg)} gates_without_code_hit={bad}")
sup = []
for n in kind_only:
    m = SCRIPT.search(bt[n][2]); s = m.group(1) if m else None
    _, hits, broad = scan(BASE, s) if s else (None, [], [])
    if hits:
        sup.append((n, "DETECTOR-HIT-AT-BASE"))
print(f"retyped n={len(kind_only)} detector_false_negatives={sup}")
ext = []
for n in kind_only:
    m = SCRIPT.search(bt[n][2]); s = m.group(1) if m else None
    _, hits, broad = scan(BASE, s) if s else (None, [], [])
    if broad:
        ext.append((n, s, [ln.strip()[:80] for _, ln in broad[:2]]))
print(f"retyped with non-detector selftest-ish mentions (adjudicated: other-tool refs/prose): n={len(ext)}")
for x in ext:
    print("  ", x)
for n in added:
    rr = tt[n]; m = SCRIPT.search(rr[2])
    _, hits, _ = scan(T, m.group(1)) if m else (None, [], [])
    print(f"added {n} kind={rr[1]} script={m.group(1) if m else None} code_hits={len(hits)}")
