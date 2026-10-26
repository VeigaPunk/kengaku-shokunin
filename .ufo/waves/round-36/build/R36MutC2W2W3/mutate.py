#!/usr/bin/env python3
"""R36MutC2W2W3 — mutation harness for C2 checks W2/W3 (plans/round36_c2_verify.py).

Installs a passing C2 package in the fixture lane, proves the baseline (checks=6
defects=0), then applies mutants ONE AT A TIME to corpus/SOURCES.md (W2) or
corpus/knowledge/tb2-regex-log-grader.md (W3), runs the counter, restores exact
bytes, and asserts restoration by sha256. Every replacement asserts uniqueness.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
ROWS_FILE = pathlib.Path(sys.argv[2])
ENTRY_FILE = pathlib.Path(sys.argv[3])
FLEET = pathlib.Path("/home/vgpnk/Projects/shokunin")
SOURCES = LANE / "corpus/SOURCES.md"
ENTRY = LANE / "corpus/knowledge/tb2-regex-log-grader.md"
README = LANE / "corpus/README.md"
CENSUS = FLEET / "scripts/sources-census.sh"

ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run_counter():
    r = subprocess.run(["python3", "plans/round36_c2_verify.py", "--lane", "."],
                       cwd=LANE, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode

def defect_lines(out):
    return [l for l in out.splitlines() if "DEFECT" in l] or ["(none)"]

# ---------------------------------------------------------------- install ----
def install_package():
    rows = ROWS_FILE.read_text().rstrip("\n").splitlines()
    assert len(rows) == 3 and all(ROW_RE.match(r) for r in rows), "rows draft malformed"
    text = SOURCES.read_text()
    assert "S108" not in text, "S108 already present"
    lines = text.splitlines(keepends=True)
    at = next(i for i, l in enumerate(lines) if l.startswith("## Paths"))
    lines[at:at] = [r + "\n" for r in rows]
    SOURCES.write_text("".join(lines))
    ENTRY.write_text(ENTRY_FILE.read_text())
    rd = README.read_text()
    idx_anchor = next(l for l in rd.splitlines(keepends=True)
                      if l.startswith("| `knowledge/tb2-protein-assembly-grader.md` |"))
    new_row = ("| `knowledge/tb2-regex-log-grader.md` | One Terminal-Bench 2.0 task grader read and "
               "executed offline: `regex-log`'s single pytest function scores a binary reward against a "
               "fixed 25-line log; six requirement classes pass while violated (S108, S109, S110) |\n")
    assert rd.count(idx_anchor) == 1
    rd = rd.replace(idx_anchor, idx_anchor + new_row, 1)
    cov_anchor = next(l for l in rd.splitlines(keepends=True)
                      if l.startswith("- **Terminal-Bench 2.0 task grader (one task)**"))
    assert rd.count(cov_anchor) == 1
    bullet = ("- **Terminal-Bench 2.0 task grader (second task)**: regex-log read and executed offline "
              "(round 36, 2026-10-25) — knowledge/tb2-regex-log-grader.md\n")
    rd = rd.replace(cov_anchor, cov_anchor + bullet, 1)
    README.write_text(rd)

def census_rows():
    r = subprocess.run([str(CENSUS), "census", "--file", str(SOURCES)],
                       capture_output=True, text=True)
    m = re.search(r"^file\trows\t(\d+)$", r.stdout, re.M)
    return m.group(1) if m else f"no-row-line exit={r.returncode}"

# ------------------------------------------------------------ mutate/run ----
P0_SOURCES, P0_ENTRY, P0_README = None, None, None

def apply(name, target, replacements, extra=None):
    """replacements: list of (old, new) exact strings, each unique in the file.
    extra: optional fn(lines) -> lines for structural mutants."""
    global P0_SOURCES, P0_ENTRY, P0_README
    p = {"S": SOURCES, "E": ENTRY, "R": README}[target]
    pre = sha(p)
    assert pre == {"S": P0_SOURCES, "E": P0_ENTRY, "R": P0_README}[target], f"{name}: file not pristine pre-mutant"
    t = p.read_text()
    for old, _new in replacements:
        assert t.count(old) == 1, f"{name}: old string count={t.count(old)} (want 1): {old[:70]!r}"
    for old, new in replacements:
        t = t.replace(old, new, 1)
    if extra is not None:
        t = "".join(extra(t.splitlines(keepends=True)))
    p.write_text(t)
    out, rc = run_counter()
    p.write_bytes({"S": P0_SOURCES_bytes, "E": P0_ENTRY_bytes, "R": P0_README_bytes}[target])
    post = sha(p)
    assert post == pre, f"{name}: RESTORATION FAILED {pre} -> {post}"
    print(f"\n== {name} (target={'SOURCES.md' if target=='S' else 'entry.md' if target=='E' else 'README.md'})")
    print(f"   pre-sha  {pre}")
    for l in defect_lines(out):
        print(f"   {l}")
    print(f"   exit={rc} summary={out.splitlines()[-2] if len(out.splitlines())>=2 else out}")
    print(f"   post-sha {post}  restored={'YES' if post == pre else 'NO'}")
    verdict = "killed" if rc != 0 else "SURVIVED"
    print(f"   verdict: {verdict}")
    return name, target, pre, post, rc, verdict, defect_lines(out)

# ------------------------------------------------------------------ main -----
install_package()
out, rc = run_counter()
print("=== BASELINE (pristine + package installed)")
print(out)
print(f"exit={rc}")
assert rc == 0, "BASELINE FAILS — mutants would be inconclusive"
P0_SOURCES_bytes = SOURCES.read_bytes(); P0_SOURCES = sha(SOURCES)
P0_ENTRY_bytes = ENTRY.read_bytes();   P0_ENTRY = sha(ENTRY)
P0_README_bytes = README.read_bytes(); P0_README = sha(README)
print(f"pristine shas: SOURCES={P0_SOURCES} ENTRY={P0_ENTRY} README={P0_README}")

src = SOURCES.read_text()
lines = src.splitlines(keepends=True)
def row_line(rid):
    hits = [l for l in lines if ROW_RE.match(l) and ROW_RE.match(l).group(1) == rid]
    assert len(hits) == 1
    return hits[0].rstrip("\n")
S108, S109, S110 = row_line("S108"), row_line("S109"), row_line("S110")
def cells(row): return [c.strip() for c in row.strip().strip("|").split("|")]
URL108 = f"/{PIN}/regex-log/tests/test_outputs.py"
USED = "corpus/knowledge/tb2-regex-log-grader.md"
SECOND = next((LANE / "corpus/knowledge").glob("benchmark-grader-semantics.md"))
assert SECOND.is_file(), "second used-by path missing on disk"

results = []
# --- W2 mutants (corpus/SOURCES.md) ---
results.append(apply("M01 row with 10 cells (recheck cell removed)", "S",
    [(S108, S108.replace(" 2026-10-25 | 180d |", " 2026-10-25 |"))]))
results.append(apply("M02 escaped backslash-pipe in teaches cell", "S",
    [(S108, S108.replace("one pytest function", r"one pytest function \| single", 1))
     if "one pytest function" in S108 else
     (S108, S108.replace("the task score is one pytest", r"the task score is one pytest \| x", 1))]))
results.append(apply("M03 /tasks/ segment in URL", "S", [(S108, S108.replace(URL108, f"/{PIN}/tasks/regex-log/tests/test_outputs.py"))]))
results.append(apply("M04 #L fragment on URL", "S", [(S108, S108.replace(URL108 + " |", URL108 + "#L87 |"))]))
results.append(apply("M05 tier B", "S", [(S108, S108.replace("| code | A |", "| code | B |"))]))
results.append(apply("M06 status queued", "S", [(S108, S108.replace("| mined | 2026-10-25 |", "| queued | 2026-10-25 |"))]))
results.append(apply("M07 used-by with second path", "S",
    [(S108, S108.replace(USED + " |", USED + ", " + SECOND.relative_to(LANE).as_posix() + " |"))]))
def s108_index(ls):
    return next(i for i, l in enumerate(ls) if l.startswith("| S108 |"))
results.append(apply("M08 duplicate S108 row", "S", [],
    extra=lambda ls: ls[:s108_index(ls) + 1] + [S108 + "\n"] + ls[s108_index(ls) + 1:]))
results.append(apply("M09a row indented 4 spaces (only copy)", "S", [(S108, "    " + S108)]))
print(f"   ROW_RE sees indented row: {bool(ROW_RE.match('    ' + S108))} (documenting invisibility)")
results.append(apply("M09b genuine row + 4-space indented duplicate", "S", [],
    extra=lambda ls: ls[:s108_index(ls) + 1] + ["    " + S108 + "\n"] + ls[s108_index(ls) + 1:]))
results.append(apply("M10 two rows with identical teaches", "S",
    [(S109, S109.replace(cells(S109)[6], cells(S108)[6]))]))
results.append(apply("M11 teaches of 7 words", "S",
    [(S110, S110.replace(cells(S110)[6], "four operating rules beyond matching: last date wins"))]))

# --- W3 mutants (entry) ---
ent = ENTRY.read_text()
ent_lines = ent.splitlines(keepends=True)
qrows = [i for i, l in enumerate(ent_lines) if l.startswith("| ") and "“" in l and re.search(r"`test_outputs\.py:\d+`|`test\.sh:\d+`|`instruction\.md:\d+`", l)]
assert len(qrows) >= 8, f"only {len(qrows)} quote rows found"
ROW26 = ent_lines[qrows[0]].rstrip("\n")     # the :10 row (7-word quote)
ROW27 = ent_lines[qrows[1]].rstrip("\n")     # the :11 row
ROW84 = next(ent_lines[i].rstrip("\n") for i in qrows if "`test_outputs.py:84`" in ent_lines[i])
ROW84B = next(ent_lines[i].rstrip("\n") for i in qrows if "`test_outputs.py:87`" in ent_lines[i])
ROW26SH = next(ent_lines[i].rstrip("\n") for i in qrows if "`test.sh:26`" in ent_lines[i])
assert "“echo 1 > /logs/verifier/reward.txt”" in ROW26SH

results.append(apply("M12 quote citation off by one line", "E", [(ROW26SH, ROW26SH.replace("`test.sh:26`", "`test.sh:27`"))]))
results.append(apply("M13 quote with one changed char", "E",
    [(ROW26SH, ROW26SH.replace("“echo 1 > /logs/verifier/reward.txt”", "“echo 2 > /logs/verifier/reward.txt”"))]))
results.append(apply("M14 26-word quote (spans cited lines 10-11)", "E",
    [(ROW26, "| the graded artefact is an agent-authored regex file | “Test that the agent created a file with a regex, that the regex is valid, and that it correctly matches (the last) dates in log lines containing at least one” | `test_outputs.py:10-11` |")]))
results.append(apply("M15 2-word quote", "E",
    [(ROW26SH, "| pass writes reward 1 | “echo 1” | `test.sh:26` |")]))
results.append(apply("M16 straight-quote row (unparsed)", "E",
    [(ROW26SH, '| pass writes reward 1 | "echo 1 > /logs/verifier/reward.txt" | `test.sh:26` |')]))
def eight_copies(ls):
    body = qrows
    first = ls[body[0]]
    out = list(ls)
    for i in body[1:]:
        out[i] = first
    return out
results.append(apply("M17 all quote rows copies of one quote (distinct=1)", "E", [], extra=eight_copies))
results.append(apply("M18 missing falsifier in negative space", "E",
    [("**Falsifier:** this entry is falsified if", "**Refuter:** this entry is refuted if")]))
neg_after = re.search(r"^## Negative space\n(.*?)(?=^## |\Z)", ENTRY.read_text(), re.S | re.M)
# verify on the mutated-then-restored file is meaningless; do a dry check of remaining 'falsif' occurrences
print(f"   (sanity: 'falsif' occurrences in entry before mutation: {ent.lower().count('falsif')})")
results.append(apply("M19 recheck without date/cadence", "E", [("recheck: 180d —", "recheck: periodically —")]))
s109_line = next(l for l in ent_lines if l.startswith("source: S109"))
s110_line = next(l for l in ent_lines if l.startswith("source: S110"))
def swap_src(ls):
    out = list(ls)
    i, j = out.index(s109_line), out.index(s110_line)
    out[i], out[j] = out[j], out[i]
    return out
results.append(apply("M20 swapped source lines (S109 <-> S110)", "E", [], extra=swap_src))

# --- final pristine proof ---
out, rc = run_counter()
print("\n=== RESTORED FINAL RUN")
print(out)
print(f"exit={rc}")
print(f"final shas: SOURCES={sha(SOURCES)} (want {P0_SOURCES}) ENTRY={sha(ENTRY)} (want {P0_ENTRY}) README={sha(README)} (want {P0_README})")
assert sha(SOURCES) == P0_SOURCES and sha(ENTRY) == P0_ENTRY and sha(README) == P0_README
assert rc == 0

# --- census invisibility demo for mutant 9 ---
print("\n=== CENSUS INVISIBILITY DEMO (mutant 9)")
r0 = subprocess.run([str(CENSUS), "census", "--file", str(SOURCES)], capture_output=True, text=True)
base_rows = re.search(r"^file\trows\t(\d+)$", r0.stdout, re.M)
print(f"census rows, pristine SOURCES.md: {base_rows.group(1) if base_rows else 'NO rows LINE'} (exit {r0.returncode})")
demo = LANE.parent / "census-demo-SOURCES.md"
ls = SOURCES.read_text().splitlines(keepends=True)
i = next(i for i, l in enumerate(ls) if l.startswith("| S108 |"))
ls.insert(i + 1, "    " + ls[i])
demo.write_text("".join(ls))
r1 = subprocess.run([str(CENSUS), "census", "--file", str(demo)], capture_output=True, text=True)
demo_rows = re.search(r"^file\trows\t(\d+)$", r1.stdout, re.M)
print(f"census rows, with 4-space indented duplicate: {demo_rows.group(1) if demo_rows else 'NO rows LINE'} (exit {r1.returncode})")
demo.unlink()
print(f"indented duplicate invisible to census gawk (0-3 space rule): {bool(base_rows and demo_rows and base_rows.group(1) == demo_rows.group(1))}")

print("\n=== SUMMARY TABLE")
caught = sum(1 for r in results if r[5] == "killed")
for name, target, pre, post, rc_, verdict, defs in results:
    print(f"{verdict:9s} rc={rc_} [{target}] {name}")
print(f"\ncaught {caught}/{len(results)}")
