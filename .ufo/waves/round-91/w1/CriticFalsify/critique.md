# CriticFalsify — round 91 falsification of the L1's numbers (read-only)

Scratch: `$S=/fast/scratch/hyaku/kengaku-r91/CriticFalsify` (clone `$S/lane` `--shared` from the lane; `$S/lane-base` a detached worktree at BASE). Removed on exit.
Revisions: BASE `59764383d4dd33d58faa50daad4c06d0cde410aa`, B `386184a6085ed01bbfbf73a4dc694a02fc3a01d5`, B2 `b836a862f5b9ba9cecbcff457003f1eabee70fba`, freeze A `cd0c116ef8c453d076031bdf5888b1e1b83bb0be`, TIP C `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0` (= lane `master`, confirmed by `git rev-parse master` and `jj-lane.sh state`).
No command below wrote to the lane tree; no git mutation ran in the lane; no subagent was spawned.

Verdict summary: C1 is NOT met at the measured tip (counter bug, finding 1). C2 is met at tip, with a literal frozen-text violation (finding 7). C3 is NOT met at the measured tip: the triage is absent from the committed tip and the gate refuses (findings 10–12). Counts for the ledger, routed rows, SOURCES rows, census and stamp hashes agree with the L1.

---

## Finding 1 — C1 counter cannot pass at tip: `parse_receipt` misreads CASE ids. DISAGREE with L1 (predicted `executed=1 mismatches=0 defects=0`)

Command (rc=1):
`python3 plans/round91_c1_replay.py --lane $S/lane --rev a8de3e69… --work $S/w-c1-a8de3e69…`
Output:
```
TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10 legs=20 mismatches=10 defects=10
DEFECT L5 receipt names unknown case ?      (x10)
PREDICATE R91-C1 fail
```
Same result with `--lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --rev a8de3e69…` (rc=1).

Evidence of cause: receipt lines are `CASE full-pass predicted=PP observed=PP ok=True …`; the id is the second positional token. `parse_receipt` (plans/round91_c1_replay.py lines 80–86) takes `id` from `key=value` tokens only, so `parts.get("id","?")` is always `?`. Calling `parse_receipt` on the tip receipt returns `ids: ['?', '?', '?', '?']  n= 10`.
Vector check done outside the counter (frozen `plans/round91-cases.json` vs receipt `predicted=`/`observed=`): `vector matches 10 of 10 ; table ids 10`. So the receipt content is correct; the counter's id parse is the only failing element at L5.

Other legs at tip (no DEFECT lines emitted): L1 receipt present; L2 SUBJECT_SHA ok; L3 LANE_TIP ancestor ok; L4 case table = A ok; L6 probe re-run rc=0 with observation block equal (no L6 defect); L7 ledger ok (no L7 defect); L8 pin ok; L9 stamp ok. Executed gating holds: `executed=0` printed while L5 fails (so the TARGET line does not overclaim).

Impact: C1 predicate ("pass iff L1–L9 all pass") is false at tip; the C1 kill rule applies ("any leg failing at the measured tip makes the claim unmet"). The fix is a one-line change in the counter (take `id` from the second token), but the counter is frozen and pinned (counter-pins-r91.json sha entry), so it is reported, not repaired. Note the same bytes are at B2 (B2→tip diff is empty for the counter).

## Finding 2 — C1 do-nothing at BASE: AGREE

`python3 plans/round91_c1_replay.py --lane $S/lane --rev 59764383… --work $S/w-c1-59764383…` rc=1:
```
TARGET executed_rows=34 member=modernize-scientific-stack located=1 executed=0 cases=0 legs=0 mismatches=0 defects=9
DEFECT L1 receipt absent at revision …          (L1 … L9, nine DEFECT lines)
PREDICATE R91-C1 fail
```
Exit 1 with `PREDICATE R91-C1 fail` as the frozen control requires. The "defects=N" value is N=9 measured (the frozen text did not predict N; it named the class). Agree on the class.

## Finding 3 — C1 receipt stamp against the tree: AGREE on every stamp field

