# C2RevFieldLoss — did attribution rewrite history? (round 51, w1, seat C2RevFieldLoss)

Reviewer seat. Item: for all 71 base rows, compare every original field
(`id, class, source, opened_round, status, close, blocker, check, note`) between
`{LANE}/corpus/routed-findings.jsonl` (base) and the merged candidate, report every
changed value old -> new, and rule each change.

**Axes named:** `adjacency` (R51-C2 — the axis this seat attacks) and `freshness`
(R51-C1 — named, not measured here). This seat moved neither axis.

**Scope:** one item, read-only against the lane. Nothing in `plans/*`, `corpus/*`,
`PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md` was written; no git mutation, no
commit, no push. Only this report file was written into the lane.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7       (lane tip, git -C {LANE} rev-parse HEAD)
BASE-BLOB 2e819d7aa175137a43129edba932c3f853a51574  (HEAD:corpus/routed-findings.jsonl)
BASE-SHA256 39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d
CAND .ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl
CAND-SHA256 cc5acda17ad89c3ab08120959864525dca74909aaab3571421be7544c158a350
CAND 75 rows, 66130 B, mtime 2026-10-28 15:38:54, hash unchanged over 3 polls to 15:39:54
```

The base ledger is byte-identical at the stage-1 freeze commit, at the base tip and at
the measured tip, so the comparison base is unambiguous:

```
$ git -C {LANE} show e07f131cf7037e58a21db6e1f3986cf401ad257c:corpus/routed-findings.jsonl | sha256sum
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  -
$ git -C {LANE} show 297e17927ba9342a87ba27a48cc5270a001de7cb:corpus/routed-findings.jsonl | sha256sum
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  -
$ sha256sum {LANE}/corpus/routed-findings.jsonl
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  {LANE}/corpus/routed-findings.jsonl
```

Base: 71 rows, each carrying exactly the 9 original keys, 71 unique ids, statuses
`closed 41 / open 27 / blocked 1 / refused 2`, `check: null` on 10 rows
(`R40-R5, R42-R3-09, R42-R3-33, R42-R3-34, R42-R3-35, R42-R3-37, R45-S5-7b…-7e`),
`note: null` on 12, `close: null` on 30, no `owner`/`disposition`/`next` key anywhere.

### The candidate is a moving target — observed versions

| time | sha256 (prefix) | size | rows | what I measured |
|---|---|---|---|---|
| 15:22 | `60de7113` | 49743 B | 71 | 1 of 8 fragments merged (C2ExecF only); 9 rows attributed |
| 15:33 | `db970426` | 60743 B | 75 | 4 status flips `open -> closed` + 4 invented `close` texts; provenance keys null |
| 15:34 | `dfed0019` | 60685 B | 75 | status flips reverted; `w1_check_note`/`evidence` **absent**; 57 check rewrites |
| 15:38:54 | `cc5acda1` | 66130 B | 75 | **measured candidate**; provenance keys restored on 18 rows; 61 check rewrites |

Every number below refers to `cc5acda1`. The churn itself is finding S5.

## What I ran (scratch `/fast/scratch/hyaku/kengaku-r51/C2RevFieldLoss`, 555 GB free on `/fast`)

```
$ git -C {LANE} show e07f131…:corpus/routed-findings.jsonl > base.jsonl
$ python3 fieldloss.py --base base.jsonl --cand merge-cand2.jsonl     # strict value+order comparison
$ python3 rulings.py  --base base.jsonl --cand merge-cand2.jsonl      # per-change ruling
$ python3 fieldloss.py --base base.jsonl --cand union-candidate.jsonl # fragment union, all 8 C2Exec[A-H]
```

`fieldloss.py` and `rulings.py` are scratch-only tools written for this seat. Both are
self-tested and are not vacuous: nine fixtures returned
`clean / clean / clean / dirty / dirty / dirty / dirty / dirty / dirty`
(identity, owner+disposition addition, null->authored completion, note rewrite, non-empty
check replacement, source rewrite, dropped row, reordered rows, deleted field), and four
synthetic classifier cases resolved as expected (`mechanical-cd`, `mechanical-lanevar`,
`mechanical-guard` -> MECHANICAL; `semantic-broaden`, `semantic-drop-term`,
`semantic-invert` -> SEMANTIC).

## Headline

**No base row's identity or lifecycle history was rewritten in the measured candidate.**
Across all 71 base rows, `id`, `class`, `source`, `opened_round`, `status`, `close`,
`blocker` and `note` are byte-identical to base — 0 changes. No row deleted, no id
duplicated, base id order preserved (extras appended at the tail), JSONL parses, file
ends with a newline.

**Every original-field change is confined to `check`, and it hits all 71 rows.** Rulings:
57 mechanical re-rootings (invertible), 10 predicate-mandated completions (base `null` ->
authored command), 2 strengthened assertions, 2 replaced assertions. **43 of those 61
rewrites carry no marker in the ledger** — the base command text is gone from the ledger
and recoverable only from `git show e07f131:corpus/routed-findings.jsonl`.

Verbatim comparison output:

```
ROWS base=71 candidate=75
STRUCTURAL 5
  row count base=71 candidate=75
  order drift at index 71: base '<none>' -> candidate 'R51-R1'
  order drift at index 72: base '<none>' -> candidate 'R51-R2'
  order drift at index 73: base '<none>' -> candidate 'R51-R3'
  order drift at index 74: base '<none>' -> candidate 'R51-R4'
