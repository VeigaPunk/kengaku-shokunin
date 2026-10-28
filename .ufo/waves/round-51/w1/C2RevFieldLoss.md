# C2RevFieldLoss — did attribution rewrite history? (round 51, w1, seat C2RevFieldLoss)

Reviewer seat. Item: for all 71 base rows, compare every original field
(`id, class, source, opened_round, status, close, blocker, check, note`) between
`{LANE}/corpus/routed-findings.jsonl` (base) and the merged candidate, report every
changed value old -> new, and rule each change.

**Axes named:** `adjacency` (R51-C2, the axis this seat judges) and `freshness`
(R51-C1, read only as context — no C1 surface was measured here). This seat moved
neither axis; it is an attack seat.

**Scope:** one item, read-only against the lane. Nothing in `plans/*`, `corpus/*`,
`PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md` was written. No git mutation, no
commit, no push. Only this report file was written into the lane.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7      (lane tip, git -C {LANE} rev-parse HEAD)
BASE-BLOB 2e819d7aa175137a43129edba932c3f853a51574  (HEAD:corpus/routed-findings.jsonl)
BASE-SHA256 39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d
CAND-SHA256 dfed001963199bdaaf5a59822b5b8b913e119d506691e9e1b30b5e1037dcef6c
CAND .ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl 75 rows 60685 B mtime 2026-10-28 15:34:04
```

The base ledger is byte-identical at the stage-1 freeze commit and at the tip:

```
$ git -C {LANE} show e07f131cf7037e58a21db6e1f3986cf401ad257c:corpus/routed-findings.jsonl | sha256sum
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  -
$ sha256sum {LANE}/corpus/routed-findings.jsonl
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  {LANE}/corpus/routed-findings.jsonl
$ git -C {LANE} show 297e17927ba9342a87ba27a48cc5270a001de7cb:corpus/routed-findings.jsonl | sha256sum
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  -
```

So the comparison base is unambiguous: 71 rows, each carrying exactly the 9 original
keys (`blocker, check, class, close, id, note, opened_round, source, status`), 71 unique
ids, statuses `closed 41 / open 27 / blocked 1 / refused 2`, `check: null` on 10 rows.

The candidate was stable across three consecutive polls of 20 s before I measured it
(`t=15:34:52 … 15:35:52`, sha256 `dfed0019…` unchanged); it was rewritten at least four
times during the wave (15:22, 15:33, 15:34, …), which is itself reported below as a
residual risk.

## What I ran (exact commands, scratch root `/fast/scratch/hyaku/kengaku-r51/C2RevFieldLoss`)

```
$ git -C {LANE} show e07f131…:corpus/routed-findings.jsonl > base.jsonl
$ python3 fieldloss.py --base base.jsonl --cand merge-cand.jsonl
$ python3 rulings.py  --base base.jsonl --cand merge-cand.jsonl
$ python3 fieldloss.py --base base.jsonl --cand union-candidate.jsonl   # fragment union (all 8 C2Exec[A-H] fragments)
```

`fieldloss.py` (strict value comparison, order-sensitive) and `rulings.py` (per-change
ruling) are scratch-only tools written for this seat; both are self-tested against nine
fixtures (identity, owner/disposition addition, null->authored completion, note rewrite,
non-empty check replacement, source rewrite, dropped row, reordered rows, deleted field)
and returned `clean / clean / clean / dirty / dirty / dirty / dirty / dirty / dirty`
respectively, plus four synthetic classifier cases
(`mechanical-cd`, `mechanical-lanevar`, `mechanical-guard` -> MECHANICAL;
`semantic-broaden`, `semantic-drop-term`, `semantic-invert` -> SEMANTIC). The instrument
is not vacuous: it catches every rewrite fixture I could construct.

## Headline

**No base row's identity or lifecycle history was rewritten in the final candidate.**
Across all 71 base rows, `id`, `class`, `source`, `opened_round`, `status`, `close`,
`blocker` and `note` are byte-identical to base: 0 changes. No row was deleted, no id
duplicated, base id order preserved (extras appended at the tail), JSONL parses, trailing
newline present.

**Every original-field change is confined to `check`, on 67 of 71 rows.** Rulings:
53 mechanical re-rootings (invertible), 10 predicate-mandated completions (base `null` ->
authored command), 2 strengthened assertions, 2 replaced assertions. Of those, **the 4
assertion-changing rows and all 53 re-rootings are unrecorded in the candidate**: the
merge dropped the provenance keys the attribution seats wrote, so the artifact the L1
would land no longer says why a check's text differs from the frozen base.

Full comparison output (verbatim counts):

```
ROWS base=71 candidate=75
STRUCTURAL 5
  row count base=71 candidate=75
  order drift at index 71: base '<none>' -> candidate 'R51-R1'
  order drift at index 72: base '<none>' -> candidate 'R51-R2'
  order drift at index 73: base '<none>' -> candidate 'R51-R3'
  order drift at index 74: base '<none>' -> candidate 'R51-R4'