Commands (each run in `$S/lane`, read-only from git objects):
- `git show b836a862:plans/round91_modernize_probe.py | sha256sum` → `d70210cbf7f326d1b33f13fa4169c6f28340a044660ce5451bf75ca06ef40e3c` (= receipt `TOOL_SHA`; same at tip).
- `git show a8de3e69:plans/round91-cases.json | sha256sum` → `89fab14b457364826065b77435626e0a16669abeebe67afe93ce6d2fe198ddf8` (= receipt `CASE_TABLE_SHA`; = same blob at freeze A).
- `git show a8de3e69:corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py | sha256sum` → `0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977` (= `SUBJECT_SHA`).
- `python3 -V` → `Python 3.14.8` (= `HOST_PYTHON`); `openssl version` → `OpenSSL 3.6.5 29 Sep 2026 …` (= `HOST_OPENSSL`); `cat /proc/sys/user/max_user_namespaces` → `122865` (= `HOST_USERNS`).
- `git merge-base --is-ancestor b836a862 a8de3e69` → rc=0 (receipt `LANE_TIP` b836a862 is an ancestor of tip).
- `git diff --stat b836a862 a8de3e69 -- plans/round91_modernize_probe.py` → empty (probe bytes unchanged B2→tip).

Note (not a defect of the stamp): the receipt is `WORKTREE dirty:1` and `LANE_TIP` is B2, not the tip. The frozen L3 is an ancestor check, so B2 passes it; the lesson discloses both.

## Finding 4 — C2 at BASE: AGREE

`python3 plans/round91_counter_pin.py --lane $S/lane --rev 59764383… --work $S/w-c2-59764383… --skip-selftest` rc=2:
```
DEFECT SETUP unreadable plans/counter-pins-r91.json
PREDICATE R91-C2 could-not-evaluate
```
Fail-closed exactly as predicted.

## Finding 5 — C2 at tip: AGREE on PINS=16; selftest count is a mispredict (disclosed as M1)

`python3 plans/round91_counter_pin.py --lane $S/lane --rev a8de3e69… --work $S/w-c2-a8de3e69… --skip-selftest` rc=0: 16 × `PIN-OK <path>`, then
```
PINS checked=16 matched=16 mismatched=0
PREDICATE R91-C2 pass
```
Default run with the selftest in the predicate path (`… --work $S/w-c2-tip-default`, no skip flag) rc=0: `SELFTEST clean-green rc=0 … SELFTEST counter-byte-mutated rc=1 …` (8 cases), `SELFTEST-DETAIL cases=8 red-green-ok=8`, `PINS checked=16 matched=16 mismatched=0`, `PREDICATE R91-C2 pass`.
The frozen text predicted C=6 selftest cases; measured 8. That mispredict is recorded in the L1 lesson as M1. Agree with the measured figure, and with the M1 disclosure.

## Finding 6 — B-revision selftest (M3, M4 of the lesson): PARTIAL AGREE (4/8 agrees; the cause stated for clean-green does not)

`git -C $S/lane show 386184a6:plans/round91_counter_pin.py > $S/c2-b.py` (13714 bytes).

Literal run from `$S` (`python3 $S/c2-b.py --lane $S/lane --rev 386184a6… --work … --selftest`) gives `SELFTEST-DETAIL cases=8 red-green-ok=0` rc=1. This is my invocation artifact: the selftest resolves its child as `Path(__file__).parent / "round91_counter_pin.py"`, which does not exist in `$S`, so all eight children return rc=2. Re-run with the checker copied to `$S/bplans/round91_counter_pin.py` (so the sibling resolves to itself):

Command (rc=1): `python3 $S/bplans/round91_counter_pin.py --lane $S/lane --rev 386184a6… --work $S/w-c2-b-selftest2 --selftest`
```
SELFTEST clean-green rc=2 want=0 defect-ok=True ok=False
SELFTEST counter-byte-mutated rc=1 want=1 defect-ok=True ok=True
SELFTEST path-absent rc=1 want=1 defect-ok=False ok=False
SELFTEST tampered-pin rc=1 want=1 defect-ok=True ok=True
SELFTEST blob-mutated rc=1 want=1 defect-ok=True ok=True
SELFTEST absent-pin-ledger rc=2 want=2 defect-ok=True ok=True
SELFTEST self-pin-mismatch rc=1 want=1 defect-ok=False ok=False
SELFTEST blob-anchor-missing rc=1 want=1 defect-ok=False ok=False
SELFTEST-DETAIL cases=8 red-green-ok=4
```
So at B: 4 of 8 red for the named reason — **agrees with M3's "4/8"**.

Causes, checked:
- The M3 text blames "the child process ran with PATH only". Disproved for clean-green: I ran the clean-green fixture with the same B checker and `env={"PATH":"/usr/bin:/bin"}` (with `--self-entry-path selfcopy.py`, `--rev HEAD`): `PINS checked=3 matched=3 mismatched=0` / `PREDICATE R91-C2 pass`, rc=0. The rc=2 for clean-green comes from the fixture itself: `checks.append(("clean-green", repo1, "", "", 0))` passes `rev=""` (fixture row, B selftest source). The lesson should name this, not PATH.
- path-absent, self-pin-mismatch and blob-anchor-missing print a defect string that does not match their named reason; the lesson's M3 list (sha vs blob id, absent path existing, self-pin not reached) is a partial account.
- At B2 (`git show b836a862:plans/round91_counter_pin.py`, run the same way from `$S/b2plans/`): `SELFTEST-DETAIL cases=8 red-green-ok=8`, rc=0. **Agrees with "8/8 at B2".**

