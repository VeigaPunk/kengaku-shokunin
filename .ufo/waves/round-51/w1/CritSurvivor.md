# CritSurvivor — survivor analysis of the routed-findings ledger (round 51, seat w1)

Seat: `CritSurvivor` (critic, leaf — no dispatch).
Lane: `kengaku-shokunin` · round 51 · hyaku run 11.
Item: for every row with `status=closed`, does a *surviving* artifact prove the close, or only the
`close` prose? Report `evidence-survives` vs `prose-only`; for prose-only rows name the cheapest
check that restores proof.
Read-only against the lane; the only lane write is this file.

## Axes named

- **adjacency (judged).** The ledger is the lane's cross-domain evidence record, and the round's C2
  claim turns it into `owner` + `disposition`. Survivor analysis is the pre-condition for an honest
  `disposition`: a row may only be `fixed-verified`/`fixed-historical` if an artifact that survives a
  clean clone proves the close. Everything below is expressed in those terms.
- **freshness (secondary).** A close whose only proof is prose is stale evidence regardless of its
  date; the "red before the fix / green at the tip" probe is the freshness test for a row.

## Revision measured

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` — one `git clone --shared` into scratch
(`/fast/scratch/hyaku/kengaku-r51/CritSurvivor/lane`), `git -C lane rev-parse --show-toplevel` =
that dir, `git status --porcelain` = 0 lines before and after every probe below.
Instrument measured: the **committed** `plans/round51_routing.py` at that revision, sha256
`7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03` (the lane working tree carries a
different copy — X7).
`git diff e07f131cf7037e58a21db6e1f3986cf401ad257c 4090c3d -- corpus/routed-findings.jsonl` is empty,
so the ledger measured here is the stage-1 freeze ledger; the before receipt
`.ufo/waves/round-51/claims/c2-before.txt` reproduces line-for-line at this revision (run below).

## Method — exact commands

All commands run with cwd = the clean clone (or a `git archive` tree extracted from it), `TMPDIR`
exported to the seat scratch. Checks were executed with `bash -lc`, 60 s timeout, `LANE` exported.

```
# 1. population
python3 dump_closed.py corpus/routed-findings.jsonl          # 41 closed of 71
# 2. does each closed row's check pass at the lane root (clean clone)?
python3 survivor_probe.py lane                               # cwd=lane, LANE=lane
# 3. does the same check pass the way the frozen counter runs it?
python3 probe2.py                                            # cwd=lane vs cwd=<scratch tmp>, LANE=lane
# 4. was the check red at the pre-fix revision? (git archive of <fix>^ / round tip, no git mutation)
python3 discriminate.py ; python3 fix_before.py
# 5. which disposition can the frozen instrument actually accept?
python3 eligible.py                                          # fixed-verified / fixed-historical / neither
# 6. committed receipts naming each row
python3 receipts.py                                          # grep -rl <id> .ufo/waves
# 7. the frozen counter and its selftest
python3 plans/round51_routing.py --lane .                    # exit 1 (before state)
python3 plans/round51_routing.py --selftest                  # cases=11 failures=0 ALL PASS
# 8. pinned-digest re-computation
sha256sum plans/round42_c1_verify.py plans/scratch_guard.py
```

## Result — the split

```
CLOSED total=41 evidence-survives=41 prose-only=0
PASS lane-root 41 / 41
PASS frozen-cwd 2 / 41
FAIL frozen-cwd 39
```

**Every closed row has a check (41/41), and every one of those checks passes at the lane root of a
clean clone at `4090c3d`.** No closed row is proven by prose alone: 0 `prose-only`.

Proof strength inside `evidence-survives` (mutually exclusive, machine-derived):

| artifact class | rows | what survives |
|---|---|---|
| `re-derivable` | 3 | the check re-runs a lane instrument or git query (`R42-R2.1` selftest, `R42-R4` git diff, `R45-S5-1` `anchor_line_check.py`) |
| `receipt` | 4 | the check asserts a committed `.ufo/waves/` receipt/build artifact (`R40-R2`, `R40-R4`, `R45-S5-5`, `R45-S5-7a`) |
| `landed-content` | 31 | the check asserts content of a committed production file (errata/registry/lesson/entry/instrument) |
| `self-record` | 2 | the only asserted artifact is the ledger itself (`R42-R3-24`, `R42-R3-25`), backed by a resolving commit |
| `absence` | 1 | a negative path test (`R39-R5`), backed by a committed measurement receipt (below) |

Two rows are non-discriminating — green both before and after the named fix: `R42-R2.1` (the tool and
its selftest already passed at the round-42 tip; harmless, the check re-derives a live selftest) and
`R39-R5` (see §"the one row whose own check proves nothing").

Pinned artifacts re-computed at this revision and still exact:

```
559fca0c9254e4c09f2406f75ba9559e370012ccb1ecdc91c9a944abbe0c6649  plans/round42_c1_verify.py
f0360e3028c79ce32fcabf7f89f0103b88205200bce802a8b2520e1f9364aa5d  plans/scratch_guard.py
```
(both match the digests quoted in `R40-R1` and `R42-R2.1`).

## Per-row table

`check @lane` / `check @frozen cwd` are exit codes; `red before fix` = the check fails at the parent
of the earliest commit the close names (or at the row's opening-round tip when no commit is named).

| row | artifact class | check @lane | check @frozen cwd | red before fix | own check |
|---|---|---|---|---|---|
| R39-R1 | landed-content | 0 | 2 | yes | ok |
| R39-R5 | absence | 0 | 0 | NO | weak |
| R40-R1 | landed-content | 0 | 2 | yes | ok |
| R40-R2 | receipt | 0 | 2 | yes | ok |
| R40-R3 | landed-content | 0 | 2 | yes | ok |
| R40-R4 | receipt | 0 | 2 | yes | ok |
| R42-R2 | landed-content | 0 | 1 | yes | ok |
| R42-R4 | re-derivable | 0 | 2 | yes | ok |
| R40-R1.1 | landed-content | 0 | 2 | yes | ok |
| R42-R2.1 | re-derivable | 0 | 1 | NO (green at round-42 tip) | ok |
| R42-R2.2 | landed-content | 0 | 2 | yes | weak |
| R42-R3-01 | landed-content | 0 | 2 | yes | ok |
| R42-R3-03 | landed-content | 0 | 0 | yes | weak |
| R42-R3-04 | landed-content | 0 | 2 | yes | ok |
| R42-R3-10 | landed-content | 0 | 2 | yes | ok |
| R42-R3-11 | landed-content | 0 | 2 | yes (77ea425^) | ok |
| R42-R3-12 | landed-content | 0 | 2 | yes | ok |
| R42-R3-13 | landed-content | 0 | 2 | yes | ok |
| R42-R3-15 | landed-content | 0 | 2 | yes | ok |
| R42-R3-17 | landed-content | 0 | 2 | yes | ok |
| R42-R3-20 | landed-content | 0 | 2 | yes | ok |
| R42-R3-21 | landed-content | 0 | 2 | yes | ok |
| R42-R3-22 | landed-content | 0 | 2 | yes | ok |
| R42-R3-23 | landed-content | 0 | 2 | yes | ok |
| R42-R3-24 | self-record | 0 | 2 | yes | weak |
| R42-R3-25 | self-record | 0 | 2 | yes | weak |
| R42-R3-28 | landed-content | 0 | 2 | yes | ok |
| R42-R3-29 | landed-content | 0 | 2 | yes | weak |
| R42-R3-30 | landed-content | 0 | 2 | yes | weak |
| R42-R3-31 | landed-content | 0 | 2 | yes | ok |
| R42-R3-38 | landed-content | 0 | 2 | yes | ok |
| R42-R3-39 | landed-content | 0 | 2 | yes | ok |
| R42-R3-40 | landed-content | 0 | 2 | yes | ok |
| R42-R3-41 | landed-content | 0 | 2 | yes | ok |
| R45-S5-1 | re-derivable | 0 | 2 | yes | ok |
| R45-S5-2 | landed-content | 0 | 2 | yes | weak |
| R45-S5-3 | landed-content | 0 | 2 | yes | ok |
| R45-S5-4 | landed-content | 0 | 2 | yes | weak |
| R45-S5-5 | receipt | 0 | 2 | yes | ok |
| R45-S5-6 | landed-content | 0 | 2 | yes | ok |
| R45-S5-7a | receipt | 0 | 1 | yes | weak |

The 10 check-less rows of the ledger (`CHECKS present=61 absent=10`) are all `status=open`
(`R40-R5`, `R42-R3-09`, `R42-R3-33/34/35/37`, `R45-S5-7b/c/d/e`) — none is closed, so the survivor
class does not reach them.

## The one row whose own check proves nothing — `R39-R5`

`close`: "measured 2026-10-26: `ls -d /fast/scratch/hyaku/kengaku-r39*` -> no such file".
`check`: `test ! -e /fast/scratch/hyaku/kengaku-r39`.

Two defects, both cheap: (a) the check is a fixed path, the close's claim is a glob, so
`kengaku-r39-extra` would not flip it; (b) it is true on any host that never ran round 39, so it is
green before and after. A receipt does survive — `.ufo/waves/round-41/build/R41RoutedRider/measure-tip.txt:33`
records `$ ls -d /fast/scratch/hyaku/kengaku-r39; echo rc=$?` and
`.ufo/waves/round-41/falsify/F41RevRider.md:46` records the glob form — which is why the row still
counts as `evidence-survives`, but the row's *own* check is not what proves it.

Cheapest restoring check (verified PASS at this revision):

```sh
test -z "$(ls -d /fast/scratch/hyaku/kengaku-r39* 2>/dev/null)"
```

## The 9 other under-proving checks and their cheapest restoring check

Each replacement was executed at `4090c3d` and printed PASS (measured, not proposed on faith):

| row | why the current check under-proves | cheapest restoring check (PASS measured) |
|---|---|---|
| R42-R2.2 | `grep -qs 'scratch-root-guard' SKILL.md` matches any mention, not the registry row | `grep -qE '^\| `scratch-root-guard`' SKILL.md` |
| R42-R3-03 | `grep A \|\| ! grep B` — passes because the file is *absent* (measured: rc=0 in an empty cwd) | `grep -q ':96' corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (drop the `\|\| !` clause) |
| R42-R3-24 | greps the ledger for the ledger (`"id": "R42-R4"…"status": "closed"`) | `python3 plans/routed_open.py --lane . --observe \| grep -q '^OBSERVE rows=71 mismatched=0'` |
| R42-R3-25 | greps the ledger for a row that merely *mentions* the tool | `grep -qE '"id": "R42-R2\.1".*plans/scratch_guard\.py' corpus/routed-findings.jsonl && python3 plans/scratch_guard.py --selftest >/dev/null 2>&1` |
| R42-R3-29 | `grep -rqs ':59-61' corpus/lessons/` matches any lesson | `grep -qF ':59-61' corpus/lessons/round-42.md` |
| R42-R3-30 | `grep -rqsE 'X7[^|]*:91-92' corpus/lessons/` matches any lesson | `grep -qE 'X7[^|]*:91-92' corpus/lessons/round-42.md` |
| R45-S5-2 | asserts only the `## Errata (round 46)` heading; the close claims a predictor change + `disagree=0` on 16 states | `grep -q '^B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok' .ufo/waves/round-46/integrate/c2-landing.txt` |
| R45-S5-4 | greps `S166` for a claim about *every* new row S157-S172 | `for n in $(seq 157 172); do grep -q "S$n" corpus/lessons/round-46.md \|\| exit 1; done` |
| R45-S5-7a | `test -f` a control receipt; the close claims `PREDICATE C1 pass` | `grep -q 'PREDICATE C1 pass' .ufo/waves/round-46/integrate/c1-landing.txt` |