COMPARED rows=71 rows_touched=67 completions=10 rewrites=57
ADDED-KEYS {"disposition": 71, "next": 28, "owner": 71}
TALLY {"COMPLETION": 10, "EXTRA-KEY": 170, "IDENTICAL": 0, "MECHANICAL": 53, "SEMANTIC": 2, "STRENGTHENED": 2}
SEMANTIC-UNMARKED 2 ['R39-R5', 'R42-R3-25']
STRENGTHENED-UNMARKED 2 ['R42-R3-21', 'R42-R3-22']
MECHANICAL-UNMARKED 53 ['R39-R1', … 'R45-S5-3']   (all 53, list elided for width)
```

`IDENTICAL 0` means no base row is untouched once the added keys are counted; four rows
(`R45-S5-4`, `-5`, `-6`, `-7a`) have **zero** original-field changes. `*UNMARKED` means
no `w1_check_note`/`evidence` key and no changed `note` on the candidate row.

## Findings, by severity

### S1 — the candidate adds 4 rows and lands at 75, against a frozen after-target of 71

`R51-R1..R51-R4` exist in no base row and in **no attribution fragment** (0 occurrences of
`R51-R` in `C2Exec[A-H].jsonl`). They are new findings about this round's own surfaces
(serving-plane identity pin, fleet ledger attribution gap, absent domain source trees,
absent served-model unit). Field loss: none — they are appended, base order intact, and
they carry `owner`/`disposition`/`next`.

But the frozen claims doc says the after target is `rows=71 (no row deleted, no row added
without an owner)` while the predicate only prints `rows=N` and never asserts it. A
75-row candidate therefore *cannot* reproduce the declared after receipt, and a reader
comparing `LEDGER rows=71` (before) with `LEDGER rows=75` (after) sees a number drift that
the claim does not explain. Either land 71 rows or amend the after target with the four
new ids named — silently shipping 75 is the `number-drift` class the lane already carries.

### S2 — the merge dropped the wave's own provenance for every rewritten check

`C2ExecA` attached `w1_check_note` to its 9 rows and `C2ExecD` attached `evidence` to its
9 rows; both keys are **absent/null on all 75 candidate rows** (0 rows carry either key).
Verbatim, fragment vs merge:

```
R39-R1.w1_check_note
  fragment: "check lane-anchored to $LANE; the original cwd-relative form exited 2 from the counter scratch cwd (measured by C2ExecA, e07f131)"
  merge   : null
R39-R5.w1_check_note
  fragment: "check strengthened from `test ! -e /fast/scratch/hyaku/kengaku-r39` to a glob, so kengaku-r39.N also reds it; re-measured 2026-10-28: no kengaku-r39* entry (check exits 0)"
  merge   : null
R42-R6.evidence
  fragment: "kengaku-only instrument: plans/scratch_guard.py exists in kengaku-shokunin and not in the fleet root, and no sibling PROVINCE.md names it. …"
  merge   : null
