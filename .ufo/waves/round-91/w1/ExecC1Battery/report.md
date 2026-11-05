# R91-C1 control battery — ExecC1Battery (wave round-91 w1)

Battery over `plans/round91_c1_replay.py` (frozen bytes at tip C `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`)
and the receipt `corpus/evidence/round91/modernize-probe.txt`. Machine-readable results:
`controls.txt` beside this file (9 CONTROL lines: the positive plus 8 controls; every observed rc
recorded as measured, never adjusted).

## Provenance

- Scratch: `S=/fast/scratch/hyaku/kengaku-r91/ExecC1Battery`; clone `$S/lane` =
  `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin` then
  `git -C $S/lane checkout -q a8de3e6933a220ad12e3fb3523ce4627a44c8cf0` (detached). Verified
  `git -C $S/lane rev-parse --show-toplevel` = `$S/lane` before every commit. Lane itself never
  modified (no commit/add/stash/checkout/reset/jj in the lane; verified `git status --porcelain`
  empty after each control's `reset --hard` back to C inside the clone).
- Every tamper control = one scratch commit in the clone, then the counter run with
  `--rev <control commit> --work $S/w-<name>`; TMPDIR pointed into `$S`.
- Host stamps at run time (match the receipt stamp): `Python 3.14.8`,
  `OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)`,
  `/proc/sys/user/max_user_namespaces` = `122865`; `/usr/bin/bwrap` present (L6 rerun executed,
  ~33 s per run).
- Control revisions (all scratch commits, parented on C unless noted): ledger-only
  `9d010ad47df882947c015e8d68aa2a907fe1e32e`; forged-tip `a458f262ced1108590e12e2aa7c1cc9d5ddfac9d`
  (receipt `LANE_TIP` = sibling `092783dbc59954bc21829c18473b186a54829edd`, built as
  `git commit-tree a8de3e69^{tree} -p a8de3e69^`, proven non-ancestor by
  `git merge-base --is-ancestor` rc 1); forged-stamp `297e245b0d75f6086f76b5834190369233bb6ec1`;
  decorative-stamp `dfd4d58fedbb7451b503db121cfecaf39cc39218`; probe-tamper
  `9189e646c39fb69a0ad2fb5f3448fc58a5eab785`.

## Control 2 — parser defect analysis (frozen counter, frozen predicate, no lane edit)

- `parse_receipt()` (`plans/round91_c1_replay.py` lines ~64-86) parses each `CASE` line inside
  `OBSERVATIONS_BEGIN/END` by splitting on whitespace and keeping only tokens containing `=` as
  `key=value` pairs, then reads the case id as `parts.get("id", "?")`.
- The receipt's CASE lines are `CASE <id> predicted=XX observed=XX ok=True
  test_modernized_code_runs=<..>,test_dependency_file_exists=<..>` — the case id is the **second
  whitespace token**, a bare token with no `=`. The parser drops it (no `id=` key exists) and
  substitutes `"?"`.
- What it prints: for each of the 10 cases, `DEFECT L5 receipt names unknown case ?` (10
  identical lines), `mismatches=10 defects=10`, `TARGET ... executed=0`, `PREDICATE R91-C1 fail`,
  rc 1. This is the entire failure at C: no other leg emits a defect in the positive run.
- Scratch-copy repair (only the case-id token extraction changed to `line.split()[1]`; predicate,
  legs and every other line untouched): run at `a8de3e69` gives rc **0**, `TARGET
  executed_rows=35 member=modernize-scientific-stack located=1 executed=1 cases=10 legs=20
  mismatches=0 defects=0`, `PREDICATE R91-C1 pass`. **The parser defect alone accounts for the L5
  failure**: L1-L4 and L6-L9 all pass at C in the same runs; the frozen predicate is not changed.
- Classification: instrument defect in the frozen counter (the receipt format and parser were
  frozen independently; the counter never matched the receipt's id placement). Reported, not
  repaired in the lane, per freeze rules.

## Executed-gating (control 8)

Code path: `plans/round91_c1_replay.py` L262 `all_pass = all(legs)`; L265-267 TARGET print feeds
`executed=` with `1 if all_pass else 0`; L271 `return 0 if all_pass else 1`. No path prints
`executed=1` without `all_pass`. Measured: at the receipt-deleted revision
`9d010ad4…` the TARGET line reads `executed=0` (legs=0, defects=6, first defect L1), rc 1.

## Results (rc measured; full defect lists in controls.txt)

| # | Control | rev | expected | observed | Decisive line |
|---|---------|-----|----------|----------|---------------|
| pos | positive at C | `a8de3e69` | 1 | **1** | 10× `DEFECT L5 receipt names unknown case ?`; executed=0 |
| 2a | parser-baseline (same run as pos) | `a8de3e69` | 1 | **1** | id token dropped → all ids `"?"` |
| 2b | parser-fix (scratch copy, id = token 2) | `a8de3e69` | 0 | **0** | `PREDICATE R91-C1 pass`, defects=0, executed=1 |
| 3 | ledger-only (receipt deleted) | `9d010ad4` | 1 | **1** | first defect `L1 receipt absent at revision: corpus/evidence/round91/modernize-probe.txt` |
| 4 | forged-tip (sibling `092783db`) | `a458f262` | 1 | **1** | first defect `L3 LANE_TIP 092783db… not an ancestor of a458f262ced1` |
| 5 | forged-stamp (TOOL_SHA `e70210cb…`) | `297e245b` | 1 | **1** | `L9 stamp fields mismatch (tool=e70210cb…)` (11th defect line) |
| 6 | decorative-stamp (`HOST_PYTHON Python 9.9.9`) | `dfd4d58f` | 1 | **1** | `L9 stamp fields mismatch (… python=Python 9.9.9 …)` (11th defect line) |
| 7 | probe-tamper (1 appended line) | `9189e646` | 1 | **1** | `L8 probe pin d70210cb… vs bytes be042c25…` + `L9 stamp fields mismatch (tool=d70210cb…)` (11th-12th defect lines) |
| 8 | executed-gating (rev of control 3) | `9d010ad4` | 1 | **1** | TARGET `executed=0` |

## Findings

1. **F1 (new instrument defect, blocks the C1 pass):** `parse_receipt` cannot see the receipt's
   case id — the id lives in a bare second token while the parser only harvests `key=value`
   tokens and defaults to `"?"`. Consequence at the measured tip: 10× `L5 receipt names unknown
   case ?`, `executed=0`, rc 1. This contradicts the frozen claim's "After" prediction
   (`exit 0`, `PREDICATE R91-C1 pass`, `executed=1`) — recorded as a mispredict; the measured
   figure at C is rc 1. A one-token parse repair in a scratch copy (predicate untouched) measures
   the tip green (`executed=1 cases=10 legs=20 mismatches=0 defects=0`, exit 0), proving the
   parser is the sole blocker and every leg L1-L4, L6-L9 passes at C.
2. **Signal-order caveat:** because the L5 noise prints before the L8/L9 defects (defect list is
   ordered by leg), controls 5/6 show their `L9` defect as the 11th line and control 7 shows
   `L8`+`L9` as the 11th-12th; the first-three-DEFECT-lines excerpts in `controls.txt` therefore
   carry the L5 lines and this report/controls.txt carry the decisive tail lines verbatim.
3. **Corroborating measurements:** C2 battery (sibling `ExecC2Battery`) measured its positive at
   C green (rc 0) with the same pin ledger that feeds C1's L8 — consistent with L8 passing here.
4. No defects attributable to the receipt content itself: every tamper control failed exactly at
   its named leg (L1, L3, L9, L8+L9), and the untampered legs stayed green in each run.

## Housekeeping

- Scratch `$S` (clone + w-* dirs) deleted at seat exit; the tree-on-disk defect condition does
  not apply (nothing left behind). Control commits are recoverable only from this report's hashes
  after deletion — outputs were captured verbatim above.
- No tools installed or upgraded for this seat (no installs to record). No pacman use; no sysctl,
  routing or `~/.omp` changes; nothing written outside the lane paths this seat names and `$S`.
