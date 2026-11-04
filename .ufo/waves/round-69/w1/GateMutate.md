# GateMutate — R69-C2 mutation probe (seat report, wave w1, round 69)

**Assignment.** Mutation-test the R69-C2 gate: each of its seven checks must be load-bearing.
**Gate under test.** `plans/round69_c2_routed_defects.py`
sha256 `ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485` (unchanged before and
after every run; the lane was never written).
**Scratch root.** `/fast/scratch/hyaku/kengaku-r69/GateMutate` (deleted before yield; receipts are
embedded below).
**Verdict.** `MUTANTS total=7 killed=7 survived=0` on both independently built pre-correction
fixtures, and the gate's own `--selftest` kills all seven deletions. Five coverage findings are
routed below (E1 pinned/write-scope, E3 self-declared input set, E6 "twelve", E7 text-mode
byte comparison, E7 green direction unreachable in a fixture); none is a survivor of the
assigned single-check deletion.

---

## 1. Fixtures (two independent pre-correction constructions)

Both fixtures are scratch copies; no lane byte was touched.

| id | construction | content |
|---|---|---|
| **F1 `fixture-selftest`** | the gate's own `--selftest --work <S>/selftest-work` path, then the stale receipts `_selftest_e7` writes were removed (`rm -rf .../corpus/evidence/round69/gates`). It is a git repo with the selftest's two commits (`tree`, `landing`). | six files + four instrument stubs, registry rows stripped, Round69 criterion removed, one `verified-at:` line, correction lines removed, no provenance, no receipts |
| **F2 `base-lane`** | `git -C L archive a518980e <six paths> \| tar -x -C base-lane`, then `git init` + two commits (`tree`, `landing`) with `git -C "$B" rev-parse --show-toplevel` asserted `== $B` before the first commit | the frozen base bytes (the claims' own do-nothing state) |

Fidelity check, F1 vs F2 sha256 (first 16 hex):

```
SAME SKILL.md                                     f1=544ad892c46a500d base=544ad892c46a500d
DIFF corpus/QUALITY.md                            f1=8ff88919a6004572 base=419fe0d444f264da
DIFF corpus/lessons/round-68.md                   f1=2cdfc4e2709de652 base=e6f5caa4db8c0e55
SAME corpus/knowledge/tb2-network-service-offline-grader.md  f1=573430ee2719f7cc base=573430ee2719f7cc
SAME plans/round63_gate_checks.py                 f1=a98d9c0f75600ea4 base=a98d9c0f75600ea4
SAME corpus/evidence/round62/class-survey.txt     f1=ee30c6984c13985f base=ee30c6984c13985f
```

The two DIFFs are construction artefacts, not corrections: F1's `QUALITY.md` is the selftest's
`# changed` landing marker, and F1's lesson carries an empty `## Corrections (round 69, dated; …)`
heading that the live (mid-landing) lane had already added — the selftest strips correction
*lines*, not that heading. Neither changes an E-verdict: both fixtures emit byte-identical
E1–E7 detail lines (below). **F2 is the primary fixture** (frozen pre-correction bytes); F1 is
the second, independent witness that the selftest construction is robust to a partially
corrected live lane.

Lane state at seat start and end (read-only, unchanged by this seat): HEAD `b288e8e0`; dirty
with `M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/knowledge/tb2-network-service-offline-grader.md`,
`M corpus/lessons/round-68.md`, `?? corpus/evidence/round69/`, `?? .ufo/waves/round-69/w1/`.
Other seats were landing corrections concurrently; this seat read the lane only.

---

## 2. Unmutated baseline — must be 7

Exact argv (cwd irrelevant; `--root` is absolute):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c2_routed_defects.py --root <S>/fixture-selftest
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c2_routed_defects.py --root <S>/base-lane
```

Raw output, identical for both fixtures:

```
E1 defect rows=0/4 missing=['round68_c1_pypi_finish', 'round68_c2_correction_gate', 'round68_report_contract', 'round68_capability_table'] thin=[]
E2 defect headings=0 q50=False round68-lesson=False spotcheck=False
E3 defect corpus/evidence/round69/c2-receipts/provenance-erratum.txt missing
E4 defect verified-at-lines=1 last-names-landing=False
E5 defect strict-lines=0
E6 defect rerecord-lines=0
E7 defect problems=['corpus/evidence/round69/gates/depth-gate.txt:missing', 'corpus/evidence/round69/gates/trio.txt:missing']
DEFECTS n=7
PREDICATE R69-C2 fail
rc=1
```

Calibration: every red names exactly the defect it is supposed to price — E1 missing rows, E2
no criterion section, E3 no erratum, E4 only one `verified-at:`, E5 no strict-share line, E6 no
re-record line, E7 no receipts. No check is red for an unrelated reason.

---

## 3. Family A — single-check deletion, n = 1..7 (the assigned probe)

Mutation definition: inside `check()`, the single funnel

```python
    def rec(n, ok, detail):
        results.append((n, ok, detail))
```

was replaced by

```python
    def rec(n, ok, detail):
        if n == <k>:
            ok = True
        results.append((n, ok, detail))
```

so check *k* can no longer report a defect and cannot contribute to `DEFECTS`. This is the
minimal single-point deletion; `diff -u gate m1.py` shows exactly two added lines and nothing
else:

```
@@ -135,6 +135,8 @@
     results = []
 
     def rec(n, ok, detail):
+        if n == 1:
+            ok = True
         results.append((n, ok, detail))
         print(f"E{n} {'ok' if ok else 'defect'} {detail}")
```

Each mutant was written to `S/mutants/m<n>.py` and run as
`python3 <S>/mutants/m<n>.py --root <fixture>` (driver: `S/mutation_driver.py`).

Raw output (`familyA.txt`):

```
GATE /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c2_routed_defects.py sha256=ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485
UNMUTATED fixture=selftest-built defects=7 rc=1
UNMUTATED fixture=base-bytes-a518980e defects=7 rc=1
MUTANT m1 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E1:defect->ok sha256=cc37fc46ee8b498b
MUTANT m1 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E1:defect->ok sha256=cc37fc46ee8b498b
MUTANT m2 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E2:defect->ok sha256=700a9a4d4b78a759
MUTANT m2 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E2:defect->ok sha256=700a9a4d4b78a759
MUTANT m3 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E3:defect->ok sha256=7ce80d528d616cdd
MUTANT m3 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E3:defect->ok sha256=7ce80d528d616cdd
MUTANT m4 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E4:defect->ok sha256=5bde9c30f5cd718b
MUTANT m4 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E4:defect->ok sha256=5bde9c30f5cd718b
MUTANT m5 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E5:defect->ok sha256=875a5c6c59e50347
MUTANT m5 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E5:defect->ok sha256=875a5c6c59e50347
MUTANT m6 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E6:defect->ok sha256=9cb386f586901062
MUTANT m6 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E6:defect->ok sha256=9cb386f586901062
MUTANT m7 fixture=selftest-built defects=6 rc=1 verdict=KILLED flipped=E7:defect->ok sha256=2462c99bde16daaf
MUTANT m7 fixture=base-bytes-a518980e defects=6 rc=1 verdict=KILLED flipped=E7:defect->ok sha256=2462c99bde16daaf
MUTANTS total=7 killed=7 survived=0
```

| mutant | check deleted | defects (F1) | defects (F2) | expected | verdict |
|---|---|---|---|---|---|
| m1 | E1 registry-rows | 6 | 6 | 6 | KILLED |
| m2 | E2 quality-criterion | 6 | 6 | 6 | KILLED |
| m3 | E3 receipt-provenance | 6 | 6 | 6 | KILLED |
| m4 | E4 verified-at | 6 | 6 | 6 | KILLED |
| m5 | E5 attack-arithmetic | 6 | 6 | 6 | KILLED |
| m6 | E6 results-rerecord | 6 | 6 | 6 | KILLED |
| m7 | E7 gate-receipts | 6 | 6 | 6 | KILLED |

Full mutant sha256:

```
cc37fc46ee8b498b000f36f1565790a82fb74fd0f86a0ac579e032ffe7a4dd00  m1.py
700a9a4d4b78a759e699a84d538f768b55ed44e3b2ddb52df30e36606d4a545f  m2.py
7ce80d528d616cdd6731ba253045f7a88ef112f510ad85c4949395f2a651479a  m3.py
5bde9c30f5cd718bef06ac218746817cf8e3bcc031a7bd2c5658166dc106460c  m4.py
875a5c6c59e50347d363deceb1715844fbd414674279bc532394fabe5425f9da  m5.py
9cb386f586901062e3fca38e4f3e4a9f32cdc05152c4a28aca94062994126522  m6.py
2462c99bde16daaf6ca72ba97f41732e4ac53550b273066ddf7aa277cb704909  m7.py
```

**Calibration caveat (stated so the result is not over-read).** Family A is run against an
all-red fixture, so it proves exactly one thing: each check contributes one defect to the
count. It cannot detect redundancy *inside* a check, nor a check that is red for the wrong
reason. Section 5 answers that separately.

---

## 4. Second detector — the gate's own `--selftest` against each mutant

Exact argv (in-process, because `selftest()` derives its lane from `__file__`; the module's
`__file__` was pinned to the real lane path, read-only, and each `--work` dir was under S):

```
python3 <S>/selftest_mutants.py
```

Raw output (`selftest-mutants.txt`):

```
m1 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
m2 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
m3 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
m4 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
m5 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
m6 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
m7 rc=1 fake=DEFECTS n=6 :: SELFTEST defects-in-fake=6 want=7 all-fail=False
```

The unmutated gate's own tally, exact argv
`python3 plans/round69_c2_routed_defects.py --selftest --work <S>/selftest-final` (rc 0):

```
SELFTEST defects-in-fake=7 want=7 all-fail=True
SELFTEST e7-stale-red=True rc=1
```

So the "a check that cannot fail refuses the gate" control is real: every single-check deletion
turns `all-fail` False and the selftest exits 1.

---

## 5. Family B — sub-assertion probes (supplementary; per-branch discrimination)

Family A cannot see inside a check, so each sub-assertion was probed on a *matched near-miss*
fixture that violates exactly one clause: the unmutated gate must report the check red, and
deleting the responsible branch must turn it green. Driver `S/subfam.py`; raw output
(`familyB.txt`):

```
E1-GREEN defects=6 E1=ok rc=1
NEARMISS e1-cells fixture=fixture-e1-cells E1=defect expect=defect
  SUBMUTANT e1-cells E1=ok verdict=KILLED sha256=a3c60de18e7c7624
NEARMISS e1-noentry fixture=fixture-e1-noentry E1=defect expect=defect
  SUBMUTANT e1-noentry E1=ok verdict=KILLED sha256=59a387a5ee13a739
NEARMISS e1-absent fixture=fixture-e1-absent E1=defect expect=defect
  SUBMUTANT e1-absent E1=ok verdict=KILLED sha256=e93d68ec2cb02a21
NEARMISS e1-verdict fixture=fixture-e1-verdict E1=defect expect=defect
  SUBMUTANT e1-verdict E1=ok verdict=KILLED sha256=3fa823620c7fe38e
NEARMISS e1-selftest fixture=fixture-e1-selftest E1=defect expect=defect
  SUBMUTANT e1-selftest E1=ok verdict=KILLED sha256=3b7ff7d07c86b0e0
UNDERCHECK e1-empty-pinned-and-write-scope E1=ok detail=E1 ok rows=4/4 missing=[] thin=[]
E3-GREEN tree=b5a8a871 landing=5d923d16 E3=ok detail=E3 ok inputs=2 differs=['corpus/QUALITY.md'] problems=[]
NEARMISS e3-tree-sha fixture=fixture-e3 E3=defect expect=defect
  SUBMUTANT e3-tree-sha E3=defect verdict=SURVIVED sha256=4f79dea4f69b4d0c
  DETAIL E3 defect inputs=2 differs=['SKILL.md', 'corpus/QUALITY.md'] problems=['tree-sha:SKILL.md', "differs-set got=['corpus/QUALITY.md'] want=['SKILL.md', 'corpus/QUALITY.md']"]
NEARMISS e3-landing-sha fixture=fixture-e3 E3=defect expect=defect
  SUBMUTANT e3-landing-sha E3=defect verdict=SURVIVED sha256=11a43c0fb2c38109
  DETAIL E3 defect inputs=2 differs=['SKILL.md', 'corpus/QUALITY.md'] problems=['landing-sha:SKILL.md', "differs-set got=['corpus/QUALITY.md'] want=['SKILL.md', 'corpus/QUALITY.md']"]
NEARMISS e3-differs fixture=fixture-e3 E3=defect expect=defect
  SUBMUTANT e3-differs E3=ok verdict=KILLED sha256=921ecd1ff05e3f18
  DETAIL E3 defect inputs=2 differs=['corpus/QUALITY.md'] problems=["differs-set got=['SKILL.md'] want=['corpus/QUALITY.md']"]
UNDERCHECK e3-omitted-changed-input E3=ok detail=E3 ok inputs=1 differs=[] problems=[]
UNDERCHECK e6-no-twelve E6=ok detail=E6 ok rerecord-lines=1
NEARMISS e3-tree-sha-isolated fixture=fixture-e3 E3=defect expect=defect
  SUBMUTANT e3-tree-sha-isolated E3=ok verdict=KILLED sha256=4f79dea4f69b4d0c
  DETAIL E3 defect inputs=2 differs=['SKILL.md', 'corpus/QUALITY.md'] problems=['tree-sha:SKILL.md']
NEARMISS e3-landing-sha-isolated fixture=fixture-e3 E3=defect expect=defect
  SUBMUTANT e3-landing-sha-isolated E3=ok verdict=KILLED sha256=11a43c0fb2c38109
  DETAIL E3 defect inputs=2 differs=['SKILL.md', 'corpus/QUALITY.md'] problems=['landing-sha:SKILL.md']
```

Notes that matter for reading it:

- `E1-GREEN` / `E3-GREEN` are the green directions: a fixture with four complete synthetic
  registry rows, and a fixture with a self-consistent synthetic erratum at the fixture's own
  two revisions (`TREE`/`LANDING` patched **in-process only** to those fixture revs; the frozen
  `27f649f8`/`1ec2e60a` constants were never edited on disk). Both checks reach `ok`, so neither
  is stuck red.
- `e3-tree-sha` and `e3-landing-sha` are marked SURVIVED because that near-miss violated **two**
  clauses at once: a wrong sha makes `at-tree != at-landing`, which drags the path into
  `observed_differs` and trips the DIFFERS clause too. The isolated arms (wrong sha, DIFFERS kept
  consistent with the written values) kill both branches. So the sha clauses are individually
  load-bearing; the SURVIVED rows are *coupling*, not vacuity.

---

## 6. Findings a claim's attacker should use

Ordered by how much they weaken R69-C2's frozen sentence; none edits the gate (no seat may).

**F1 — E1 does not price "pinned values" or "write scope" (coverage, medium).**
The frozen E1 sentence says each row carries "a self-test cell, pinned values and write scope".
The code tests only `len(cells) >= 8`, `entry` present in the entry cell, the entry file exists,
`` `0` ``/`` `1` `` in the verdict cell, and a non-empty self-test cell. A fixture whose four rows
have **empty cells 5 and 6** (pinned values, write scope) is accepted:
`UNDERCHECK e1-empty-pinned-and-write-scope E1=ok detail=E1 ok rows=4/4 missing=[] thin=[]`.
So a registry row can satisfy E1 while carrying neither pinned values nor a write scope. The
landing can pass E1 with a row that is thinner than the frozen sentence.

**F2 — E3's "every bound input" is self-declared; omission is unpriced (coverage, medium).**
`observed_differs` is built only from the erratum's own `INPUT` lines, so the DIFFERS comparison
is an internal-consistency test, never a completeness test. An erratum listing a single unchanged
input and no `DIFFERS` line is accepted while `corpus/QUALITY.md` demonstrably differs between
`TREE` and `LANDING`:
`UNDERCHECK e3-omitted-changed-input E3=ok detail=E3 ok inputs=1 differs=[] problems=[]`.
The gate re-derives the shas it is told to re-derive; it has no external bound-input manifest to
re-derive the *set* from. E3's "every bound input" is therefore only as strong as the erratum's
own list.

**F3 — E6 does not price "twelve" (coverage, low).**
The frozen E6 sentence says the record "points at the twelve per-seat reports"; the code requires
`w1-results.json`, `output: ""`, and `per-seat`. A line with no count is accepted:
`UNDERCHECK e6-no-twelve E6=ok detail=E6 ok rerecord-lines=1`.

**F4 — E7's "byte for byte" is text-mode (calibration, low).**
`check()` compares `fresh != path.read_text(encoding="utf-8")` and `run_command` uses
`text=True`, so line-ending differences are normalized away. Probe (`crlf.txt`, two CRLF lines):
`raw_has_crlf=True`, `read_text_has_cr=False`, `byte_equality_would_differ=True`,
`text_comparison_equal_to_lf=True`. A receipt committed with CRLF would compare equal to an LF
fresh run. The claim's phrase "byte for byte" is not what the code measures.

**F5 — E7's green direction cannot be witnessed in a fixture (calibration, low; already
disclosed by the gate).**
Running E7's depth arm inside `fixture-e1` gives
`ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=2 share=0.06` /
`PREDICATE R63-C2 fail`, rc 1 — the fixture lacks the 33 referenced evidence paths. Therefore
`_selftest_e7` can only exercise the stale-receipt (red) arm, and the green arm rests entirely on
the landing run. This matches the gate's own docstring; it is recorded so the close does not
mistake `e7-stale-red=True` for two-sided evidence.

**F6 — structural coupling inside E3 (informational).**
A wrong at-tree/at-landing sha also flips that input into `observed_differs`, so the DIFFERS
clause re-catches sha errors unless the erratum's DIFFERS set is kept consistent with its own
wrong values. Not a defect; it means E3's reported problem list can name two clauses for one
error, and a reader should not count problems as independent findings.

---

## 7. Restoration and write-scope evidence

- The gate file's sha256 is `ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485`
  before the first run and after the last run — identical. No mutant was ever written into the
  lane; all seven live under `S/mutants/`.
- The lane's `git status --porcelain` at seat start and at seat end is the same eight entries
  (`M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/knowledge/tb2-network-service-offline-grader.md`,
  `M corpus/lessons/round-68.md`, `?? .ufo/waves/round-69/w1.ready`,
  `?? .ufo/waves/round-69/w1.ready.dispatched`, `?? .ufo/waves/round-69/w1/`,
  `?? corpus/evidence/round69/`) — these are other seats' concurrent landings, not mine.
  HEAD stayed `b288e8e0`.
- Git writes were confined to two scratch fixtures: `base-lane` (`git init` only after
  `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$B" ] || git init`, then
  `rev-parse --show-toplevel` asserted `== $B` before the first commit) and `fixture-e3`
  (asserted not a repo, `git init`, then `rev-parse --show-toplevel` asserted `== e3` before the
  first commit). The `fixture-selftest` repo was created by the gate's own `--selftest`.
