# MutC1 — mutation / forgery attack on R97-C1 and R97-C2

Seat: mutation-tester (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, round 97.
Measured tip **T = `f1083da60e7ff6b88f7420aae7424f7762d14700`**, BASE `4992cd0e`, freeze F `8d9d2713`.
Scratch: `/fast/scratch/hyaku/kengaku-r97/MutC1` (six `--shared` clones at T, detached; `TMPDIR` explicit).
No lane, fleet or sibling edit; no `task` call; no sysctl/service change; all Git writes named the
clone root after `git rev-parse --show-toplevel` printed it. Every mutant is a commit in a private
clone; the clone was reset to T after each probe (`restored=True`, `git status --porcelain` empty,
`HEAD == T`).

Axes attacked: **coverage** (one falsifier per leg L1–L9 of the frozen C1 counter) and **calibration**
(forged receipt, ledger-only claim, pinned-vs-unpinned version drift, and the C2 registry detector).

## Frozen commands (run exactly as the claims file writes them)

```
# C1, from the lane root
python3 plans/round97_c1_replay.py --lane . --rev T --work DIR --grader-venv G
# C2
python3 plans/round97_gate_selftest_census.py --lane . --rev T
```

Venv G staged per the contract: `uv venv -p 3.13 G && uv pip install --python G/bin/python
rdflib==7.1.4 pytest==8.4.1` → CPython 3.13.16, rdflib 7.1.4, pytest 8.4.1, pyparsing 3.3.3.

## Baselines (pristine T)

| command | rc | observed |
|---|---|---|
| C1 at T | 0 | `LEGS L1..L9=pass`; `TARGET executed_rows=41 member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18 legs=72 mismatches=0 defects=0`; `PREDICATE R97-C1 pass` (18.1 s) |
| C2 at T | 0 | `ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0`; `GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0`; `MISMATCH_TOTAL n=0`; `PREDICATE R97-C2 pass` |
| C2 at BASE | 1 | `GATES total=127 with_selftest=83 without=44`; `MISMATCH_TOTAL n=44`; `PREDICATE R97-C2 fail` (matches the frozen BEFORE) |

Receipts: `c1-baseline-T.txt`, `c2-baseline-T.txt`, `c2-baseline-BASE.txt`.

## C1 — one falsifier per leg

Each row is a separate commit on a clone at T; the frozen command was run against that revision
(`--rev <mutant>`), everything else unchanged. `killed` = the frozen command rejects the mutated
tree (leg fail rc 1, or setup refusal rc 2); `survived` = it still prints `PREDICATE R97-C1 pass`.

| mutant | mutation | expected | observed (LEGS) | rc | verdict |
|---|---|---|---|---|---|
| c1-L1-receipt-absent | delete the receipt | L1 fail | L1,L2,L3,L5,L6,L9 fail | 1 | **killed** |
| c1-L2-subject-forged | receipt `SUBJECT_SHA` → zeros | L2 fail only | L2 fail only | 1 | **killed** |
| c1-L2-capture-byte | append a byte to `tests/test.sh` | L2 fail | probe refuses: `DEFECT SETUP capture sha mismatch tests/test.sh`, `could-not-evaluate` | 2 | **killed** (setup refusal; L2 line never printed) |
| c1-L3-tip-orphan | receipt `LANE_TIP` → orphan commit | L3 fail only | L3 fail only | 1 | **killed** |
| c1-L4-table-reformat | whitespace-only change to `round97-cases.json` + receipt `CASE_TABLE_SHA` updated to match | L4 fail only | L4 fail only | 1 | **killed** |
| c1-L5-predicted-token | receipt C07 `predicted=` token changed | L5 fail | L5 + L6 fail | 1 | **killed** |
| c1-L5-drop-case | drop C18 CASE+DETAIL | L5 coverage fail | L5 + L6 fail | 1 | **killed** |
| c1-L6-detail-forge | C07 DETAIL `rows=5`→`4` | L6 fail only | L6 fail only | 1 | **killed** |
| c1-L6-graderside-forge | receipt `GRADER_SIDE` rdflib 7.1.4→7.1.5 | L6 stamp fail | L6 fail only | 1 | **killed** |
| c1-L6-unpinned-forge | receipt `GRADER_UNPINNED` 3.13.16/3.3.3 → 3.13.99/3.2.0 | pass (not compared) | all pass | 0 | **survived (by design)** |
| c1-L7-status-pending | member `status` executed→pending | L7 fail only | L7 fail only | 1 | **killed** |
| c1-L7-remove-base | demote BASE member `build-pmars` | L7 fail (set_removed) | L7 fail only, `set_removed=['build-pmars']` | 1 | **killed** |
| c1-L7-extra-executed | add executed member `zzz-calibration-ghost` | (claim's literal TARGET) | all pass; `executed_rows=42 … cells=file-artifact:33` | 0 | **survived** (see F1) |
| c1-L7-classes | member `classes` += `subprocess-exec` | L7 fail only | L7 fail only | 1 | **killed** |
| c1-L7-legacy-receipt | member `receipt` → another path | L7 fail only | L7 fail only | 1 | **killed** |
| c1-L8-probe-comment | append a comment to the probe + receipt `TOOL_SHA` updated | L8 fail only | L8 fail only | 1 | **killed** |
| c1-L9-bash | receipt `HOST_BASH` → 9.9.9 | L9 fail only | L9 fail only | 1 | **killed** |
| c1-L9-toolsha | receipt `TOOL_SHA` → zeros | L9 fail | L6 + L9 fail | 1 | **killed** |
| c1-forged-receipt | every DETAIL line rewritten to a plausible `rows=4 … names=-` | L6 fail | L6 fail only | 1 | **killed** |
| c1-ledger-only-base | BASE tree + ledger flip only (no receipt, no capture, no probe) | L7 pass, claim impossible | L7 pass; L1–L6,L8,L9 fail | 1 | **killed** (ledger alone insufficient) |
| c1-L2-member-field | receipt `MEMBER` → `other-grader` | (informational) | all pass | 0 | **survived** (F4) |
| c1-L6-legorder-field | receipt `LEG_ORDER` → `a,b,c,d` | (informational) | all pass | 0 | **survived** (F4) |

### Forged receipt, strongest form (forged sandbox)

`fakebwrap` delegates to the real `/usr/bin/bwrap` except for the harness call, where it emits the
case table's predicted vector and a fabricated DETAIL. Running the **public probe** with it produced
a complete, internally consistent receipt (rc 0, `mismatches 0`, 18/18 `ok=True`; sha256
`8cabe7cf…`), committed in place of the real receipt (`acfaacf7…`).

| invocation | rc | observed | verdict |
|---|---|---|---|
| replay at the forged receipt, **default** `/usr/bin/bwrap` | 1 | `L6=fail` (`obs=36 want=36 equal=False stamps_equal=True`) | **killed** |
| replay at the same receipt, `--bwrap fakebwrap` | 0 | `LEGS L1..L9=pass`, `PREDICATE R97-C1 pass` | **survived** (non-predicate invocation; F2) |

The first `--bwrap fakebwrap` attempt was **invalid** (the fake sandbox needed `MUT_TABLE` in the
environment; the probe returned rc 1 and the replay reported `L6=fail rerun rc=1`). Re-run with the
environment set, as recorded above. The first ledger-only attempt was also **invalid** (the clone was
checked out at BASE, where `plans/round97_c1_replay.py` does not exist); re-run with T's script
against the BASE+ledger clone, as recorded above.

### Pinned vs unpinned version drift (venv level, T tree)

| venv | versions | rc | observed | label |
|---|---|---|---|---|
| G (control) | 3.13.16 / 7.1.4 / 8.4.1 / 3.3.3 | 0 | all legs pass | control |
| Grdflib | rdflib **7.1.3** | 2 | `DEFECT SETUP venv … 'VERSIONS 3.13.16 7.1.3 8.4.1 3.3.3'` | **invalid** (pinned guard fires) |
| Gpytest | pytest **8.4.0** | 2 | `DEFECT SETUP venv … 8.4.0 …` | **invalid** (pinned guard fires) |
| G312 | CPython **3.12.15** | 2 | `DEFECT SETUP venv … 3.12.15 …` | **invalid** (minor guard fires) |
| Gunpinned | pyparsing **3.2.0** (unpinned) | 0 | all legs pass | **survived (by design)** |

### Setup guards (T tree)

`wrong cwd` → rc 2 `cwd … is not the lane root`; `--bwrap /nonexistent` → rc 2
`sandbox-unavailable`; unresolved `--rev` → rc 2 `unresolved-revision`. All **invalid** by design.

## C2 — registry detector falsifiers

Each row is a commit on a clone at T; the census was run with the mutated detector on the mutated
revision, and the gate's own `--selftest` was run from the same tree.

| mutant | mutation | census (rc / findings) | selftest | verdict |
|---|---|---|---|---|
| c2-M1-revert-kind | `ledger-tip` probe→gate | 1 / MISMATCH 1 | pass | **killed** |
| c2-M2-blanket | `interval-reverdict` gate→probe | 1 / DEMOTED 1 | pass | **killed** |
| c2-M3-cell-forge | `ledger-tip` self-test cell → `--selftest` | 1 / CELL-CHANGED 1 | pass | **killed** |
| c2-M4-delete-row | delete `ledger-tip` | 1 / ROW-REMOVED | pass | **killed** |
| c2-M5-duplicate-row | duplicate `ledger-tip` | 1 / ROW-DUPLICATE | pass | **killed** |
| c2-M6-script-forge | append `if "--selftest" in sys.argv` to `ledger_tip.py` | 1 / SCRIPT-CHANGED + DEMOTED | pass | **killed** |
| c2-M7-comment-forge | revert kind to gate **and** append `# "--selftest" in sys.argv (comment)` | 1 / SCRIPT-CHANGED; **MISMATCH 0** | pass | **killed** by anti-laundering; MISMATCH fooled (F6) |
| c2-M8-new-gate-plain | new gate row + script with no spelling | 1 / MISMATCH | pass | **killed** |
| c2-M9-dead-branch | new gate row + `if False and "--selftest" in sys.argv` | 0 / none | pass | **survived** (F6) |
| c2-M10-prose-mention | new gate row + comment `# … "--selftest" in prose only` | 0 / none | pass | **survived** (F6) |
| c2-M11-kind-case | `ledger-tip` kind → `Gate` | 0 / none | pass | **survived** (F7) |
| c2-M12-no-script-entry | probe row entry → `python3 -m ledger_tip` | 1 / CELL-CHANGED only | pass | **killed** (wrong leg; see M18) |
| c2-M13-narrow-p2 | drop detector pattern `["']--self-?test["']\s*(?:in|==|not in)\b` | 0 / none | **fail 1** | **killed** by selftest |
| c2-M14-always-true | `has_selftest` → `True` | 1 / DEMOTED 44 | **fail 6** | **killed** |
| c2-M15-always-false | `has_selftest` → `False` | 1 / MISMATCH 84 | **fail 6** | **killed** |
| c2-M16-narrow-p1 | drop `add_parser\(\s*["']self-?test["']` pattern | 1 / MISMATCH 1 (`round54-c1`) | **pass** | **killed** by census only (F8) |
| c2-M17-narrow-p3 | drop `(?:\bin|==)\s*\(?["']--self-?test["']` pattern | 1 / MISMATCH 4 (`stage-scan`, `round85/86-c1-replay`, `round86-c2-repin`) | **pass** | **killed** by census only (F8) |
| c2-M18-new-gate-no-script | new gate row whose entry names no `.py/.sh/.mjs` | 1 / MISMATCH `no-script` | pass | **killed** |

Invocation controls: `--base T --rev T` at T → rc 0 (vacuous anti-laundering; non-predicate
invocation, F9); no `--rev` → rc 2 `--rev REV is required`; `--selftest --work` at T → rc 0
`SELFTEST cases=8 failed=0`.

## Claim-shape verification at T (read-only, independent of the counters)

- 10/10 `frozen-instruments` sha256 match at T; 3/3 `candidate-bytes` sha256 match at T.
- Registry: exactly **44** rows change kind, all `gate→probe`; **0** other cells change in those
  rows; **3** rows are new (`round97-sparql-probe`, `round97-c1-replay`,
  `round97-gate-selftest-census`); **0** of the 44 scripts differ BASE→T.
- Kind population at T: 84 `gate`, 87 `probe` (171 rows); all 84 gate scripts have at least one
  spelling hit on a non-comment line (0 comment-only / prose-only hits).
- Ledger: only `sparql-university` differs BASE→T; executed 40→41; no member removed.

## Findings

**F1 (C1, calibration, medium).** L7 is keyed to set containment, never to the printed total. An
unearned executed member passes the counter (`executed_rows=42`, `cells=file-artifact:33`,
`PREDICATE pass`). The claim's *literal* TARGET line (`executed_rows=41 … cells=file-artifact:32`)
still rejects it, so the claim is not violated on the candidate bytes — but the counter's exit code
alone does not enforce the number it prints.

**F2 (C1, trust boundary, info).** L6 trusts the `--bwrap` binary it is handed. A forged sandbox that
fabricates harness payloads yields a receipt that passes all nine legs when the counter is invoked
with that same sandbox, and is killed by the default `/usr/bin/bwrap`. The frozen predicate does not
pass `--bwrap`, so the claim holds only when the command is run as written.

**F3 (C1, by design).** `GRADER_UNPINNED` (CPython micro, pyparsing) is not compared: forging it, and
running a pyparsing-3.2.0 venv, both pass. The pinned values are enforced: rdflib 7.1.3, pytest
8.4.0 and CPython 3.12.15 each make the counter refuse (rc 2). This is the documented round-96 W-2
behaviour.

**F4 (C1, informational, low).** Receipt `MEMBER` and `LEG_ORDER` are parsed but never compared;
forging either passes. The claim does not pin them.

**F5 (C1, reporting, low).** A tampered capture is rejected as `could-not-evaluate` (rc 2) before any
`LEGS` line is printed, so L2's own fail line is never shown. Rejection is correct; the diagnostic is
a setup refusal rather than a leg fail.

**F6 (C2, detector sensitivity, medium).** The spelling regex counts a comment/prose mention
(`# … "--selftest" in …`) and a dead branch (`if False and "--selftest" in sys.argv`) as a self-test;
new gate rows carrying only those pass the census. This contradicts the census docstring's "not a
mention in prose". The T population is clean (0 comment-only hits among 84 gate scripts), so the
44→0 result is not inflated by this gap; it is a future-forgery surface.

**F7 (C2, population definition, low).** Kind matching is exact lowercase and the kind cell is
excluded from CELL-CHANGED, so a row typed `Gate` escapes both MISMATCH and CELL-CHANGED. At T every
gate row is exactly `gate`.

**F8 (C2, selftest coverage, low-medium).** The gate's `--selftest` does not exercise 2 of its 6
detector spellings: dropping the `add_parser("selftest")` pattern (M16) or the `in|== "--selftest"`
pattern (M17) leaves the selftest green, while the census at T reports 1 and 4 MISMATCH. Pattern 2
narrowing is caught by the selftest (M13). The selftest is therefore not a complete falsifier of its
own detector; the real population is.

**F9 (C2, invocation, info).** `--base T` at T passes vacuously (the anti-laundering legs compare T
with itself). The frozen predicate pins the default BASE, so this is a non-predicate invocation.

**F10 (both, info).** Each counter's own bytes are pinned only in the claims file, not by any leg
(a counter cannot verify itself). I verified all 10 frozen-instrument hashes and all 3 candidate-byte
hashes at T independently; they match.

## Verdict

- **R97-C1: independently exercised and falsified at every leg.** 18/22 receipt mutants killed by
  the frozen replay, plus the forged-sandbox receipt killed under the default `--bwrap` (19 killed in
  all; one falsifier per L1–L9, plus forged receipt, forged sandbox, ledger-only and pinned-version
  drift). 5 survived, all explained: three by explicit design (unpinned versions; two
  informational receipt fields), one by the claim's literal-text predicate rather than the counter
  (extra executed row, F1), and one only under a non-predicate `--bwrap` invocation (F2). No survivor
  flips the frozen predicate on the candidate bytes.
- **R97-C2: independently exercised and falsified.** 14/18 mutants rejected by the census itself;
  M13 is rejected only by the gate's own `--selftest` (census green, selftest red); 3 survive both
  (dead branch, comment mention, capital-`Gate`) and are absent from the T population. The claim's byte shape (44 kind cells, no old script, 3 new rows, ledger 40→41) is
  exactly as stated, and the 44→0 result reproduces at T and fails 44 at BASE.
- No production defect found that would move either claim to *not met* under the frozen commands.
  Findings F1, F2, F6, F8 are routed as calibration limits for round 98, not repaired here.

## Restoration evidence

Every mutant: clone reset to `--detach T`, `git clean -fdq`, `git status --porcelain` empty,
`HEAD == f1083da6…` (per-mutant `restored: true` in `summary-fx*.json`; final clone states and the
overwritten-summary note in `restoration.txt`). The forged
receipt commit (`3785c073…`) and the ledger-only commit (`bfcaaa18…`) are unreferenced objects in
private clones only; the lane was never written. Scratch `/fast/scratch/hyaku/kengaku-r97/MutC1`
removed after these receipts were copied.

## Receipts

- `.ufo/waves/round-97/w1/MutC1/` — all mutant outputs (`c1-*.txt`, `c2-M*.census.txt`,
  `c2-M*.selftest.txt`), baselines (`c2-baseline-*.txt`), guards (`c1-guard-*.txt`), venv matrix
  (`venv-*.txt`), forged-sandbox runs (`bwrap-*.txt`), per-clone summaries (`summary-fx*.json`),
  the driver (`drive.py`), the forged sandbox (`fakebwrap`), `restoration.txt`, and `SHA256SUMS`.
- Machine-readable matrix: `.ufo/waves/round-97/w1/MutC1/matrix.json` (22 C1 rows, 18 C2 rows).
- Key hashes: real receipt at T `acfaacf71b69e3ec64b520ba2db16b578ac3eccff7f50705bbcfdb06417b0602`;
  forged receipt `8cabe7cf258c4a2f9e2658a3226524d674484a327a254cd42fa454260328c24a`; claims file at T
  `a7ad0a9da9fb07adaef31d7f86029d265b7884b0d023f0717b798aeef62185b3`.
- Tool installs: none (pre-installed `uv` only; `bubblewrap 0.13.1` from the host).

Report: .ufo/waves/round-97/w1/MutC1.md
