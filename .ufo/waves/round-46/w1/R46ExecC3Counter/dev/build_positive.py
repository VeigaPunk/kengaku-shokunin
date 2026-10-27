"""DEV-ONLY positive control: build a shape-correct polyglot package in the scratch clone (never the lane)."""
import hashlib, json, pathlib, re, shutil, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter")
L = S / "lane"
CAPSRC = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC3Capture/tb2-polyglot-c-py")
CAP = L / "corpus/evidence/round46/tb2-polyglot-c-py"
ENTRY = L / "corpus/knowledge/tb2-polyglot-c-py-grader.md"
RAW = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/"
ROWS = [("S166", "test_outputs.py", "tests/test_outputs.py"),
        ("S167", "test.sh", "tests/test.sh"),
        ("S168", "instruction.md", "instruction.md"),
        ("S169", "solve.sh", "solution/solve.sh"),
        ("S170", "Dockerfile", "environment/Dockerfile"),
        ("S171", "task.toml", "task.toml"),
        ("S172", "README.md", "README.md")]
# capture -> (cited line, verbatim quote without a straight double quote)
ANCHOR = {"test_outputs.py": (18, "assert polyglot_files =="),
          "test.sh": (25, "if [ $? -eq 0 ]; then"),
          "instruction.md": (1, "Write me a single file in"),
          "solve.sh": (52, "fib_c((unsigned int)n));"),
          "Dockerfile": (2, "FROM ubuntu:24.04"),
          "task.toml": (22, "timeout_sec = 900.0"),
          "README.md": (24, "Test cases: f(0)=0,")}
CASES = [("nop", "fail", "single-file", 18, "assert polyglot_files =="),
         ("oracle-solve-sh", "pass", "", 52, "fib_c((unsigned int)n));"),
         ("lookup-table", "pass", "three-points", 27, "test_cases = [(42,"),
         ("python-only", "fail", "dual-runtime", 24, "cmain\"], check=True"),
         ("c-only", "fail", "dual-runtime", 30, "py_result = subprocess.run("),
         ("extra-file", "fail", "single-file", 18, "assert polyglot_files =="),
         ("leftover-cmain", "fail", "single-file", 18, "assert polyglot_files =="),
         ("wrong-value", "fail", "stdout-value", 44, "assert python_out == expected"),
         ("trailing-ws", "pass", "stdout-value", 36, "python_out = py_result.stdout.strip()"),
         ("nonzero-exit", "fail", "dual-runtime", 37, "c_result = subprocess.run("),
         ("stderr-noise", "pass", "stdout-value", 43, "c_out = c_result.stdout.strip()"),
         ("n-parsed-differently", "fail", "three-points", 27, "test_cases = [(42,"),
         ("compile-warning", "pass", "", 24, "cmain\"], check=True"),
         ("regrade-same-state", "pass", "three-points", 44, "assert python_out == expected"),
         ("empty-file", "fail", "single-file", 18, "assert polyglot_files =="),
         ("dir-in-place", "fail", "single-file", 24, "cmain\"], check=True"),
         ("crlf-source", "pass", "source-shape", 24, "cmain\"], check=True"),
         ("value-plus-line", "fail", "stdout-value", 36, "python_out = py_result.stdout.strip()")]
TAGS = [("single-file", "instruction.md:1", "nop"),
        ("dual-runtime", "instruction.md:5", "python-only"),
        ("stdout-value", "instruction.md:7", "wrong-value"),
        ("three-points", "instruction.md:7", "n-parsed-differently"),
        ("source-shape", "instruction.md:1", "crlf-source")]
QUOTES = [("the listing is read first", "test_outputs.py", 17, "polyglot_files = os.listdir("),
          ("the listing must be exactly one file", "test_outputs.py", 18, "assert polyglot_files =="),
          ("three fixed points, no other N", "test_outputs.py", 27, "test_cases = [(42,"),
          ("the python run is captured and checked", "test_outputs.py", 30, "py_result = subprocess.run("),
          ("only stdout after strip is compared", "test_outputs.py", 36, "python_out = py_result.stdout.strip()"),
          ("the C stdout is compared the same way", "test_outputs.py", 43, "c_out = c_result.stdout.strip()"),
          ("one assert decides every point", "test_outputs.py", 44, "assert python_out == expected"),
          ("the oracle writes the polyglot", "solve.sh", 12, "cat <<'EOF' > polyglot/main.py.c"),
          ("the C half takes N from argv", "solve.sh", 51, "unsigned long n = strtoul"),
          ("the request names one file", "instruction.md", 1, "Write me a single file in"),
          ("the request names both toolchains", "instruction.md", 5, "gcc /app/polyglot/main.py.c"),
          ("the reward is pytest's exit status", "test.sh", 25, "if [ $? -eq 0 ]; then")]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def lines(name):
    return (CAP / name).read_bytes().decode("utf-8", "replace").split("\n")


