# C2BlindSpotR73 — frozen audit falsification

Axes: coverage and calibration. One isolated fixture per case; no frozen rule or target edited.

## Method and command

`python3 /fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/probe.py` (driver exit 0). Every detector invocation: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/<ID>`.

Each case ran pristine → mutated → restored using the same CLI. All pristine and restored runs returned 0. All fixture-file SHA-256 maps restored exactly, including scripts and erratum bytes, not merely SKILL.md. The harness rebuilds the fixture in a finally block. Frozen instrument SHA-256 before/after: `9ec8f4d2ba2233751f3ef54c31fe169dfd89b39249dcc459b6b9e75756345828` / `9ec8f4d2ba2233751f3ef54c31fe169dfd89b39249dcc459b6b9e75756345828`.

Python 3.14.8. No tools installed. No git/jj operations. Fixture builder was imported read-only; Python import may generate a normal __pycache__ artifact, so source-byte immutability is the claim here, not proof of zero incidental cache writes.

Driver defect corrected: the first attempt mistakenly counted summary `DEFECTS n=0` as a defect. Final classification matches only stripped lines starting `DEFECT `. Earlier provisional classifications are not the results below.

## Control

```text
INSTRUMENTS total=1 derived=registry rows=1
PARSED scripts=1 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

## Results

16 cases: 3 caught / killed (C01, C12, C13), 13 passed / survived. Passing is evidence of detector acceptance, not automatically a violation of the frozen literal rule. No baseline was red or inconclusive.

### C01 — gate row: verdict map has the word `failed` but no code `0`

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-g` | gate | `python3 plans/tool_b.py` | `1` failed · `2` setup | none declared | pinned bytes | read-only | kengaku |
```

**caught / killed**; relevant leg: D2 gate-verdict. Caught: no-zero branch works; landing should retain this requirement.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 defect n=1
  DEFECT `tool-g`:gate-verdict:1,2
D3 ok n=0
D4 ok n=0
MISMATCH 1
DEFECTS n=1
PREDICATE R73-C2 fail
rc=1
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C02 — probe row declares only `0`; its script exits `2` on the setup path

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-p` | probe | `python3 plans/tool_probe.py` | `0` clean | none declared | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 probe-verdict. Semantic blind spot: the map omits an explicit exit 2; landing should not equate a zero declaration with complete exit coverage.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

Script bytes supporting the counterexample:
```python
plans/tool_a.py
import argparse
p=argparse.ArgumentParser()
p.add_argument('--selftest')

plans/tool_b.py
# second instrument

plans/tool_probe.py
import sys
if '--selftest' in sys.argv:
    sys.exit(0)
sys.exit(2)   # setup/could-not-evaluate path the row never declares

```

### C03 — entry declares `--strict`; the script names it only in a comment

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-f` | gate | `python3 plans/tool_a.py --strict` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 entry. Semantic blind spot: entry flags are not checked at all; landing should distinguish script existence from executable command validity.

```text
INSTRUMENTS total=1 derived=registry rows=2
PARSED scripts=1 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

Script bytes supporting the counterexample:
```python
plans/tool_a.py
import argparse
p=argparse.ArgumentParser()
p.add_argument('--selftest')
# --strict is named here only as a string literal; it is never registered

plans/tool_b.py
# second instrument

