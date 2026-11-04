# ReviewerC2R79 — R79-C2 independent review

Recommendation: **FAIL** (recommendation only). Axes: coverage of the seven routed defects; calibration of “discharged, not restated.” Frozen predicates, targets, controls, and kill rules remain unchanged. Review revision: `5d6843134017780c045e92eed4e83264188a7d47`; `master` resolved to this same revision during review. No landing implementation existed to assess: scoped diff from `660ec0b9` added the 422-line counter only, and the routed ledger contained no R78-D1…D7 rows.

## Findings, highest severity first

### High — the counter certifies incidental ids as repairs

`plans/round79_c2_closure_debt.py:177–196` checks only that a tracked named file contains the id and that an arbitrary shell command exits zero. It does not establish that the file repairs the routed defect or that the command tests the repaired condition.

Executed a fresh, committed scratch fixture using the **unmodified frozen CLI**, not an imported counter. Its spot-check was the actual committed spot-check, with all seven correctly located sources. The only purported repair was this tracked file:

```text
# Routing recap only; no repairs performed
R78-D1
R78-D2
R78-D3
R78-D4
R78-D5
R78-D6
R78-D7
```

Each row closed against `corpus/lessons/round-79.md` with `check: "test -f corpus/lessons/round-79.md"`. No SCORECARD correction, LOG correction, source metadata repair, or rerun receipt was present in the fixture. Observed:

```text
DEBT-TOTAL ids=7 registered=7 closed=7 checks_passed=7
DEFECTS n=0
TARGET ids=7 closed=7 checks_passed=7 indexed=yes
PREDICATE R79-C2 pass
rc=0
```

This is a strictly smarter presence control that reaches the frozen target while leaving the substantive defects unrepaired. Merely requiring red-at-base will not fix this: `git -C <lane> cat-file -e 660ec0b9:corpus/lessons/round-79.md` returned 128, so this existence check fails at base because the incidental recap did not exist.

Required added defect concept: **CHECK-NOT-REPAIR-SENSITIVE** (or equivalent), demonstrated by removing/reverting the actual repair while retaining the registration, recap, markers, and check implementation; the check must then fail. An accompanying **CLOSE-NOT-REPAIR** semantic/provenance requirement must distinguish a repair from a document merely listing ids. This is a proposed added defect, not an amendment made by this reviewer.

A second executed attack used `grep -q R78-D1 corpus/routed-findings.jsonl` (corresponding id per row). The check finds its own ledger id/check text, independent of any repair. It produced the same zero-defect, seven-check pass. This directly confirms the self-marker attack.

### High — empty checks and decorated routing paths bypass explicit exclusions

The trivial-command regex at line 52 excludes only whole-string alternatives; `check()` at 188–196 does not reject empty strings. An executed attack with `check: ""` for every row returned the same passing target and rc 0, while each printed DEBT line said `check=absent`. This is the cheapest surviving check: zero command bytes. `bash -lc ''` returns zero. A missing/non-string check is rejected, but an empty string is not. `true # repair supposedly checked` likewise evades the anchored regex.

The routing-file exclusion at 174–175 compares the entire `close` string with the bare path, before extracting a named file at 177. An executed attack used each real source line as close, for example:

```json
{"id":"R78-D1","source":"corpus/lessons/round-78-verifier-spotcheck.md:149","status":"closed","close":"corpus/lessons/round-78-verifier-spotcheck.md:149","check":"true # repair supposedly checked"}
```

All seven rows passed: `DEFECTS n=0`, exact frozen target, rc 0. Thus the forbidden spot-check itself is accepted with a line suffix. Normalize/extract the referenced artifact before applying the exclusion. Blocking this spelling and empty checks alone would still leave the incidental-lesson attack above.

### Medium — the advertised presence control has a confounding source failure

`control()` at 383 hardcodes every source to spot-check line 5. The actual seven id lines are 149, 158, 165, 171, 176, 184, 189. Executed `--control-presence` observed:

```text
CONTROL presence ids=7 closed=7 defects=21 codes=CHECK-TRIVIAL,CLOSE-NOT-REPAIR,SOURCE-LINE
CONTROL presence target_reached=False
rc=0
```

Seven CLOSE-NOT-REPAIR plus seven CHECK-TRIVIAL are sufficient to kill that exact weak control; seven unrelated SOURCE-LINE errors also kill it. Therefore its loss does not isolate the intended defenses. Correct sources plus an incidental tracked id file and a fallible-but-unrelated check survive, as reproduced above. The frozen claim's stated two-class/14-defect explanation omits this third class.

## Independent id derivation

Read the complete frozen claim before commands. Independently read §6 of the committed round-78 spot-check, without running/importing the counter to derive ids. The seven bullet-start ids are:

| id | exact source line carrying id | routed repair subject |
|---|---:|---|
| R78-D1 | 149 | Incorrect C2 before-defect split |
| R78-D2 | 158 | Surviving stale round-77 stamp prose |
| R78-D3 | 165 | Stale at-tip routed queue block |
| R78-D4 | 171 | S254/S255 citation metadata |
| R78-D5 | 176 | Overstated quality/base redness |
| R78-D6 | 184 | Dirty-tree evidence called clean |
| R78-D7 | 189 | Spot-check index and routed registration debt |

Each `source` is `corpus/lessons/round-78-verifier-spotcheck.md:<line>`; every cited line contains its corresponding id. The independent union has exactly seven distinct ids.

## Complete emitted-defect matrix