- All scratch (`/fast/scratch/hyaku/kengaku-r69/GateMutate`) is deleted after this report; the
  receipts above are the preserved evidence.

---

## 8. Commands explicitly NOT run

- **The R69-C1 nginx battery** (`plans/round69_c1_nginx_probe.py`) — not this seat's item; no
  bind of 127.0.0.1:8080, no port-lock acquisition, no `ss -ltnp` needed.
- **The unmutated gate against the real lane as a scored run** (`python3
  plans/round69_c2_routed_defects.py` with no `--root`) — the lane was mid-landing; the green
  run is the close's.
- **E7's green arm / the `trio` command** — E7 short-circuits on missing receipts in every
  fixture, so `plans/round63_gate_checks.py trio` never executed; the depth arm was run once
  manually in `fixture-e1` (rc 1, §F5).
- **Any mutation of the lane, any git/jj write in L, any write to `.ufo/state/`, `MANIFEST.json`,
  sibling lanes or the fleet root.**
- **Any package install or upgrade** — no tool was needed (Python 3.14.8 present); no `pacman`,
  `uv`, `npx` or binary install was attempted, so there is no tool/version/channel entry to
  record.

---

## 9. Bottom line

`MUTANTS total=7 killed=7 survived=0`. Against the frozen pre-correction state (two independent
fixtures) and against the gate's own `--selftest`, every one of E1–E7 is load-bearing for the
`DEFECTS` tally, and every sub-assertion probed in §5 is individually load-bearing on a matched
near-miss. The gate is not vacuous. What it does **not** price — E1's pinned-values/write-scope
cells, E3's completeness over an externally defined input set, E6's "twelve", and E7's
byte-level (vs text-level) equality — is routed as F1–F4 for the claim's attacker; those are
coverage findings against the frozen sentence, not permission to edit the gate.
