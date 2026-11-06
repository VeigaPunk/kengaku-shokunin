# ReviewerC2 — surgical review of the R95-C2 instruments at T

Seat: ReviewerC2 (leaf; no subagents, no task, no commits, no lane git mutations).
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin (master). Measured tip T = `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`.
Scope: `plans/round95_c2_counter.py` (diffed against `plans/round94_c2_counter.py`), `plans/round95_false_gate_census.py`,
`plans/round95-false-gates.tsv`, and the 14 false-gate files they name. Out of scope for this seat: R95-C1, legacy gate, sources, overlap.

Scratch: `S=/fast/scratch/hyaku/kengaku-r95/ReviewerC2` (clone `$S/lane` = `git clone --shared` + `checkout --detach T`; every counter/census `--work` under `$S`; scratch removed before yield, receipts copied here).
Tool installs: none. Lane: no git/jj mutation; all git calls were read-only (`show`, `log`, `rev-parse`) or in fixture repos with `-C` and asserted toplevel.

## 0. Verdict on the frozen predicates at T (reproduced)

| run | command (cwd = clone at T) | result |
|---|---|---|
| honest counter | `python3 plans/round95_c2_counter.py --lane "$S/lane" --rev T --work "$S/honest"` | rc 0; W1 pass, W2 pass 20/20, W3 pass probes=3 (each probe `SELFTEST cases=15 ok=14`), W4 pass (11/11/0, freeze d9cd18a7519a), W5 pass 10/10; `TARGET legs_passed=5 of 5`; `PREDICATE R95-C2 pass`. Receipt `receipts/honest-counter-T-rerun.txt`. |
| census | `python3 plans/round95_false_gate_census.py --lane "$S/lane" --rev T --work "$S/census"` | 14 × `GATE … passes=0 designated_red=1`; `HONEST rc=0 predicate=pass`; `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`; `PREDICATE R95-C2 pass`; rc 0. Receipt `receipts/census-T-rerun.txt`, per-row outputs `receipts/census-out/`. Matches L1's `c2-tip.txt`. |
| do-nothing (BEFORE) | 14 × `controls/before-r94-counter-<id>.txt` at BASE | all 14 `PREDICATE R94-C2 pass`, rc 0 (checked by grep). Not re-run here. |
| frozen table | `sha256sum` of tabled files at T vs F `d9cd18a7`'s table | counter 2fc2e7f0, census 38fed2c2, tsv 6b455d9e, gate v2 8574b4d5 — all equal to the frozen table. |

Conclusion on the frozen predicate: reproduced. Nothing below flips R95-C2 at T; the findings are about what the instruments can and cannot detect.

## 1. Are the 14 designated legs the REASON each row fails?

Yes, for 14/14. Each row was read from its `census-out/out-<id>.txt` and from a diff against gate v2 (`receipts/forgery-diffs/14-rows-vs-gate-v2.diff`).

| row | defect (diff vs gate v2) | designated leg | observed RED that carries the defect |
|---|---|---|---|
| F1 paths-dup-accepted | dup-`--paths` guard removed | W2 w2-paths-dup | `rc=0 summary=(2,2,0) want=None` |
| F2 paths-absent-dropped | absent-at-freeze path `continue` | W2 w2-paths-absent | `rc=0 summary=(1,1,0) want=None` |
| F3b octopus-anchor-kept | octopus → plain rev-list | W2 w2-octopus | `rc=0 (1,1,0) want (1,0,1)` |
| F4b touched-M-only | counts only `--diff-filter=M` | W2 w2-delete-readd | `rc=0 (1,1,0) want (1,0,1)` |
| F5 rename-intact | rename followed | W2 w2-rename | `rc=0 (1,1,0) want (1,0,1)` |
| F6b entry-rc-remap | `rc 2→1` when `--paths` | W2 w2-paths-absent | `rc=1 want_rc=2`, `predicate_line_ok=False` (also w2-paths-dup) |
| F7 spaced-row-dropped | rows with >2 tokens dropped | W2 w2-spaced-row | `rc=0 (1,1,0) want rc 2` |
| X1 stub-battery | battery replaced by 15 green stubs | W3 | every probe run `SELFTEST cases=15 ok=15` → `W3 fail probes=3` |
| M01 paths-dup-guard-dropped | same as F1 as an `if False and` | W2 w2-paths-dup | as F1 |
| M02 unterminated-accepted | `if False and inside` | W2 w2-unterminated | `rc=0 (1,1,0) want rc 2` |
| M07 battery-nonfatal | `passed = not broken` | W3 | each probe `rc=0 predicate=pass` with `ok=14` |
| M15 predicate-always-pass | prints `pass` always | W2 w2-edited | `predicate_line_ok=False` (also all rc-1 fixtures) |
| M19 battery-red-concealed | `ok={len(bat)}` echo + `passed = not broken` | W3 | each probe `SELFTEST cases=15 ok=15` despite red |
| M20 battery-broken-and-concealed | B02 want→False + forged echo | W3 | each probe `SELFTEST cases=15 ok=15` |