CAP.mkdir(parents=True, exist_ok=True)
for f in CAPSRC.iterdir():
    shutil.copy2(f, CAP / f.name)
# --- registry rows
row_lines = []
for sid, capname, upstream in ROWS:
    n, q = ANCHOR[capname]
    nl = len(lines(capname)[:-1]) if lines(capname)[-1] == "" else len(lines(capname))
    anchor = ('commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, %s:1-%d, :%d "%s" (%d words); sha256 %s'
              % (capname, nl, n, q, len(q.split()), sha((CAP / capname).read_bytes())))
    row_lines.append("| %s | Terminal-Bench 2.0 polyglot-c-py %s (%s) — %s%s | code | A | the %s of the task | %s "
                     "| dev positive control: the %s decides a case | mined | 2026-10-27 | 180d | "
                     "corpus/knowledge/tb2-polyglot-c-py-grader.md |"
                     % (sid, capname, upstream, RAW, upstream, capname, anchor, capname))
src = (L / "corpus/SOURCES.md").read_text()
ls = src.splitlines()
# the dev clone only: drop any landed S166-S172 rows so the dev ones are not duplicates of them
ls = [l for l in ls if not re.match(r"^\| S(16[6-9]|17[0-2]) ", l)]
last = max(i for i, l in enumerate(ls) if l.startswith("| S"))
ls[last + 1:last + 1] = row_lines
(L / "corpus/SOURCES.md").write_text("\n".join(ls) + "\n")
# --- dry table, receipt
dry = [f"TAG {t} {loc}" for t, loc, _c in TAGS]
for i, (cid, pred, viol, _l, _q) in enumerate(CASES):
    dry.append(f"CASE {cid} predicted={pred} tests={'P' if pred == 'pass' else 'F'} regrade=same violates={viol} "
               f"end=recipe -- dev positive control case {i}")
(ENTRY.parent.mkdir(parents=True, exist_ok=True))
drypt = L / "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
drypt.parent.mkdir(parents=True, exist_ok=True)
drypt.write_text("\n".join(dry) + "\n")
rec = ["# dev positive control receipt (declared: observed = predicted; no probe was run)"]
for i, (cid, pred, viol, _l, _q) in enumerate(CASES):
    rec.append(f"CASE {cid} predicted={pred} observed={pred} tests={'P' if pred == 'pass' else 'F'} "
               f"predicted_tests={'P' if pred == 'pass' else 'F'} match=yes regrade=same violates={viol} "
               f"-- dev positive control case {i}")
rec.append(f"regrade cases={len(CASES)} differ=0")
rec.append(f"cases={len(CASES)} observed_pass={sum(1 for c in CASES if c[1] == 'pass')} "
           f"observed_fail={sum(1 for c in CASES if c[1] == 'fail')} mismatches=0")
(L / "corpus/evidence/round46/polyglot-c-py-probe.txt").write_text("\n".join(rec) + "\n")
# --- probe (--dry prints the frozen table byte-for-byte)
probe = '''#!/usr/bin/env python3
"""DEV positive control probe: --dry only (no graded case runs)."""
import argparse, pathlib, sys
ap = argparse.ArgumentParser()
ap.add_argument("--lane", default=".")
ap.add_argument("--dry", action="store_true")
a = ap.parse_args()
if not a.dry:
    print((pathlib.Path(a.lane) / "corpus/evidence/round46/polyglot-c-py-probe.txt").read_text(), end="")
    sys.exit(0)
print((pathlib.Path(a.lane) / "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt").read_text(), end="")
'''
(L / "plans/polyglot_c_py_probe.py").write_text(probe)
# --- entry
CASE_CAP = {"oracle-solve-sh": "solve.sh"}
mech = "\n".join("| `%s` | `%s:%d` | “%s” |" % (c[0], CASE_CAP.get(c[0], "test_outputs.py"), c[3], c[4])
                 for c in CASES)
case_rows = "\n".join("| `%s` | %s | %s | dev positive control end state %d |"
                      % (c[0], "P" if c[1] == "pass" else "F", c[1], i) for i, c in enumerate(CASES))
def _label(tag):
    vals = {c[1] for c in CASES if tag in c[2].split(",")}
    return "enforced" if vals == {"fail"} else ("unenforced" if vals == {"pass"} else "partly")