```

### C04 — self-test cell names a script with no flag at all

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-n` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | `python3 plans/tool_b.py` | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 self-test. Passed, but ambiguous: a bare script can legitimately be a self-test; landing should care only if script-plus-flag is promised.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C05 — self-test cell names a script that does not exist

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-x` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | `python3 plans/ghost.py --selftest` | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 self-test / D1 referenced scripts. Strong blind spot: nonexistent self-test script is accepted; landing should care about advertised commands that cannot run.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C06 — pinned-values cell names a path that does not exist

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-m` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | `corpus/evidence/round73/w1/does-not-exist.md` sha256-pinned | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 pinned-values. Nonempty-only contract boundary: no referent validation is promised by the narrow leg; landing should qualify pin-validity claims.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C07 — duplicate row name differing only in case (`Tool-A` vs `tool-a`)

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `Tool-A` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D3 EVERY-ROW. Exact-name boundary: case-sensitive names can be distinct on Linux; landing should care if registry identifiers are intended to be case-insensitive.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C08 — owner cell is `kengaku-ish`

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-o` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku-ish |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 owner. Literal prefix rule accepts this intentionally; landing should care about ownership ambiguity, not call it a failed frozen rule.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C09 — gate row: `0` clean · `0` failed — a failure word, no distinct failure code

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-z` | gate | `python3 plans/tool_b.py` | `0` clean · `0` failed | none declared | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 gate-verdict. Semantic blind spot allowed by failure-word rule: no nonzero failure code is declared; landing should not infer a meaningful failure map.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C10 — row with 9 cells (stray cell) is dropped by the parser

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-9` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku | stray |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 eight-cell validation / D3 EVERY-ROW. Strong blind spot: malformed row disappears before pricing; landing should care because every-row accounting is undermined.

```text
INSTRUMENTS total=1 derived=registry rows=1
PARSED scripts=1 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C11 — row with 7 cells (no owner cell) is dropped by the parser

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-7` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 eight-cell validation / D3 EVERY-ROW. Strong blind spot: missing owner column causes complete row omission; landing should care for the same every-row reason.

```text
INSTRUMENTS total=1 derived=registry rows=1
PARSED scripts=1 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C12 — duplicate row name, byte-identical (D3 positive control)

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-a` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku |
```

**caught / killed**; relevant leg: D3 EVERY-ROW. Caught positive control: exact duplicates are detected; landing should retain it.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 defect n=1
  DEFECT DUPLICATE-ROW `tool-a`
D4 ok n=0
MISMATCH 1
DEFECTS n=1
PREDICATE R73-C2 fail
rc=1
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C13 — owner cell is `sibling` (D2 owner positive control)

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-sib` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | sibling |
```

**caught / killed**; relevant leg: D2 owner. Caught positive control: plainly foreign owner is detected; landing should retain it.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 defect n=1
  DEFECT `tool-sib`:owner:sibling
D3 ok n=0
D4 ok n=0
MISMATCH 1
DEFECTS n=1
PREDICATE R73-C2 fail
rc=1
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

### C14 — entry declares --strict absent entirely from the script

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-af` | gate | `python3 plans/tool_a.py --strict` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 entry. Strong semantic boundary: even an entirely absent flag passes; landing should not claim entry-command validity.

```text
INSTRUMENTS total=1 derived=registry rows=2
PARSED scripts=1 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

Script bytes supporting the counterexample:
```python
plans/tool_a.py
import argparse
p=argparse.ArgumentParser()
p.add_argument('--selftest')

plans/tool_b.py
# second instrument

```

### C15 — self-test flag appears only in a comment, never implemented

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
| `tool-cb` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | `python3 plans/tool_b.py --selftest` | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D2 self-test. Substring-backed boundary: a comment satisfies backing; landing should distinguish text presence from actual CLI support.

```text
INSTRUMENTS total=2 derived=registry rows=2
PARSED scripts=2 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

Script bytes supporting the counterexample:
```python
plans/tool_a.py
import argparse
p=argparse.ArgumentParser()
p.add_argument('--selftest')

plans/tool_b.py
# second instrument
# --selftest is documented here only; never registered

```

### C16 — third erratum item contradicts the first label revision binding

Fixture row(s), excluding header:

```markdown
| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
```

**passed / survived (blind-spot candidate)**; relevant leg: D4 ERRATA. Strong blind spot: first matching item masks a later contradictory binding; landing should care about each-item wording.

```text
INSTRUMENTS total=1 derived=registry rows=1
PARSED scripts=1 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
rc=0
```

Pristine rc=0; restored rc=0; full fixture bytes restored=True.

Mutated erratum:
```markdown
# fixture claims

The label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.

## Errata — round 72

1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.
2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.
3. The label `Do-nothing control (committed at freeze)` is fine at d8a77d3f.