## Finding 7 — C2 frozen tip rule and kill rule: literal violation (disclosed in M3), DISAGREE with the frozen text's "B" as pin anchor

`git diff --stat 386184a6 a8de3e69 -- <the ten pinned paths>`:
```
plans/counter-pins-r91.json  |   2 +-
plans/round91_counter_pin.py | 215 +++++++++++++++++++++-----------------
2 files changed, 105 insertions(+), 112 deletions(-)
```
`git diff --stat b836a862 a8de3e69 -- <same paths>` → empty (rc=0).
The frozen tip rule prints nothing against B; it prints against B. The C2 kill rule says "any edit to a pinned file, the pin ledger or this file after commit B". B2 edits both `plans/round91_counter_pin.py` and the pin ledger. The L1 discloses this (M3, "pinned commit moved from B to B2 … before any scoring"), so it is not hidden, but the literal frozen rule is violated and the claim text does not say which commit is the pin anchor. Verdict: the frozen element is wrong; reported, not repaired.

## Finding 8 — Ledger at BASE and tip: AGREE with every figure

`plans/grader-population-ledger.json` read with python3 at each revision:
- BASE `59764383`: members 88, executed 34; class cells `file-artifact 25`, `filesystem-metadata 2`, `numeric-band 3`, `stdout-inspection 10`, `subprocess-exec 12`. Member row: `status: unexecuted`.
- TIP `a8de3e69`: members 88, executed 35; `file-artifact 26`, `filesystem-metadata 3`, `numeric-band 4`, `stdout-inspection 11`, `subprocess-exec 13`. Member row: `status: executed, round: 91, receipt: corpus/evidence/round91/modernize-probe.txt, verdict: cases`.
The L1's 34→35, 25→26, 2→3, 3→4, 10→11, 12→13 all match. Agree.

## Finding 9 — Routed-findings rows at tip: AGREE on pending=30 parked=7 — but the triage is not in the tip

Python over `git show a8de3e69:corpus/routed-findings.jsonl` (213 lines, 0 malformed; effective state = status of the latest superseding row):
- effective status: closed 117, refused 25, blocked 7, open 30.
- open opened-round histogram: 82:1, 83:1, 84:4, 85:7, 86:2, 87:2, 88:2, 89:11 (sum 30). **No open row was opened in round 91.**
- blocked: R51-R1 (kama), R51-R2 (protocol), R51-R3 (owner `unowned:integrator`), R51-R4 (kama), R84-V4 (kengaku), R85-V8 (kengaku), R87-V1 (kengaku). The gate counts `unowned:integrator` as owned (non-empty string); that is a placeholder string passing the owner test. Flag.
- `git diff --stat 59764383 a8de3e69 -- corpus/routed-findings.jsonl` → empty; `git rev-parse` of the file blob is `830c0dae…` at BASE and at tip. **The routed-findings file is byte-identical from BASE to tip: no round-91 triage row is committed.** `resolutions=34` at BASE and at tip.
- The lane working tree (`git status --porcelain`, read-only): ` M SCORECARD.md`, ` M corpus/QUALITY.md`, `?? .ufo/waves/round-91/`. `corpus/routed-findings.jsonl` on disk is byte-equal to the tip blob (`cmp` rc=0). So the triage is not even uncommitted in the working tree.

## Finding 10 — C3 gate at tip: DISAGREE (predicted `freeze=admitted`; measured `refused`)