## Counterexamples against the frozen C2 counter (the load-bearing part)

These are the ways the round's own instrument would misreport the ledger it is measuring. All are
measured at `4090c3d`; none requires a model or a network.

**X1 — the frozen `--run-checks` cwd hides 39 of the 41 surviving checks.** `check()` runs each
command with `cwd=tmp` (a fresh scratch dir), not the lane. Measured: 41/41 closed-row checks exit 0
with `cwd=<clone root>`, **2/41** with `cwd=<scratch tmp>`; 39 rows change exit code between the two.
If the L1 marks any of those 39 `fixed-verified`, `CHECK_FAILED` rises and the after-target
(`CHECK_FAILED 0`) is unreachable. The claim's declared limit ("in a scratch cwd") forbids silently
changing the instrument, so the smallest safe correction is at the data: prefix every
`fixed-verified` row's check with `cd "$LANE" && ` (the instrument already exports `LANE`).

**X2 — the two rows the frozen counter *would* accept as `fixed-verified` are the two whose checks
prove nothing.** Under `cwd=<scratch tmp>` only `R39-R5` (`test ! -e /fast/…/kengaku-r39`) and
`R42-R3-03` (`grep A || ! grep B`) exit 0. The first is true on any host; the second passes *because
the target file is invisible in the scratch cwd*:

```
$ bash -lc "grep -q ':96' corpus/knowledge/tb2-circuit-fibsqrt-grader.md || ! grep -q 'dropped if that fails' corpus/knowledge/tb2-circuit-fibsqrt-grader.md"; echo $?
0        # cwd = empty dir: both files absent, the negation is vacuously true
```
So the instrument's `fixed-verified` leg currently *selects* the vacuous checks and rejects every
real one. X1's fix removes this too (at the lane root the disjunction passes for the intended reason),
but the disjunction should still be dropped — a `fixed-verified` check must not be satisfiable by
absence.

**X3 — the `fixed-historical` leg rejects 4 rows that name a real commit.** `close.split()[0].strip(",")`
keeps a trailing colon, so `c1ec334c:` fails the hex regex and `corpus/QUALITY.md:759` fails the path
test. Measured eligibility for the 41 closed rows under the frozen rules:

```
FIXED-VERIFIED eligible under frozen cwd: 2 -> ['R39-R5', 'R42-R3-03']
FIXED-HISTORICAL eligible (instrument first-token rule): 17
NEITHER (would need accepted-risk/routed/referral): 22
```
22 rows are eligible for neither disposition although all 41 checks pass at the lane root. Five of
the 22 fail only because of the colon (`R40-R2` `…:5`, `R40-R4` `…:28`, `R42-R4` `corpus/QUALITY.md:759`,
`R45-S5-1` `c1ec334c:`, `R45-S5-2` `c1ec334c:`); the other 17 open with prose ("round-43", "children",
"F1-F4", "round-46"). Correction: `tok = tok.rstrip(":,")` and strip a `:<line>` suffix before the
path test (one line in `check()`), or make each `close` begin with a bare ref (data edit).