```

This is the mechanism that turns 53 permitted-but-recorded re-rootings into unrecorded
rewrites. Ruling: **unrecorded rewrite by omission** — the values were not "lost" from
the base (they never existed there) but the wave's justification was deleted from the
artifact, so a later reader cannot tell an anchored check from an edited assertion.

### S3 — the merge re-decided 11 dispositions and invented 25 `next` values

`disposition` is an added field (not base), so this is outside field loss, but it means
the merged artifact is not the wave's record:

```
R42-R3-01, R42-R3-03, R42-R3-04, R45-S5-4, R45-S5-5, R45-S5-6, R45-S5-7a: fixed-historical -> fixed-verified  (7)
R42-R3-33, R42-R3-34, R45-S5-7b, R45-S5-7d                              : fixed-verified   -> accepted-risk   (4)
next added to 28 accepted-risk rows, 25 of them the identical string "kengaku round 52 backlog"
```

`next` is predicate-required only for `routed`/`referral` rows (4 here). The other 28 are
an invented backlog claim, and a bare `"kengaku round 52 backlog"` names no checkable
obligation. `R45-S5-5.close`: the fragment had replaced the base close text; the merge
restored the base text — correct for field preservation, but it means the merge both
reverted one seat's edit and applied others, without a record of either decision.

### S4 — one fragment-authored check was replaced wholesale

`R42-R3-25` differs from base **and** from its attribution fragment:

```
OLD (base, also fragment + anchoring): grep -qE '"id": "R42-R2(\.[0-9]+)?".*plans/scratch_guard\.py' corpus/routed-findings.jsonl
FRAGMENT:  grep -qE '"id": "R42-R2(\.[0-9]+)?".*plans/scratch_guard\.py' "$LANE/corpus/routed-findings.jsonl" && git -C "$LANE" cat-file -e HEAD:plans/scratch_guard.py
MERGE:     python3 -c "import json,sys;rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()];sys.exit(0 if any(r.get('id','').startswith('R42-R2') and 'plans/scratch_guard.py' in (r.get('check') or '') for r in rows) else 1)" "$LANE/corpus/routed-findings.jsonl" && git -C "$LANE" cat-file -e HEAD:plans/scratch_guard.py
```

The merge's rewrite is arguably a *better* check (it parses instead of grepping), but it
is a third version of a state record with no recorded author. Ruling: **unrecorded
rewrite** — keep the fragment's check, or record the substitution.

### S5 — no merge-seat report exists

`C2ExecLedgerMerge.jsonl` exists; `.ufo/waves/round-51/w1/C2ExecLedgerMerge.md` does not
(`ls: cannot access …: No such file or directory`). The seat's own report is the only
place the "no original field value lost" verification would have been recorded — which is
exactly the check that S2/S3/S4 fail. Routed defect class (settled seat, no report file).

## Per-row result, all 71 base rows

`IDENTICAL` = all 9 original fields equal. Every other row differs **only** in `check`.

| row | changed original fields | ruling |
|---|---|---|
| R39-R1 | check | MECHANICAL (anchored) |
| R39-R2 | check | MECHANICAL (anchored) |
| R39-R3 | check | MECHANICAL (anchored) |
| R39-R4 | check | MECHANICAL (anchored) |
| R39-R5 | check | **SEMANTIC — assertion broadened** |
| R40-R1 | check | MECHANICAL (anchored) |
| R40-R2 | check | MECHANICAL (anchored) |
| R40-R3 | check | MECHANICAL (anchored) |
| R40-R4 | check | MECHANICAL (anchored) |
| R40-R5 | check | COMPLETION (null -> authored) |
| R42-R1 | check | MECHANICAL (anchored) |
| R42-R2 | check | MECHANICAL (anchored) |
| R42-R3 | check | MECHANICAL (anchored) |
| R42-R4 | check | MECHANICAL (anchored) |
| R42-R5 | check | MECHANICAL (anchored) |
| R40-R1.1 | check | MECHANICAL (anchored) |
| R42-R2.1 | check | MECHANICAL (anchored) |
| R42-R2.2 | check | MECHANICAL (anchored) |
| R42-R6 | check | MECHANICAL (anchored) |
| R42-R3-01 | check | MECHANICAL (anchored) |
| R42-R3-02 | check | MECHANICAL (anchored) |
| R42-R3-03 | check | MECHANICAL (anchored) |
| R42-R3-04 | check | MECHANICAL (anchored) |
| R42-R3-05 | check | MECHANICAL (anchored) |
| R42-R3-06 | check | MECHANICAL (anchored) |
| R42-R3-07 | check | MECHANICAL (anchored) |
| R42-R3-08 | check | MECHANICAL (anchored) |
| R42-R3-09 | check | COMPLETION (null -> authored) |
| R42-R3-10 … R42-R3-17 | check | MECHANICAL (anchored, `${LANE:-.}/` form) |
| R42-R3-18, -19, -20, -23, -24, -26 | check | MECHANICAL (anchored) |
| R42-R3-21 | check | **STRENGTHENED — clause appended** |
| R42-R3-22 | check | **STRENGTHENED — clause appended** |
| R42-R3-25 | check | **SEMANTIC — command replaced** |
| R42-R3-27 … R42-R3-32 | check | MECHANICAL (anchored) |
| R42-R3-33, -34, -35, -37 | check | COMPLETION (null -> authored) |
| R42-R3-36, -38, -39, -40, -41 | check | MECHANICAL (anchored, `${LANE:?}` form) |
| R45-S5-1, -2, -3 | check | MECHANICAL (anchored, `${LANE:?}` form) |
| R45-S5-4, -5, -6, -7a | **none — IDENTICAL** | — |
| R45-S5-7b, -7c, -7d, -7e | check | COMPLETION (null -> authored) |

The 53 MECHANICAL rows are exactly invertible. The documented inverse transform (applied
by `rulings.py`, verified row by row) is: strip `cd "$LANE" && ` / `cd "${LANE:?}" && `,
replace `"$LANE/` and `"${LANE:-.}/` and `"${LANE:?}/` with `"`, `--lane "$LANE"` with
`--lane .`, `"$LANE"` with `.`, drop any leading `test -f <path> && ` guard, unwrap a
`{ …; }` group around an `||` chain, and ignore quote style. Applied to the candidate
value, each of the 53 reproduces the base value **exactly**. Which form each row got:

```
cd "$LANE" && prefix               22 rows: R42-R1..R42-R5, R40-R1.1, R42-R2.1, R42-R2.2, R42-R6,
                                             R42-R3-01..R42-R3-08, R42-R3-28..R42-R3-32