Command: `python3 plans/round91_burndown.py --lane $S/lane --rev a8de3e69… --work $S/w-c3-a8de3e69… --freeze-round 92` rc=1:
```
CHECK R42-R2 base-rc=1 … override-rc=0 … reason=None
CHECK R42-R3-33 base-rc=0 … override-rc=0 … reason=None
CHECK R42-R3-37 base-rc=0 … override-rc=0 … reason=None
CHECK R82-V8 … (only in the clone; see finding 13)
ROWS total=213 valid=212 invalid=1 superseded=34
DEFECT override-unjustified R42-R2
DEFECT override-unjustified R42-R3-33
DEFECT override-unjustified R42-R3-37
DEFECT check-failed R82-V8 rc=1 'CHECK v8 fail'     (clone run only)
freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3
SEEDS window=83-91 count=46 min=6 ok=True
PREDICATE R91-C3 fail
```
Run from the real lane path (`--lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --rev a8de3e69…`): same, minus the R82-V8 DEFECT; rc=1; `PREDICATE R91-C3 fail`.
Causes:
- `override-unjustified` on R42-R2, R42-R3-33, R42-R3-37: their superseding rows (`R42-R2-R90`, `R42-R3-33-R90`, `R42-R3-37-R90`, round-90 rows) have a `check` that differs from the base check and `supersedes` set, with no `override_reason`. The round-91 gate treats these round-90 closures as overrides and refuses them. The frozen claim's override rule is applied to rows it was not written for; nothing in the claim triages them.
- `pending=30`: every open row was opened in round 82–89; `oldest_pending_round=82 < 92-2`, so the frozen freeze rule refuses.
- The triage resolutions the claim requires (`resolutions>=35`, pending = round-91 rows only) are absent (finding 9).

Predicted vs measured (C3 "After"): `freeze=admitted` → `refused`; `pending=<round 91 only>` → 30; `parked=<all owned>` → 7 (owned, but R51-R3 is `unowned:integrator`, finding 9); `resolutions>=35` → 34; `checks_run>=117` → 114; `SELFTEST cases=9` → 13 (finding 12). C3 **not met**.

## Finding 11 — C3 BEFORE (BASE): PARTIAL AGREE

`python3 plans/round91_burndown.py --lane $S/lane --rev 59764383… --work $S/w-c3-59764383… --freeze-round 92` rc=1: `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`, `PREDICATE R91-C3 fail`. Same line as tip (routed-findings identical). Agree: refused, rc=1.
Disagree on the predicted detail: `pending>=29` agrees (30), but `malformed_or_invalid_unresolved>=1` does not: measured `malformed_unresolved=0` (the R82-F1 row is already superseded at BASE by `R82-F1-R90`; `ROWS … invalid=1 superseded=34`).
Note: the BASE and tip runs use the tip's `round91_burndown.py` over the BASE blob (the file does not exist at BASE). That is the intended do-nothing control, but it means the BASE verdict says nothing about the BASE gate's own code.

## Finding 12 — C3 selftest: all 13 cases green; prediction of 9 was wrong

`python3 plans/round91_burndown.py --lane $S/lane --work $S/w-c3-selftest --selftest` rc=0; `SELFTEST cases=13 red-green-ok=13`; each red case prints `substring-ok=True` and the named clause. Claim predicted `cases=9`: mispredict (count unit not derived; same class as M1). The selftest's own cases are sound in what they show; I did not attempt mutants.

## Finding 13 — R82-V8 check passes only from the real lane path: DISAGREE with the claim's "passes from a clone cwd"

The checker's v8 (`plans/round83_c2_checks.py`): `origin = R83_ORIGIN_REPO or ROOT`; `fleet = R83_FLEET_REPO or origin.parent`.
- From `$S/lane` (clone, `origin.parent = $S`): `python3 plans/round83_c2_checks.py v8` → `CHECK v8 fail`, rc=1.
- From `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (real lane, `origin.parent` = fleet root): the C3 gate has no R82-V8 DEFECT; the check passes.
So the claim's "the resolution row's check passes from a clone cwd" is false. `git diff --stat` B→tip does not list `plans/round83_c2_checks.py`: the repair the claim describes was not made (the lesson's M6 says the same). Verdict: frozen claim text describes a repair that is absent; reported, not repaired.

## Finding 14 — F1 counter (R82-F1 QUOTE_RE repair): AGREE at tip; the BASE behaviour is not what M4 says

At tip, `python3 plans/round91_f1_counter.py --lane $S/lane --work $S/w-f1-tip` rc=0:
```
PARSED S260=1,S261=2,S265=1,S266=2
ANCHORLINE rows=274 cited=84 captured=71 uncaptured=13 defective=10 repaired=10 live=0 cells=0 rc=0
WRONG-LINE-CAUGHT True
PREDICATE R91-F1 pass
```
Agree: four blind-spot rows parse; full checker `live=0`; the wrong-line fixture is caught.
At BASE: `python3 plans/round91_f1_counter.py --lane $S/lane-base --work $S/w-f1-base-tree` rc=1, with an uncaught traceback: `AttributeError: module 'anchor_line_check_r91' has no attribute 'anchor_quotes'`. The counter prints no `PARSE-ABSENT` line and no `could-not-evaluate` (exit 2): it has no guard for a missing symbol. M4 says the BASE checker shows `PARSE-ABSENT` for all four rows; the substance is right (the BASE QUOTE_RE finds 0 quotes in each of S260/S261/S265/S266 cells, measured by calling the BASE module's `parse_rows`/`QUOTE_RE.findall`), but the counter's printed evidence is a traceback. Defect for operability: missing-symbol path should print `DEFECT SETUP` and `PREDICATE R91-F1 could-not-evaluate` with exit 2.

## Finding 15 — Registry rows and census: AGREE

- `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at BASE → `272`; at tip → `274`. Agree with 272 and 274.
- `scripts/sources-census.sh` lives in the fleet root, not in the lane. From the lane (`cd $S/lane && scripts/sources-census.sh …`) it prints `command not found` rc=127. From the fleet root (`cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku; echo rc=$?`) the last line is `kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md` and `rc=0`. The claims' "exit 0 required" is met on the real lane file, but the command as written in the lesson/claim does not run from the lane root. Operability note.
- Census output also prints ~40 `W04 duplicate url … across scopes` warnings (warnings, not failures; rc=0).