**X4 — `fixed-historical` tests resolution, not provenance.** `git cat-file -e <tok>^{commit}` accepts
any commit; a row can cite `77ea425a` (a 19-file landing commit) without that commit touching its
artifact. Not exploited today — measured, the 13 rows whose first token is `77ea425a` all name a
commit whose `--name-only` list contains the file their check asserts (`R39-R1`'s `ec17216` does too)
— but the predicate cannot tell the two cases apart. One-line strengthening if the L1 wants the
disposition to mean something: require `git show --name-only --format= <c>` to list the `source` or
`check` path.

**X5 — seven closed rows have no committed receipt naming them.** All `R45-S5-*` rows return 0 hits
from `grep -rl <id> .ufo/waves` (excluding round-51); their evidence is the check plus receipts that
do not name the row (`R45-S5-2`'s `disagree=0` is in `.ufo/waves/round-46/integrate/c2-landing.txt:6`,
unnamed; `R45-S5-7a`'s `PREDICATE C1 pass` is in `…/c1-landing.txt:210`, unnamed). Not a defect of the
close, but it means a reader cannot follow a receipt back to the row: the cheapest repair is to add
the row id to the receipt line when the L1 attributes these rows.

**X6 — the frozen owner universe never reads `../shokunin.conf`.** `load_owners` matches
`([a-z][a-z0-9-]{2,15}):\s*\{`, but the real conf writes lanes as `id | repo | axes` rows. Measured
against the live conf: **0 matches** for the frozen regex, **23** for the working-tree regex. The
frozen owner universe is therefore exactly `FALLBACK_OWNERS` (17 hardcoded names), so the claim's
sentence "every `owner` names a fleet lane from `../shokunin.conf`" is not what the frozen bytes
measure. Concretely, a fixture row owned by a real lane that the fallback list omits is rejected:

```
$ python3 plans/round51_routing.py --lane fx/fleet/lane      # fixture, conf copied verbatim
OWNERS attributed=0 unattributed=1
  DETAIL OWNER R1 owner 'tsukuroi' not a fleet lane
PREDICATE R51-C2 fail                                        (exit 1)
```
Seven real lanes (`audio`, `game-dev-2d`, `game-dev-3d`, `lore`, `mado`, `revenger`, `tsukuroi`) are
rejected this way; `unowned:integrator` is accepted without being a lane at all (the claim allows it
by name). Correction: read the conf's `id | …` rows (the working-tree edit already does) and keep the
fallback only as a degraded-mode set, flagged in the output when it is the only source.

**X7 — the freeze is dirty: the lane's working tree carries an uncommitted edit to the frozen
counter.** At measurement time `git status --porcelain` in the lane printed
` M plans/round51_routing.py` (mtime `2026-10-28 15:33:21 -0300`), committed blob sha256
`7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03` vs working-tree
`6f084fdfa3caf003c9e8580d96c4eb63e434f90b7cd9c1bdd8ca70619ad472ba` (+13/−5). Every measurement in
this report is of the **committed** bytes at `4090c3d`. The working-tree diff changes three frozen
things: `cwd=str(tmp)` → `cwd=str(lane)`, timeout `60` → `90`, and the owner loading (X6). Two
consequences the L1 must settle before landing:

1. The claim's declared limit is "a 60 s timeout each **in a scratch cwd**". Landing the working-tree
   copy without a dated claims amendment makes the C2 measurement *not* the frozen predicate — the
   exact "shipped counter is not the one described" class of round-50 D2.
2. The working-tree edit already implements the X1/X2 and X6 corrections. Take that path and amend
   the claims (dated, with both digests), rather than re-deriving it; X3 (colon token) and X4
   (provenance) are still unfixed in both versions.

## Limits

- The survivor class is measured only through each row's own `check` and the artifacts that check
  names. A row can be `evidence-survives` while the check under-proves it — 10 such rows are listed
  above; I did not re-verify the *content* of every errata sentence against the underlying defect
  (that is the reviewer/executor seats' item), only that the artifact is committed, present, and
  absent before the fix.
- `git archive` trees have no `.git`, so `R42-R4`'s `git diff` check could not be evaluated at its
  before-revision; its `red before fix` verdict comes from the round-42 tip instead.
- Host-state claims (`R39-R5`) can only be re-measured on this host; the committed receipt is the
  only portable evidence and it is a round-41 re-measurement, not a round-39 one.
- No model was used; no network was used. No tool was installed or upgraded (nothing needed).
- Scratch `/fast/scratch/hyaku/kengaku-r51/CritSurvivor` was removed before yield; free space seen
  at start: `553G` on `/fast` (32 % used).

## Verdict

The ledger's closed half is in better survivor shape than the round's own counter can see: 41/41
closed rows carry a check that passes in a clean clone and 39/41 fail at the pre-fix revision, so
`prose-only = 0` and `evidence-survives = 41`. The exposure is entirely on the instrument side —
its cwd semantics reject 39 real checks and accept exactly the 2 vacuous ones, its token rule rejects
4 real commit refs, 22 rows are currently eligible for no disposition at all, and its owner universe
never reads `../shokunin.conf` (7 real lanes rejected). The lane working tree already holds an
uncommitted fix for two of those; landing it without a dated claims amendment would make the round's
C2 measurement not the frozen predicate. Fix the instrument defects and amend, or the `disposition`
field will be filled with values the evidence does not support.

VERDICT: PASS-WITH-FINDINGS — survivor split 41 evidence-survives / 0 prose-only; 10 checks
under-prove their close (cheapest replacements given and verified); 5 instrument defects (cwd, colon
token, vacuous-disjunction acceptance, non-discriminating provenance, hardcoded owner universe) plus
a dirty freeze (`M plans/round51_routing.py`, +13/−5, unamended) block the C2 after-target as frozen.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