COMPARED rows=71 rows_touched=71 completions=10 rewrites=61
ADDED-KEYS {"disposition": 71, "evidence": 9, "next": 28, "owner": 71, "w1_check_note": 9}
TALLY {"COMPLETION": 10, "EXTRA-KEY": 188, "IDENTICAL": 0, "MECHANICAL": 57, "SEMANTIC": 2, "STRENGTHENED": 2}
SEMANTIC-UNMARKED 1 ['R42-R3-25']
STRENGTHENED-UNMARKED 2 ['R42-R3-21', 'R42-R3-22']
MECHANICAL-UNMARKED 40 ['R42-R1', 'R42-R2', … 'R45-S5-7a']
```

Field census of original-field diffs (`57 MECHANICAL + 2 STRENGTHENED + 2 SEMANTIC +
10 COMPLETION = 71`, all of them `check`; no other original field appears):

```
$ grep -E '^   DIFF' rulings-cand2.txt | awk '{print $3}' | sort | uniq -c
     10 COMPLETION
     57 MECHANICAL
      2 SEMANTIC
      2 STRENGTHENED
```

## Findings, by severity

### S1 — the candidate adds 4 rows and lands at 75 against a frozen after-target of 71

`R51-R1..R51-R4` exist in no base row and in **no attribution fragment** (`grep -c R51-R`
over `C2Exec[A-H].jsonl` = 0). They are new findings about this round's own surfaces
(serving-plane identity pin, fleet ledger attribution gap, absent domain source trees,
absent served-model unit) and each carries `owner`/`disposition`/`next`.

Field loss: none — they are appended, base order intact. But the frozen claims doc states
the after target is `rows=71 (no row deleted, no row added without an owner)`, and the
predicate only prints `rows=N` without asserting it. A 75-row candidate cannot reproduce
the declared after receipt: `LEDGER rows=71` (before) vs `rows=75` (after) is a number
drift the claim does not explain. Land 71 rows, or amend the after target and name
R51-R1..R4. Shipping 75 silently is the `number-drift` class this lane already carries.

### S2 — 43 of 61 rewritten checks carry no marker; the base command is not in the ledger

The candidate keeps `w1_check_note` on 9 rows (C2ExecA) and `evidence` on 9 rows
(C2ExecD) — 18 marked rewrites. The other 43 (40 mechanical, 2 strengthened, 1 replaced)
have neither key and no changed `note`, so nothing in the ledger says the command differs
from the frozen base. The immediately preceding version (`dfed0019`, 15:34) had dropped
all 18 markers; they were restored in `cc5acda1`.

Example of the surviving marker (good), and of an unmarked rewrite (bad):

```
R39-R1.w1_check_note = "check lane-anchored to $LANE; the original cwd-relative form exited 2 from the counter scratch cwd (measured by C2ExecA, e07f131)"   [marked]
R42-R3-27            no w1_check_note, no evidence, note unchanged; check rewritten from
  "test \"$(python3 plans/scratch_guard.py --selftest …)\" -ge 37"
  to "test \"$(cd \"$LANE\" && python3 plans/scratch_guard.py --selftest …)\" -ge 37"                                            [unmarked]