All 15 emitted defect classes in frozen `check()` are covered below. These minimal cases are **branch reasoning from frozen code**, not claims of executed matrix tests. Start with this D1 row in an otherwise valid seven-row fixture:

```json
{"id":"R78-D1","status":"closed","source":"corpus/lessons/round-78-verifier-spotcheck.md:149","close":"repair.md","check":"test -f repair.md"}
```

Assume tracked `repair.md` contains `R78-D1`, correct index text, and other six valid rows. Apply only the indicated alteration; some alterations also affect the target or produce other diagnostics.

| defect | minimal alteration/input | why it fires; frozen line |
|---|---|---|
| DEBT-UNREGISTERED | Delete D1 row | No `found` rows; 150–153 |
| DEBT-DUPLICATE | Append identical D1 row | `len(found)>1`; first row still evaluated; 154–157 |
| ROW-INVALID | Add raw JSONL line `{` | JSONDecodeError becomes `__invalid__`; 109–116, 141–143 |
| STATUS-UNKNOWN | `status:"bogus"` | Outside four-status enum; 159–160 |
| SOURCE-MISMATCH | `source:"other.md:149"` | Wrong source path; 162–164 |
| SOURCE-LINE | `source:"corpus/lessons/round-78-verifier-spotcheck.md:1"` | Correct path, line lacks D1; 166–168; line 0/out-of-range also fires |
| CLOSE-ABSENT | `close:null` | Closed row requires nonempty string; 172–173 |
| CLOSE-NOT-REPAIR | Bare spot-check path as `close` | Exact stripped-string equality; 174–175; suffix bypass reproduced |
| CLOSE-NOT-EVIDENCE | `close:"repair.md"`, file contains no D1 | Tracked path resolves but id substring absent; 179–181 |
| CLOSE-COMMIT | `close:"deadbee"`, no such commit | Hash recognized, merge-base fails; 182–185 |
| CLOSE-UNRESOLVED | `close:"missing.md"`, untracked, no hash | Neither tracked recognized path nor commit branch; 177–187 |
| CHECK-TRIVIAL | `check:"true"` (or null) | Non-string or regex match; 188–190; **empty string does not fire** |
| CHECK-FAIL | `check:"false"` | Nontrivial spelling, command exits 1; 191–196; timeout likewise |
| BLOCKER-ABSENT | `status:"blocked"`, omit blocker | Blocked/refused branch requires truthy blocker; 197–199 |
| INDEX-MISSING | Remove basename from README | Basename substring absent; 202–205 |

There is no emitted `TARGET` defect class: the status-reopened mutant loses via `run()`'s final conjunction. No automatic defect detects a check that passes at base, despite the separate frozen kill rule requiring it to be reported. Commit closes are also accepted solely by ancestry; that branch never verifies the id or repair content of the commit. This is a residual weakness of the same repair-provenance issue, not an additional executed attack.

## Reproduction and scope

Fixture procedure used twice: create `$HYAKU_SCRATCH/kengaku-r79/ReviewerC2R79/XXXX` with `mktemp -d`; initialize with `git -C "$D" init -q`; assert the top-level equals `$D`; write the four fixture artifacts plus the exact counter obtained with `git -C <lane> show 5d6843134017780c045e92eed4e83264188a7d47:plans/round79_c2_closure_debt.py`; git-add/commit **only inside that fixture**, reasserting its top-level before commit and supplying identity only to that fixture commit. Invoke:

```text
python3 "$D/counter.py" --lane "$D" --work "$HYAKU_SCRATCH/kengaku-r79/ReviewerC2R79/work"
python3 "$D/counter.py" --lane "$D" --work "$HYAKU_SCRATCH/kengaku-r79/ReviewerC2R79/work" --control-presence
```

The README contains the exact spot-check basename; sources use the independently derived lines. Incidental lesson contains only the seven ids, not repair assertions. Vary rows using the commands and close fields above. All four attack variants actually executed: incidental-file existence, self-grep, empty check, and decorated routing close with commented true. Each reached `ids=7 closed=7 checks_passed=7 indexed=yes`, `DEFECTS n=0`, rc 0. All scratch was removed in `finally`; no lane files except this assigned report were written. No tools installed or updated.

## Residual risk and verification gaps

- `xd://lsp` is unavailable (`No such tool`); no semantic references/definition/diagnostics claims are made. Used committed-byte reads, scoped git diff, and literal ledger search as fallback.
- Reviewed the actual frozen counter addition and its observable CLI behavior. Did not review a future landing implementation or execute future repair checks; none was available at this revision. Did not run the full selftest/mutant suite or baseline counter because this assignment's decisive false-green controls already establish the scoped failure.
- No runtime-routing or resume code is changed by this diff; canonical-runtime and resume-continuity invariants are outside this counter's affected surface. Saturation is not independently proven: “ceiling 10, exercised” cannot turn these false greens into closure evidence.
- Self-evaluation: accuracy 4/5 (committed code plus four observed false greens; matrix is reasoned, not executed); completeness 4/5 (all requested items, no landing implementation available); clarity 4/5 (separates observations from branch reasoning); actionability 4/5 (names missing sensitivity/provenance defenses without changing frozen claims); conciseness 4/5 (matrix retained for complete class coverage). Overall 4.0/5. Highest-impact improvement is repair-removal sensitivity testing rather than another marker-presence test. User-agreement check: FAIL is grounded in exact target-reaching unrepaired controls, not a preference about design.