"$LANE/ on path arguments          17 rows: R39-R1..R39-R4, R40-R1..R40-R4, R42-R3-18..R42-R3-26
                                    (14 mechanical; R42-R3-21/-22 strengthened, R42-R3-25 replaced)
"${LANE:-.}/"                      8 rows: R42-R3-10..R42-R3-17
cd "${LANE:?}" && prefix            8 rows: R42-R3-36, R42-R3-38..R42-R3-41, R45-S5-1..R45-S5-3
cd "$LANE" && inside $( )           1 row : R42-R3-27
also: 8 rows gained a leading `test -f <file> && ` guard, 1 row gained a `{ …; }` group
      around an `||` chain, 22 rows differ in quote style only on top of the anchoring
                                    (22+14+8+8+1 = 53 mechanical)
```

Example (R39-R1), old -> new:

```
old: grep -q '^| `order-check`' SKILL.md && grep -q '^| `round39-c1-audit`' SKILL.md
new: grep -q '^| `order-check`' "$LANE/SKILL.md" && grep -q '^| `round39-c1-audit`' "$LANE/SKILL.md"
```

Ruling for all 53: **allowed transform in substance, unrecorded in the artifact.** The
frozen counter runs each `check` as `bash -lc` with `cwd=<scratch>` and `LANE=<lane>`
(`plans/round51_routing.py`, `subprocess.run(..., cwd=str(tmp), env={… "LANE": str(lane)})`),
and 59 of the 61 non-null base checks use repo-relative paths, so a base check cannot pass
un-anchored. Anchoring is therefore *required* by the claim, is mechanical, and is
recoverable from `git show e07f131:corpus/routed-findings.jsonl`. It is still a change to
an original field value with no marker in the merged ledger — the L1 must either keep a
recorded marker (the seats already wrote one; see S2) or state the transform in the
landing note.

## The four assertion-changing rows, verbatim old -> new

```
R39-R5   SEMANTIC (broadened)
  old: test ! -e /fast/scratch/hyaku/kengaku-r39
  new: test -z "$(ls -d /fast/scratch/hyaku/kengaku-r39* 2>/dev/null)"
  effect: a directory kengaku-r39.N that the base check passed now fails. Recorded only
  in the fragment's w1_check_note, which the merge deleted (S2).

R42-R3-21  STRENGTHENED (base kept as prefix, extra clause appended)
  old: grep -qE 'NF ?!= ?13' corpus/QUALITY.md
  new: grep -qE "NF ?!= ?13" "$LANE/corpus/QUALITY.md" && [ "$(awk -F'|' '/^\| S[0-9]+/ && NF!=13' "$LANE/corpus/SOURCES.md" | wc -l)" -eq 0 ]