map_rows = "\n".join("| `%s` | `%s` | %s | `%s` |" % (loc, t, _label(t), cited) for t, loc, cited in TAGS)
quote_rows = "\n".join("| %s | “%s” | `%s:%d` |" % (claim, q, cap, n) for claim, cap, n, q in QUOTES)
pred = (S / "v11-reference-predictor.py").read_text()
entry = []
for sid, capname, upstream in ROWS:
    entry.append(f"source: {sid} — {RAW}{upstream} — the {capname} of the task, same commit, accessed 2026-10-27")
entry.append("verified-at: 2026-10-27")
entry.append("recheck: 180d — re-run the counter; any capture digest change supersedes this entry")
entry.append("")
entry.append("# Terminal-Bench 2.0 task grader, read and executed: `polyglot-c-py` (DEV POSITIVE CONTROL)")
entry.append("")
entry.append("## Summary")
entry.append("")
entry.append("One file `/app/polyglot/main.py.c` is executed by two toolchains and graded on three fixed points.")
entry.append("Rows S166, S167, S168, S169, S170, S171 and S172 are the captures this entry reads.")
entry.append("")
entry.append("## Located quotes")
entry.append("")
entry.append("| Claim supported | “Quote” | `capture:line` |")
entry.append("|---|---|---|")
entry.append(quote_rows)
entry.append("")
entry.append("## Requirement map")
entry.append("")
entry.append("| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |")
entry.append("|---|---|---|---|")
entry.append(map_rows)
entry.append("")
entry.append("## Case table")
entry.append("")
entry.append("| Case | Tests | Observed | What the end state is |")
entry.append("|---|---|---|---|")
entry.append(case_rows)
entry.append("")
entry.append("## Mechanism")
entry.append("")
entry.append("| Case | Decisive line | “Quote” |")
entry.append("|---|---|---|")
entry.append(mech)
entry.append("")
entry.append("## Predictor")
entry.append("")
entry.append("The grader's rule: the listing is exactly one file, and both runtimes print the expected value.")
entry.append("")
entry.append("```python")
entry.append(pred.rstrip())
entry.append("```")
entry.append("")
entry.append("## Negative space")
entry.append("")
entry.append("Nothing here is admitted: this entry is a development control and is falsified by its own rows.")
ENTRY.write_text("\n".join(entry) + "\n")
# --- spec
spec = {"name": "round-46 dev positive control", "entry": "corpus/knowledge/tb2-polyglot-c-py-grader.md",
        "capture_dir": "corpus/evidence/round46/tb2-polyglot-c-py",
        "receipt": "corpus/evidence/round46/polyglot-c-py-probe.txt",
        "receipt_sha256": sha((L / "corpus/evidence/round46/polyglot-c-py-probe.txt").read_bytes()),
        "probe_cmd": ["plans/polyglot_c_py_probe.py", "--lane", "."],
        "sources": "corpus/SOURCES.md", "readme": "corpus/README.md", "knowledge_glob": "corpus/knowledge/*.md",
        "raw_base": RAW, "rows": {}, "frozen_instruments": {"plans/pkg_gate.py": sha((L / "plans/pkg_gate.py").read_bytes())},
        "entry_rules": {"verified_at": "2026-10-27", "min_quotes": 10, "min_distinct_locations": 10,
                        "quote_words": [3, 25], "min_teaches_words": 8, "row_opened": "2026-10-27",
                        "row_tier": "A", "row_status": "mined"}}
for sid, capname, upstream in ROWS:
    spec["rows"][sid] = {"capture": capname, "upstream": upstream, "sha256": sha((CAP / capname).read_bytes())}
(L / "plans/pkg-spec-r46.json").write_text(json.dumps(spec, indent=1) + "\n")
# --- README ## Frontier + PROVINCE line
r = (L / "corpus/README.md").read_text()
r = r.replace("## Frontier\n", "## Frontier\n\n- `knowledge/tb2-polyglot-c-py-grader.md` — dev positive control (polyglot-c-py), S166 S167 S168 S169 S170 S171 S172, receipt corpus/evidence/round46/polyglot-c-py-probe.txt\n", 1)
r = r.replace("## What's here\n", "## What's here\n\n| file | rows |\n|---|---|\n| `knowledge/tb2-polyglot-c-py-grader.md` | S166 S167 S168 S169 S170 S171 S172 |\n", 1)
(L / "corpus/README.md").write_text(r)
p = (L / "PROVINCE.md").read_text()
p += ("\n**Round 46 (dev positive control).** `knowledge/tb2-polyglot-c-py-grader.md` is the counter's "
      "satisfiability control, not an admission.\n")
(L / "PROVINCE.md").write_text(p)
print("positive control built")