## Finding 16 — Lane working tree (not part of the measured tip)

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain` → ` M SCORECARD.md`, ` M corpus/QUALITY.md`, `?? .ufo/waves/round-91/`. `git diff --stat` → SCORECARD.md +26, corpus/QUALITY.md +7. No committed round-91 LOG entry exists (`grep` of LOG.md finds only round-90 text for "round 91"). Nothing here changes the gate outputs, which read committed revisions.

---

## Consolidated table

| item | L1 figure | measured | verdict |
|---|---|---|---|
| C1 BASE rc / predicate | fail, rc 1 | rc 1, `PREDICATE R91-C1 fail` | agree |
| C1 tip rc / TARGET | executed=1 mismatches=0 defects=0 legs=20 | rc 1; executed=0 mismatches=10 defects=10 (L5 id parse) | **disagree** (F1) |
| C2 BASE | could-not-evaluate, rc 2 | rc 2 | agree |
| C2 tip | PINS 16/16, pass | rc 0, 16/16, pass | agree |
| C2 selftest count | 6 predicted | 8 | mispredict (M1) |
| C2 B selftest | 4/8 | 4/8 (literal run from scratch root: 0/8, invocation artifact) | agree (cause of clean-green red is `rev=""`, not PATH) |
| C2 B2 selftest | 8/8 | 8/8 rc 0 | agree |
| C2 tip rule vs B | prints nothing | prints 2 files | **literal violation** (F7) |
| C2 tip rule vs B2 | — | prints nothing | agree |
| ledger BASE | 34; 25/2/3/10/12 | 34; 25/2/3/10/12 | agree |
| ledger tip | 35; 26/3/4/11/13 | 35; 26/3/4/11/13 | agree |
| TOOL_SHA | d70210cb… | d70210cb… (B2 and tip) | agree |
| CASE_TABLE_SHA | 89fab14b… | 89fab14b… | agree |
| SUBJECT_SHA | 0c24195f… | 0c24195f… | agree |
| HOST_PYTHON / OPENSSL / USERNS | 3.14.8 / 3.6.5 / 122865 | same | agree |
| LANE_TIP ancestor | yes | rc 0 | agree |
| routed open / blocked | 30 / 7 | 30 / 7 | agree on counts; triage absent from tip (F9) |
| routed open opened in round 91 | (C3 predicate requires 0 before 91) | 0 in 91; all 30 in 82–89 | **disagree** (F10) |
| C3 BASE | refused, pending>=29, malformed>=1 | refused, pending=30, malformed=0 | partial (F11) |
| C3 tip | admitted | refused rc 1 (3 override-unjustified + pending) | **disagree** (F10) |
| C3 selftest cases | 9 | 13, 13/13 green | mispredict (F12) |
| C3 checks_run / resolutions | >=117 / >=35 | 114 / 34 | **disagree** |
| R82-V8 from clone | passes (claim) | fails rc 1 from clone; passes from real lane | **disagree** (F13) |
| F1 counter tip | PARSED 4 rows, live=0, caught | same, rc 0 | agree |
| F1 counter BASE | PARSE-ABSENT (M4) | traceback AttributeError, rc 1 | partial (F14) |
| SOURCES rows | 272 / 274 | 272 / 274 | agree |
| census | exit 0 | rc 0 from fleet root; rc 127 from lane | agree (operability note) |

## Calibration note

Three numbers I could not falsify: the ledger counts, the stamp hashes, and the routed counts (30/7). Two things I could: the C1 counter's id parse (blocks C1 at tip), and the absence of the round-91 triage from the committed tip (blocks C3). The B-revision selftest 4/8 agrees with the lesson; the cause the lesson gives for clean-green is not the cause I measured.