R42-R3-22  STRENGTHENED (base kept as prefix, extra clause appended)
  old: grep -q 'parse_registry.*:25' corpus/QUALITY.md
  new: grep -q "parse_registry.*:25" "$LANE/corpus/QUALITY.md" && sed -n 25p "$LANE/plans/registry_check.py" | grep -q "def parse_registry"

R42-R3-25  SEMANTIC (command replaced; see S4)
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

Ruling for all 10: **allowed field completion.** The base value was `null` and the frozen
predicate requires every `check` to be a non-empty command; the attribution seat spec
explicitly authorises "where `check` is empty, author a one-line shell check". No base
content is lost because there was none. Note R45-S5-7c and R45-S5-7e are `&& echo …`
shaped (they print, they do not assert); that is a check-quality question for
`C2CritChecks`, not field loss.

## Additions (not original fields, ruled for completeness)

```
owner        71/71 base rows (+4 new)   predicate-mandated addition
disposition  71/71 base rows (+4 new)   predicate-mandated addition
next          0 in base -> 32          4 routed (required) + 28 accepted-risk (not required)
```

Base rows carry none of these keys; adding them is not loss. The `next` population is
reported in S3 because 25 of the 28 are an identical invented string.

## Residual risk

- **The candidate is not stable.** The merge file was rewritten at least four times while
  the wave ran. One intermediate snapshot (copy taken 15:33, 60743 B, sha256
  `db970426d3705ce79740abb4574ef12e1cb99ea0bbd175961857f213b9079b84`) *did* contain four
  status flips `open -> closed` (R42-R3-33, R42-R3-34, R45-S5-7b, R45-S5-7d) with close
  text `"round 51: check re-derives the fix and exits 0"`, which the final version
  reverted. Net open count stayed 27 only because four new `open` rows were added at the
  same time — a number-preserving history rewrite. It is not in the candidate I measured,
  but nothing in the merge process prevents it from returning.
- The `check` rewrites are recoverable only from `git show e07f131:corpus/routed-findings.jsonl`;
  if the lane ever rewrites history or the base blob is dropped, the original commands are
  gone from the ledger itself.
- I did not run the checks (that is `C2RevRecount`/`C2Exec*Checks`), so I make no claim
  about which of the 67 rewritten checks pass; I only ruled on what the text lost.
- Fragments A and B were themselves rewritten mid-wave (e.g. `R40-R5`'s authored check
  changed between the 15:26 and 15:30 versions of B), so "the fragment's value" is only
  pinned as of the hashes at my snapshot time.

## Limits

- Field-loss review only: I did not judge whether an `owner` is the *right* lane, whether
  a `disposition` is *correct*, or whether a check passes. Those are `C2CritSpotAttribution`,
  `C2CritDisposition`, `C2CritChecks`.
- I read the candidate as a file, not through the counter; `PREDICATE R51-C2` is
  `C2RevRecount`'s measurement.
- The 4 added rows' `source` pointers were not resolved by me (counter's job).
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2RevFieldLoss` (555 GB free on `/fast` at
  start) was removed before yield; nothing this report cites lives there — every number
  above is reproduced by the commands and hashes it names.
- No tool was installed or upgraded this seat; no pacman transaction was run.

## Recommended repair for the L1 (single integration owner)

1. Land the **fragment union** (71 rows, `sha256 66d3c3ee…` at my snapshot), not the
   merge as-is: it keeps `w1_check_note`/`evidence`, keeps the seats' dispositions, adds
   no `next` to accepted-risk rows, and contains no status flips.
2. If the merge is kept, restore the 18 provenance fields, restore the 11 dispositions,
   drop the 25 invented `next` values, restore `R42-R3-25`'s fragment check, and record
   the 53 re-rootings + 4 assertion changes in the landing note.
3. Decide the row count explicitly: 71 (frozen target) or 75 (amended target with
   R51-R1..R4 named and justified). Do not ship a silent drift.
4. Require `C2ExecLedgerMerge.md` — the merge seat is a settled seat with no report.

VERDICT: **field loss is confined to `check` and is repairable, but the merged candidate
is not landable as-is** — 0 of 71 rows lost `id/class/source/opened_round/status/close/blocker/note`,
67 rows had `check` rewritten (53 invertible anchorings, 10 predicate-mandated
completions, 2 strengthened, 2 replaced), the wave's provenance keys for those rewrites
were deleted by the merge, 11 dispositions were re-decided, 25 `next` values were invented,
4 rows were added against a frozen `rows=71` target, and the merge seat filed no report.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