Side effects (not designation failures): mutants that delete an anchor line also make W5 report `anchor-missing` (e.g. F1, F2, M01, M02). Rows with a rc-remap (F6b) also trip paths-mode fixtures. Designation is still the reason.

W3 probes (checked directly, `receipts/cli-checks/w3-probe-designated-cases.txt`): P1 reddens only `B11`, P2 only `B02`, P3 only `B13`, each `SELFTEST cases=15 ok=14`. So the probe design is live for those three cases.

## 2. W3 battery-probe design

- Sound against the question it asks: each probe red-drives its case, rc 1, PREDICATE fail, and the honest gate's echo is green (W1 and W3(a)). The honest gate cannot be made red by the probes: the probes only run on copies in `$S`, and W3 only reads their output. The anchors match exactly once in gate v2 (count 1 for each).
- **Not sound as a battery check** (held-out H1, H2): W3 requires only that *some* case goes red for each probe (`st[0][1] < 15`); it does not require the designated case (B11/B02/B13) to be the one that goes red, nor that the other 12 cases are live. Results:
  - H1 (single hollow case `B07`, can never fail): `PREDICATE R95-C2 pass`, rc 0 (`receipts/held/out-H1b-B07-hollow.txt`).
  - H2 (all cases hollow except B02/B11/B13): `PREDICATE R95-C2 pass`, rc 0 (`receipts/held/out-H2-hollow-except-probed.txt`), i.e. a 12-of-15-hollow battery passes every leg.
  - So a battery forged to be red only where the probe pokes it is accepted. The docstring's claim that W3 catches stubbed/non-fatal/concealed batteries is true only for whole-battery forgeries.
- **Honest gate falsely red by anchor coupling** (H7): a semantically identical refactor of gate v2 (`if touched:` → `if touched != 0:`, `if dups:` → `if len(dups) > 0:`) makes the counter FAIL: `W3 P2 RED anchor-missing`, `W3 P3 RED anchor-missing`, `W5 K7 RED anchor-missing`, `PREDICATE R95-C2 fail`, rc 1 (`receipts/held/out-H7-equivalent-refactor.txt`). W3 and W5 are byte-anchored; the counter cannot tell an honest refactor from a forgery.

## 3. Census pass detection

- `PASS_LINE = ^PREDICATE R\d+-C2 pass$` plus rc 0 accepts any claim number. For the false-gate rows this only ever *counts* a pass (the wrong direction is harmless): a counter that prints pass for a false gate increments `passing`, which fails the census. A counter printing the wrong claim id on honest runs fails `honest` only if it does not print a pass line. So "wrong claim count" in the pass line cannot make the census green by itself.
- The census's green path depends on `designated_red`, which is a text match (`^W2 w2-… RED ` or `^W3 fail `) on counter stdout. A counter that prints the designated lines whenever it is handed a `--tool-file` and returns 1 passes the census: **H4** (`receipts/held/census-H4.txt`): `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, rc 0. This is a measurement-independence defect: the 14 → 0 number is only as independent as the counter's own printed text. The real counter at T contains no such branch (read in full; the `--tool-file` path only copies the file, and every RED line is printed after its leg runs), so T is not affected.
- The census's `--counter` option works (used for H4), but the census never recomputes any designated fixture itself.

## 4. Exclusion of M04 / M10 / M18 (tsv header)