```

## Most fragile leg

D2 is the most fragile: its broad eight-field label hides heterogeneous weak tests (nonempty pinned/scope cells, raw owner prefix, failure-word substring, unvalidated entry flags, and self-test early returns that treat missing scripts as backed). D3 also loses malformed rows before it can enforce every-row accounting; D4 checks only the first matching item.

These are findings, not permission to change the frozen predicate or targets. Literal contract boundaries (notably owner-prefix, pinned nonempty, exact-name comparison, and failure-word acceptance) are explicitly distinguished above from stronger semantic expectations.

Before the final run, the cases directory was removed: an earlier repeated run had retained an added script as baseline. Final raw receipts below are exclusively the clean run, with complete restoration maps matching.

## Reproduction harness

```python
#!/usr/bin/env python3
"""Blind-spot probe: one defect-bearing fixture per case, run only through the frozen audit.

Fixtures are built with the frozen instrument's OWN builders (build_fixture/row_text),
imported read-only, so a case's fixture is byte-comparable to the audit's selftest fixtures.
Baseline control = the unmutated fixture must be green; a case that stays green is a blind spot.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FROZEN = LANE / "plans/round73_c2_registry_audit.py"
S = Path("/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73")
CASES = S / "cases"

spec = importlib.util.spec_from_file_location("frozen_audit", FROZEN)
mod = importlib.util.module_from_spec(spec)
sys.modules["frozen_audit"] = mod
spec.loader.exec_module(mod)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(lane: Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(FROZEN), "--lane", str(lane)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + (("STDERR " + p.stderr) if p.stderr else "")


PROBE_EXIT2 = (
    "import sys\n"
    "if '--selftest' in sys.argv:\n"
    "    sys.exit(0)\n"
    "sys.exit(2)   # setup/could-not-evaluate path the row never declares\n"
)

COMMENT_FLAG = (
    "import argparse\n"
    "p=argparse.ArgumentParser()\n"
    "p.add_argument('--selftest')\n"
    "# --strict is named here only as a string literal; it is never registered\n"
)


def append_skill(root: Path, text: str) -> None:
    with (root / "SKILL.md").open("a") as fh:
        fh.write(text)


def case_gate_no_zero(root: Path) -> None:
    append_skill(root, mod.row_text("tool-g", "plans/tool_b.py",
                                    verdict="`1` failed · `2` setup"))


def case_probe_zero_only(root: Path) -> None:
    (root / "plans" / "tool_probe.py").write_text(PROBE_EXIT2)
    append_skill(root, mod.row_text("tool-p", "plans/tool_probe.py", kind="probe",
                                    verdict="`0` clean"))


def case_entry_flag_comment(root: Path) -> None:
    (root / "plans" / "tool_a.py").write_text(COMMENT_FLAG)
    append_skill(root, mod.row_text("tool-f", "plans/tool_a.py --strict"))


def case_selftest_no_flag(root: Path) -> None:
    append_skill(root, mod.row_text("tool-n", "plans/tool_b.py",
                                    selftest="`python3 plans/tool_b.py`"))


def case_selftest_ghost(root: Path) -> None:
    append_skill(root, mod.row_text("tool-x", "plans/tool_b.py",
                                    selftest="`python3 plans/ghost.py --selftest`"))


def case_pinned_missing(root: Path) -> None:
    append_skill(root, mod.row_text(
        "tool-m", "plans/tool_b.py",
        pinned="`corpus/evidence/round73/w1/does-not-exist.md` sha256-pinned"))


def case_dup_case(root: Path) -> None:
    append_skill(root, mod.row_text("Tool-A", "plans/tool_b.py"))


def case_owner_ish(root: Path) -> None:
    append_skill(root, mod.row_text("tool-o", "plans/tool_b.py", owner="kengaku-ish"))


def case_gate_zero_twice(root: Path) -> None:
    append_skill(root, mod.row_text("tool-z", "plans/tool_b.py",
                                    verdict="`0` clean · `0` failed"))


def case_nine_cells(root: Path) -> None:
    append_skill(root, "| `tool-9` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed "
                       "| none declared | pinned bytes | read-only | kengaku | stray |\n")


def case_seven_cells(root: Path) -> None:
    append_skill(root, "| `tool-7` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed "
                       "| none declared | pinned bytes | read-only |\n")


def case_dup_exact(root: Path) -> None:
    append_skill(root, mod.row_text("tool-a", "plans/tool_b.py"))


def case_owner_sibling(root: Path) -> None:
    append_skill(root, mod.row_text("tool-sib", "plans/tool_b.py", owner="sibling"))


def case_entry_flag_absent(root: Path) -> None:
    # tool_a.py never mentions --strict, in code or comment: no leg reads entry flags at all
    append_skill(root, mod.row_text("tool-af", "plans/tool_a.py --strict"))


def case_selftest_comment_backed(root: Path) -> None:
    (root / "plans" / "tool_b.py").write_text(
        "# second instrument\n# --selftest is documented here only; never registered\n")
    append_skill(root, mod.row_text("tool-cb", "plans/tool_b.py",
                                    selftest="`python3 plans/tool_b.py --selftest`"))


def case_errata_third_item(root: Path) -> None:
    claims = root / mod.CLAIMS_REL
    label0 = mod.ERRATUM_ITEMS[0][0]
    wrong0 = mod.ERRATUM_ITEMS[1][1]      # a revision that belongs to the other label
    claims.write_text(claims.read_text()
                      + f"3. The label `{label0}` is fine at {wrong0}.\n")


# (id, human defect sentence, expected, mutator, row count delta if silently dropped)
PLAN = [
    ("C01", "gate row: verdict map has the word `failed` but no code `0`", "caught",
     case_gate_no_zero, None),
    ("C02", "probe row declares only `0`; its script exits `2` on the setup path", "passed",
     case_probe_zero_only, None),
    ("C03", "entry declares `--strict`; the script names it only in a comment", "passed",
     case_entry_flag_comment, None),
    ("C04", "self-test cell names a script with no flag at all", "passed",
     case_selftest_no_flag, None),
    ("C05", "self-test cell names a script that does not exist", "passed",
     case_selftest_ghost, None),
    ("C06", "pinned-values cell names a path that does not exist", "passed",
     case_pinned_missing, None),
    ("C07", "duplicate row name differing only in case (`Tool-A` vs `tool-a`)", "passed",
     case_dup_case, None),
    ("C08", "owner cell is `kengaku-ish`", "passed", case_owner_ish, None),
    ("C09", "gate row: `0` clean · `0` failed — a failure word, no distinct failure code",
     "passed", case_gate_zero_twice, None),
    ("C10", "row with 9 cells (stray cell) is dropped by the parser", "passed",
     case_nine_cells, 0),
    ("C11", "row with 7 cells (no owner cell) is dropped by the parser", "passed",
     case_seven_cells, 0),
    ("C12", "duplicate row name, byte-identical (D3 positive control)", "caught",
     case_dup_exact, None),
    ("C13", "owner cell is `sibling` (D2 owner positive control)", "caught",
     case_owner_sibling, None),
    ("C14", "entry declares --strict absent entirely from the script", "passed",
     case_entry_flag_absent, None),
    ("C15", "self-test flag appears only in a comment, never implemented", "passed",
     case_selftest_comment_backed, None),
    ("C16", "third erratum item contradicts the first label revision binding", "passed",
     case_errata_third_item, None),
]


def main() -> int:
    CASES.mkdir(parents=True, exist_ok=True)
    out = {"frozen": str(FROZEN), "frozen_sha256": sha(FROZEN), "control": {}, "cases": []}

    control = mod.build_fixture(CASES / "control")
    rc, text = run(control)
    out["control"] = {"rc": rc, "stdout": text, "skill_sha256": sha(control / "SKILL.md")}

    for cid, defect, expected, mutate, delta in PLAN:
        root = mod.build_fixture(CASES / cid)
        skill = root / "SKILL.md"
        pristine = skill.read_bytes()
        pristine_sha = hashlib.sha256(pristine).hexdigest()
        rc_b, text_b = run(root)
        before_files = {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}
        mutate(root)
        mutated_sha = sha(skill)
        mutated_rows = skill.read_text().splitlines()[4:]
        mutated_files = {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}
        mutated_sources = {str(p.relative_to(root)): p.read_text() for p in root.rglob("*.py")}
        mutated_claims = (root / mod.CLAIMS_REL).read_text()
        try:
            rc_m, text_m = run(root)
        finally:
            shutil.rmtree(root)
            mod.build_fixture(root)
        restored_sha = sha(skill)
        after_files = {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}
        rc_r, text_r = run(root)
        defects = [ln.strip() for ln in text_m.splitlines()
                   if ln.strip().startswith("DEFECT ")]
        observed = "caught" if (rc_m != 0 or defects) else "passed"
        out["cases"].append({
            "id": cid, "defect": defect, "expected": expected, "observed": observed,
            "agree": observed == expected, "fixture": str(root),
            "pristine_sha256": pristine_sha, "mutated_sha256": mutated_sha,
            "restored_sha256": restored_sha, "restored_identical": restored_sha == pristine_sha,
            "rc_pristine": rc_b, "stdout_pristine": text_b,
            "before_files": before_files, "mutated_files": mutated_files,
            "after_files": after_files, "all_bytes_restored": before_files == after_files,
            "mutated_rows": mutated_rows, "mutated_sources": mutated_sources,
            "mutated_claims": mutated_claims,
            "rc_mutated": rc_m, "stdout_mutated": text_m,
            "defect_lines": defects,
            "rc_restored": rc_r, "stdout_restored": text_r,
        })
        print(f"{cid} expected={expected} observed={observed} "
              f"agree={observed == expected} rc={rc_m} defects={defects}")

    out["frozen_sha256_after"] = sha(FROZEN)
    (S / "results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"all_agree={all(c['agree'] for c in out['cases'])} "
          f"cases={len(out['cases'])}")
    print(f"control_rc={out['control']['rc']} "
          f"control_last={out['control']['stdout'].strip().splitlines()[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## Raw receipts and before/mutated/restored SHA-256 maps

```json
{
  "frozen": "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round73_c2_registry_audit.py",
  "frozen_sha256": "9ec8f4d2ba2233751f3ef54c31fe169dfd89b39249dcc459b6b9e75756345828",
  "control": {
    "rc": 0,
    "stdout": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
    "skill_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730"
  },
  "cases": [
    {
      "id": "C01",
      "defect": "gate row: verdict map has the word `failed` but no code `0`",
      "expected": "caught",
      "observed": "caught",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C01",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "be4dc5cc603df1a73ef88af6568d67754b244886d0159cd7827dd2bdcfd9773d",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "be4dc5cc603df1a73ef88af6568d67754b244886d0159cd7827dd2bdcfd9773d",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-g` | gate | `python3 plans/tool_b.py` | `1` failed \u00b7 `2` setup | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 1,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 defect n=1\n  DEFECT `tool-g`:gate-verdict:1,2\nD3 ok n=0\nD4 ok n=0\nMISMATCH 1\nDEFECTS n=1\nPREDICATE R73-C2 fail\n",
      "defect_lines": [
        "DEFECT `tool-g`:gate-verdict:1,2"
      ],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C02",
      "defect": "probe row declares only `0`; its script exits `2` on the setup path",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C02",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "f369d56a832a259ac3cde5c2cbdfa4f460915466d0a572b18b6a28b15ec06a22",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "f369d56a832a259ac3cde5c2cbdfa4f460915466d0a572b18b6a28b15ec06a22",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "plans/tool_probe.py": "055cc1a7f3439f9e15e0baa3afa6fcc0c6bebca29ca4616ec808f983028b8805",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-p` | probe | `python3 plans/tool_probe.py` | `0` clean | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n",
        "plans/tool_probe.py": "import sys\nif '--selftest' in sys.argv:\n    sys.exit(0)\nsys.exit(2)   # setup/could-not-evaluate path the row never declares\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C03",
      "defect": "entry declares `--strict`; the script names it only in a comment",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C03",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "177e5eb4c377728f1e64a4f673bdb545a34855e07fe55f6a8f1a4c93bde2f25d",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "177e5eb4c377728f1e64a4f673bdb545a34855e07fe55f6a8f1a4c93bde2f25d",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "940f3c927182e7ecca795593c98e56f722151421691708b22730213beea69b81",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-f` | gate | `python3 plans/tool_a.py --strict` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n# --strict is named here only as a string literal; it is never registered\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=1 derived=registry rows=2\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C04",
      "defect": "self-test cell names a script with no flag at all",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C04",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "b8f2448efc20ff9ecd25ef1e26afc805255a16711691839814846c23e8b328b9",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "b8f2448efc20ff9ecd25ef1e26afc805255a16711691839814846c23e8b328b9",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-n` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_b.py` | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C05",
      "defect": "self-test cell names a script that does not exist",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C05",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "8a3b24a9f0291a2c2cc3e537601879bbc0aacfcfea2e1e6d84f2325ce5359777",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "8a3b24a9f0291a2c2cc3e537601879bbc0aacfcfea2e1e6d84f2325ce5359777",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-x` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | `python3 plans/ghost.py --selftest` | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C06",
      "defect": "pinned-values cell names a path that does not exist",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C06",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "852b8b730a81ab12141c0af67e7dd101c7ab9ad4c3c33ee3a6fd26cd30988593",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "852b8b730a81ab12141c0af67e7dd101c7ab9ad4c3c33ee3a6fd26cd30988593",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-m` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | `corpus/evidence/round73/w1/does-not-exist.md` sha256-pinned | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C07",
      "defect": "duplicate row name differing only in case (`Tool-A` vs `tool-a`)",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C07",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "124dc1b2aef11ff30f2dbcc83454e88e03c5d72930eb41cd4bdcc15a943f39a3",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "124dc1b2aef11ff30f2dbcc83454e88e03c5d72930eb41cd4bdcc15a943f39a3",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `Tool-A` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C08",
      "defect": "owner cell is `kengaku-ish`",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C08",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "567082400de39624f57ce7205fa188a21ee6e17e0d193d0d1709a2e4e832c41c",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "567082400de39624f57ce7205fa188a21ee6e17e0d193d0d1709a2e4e832c41c",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-o` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku-ish |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C09",
      "defect": "gate row: `0` clean \u00b7 `0` failed \u2014 a failure word, no distinct failure code",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C09",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "be667c5831d23a0516d27e69e47b7ce4f0e3ad16b2378e4fe69ae6a0bfa6d554",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "be667c5831d23a0516d27e69e47b7ce4f0e3ad16b2378e4fe69ae6a0bfa6d554",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-z` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `0` failed | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C10",
      "defect": "row with 9 cells (stray cell) is dropped by the parser",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C10",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "77d54c473d18a26320221adc62ac9ba88b3e3fc342b88ab184827c79674b61e1",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "77d54c473d18a26320221adc62ac9ba88b3e3fc342b88ab184827c79674b61e1",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-9` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku | stray |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C11",
      "defect": "row with 7 cells (no owner cell) is dropped by the parser",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C11",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "24cb34b473b384f5d22c8d39e0ed38f797e7079663cbef275bd1d380b7393198",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "24cb34b473b384f5d22c8d39e0ed38f797e7079663cbef275bd1d380b7393198",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-7` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C12",
      "defect": "duplicate row name, byte-identical (D3 positive control)",
      "expected": "caught",
      "observed": "caught",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C12",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "0b34c76efbe84eef0cdf1d53cc411fed80cb66c26a89b617767adb7a2a7081f3",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "0b34c76efbe84eef0cdf1d53cc411fed80cb66c26a89b617767adb7a2a7081f3",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-a` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 1,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 defect n=1\n  DEFECT DUPLICATE-ROW `tool-a`\nD4 ok n=0\nMISMATCH 1\nDEFECTS n=1\nPREDICATE R73-C2 fail\n",
      "defect_lines": [
        "DEFECT DUPLICATE-ROW `tool-a`"
      ],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C13",
      "defect": "owner cell is `sibling` (D2 owner positive control)",
      "expected": "caught",
      "observed": "caught",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C13",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "78c1701d3f0c9eb12a056833d80f7053a412bdb639ad265402da899aa66a6d02",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "78c1701d3f0c9eb12a056833d80f7053a412bdb639ad265402da899aa66a6d02",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-sib` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | sibling |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 1,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 defect n=1\n  DEFECT `tool-sib`:owner:sibling\nD3 ok n=0\nD4 ok n=0\nMISMATCH 1\nDEFECTS n=1\nPREDICATE R73-C2 fail\n",
      "defect_lines": [
        "DEFECT `tool-sib`:owner:sibling"
      ],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C14",
      "defect": "entry declares --strict absent entirely from the script",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C14",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "8b936c7e1af15227e8ff178ca423fd986c14ef55c98a740eea6feb02dfa28531",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "8b936c7e1af15227e8ff178ca423fd986c14ef55c98a740eea6feb02dfa28531",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-af` | gate | `python3 plans/tool_a.py --strict` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=1 derived=registry rows=2\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C15",
      "defect": "self-test flag appears only in a comment, never implemented",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C15",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "fdb00575d715adb879ecc636f0e01f3a081fce8fa14d7e15ca92f602c0f7ab96",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "fdb00575d715adb879ecc636f0e01f3a081fce8fa14d7e15ca92f602c0f7ab96",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "eadb065fe6378cbb88b9691238126079abbaafde35dd5b91c62c19cfed586106",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |",
        "| `tool-cb` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_b.py --selftest` | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n# --selftest is documented here only; never registered\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=2 derived=registry rows=2\nPARSED scripts=2 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    },
    {
      "id": "C16",
      "defect": "third erratum item contradicts the first label revision binding",
      "expected": "passed",
      "observed": "passed",
      "agree": true,
      "fixture": "/fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/C16",
      "pristine_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "mutated_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_sha256": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
      "restored_identical": true,
      "rc_pristine": 0,
      "stdout_pristine": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "before_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "mutated_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "7de9af022ecd3c0d994dd08d74aee1b7f198d74762db6063f5bbc109e5e7cfa8",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "after_files": {
        "SKILL.md": "7f4c7f656ddcd5cd17c906117cab257b284e3d654b2708765ea0133040254730",
        "SCORECARD.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "LOG.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac",
        "plans/tool_a.py": "1610d114c3da814941356a733cd8fcb9769a31dde683f7a95213e19d6daa1906",
        "plans/tool_b.py": "c005136c44410f5ae13ac1e8f312bc5af14f08493cbf33457a751ca4cd4b1a11",
        "plans/round-71-claims.md": "257a6ebe7a30fafe8ae6fcd397b3a13e9bc08e9844ed19f937ba9745c006f79a",
        "corpus/README.md": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
      },
      "all_bytes_restored": true,
      "mutated_rows": [
        "| `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |"
      ],
      "mutated_sources": {
        "plans/tool_a.py": "import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n",
        "plans/tool_b.py": "# second instrument\n"
      },
      "mutated_claims": "# fixture claims\n\nThe label `Do-nothing control (committed at freeze)` and the label `Red-before (committed at freeze)` are superseded.\n\n## Errata \u2014 round 72\n\n1. The label `Do-nothing control (committed at freeze)` is false of d8a77d3f; the control landed with c80fcdb3.\n2. The label `Red-before (committed at freeze)` is half right: the receipt is committed at d8a77d3f.\n3. The label `Do-nothing control (committed at freeze)` is fine at d8a77d3f.\n",
      "rc_mutated": 0,
      "stdout_mutated": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n",
      "defect_lines": [],
      "rc_restored": 0,
      "stdout_restored": "INSTRUMENTS total=1 derived=registry rows=1\nPARSED scripts=1 failed=0\nD1 ok n=0\nD2 ok n=0\nD3 ok n=0\nD4 ok n=0\nMISMATCH 0\nDEFECTS n=0\nPREDICATE R73-C2 pass\n"
    }
  ],
  "frozen_sha256_after": "9ec8f4d2ba2233751f3ef54c31fe169dfd89b39249dcc459b6b9e75756345828"
}
```