```

Ruling: **allowed transform in substance, unrecorded in the artifact.** The frozen counter
runs each `check` as `bash -lc` with `cwd=<scratch>` and `LANE=<lane>`
(`plans/round51_routing.py`: `subprocess.run(..., cwd=str(tmp), env={… "LANE": str(lane)})`),
and 59 of the 61 non-null base checks use repo-relative paths, so an un-anchored base
check cannot pass. Anchoring is therefore required by the claim and is mechanical — but
it is still a change to an original field value with no record for 43 rows.

### S3 — the merge re-decided 11 dispositions and invented 25 `next` values

`disposition` is an added field, so this is outside field loss — but it means the merged
artifact is not the wave's record. Fragment -> merge, verbatim:

```
R42-R3-01, R42-R3-03, R42-R3-04, R45-S5-4, R45-S5-5, R45-S5-6, R45-S5-7a : fixed-historical -> fixed-verified  (7)
R42-R3-33, R42-R3-34, R45-S5-7b, R45-S5-7d                              : fixed-verified   -> accepted-risk   (4)
next added to 28 accepted-risk rows, 25 of them the identical string "kengaku round 52 backlog"
```

`next` is predicate-required only for `routed`/`referral` rows (4 here, all on the new
rows). The other 28 are invented, and `"kengaku round 52 backlog"` names no checkable
obligation. Also `R45-S5-5.close`: the fragment had replaced the base close text; the
merge restored the base text — correct for field preservation, but the merge both reverted
one seat's edit and applied others with no record of either decision.

### S4 — one fragment-authored check was replaced wholesale

`R42-R3-25` differs from base **and** from its attribution fragment:

```
OLD (base, and the fragment's anchored form):
  grep -qE '"id": "R42-R2(\.[0-9]+)?".*plans/scratch_guard\.py' "$LANE/corpus/routed-findings.jsonl" && git -C "$LANE" cat-file -e HEAD:plans/scratch_guard.py
MERGE:
  python3 -c "import json,sys;rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()];sys.exit(0 if any(r.get('id','').startswith('R42-R2') and 'plans/scratch_guard.py' in (r.get('check') or '') for r in rows) else 1)" "$LANE/corpus/routed-findings.jsonl" && git -C "$LANE" cat-file -e HEAD:plans/scratch_guard.py
```

The merge version is arguably a *better* check (it parses instead of grepping), but it is
a third version of a state record with no recorded author. Ruling: **unrecorded rewrite** —
keep the fragment's check or record the substitution.

### S5 — the candidate was rewritten at least five times mid-wave, and the merge seat has no report

`C2ExecLedgerMerge.jsonl` changed at 15:22, 15:33, 15:34 and 15:38:54 while the wave ran
(table above). One intermediate version (`db970426`, 15:33, 60743 B) contained four
`open -> closed` status flips (R42-R3-33, R42-R3-34, R45-S5-7b, R45-S5-7d) with close text
`"round 51: check re-derives the fix and exits 0"`; the final version reverts them. The
net open count stayed 27 in that version only because four new `open` rows were added at
the same time — a number-preserving history rewrite. It is not in the candidate I measured,
but nothing in the merge process prevents its return, and a reviewer sampling at 15:33
would have reported a closed-defect count four lower than the truth.

`C2ExecLedgerMerge.md` does not exist (`ls: cannot access …: No such file or directory`).
The merge seat is a settled seat with no report — the routed defect class — and its report
is the only place the "no original field value lost" verification would have been recorded,
which is exactly the check S2/S3/S4 fail.

## Per-row result, all 71 base rows

Every row differs only in `check`; no other original field changes anywhere.

| row | ruling |
|---|---|
| R39-R1, R39-R2, R39-R3, R39-R4 | MECHANICAL (anchored) |
| R39-R5 | **SEMANTIC — assertion broadened** |
| R40-R1, R40-R2, R40-R3, R40-R4 | MECHANICAL (anchored) |
| R40-R5 | COMPLETION (null -> authored) |
| R42-R1, R42-R2, R42-R3, R42-R4, R42-R5 | MECHANICAL (anchored) |
| R40-R1.1, R42-R2.1, R42-R2.2, R42-R6 | MECHANICAL (anchored) |
| R42-R3-01 … R42-R3-08 | MECHANICAL (anchored) |
| R42-R3-09 | COMPLETION (null -> authored) |
| R42-R3-10 … R42-R3-17 | MECHANICAL (anchored, `${LANE:-.}/` form) |
| R42-R3-18, -19, -20, -23, -24, -26 | MECHANICAL (anchored) |
| R42-R3-21 | **STRENGTHENED — clause appended** |
| R42-R3-22 | **STRENGTHENED — clause appended** |
| R42-R3-25 | **SEMANTIC — command replaced** |
| R42-R3-27 | MECHANICAL (anchored inside a command substitution) |
| R42-R3-28 … R42-R3-32 | MECHANICAL (anchored) |
| R42-R3-33, -34, -35, -37 | COMPLETION (null -> authored) |
| R42-R3-36, -38, -39, -40, -41 | MECHANICAL (anchored, `${LANE:?}` form) |
| R45-S5-1, -2, -3 | MECHANICAL (anchored, `${LANE:?}` form) |
| R45-S5-4, -5, -6, -7a | MECHANICAL (anchored by the **merge**, not by any attribution seat — these four rows were untouched in every fragment) |
| R45-S5-7b, -7c, -7d, -7e | COMPLETION (null -> authored) |

The 57 MECHANICAL rows are exactly invertible. The documented inverse (applied by
`rulings.py`, verified row by row) is: strip `cd "$LANE" && ` / `cd "${LANE:?}" && `,
replace `"$LANE/`, `"${LANE:?}/`, `"${LANE:-.}/` with `"`, `--lane "$LANE"` with
`--lane .`, `"$LANE"` with `.`, drop a leading `test -f <path> && ` guard, unwrap a
`{ …; }` group around an `||` chain, and ignore quote style. Applied to the candidate
value, each of the 57 reproduces the base value **exactly**. Which form each row got:

```
cd "$LANE" && prefix                22 rows: R42-R1..R42-R5, R40-R1.1, R42-R2.1, R42-R2.2, R42-R6,
                                              R42-R3-01..R42-R3-08, R42-R3-28..R42-R3-32
"$LANE/ on path arguments           17 rows: R39-R1..R39-R4, R40-R1..R40-R4, R42-R3-18..R42-R3-26
                                     (14 mechanical; R42-R3-21/-22 strengthened, R42-R3-25 replaced)
cd "${LANE:?}" && prefix            12 rows: R42-R3-36, R42-R3-38..R42-R3-41, R45-S5-1..R45-S5-3,
                                              R45-S5-4, R45-S5-5, R45-S5-6, R45-S5-7a
"${LANE:-.}/"                        8 rows: R42-R3-10..R42-R3-17
cd "$LANE" && inside $( )            1 row : R42-R3-27
also: 8 rows gained a leading `test -f <file> && ` guard, 1 row gained a `{ …; }` group
      around an `||` chain, 22 rows differ in quote style only on top of the anchoring
                                      (22+14+12+8+1 = 57 mechanical)
```

Worked example (R39-R1), old -> new:

```
old: grep -q '^| `order-check`' SKILL.md && grep -q '^| `round39-c1-audit`' SKILL.md
new: grep -q '^| `order-check`' "$LANE/SKILL.md" && grep -q '^| `round39-c1-audit`' "$LANE/SKILL.md"
```

## The four assertion-changing rows, verbatim old -> new

```
R39-R5   SEMANTIC (broadened) — unmarked in the candidate
  old: test ! -e /fast/scratch/hyaku/kengaku-r39
  new: test -z "$(ls -d /fast/scratch/hyaku/kengaku-r39* 2>/dev/null)"
  effect: a directory kengaku-r39.N that the base check passed now fails.

R42-R3-21  STRENGTHENED (base kept as prefix, clause appended) — unmarked
  old: grep -qE 'NF ?!= ?13' corpus/QUALITY.md
  new: grep -qE "NF ?!= ?13" "$LANE/corpus/QUALITY.md" && [ "$(awk -F'|' '/^\| S[0-9]+/ && NF!=13' "$LANE/corpus/SOURCES.md" | wc -l)" -eq 0 ]

R42-R3-22  STRENGTHENED (base kept as prefix, clause appended) — unmarked
  old: grep -q 'parse_registry.*:25' corpus/QUALITY.md
  new: grep -q "parse_registry.*:25" "$LANE/corpus/QUALITY.md" && sed -n 25p "$LANE/plans/registry_check.py" | grep -q "def parse_registry"

R42-R3-25  SEMANTIC (command replaced) — unmarked; see S4
  old: grep -qE '"id": "R42-R2(\.[0-9]+)?".*plans/scratch_guard\.py' corpus/routed-findings.jsonl
  new: python3 -c "import json,sys;rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()];sys.exit(0 if any(r.get('id','').startswith('R42-R2') and 'plans/scratch_guard.py' in (r.get('check') or '') for r in rows) else 1)" "$LANE/corpus/routed-findings.jsonl" && git -C "$LANE" cat-file -e HEAD:plans/scratch_guard.py
```

## The 10 completions, verbatim new value (base was `null`)

```
R40-R5     cd "$LANE" && test -n "$(git log --format=%h 34158b0..HEAD -- plans/order_check.py)" && python3 plans/mutant_direction_check.py --lane . --counter plans/round42_c1_verify.py >/dev/null 2>&1
R42-R3-09  grep -qF "and pytest's cache" "${LANE:-.}/corpus/knowledge/tb2-circuit-fibsqrt-grader.md" && ! grep -qE '^[[:space:]]*(import pytest|from pytest)' "${LANE:-.}/plans/fibsqrt_probe.py" && ! grep -qF -- '-m pytest' "${LANE:-.}/plans/fibsqrt_probe.py" && ! grep -qF 'pytest.main' "${LANE:-.}/plans/fibsqrt_probe.py"
R42-R3-33  grep -qF '9 witnessed of 20' "$LANE/plans/round-43-claims.md"
R42-R3-34  grep -qF 'NA7' "$LANE/.ufo/waves/round-43/claims/control-c1-direction-mislabel.txt"
R42-R3-35  cd "$LANE" && ls .ufo/waves/round-43/claims/ | grep -qiE 'xo|substitute'
R42-R3-37  cd "${LANE:?}" && grep -q 'host="libc-rand"' plans/feal_probe.py && grep -q "libc.srand" plans/feal_probe.py && grep -q "host=libc-rand" corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md
R45-S5-7b  python3 -c 'import importlib.util,sys;from pathlib import Path;p=Path(sys.argv[1]);s=importlib.util.spec_from_file_location("c3",p/"plans/round46_c3_verify.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);b="def predict(text):\n    table = {\"x\": True}\n    return table.get(text, False)\n";l=m.lint_block(b);print("lint=",l);sys.exit(0 if "{" in l else 1)' "$LANE"
R45-S5-7c  grep -q '"uv", "run", "--no-project", "--with", "biopython==1.85"' "$LANE/plans/pkg_gate.py" && echo unpinned-uv-fetch-present
R45-S5-7d  python3 -c 'import importlib.util,sys;from pathlib import Path;p=Path(sys.argv[1]);s=importlib.util.spec_from_file_location("ff",p/"plans/fixture_fence.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);v,e=m._argv(Path("."),"anchor",["--evidence-ref","{T}/../../etc"]);print("err=",e);sys.exit(0 if v is None and "placeholder" in (e or "") else 1)' "$LANE"
R45-S5-7e  test -f "$LANE/.ufo/waves/round-46/w2/R46W2C1MutCounter.md" && test -f "$LANE/.ufo/waves/round-46/w1/R46MutC2Gate.md" && echo successor-mutant-receipts-present
```

Ruling for all 10: **allowed field completion.** The base value was `null`, the frozen
predicate requires every `check` to be a non-empty command, and the attribution seat spec
authorises "where `check` is empty, author a one-line shell check". No base content is
lost because there was none. Note `R45-S5-7c` and `R45-S5-7e` are `&& echo …` shaped —
they print, they do not assert. That is a check-quality question for `C2CritChecks`, not
field loss.

## Additions (not original fields; ruled for completeness)

```
owner        0 in base -> 71 base rows (+4 new)   predicate-mandated
disposition  0 in base -> 71 base rows (+4 new)   predicate-mandated
next         0 in base -> 28 base rows (+4 new)   4 routed (required) + 28 accepted-risk (not required; S3)
evidence     0 in base -> 9 rows                  extra provenance key (C2ExecD)
w1_check_note 0 in base -> 9 rows                 extra provenance key (C2ExecA)
```

Adding keys is not loss. The two extra keys are wave-scoped names (`w1_…`) that should be
renamed or folded into `note` before landing; the counter ignores unknown keys, so they
are inert for the predicate.

## Residual risk

- The candidate is unstable (S5). Every number here is pinned to `cc5acda1`; a later
  rewrite invalidates them, and one intermediate version already shipped a status rewrite.
- The 43 unmarked check rewrites are recoverable only from `git show e07f131:corpus/routed-findings.jsonl`.
- I did not run the checks (that is `C2RevRecount`/`C2Exec*Checks`), so I make no claim
  about which of the 61 rewritten checks pass; I only ruled on what the text lost.
- Fragments A and B were themselves revised mid-wave (`R40-R5`'s authored check changed
  between the 15:26 and 15:30 versions of B), so "the fragment's value" is pinned only as
  of the hashes at my snapshot time.
- Base rows that were already `fixed-verified` under the old schema do not exist — the
  base has no disposition at all, so 41 `fixed-verified` rows are new claims whose check
  behaviour I did not verify.

## Limits

- Field-loss review only: I did not judge whether an `owner` is the *right* lane, whether a
  `disposition` is *correct*, or whether any check passes. Those are
  `C2CritSpotAttribution`, `C2CritDisposition`, `C2CritChecks`.
- I read the candidate as a file, not through the counter; `PREDICATE R51-C2` is
  `C2RevRecount`'s measurement.
- The 4 added rows' `source` pointers were not resolved by me (the counter's job).
- Scratch was removed before yield; nothing this report cites lives there — every number
  above is reproducible from the commands and hashes it names.
- No tool was installed or upgraded this seat; no pacman transaction was run.

## Recommended repair for the L1 (single integration owner)

1. **Freeze the candidate first.** A moving merge file cannot be reviewed or landed; pin
   one hash, then measure.
2. Restore the 11 dispositions the merge re-decided, drop the 25 invented
   `"kengaku round 52 backlog"` `next` values, restore `R42-R3-25`'s fragment check.
3. Record every remaining rewrite: the 40 unmarked mechanical re-rootings and the 2
   strengthened clauses need the marker the other 18 rows already have (or a landing-note
   statement of the anchoring transform). Keep `R39-R5`'s broadening marked — it changes
   which directories red the row.
4. Decide the row count explicitly: 71 (frozen target) or 75 (amended target, R51-R1..R4
   named and justified). Do not ship a silent drift.
5. Require `C2ExecLedgerMerge.md` — settled seat, no report.

VERDICT: **no base row's identity or lifecycle history was rewritten, but the merged
candidate is not landable as-is** — 0 of 71 rows changed `id/class/source/opened_round/
status/close/blocker/note`; all 71 had `check` rewritten (57 invertible anchorings, 10
predicate-mandated completions, 2 strengthened, 2 replaced); 43 of those 61 rewrites carry
no marker in the ledger; the merge re-decided 11 dispositions, invented 25 `next` values,
added 4 rows against a frozen `rows=71` target, and shipped at least five versions
(one of which contained four unrecorded `open -> closed` status flips); the merge seat
filed no report.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