- **M18** (`resolve()` without `^{commit}` peel): justified. Verdict-neutral; the only observable difference is the echoed FREEZE id (tag object vs commit) for an annotated-tag `--freeze` (`receipts/cli-checks/M18-annotated-tag-freeze.txt`: both `rc=1`, same INSTRUMENT and PREDICATE). Counter inputs are always raw commit shas.
- **M04** (`elif sha(at_t) != sha(at_f)` in place of `want`): the MutTesterGate "equivalence argument" is wrong as stated. It is not equivalent: (a) reason strings change; (b) when a claims row's path is absent at freeze, `sha(None)` raises `TypeError`, rc 1, no PREDICATE line, no summary (`receipts/cli-checks/M04-absent-at-freeze-row.txt`; the honest gate gives rc 1 with `broken`). The exclusion is still harmless to the claim: by case analysis M04 never turns a breach into a pass (if `at_f == want` the two comparisons agree; if `at_f != want` both are broken). The counter does not kill M04 (H3: `PREDICATE R95-C2 pass`, rc 0). Documentation defect: the tsv reason should say "not a false pass", not "equivalence".
- **M10** (rc guard on `rev-list` dropped): the exclusion "no observable" is FALSE. On a damaged object store (tree of a post-freeze side commit deleted) the honest gate reports `DEFECT SETUP rev-list failed` and `could-not-evaluate` (rc 2), while M10 reports `INSTRUMENT probe.py … touched=0 verdict=intact`, `PREDICATE freeze-integrity pass`, rc 0 — a breach (`probe.py` edited after freeze on the merged side branch) certified intact (`receipts/cli-checks/M10-damaged-object-store.txt`). The counter has no fixture with a damaged store; see §5 for its verdict on M10. M10 is not in the 14, and the shipped gate v2 has the guard, so R95-C2 at T is unaffected; the tsv exclusion rationale is wrong.

## 5. Held-out forgeries and controls (not in the 14; each run through the counter at T with `--tool-file`)

| id | construction | counter result | reading |
|---|---|---|---|
| H1 | B07 battery case hollowed (`lambda v: True`) | PASS, rc 0 (5/5) | miss |
| H2 | all battery cases hollowed except B02, B11, B13 | PASS, rc 0 (5/5) | miss |
| H3 | `elif sha(at_t) != sha(at_f)` (M04) | PASS, rc 0 (5/5) | miss; not a false pass (§4) |
| H4 | counter that prints designated RED lines on `--tool-file`; census run | census PASS, rc 0 | census measurement-independence miss (§3) |
| H5 | edit-then-revert accepted (`touched and at_t != at_f`), B03 hollowed | FAIL: W2 w2-edit-revert, w2-edit-revert-unrelated, w2-treesame-merge, … also `W3 P2 anchor-missing` | caught (control) |
| H6 | `--first-parent` instead of `--full-history` | FAIL: W1b, W2 w2-treesame-merge, w2-octopus, … | caught (control) |
| H7 | semantically identical refactor of gate v2 | FAIL: W3 P2/P3 and W5 K7 anchor-missing | honest gate falsely red (§2) |
| M10 | rc guard dropped (`if False and log.returncode != 0`), damaged object store | PASS, rc 0 (5/5) — counter sees nothing wrong with a false `intact` | miss; no fixture builds a damaged store (§4) |

Note on H1: the first invocation of H1 produced no output (the file contained only `RC=0`); it is kept as `receipts/held/out-H1b-B07-hollow.txt` (the re-run) and the empty first output was deleted from the receipt set.

M10 through the counter: `receipts/held/out-M10-rev-list-rc-ignored.txt` — `PREDICATE R95-C2 pass`, rc 0. The counter cannot see this defect.

## 6. Verdict-level findings (routed to round 96, not repaired in round)

FINDING C2-F1 major: census green path trusts counter-printed designated RED lines; a forged counter printing them passes census (H4). Not a flip at T; the real counter has no such path.
FINDING C2-F2 major: W3 checks only that some case goes red per probe, not the designated case; a battery hollowed to the three probed cases (H2) or one case (H1) passes R95-C2. Not a flip at T (no 14-row uses a partial hollow battery; X1, M19, M20 are caught).
FINDING C2-F3 major: M10 (rc guard dropped) produces a false `intact` on a damaged object store where the honest gate says could-not-evaluate; the tsv's "no observable" exclusion is wrong. Not a flip at T (population excludes M10; gate v2 has the guard).
FINDING C2-F4 minor: the counter is byte-anchored in W3 and W5; a semantically identical gate refactor fails R95-C2 (H7).
FINDING C2-F5 minor: M04 exclusion rationale is wrong (crash path, reason strings); M04 cannot turn a breach into a pass; counter passes M04 (H3).
FINDING C2-F6 info: M18 exclusion is justified (verdict-neutral).
FINDING C2-F7 info: all 14 designated legs are the reasons; side-effect legs (anchor-missing, predicate mismatch) also fire on some rows.

## 7. Not done / residuals

- Legacy/harm gates, sources and overlap are outside this item and were not reviewed.
- The do-nothing census (R94 counter) was not re-run; the 14 BEFORE receipts were checked.
- The 14 false gates' sha256 and the frozen table were checked, not re-derived from history.
- No flag or sysctl changed. No package installed.
