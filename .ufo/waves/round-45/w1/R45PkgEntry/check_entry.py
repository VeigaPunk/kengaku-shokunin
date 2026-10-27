#!/usr/bin/env python3
"""Local self-check of the R45PkgEntry draft against the frozen C2 counter's own regexes and DECISIVE table.
Reads the lane read-only; writes nothing outside this scratch dir."""
import importlib.util, json, pathlib, re, sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
ENTRY = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("c2", LANE / "plans/round45_c2_verify.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

specj = json.loads((LANE / "plans/pkg-spec-r45.json").read_text())
entry = ENTRY.read_text()
tags, frozen_ids = m.dry(LANE)
print("dry: tags=%d cases=%d" % (len(tags), len(frozen_ids)))

# --- synthesize the receipt rows the dry table freezes (predicted only; observed=predicted) ---
rows = []
for line in (LANE / "corpus/evidence/round45/password-recovery-dry-cases-freeze.txt").read_text().splitlines():
    mm = re.match(r"^CASE (\S+) predicted=(pass|fail) tests=([PF-]+) violates=(\S*) end=(\S+) ", line)
    if mm:
        rows.append(mm.groups())
print("frozen rows=%d" % len(rows))

# --- V9: case table equality ---
want = [(cid, tests, pred) for cid, pred, tests, _v, _e in rows]
sec = re.search(r"^## Case table\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
got = [m.CASE_ROW.match(l).groups() for l in sec.group(1).splitlines() if m.CASE_ROW.match(l)] if sec else []
print("V9 case_rows=%d/%d equal=%s" % (len(got), len(want), got == want))
if got != want:
    for g, w in zip(got, want):
        if g != w:
            print("  MISMATCH got=%r want=%r" % (g, w))
body = "\n".join(l for l in entry.splitlines() if not l.startswith("source:"))
missing = [sid for sid in specj["rows"] if sid not in body]
print("V9 body row ids absent=%r" % (missing,))

# --- V10: mechanism rows ---
order = [cid for cid, *_ in rows]
sec = re.search(r"^## Mechanism\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
raw = [l for l in sec.group(1).splitlines() if l.startswith("|") and "`" in l and "“" in l]
got = [m.MECH_ROW.match(l).groups() if m.MECH_ROW.match(l) else None for l in raw]
unparsed = [l for l, g in zip(raw, got) if g is None]
parsed = [g for g in got if g]
print("V10 mech rows parsed=%d/%d unparsed=%d" % (len(parsed), len(raw), len(unparsed)))
for l in unparsed:
    print("  UNPARSED %r" % l[:100])
bad = []
if [g[0] for g in parsed] != order:
    bad.append("ids differ")
capdir = LANE / m.CAP
for cid, cap, line, quote in parsed:
    allowed = m.DECISIVE.get(cid, {}).get(cap, ())
    if int(line) not in allowed:
        bad.append("%s:%s:%s not decisive (allowed=%r)" % (cid, cap, line, allowed)); continue
    if cap not in m.CAPTURES or m.sha256(capdir / cap) != m.CAPTURES[cap]:
        bad.append("%s:%s capture not pinned" % (cid, cap)); continue
    lines = (capdir / cap).read_text().splitlines()
    q = m.norm(quote)
    if len(q.split()) < 2 or int(line) > len(lines) or q not in m.norm(lines[int(line) - 1]):
        bad.append("%s:%s:%s quote not on line" % (cid, cap, line))
print("V10 bad=%r" % (bad,))

# --- V7: requirement map ---
parsed_cases = {cid: (pred, set(v.split(",")) - {""}) for cid, pred, _t, v, _e in rows}
sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
vbad, seen = [], {}
for l in sec.group(1).splitlines():
    mm = m.MAP_ROW.match(l)
    if not mm:
        if l.startswith("|") and "instruction.md:" in l:
            vbad.append("unparsed %r" % l[:60])
        continue
    line, tag, label, rest = mm.groups()
    seen[tag] = seen.get(tag, 0) + 1
    if tag not in tags:
        vbad.append("%s not frozen" % tag); continue
    if tags[tag] != "instruction.md:%s" % line:
        vbad.append("%s wrong line %s" % (tag, line)); continue
    viol = {cid: obs for cid, (obs, v) in parsed_cases.items() if tag in v}
    if not viol:
        vbad.append("%s no violator" % tag); continue
    want_label = m.derive(set(viol.values()))
    if label != want_label:
        vbad.append("%s labelled %s derived %s" % (tag, label, want_label))
    cited = re.findall(r"`([a-z0-9_-]+)`", rest)
    if not cited or any(c not in viol for c in cited):
        vbad.append("%s cites missing/non-violator %r" % (tag, cited))
miss = sorted(set(tags) - set(seen))
dup = sorted(t for t, n in seen.items() if n > 1)
print("V7 rows=%d tags=%d missing=%r dup=%r bad=%r" % (sum(seen.values()), len(tags), miss, dup, vbad))

# --- V11 predictor: section parse + lint + the 48-state agreement (needs bwrap; run if allowed) ---
sec = m.PRED_SECTION.search(entry)
blocks = m.PRED_BLOCK.findall(sec.group(1)) if sec else []
print("V11 blocks=%d lint=%r bytes=%r" % (len(blocks), m.lint_block(blocks[0]) if blocks else "no block",
                                          len(blocks[0].encode()) if blocks else 0))
if blocks and not m.lint_block(blocks[0]):
    # pure-python cross-check of the block against an emulation of the two test functions (no bwrap needed
    # for THIS cross-check; the counter's own bwrap run is the authority)
    ns = {}
    exec(compile(blocks[0], "predictor", "exec"), ns)
    ANSWER = "8XDP5Q2RT9ZK7VB3BV4WW54"
    def grade(text):
        if text is None:
            return False
        # Path.read_text(): universal newlines + utf-8
        guesses = text.replace("\r\n", "\n").replace("\r", "\n").strip().split("\n")
        return ANSWER in guesses
    st = m.states(ANSWER)
    dis = [(k, grade(t), ns["predict"](t)) for k, t in st if grade(t) != ns["predict"](t)]
    npass = sum(grade(t) for _k, t in st)
    print("V11 states=%d grader_pass=%d grader_fail=%d disagree=%d %r" %
          (len(st), npass, len(st) - npass, len(dis), dis[:4]))
