# R90 CriticFalsify — critique of the round-90 claims (read-only)

Seat: CriticFalsify (leaf, no subagents, no mutating git in the lane). Lane clone and fixtures under
`/fast/scratch/hyaku/kengaku-r90/CriticFalsify` (scratch only; receipts copied to `evidence/` here before
the scratch removal). Revisions measured: BASE `dcdd494ef4b4a6c0ae349ecb597527124ee54f91`, pin commit B
`664435cfcb9419c4e8ac7828a55aec11a1f36ec4`, freeze commit A `45171d231f0444625106abf63cd4b0804d8812bd`.
Revision trees were taken with `git -C <lane> archive <rev>` (no checkout in the lane). Every number below
carries the command and its output (or the evidence file it was copied from, under `evidence/`).

Shell note: the persistent shell carried `set -e` from an earlier call in this seat; it was reset with
`set +e +u` before the later measurements. No command output below was produced under errexit.

Tooling: no install was made by this seat. `bwrap 0.13.1` (`/usr/bin/bwrap`), `git 2.56.0`, `Python 3.14.8`,
`OpenSSL 3.6.5` were used as found.

---

## 1. Re-run of the L1 BASE battery (BASE and B)

Command (all three counters taken from the B tree; lane = my clone; `evidence/batt-out.txt`,
script `evidence/run-batt.sh`):

```
python3 x-664435cf/plans/round90_c1_replay.py --lane <clone> --rev dcdd494e… --work w-c1base   -> rc=1
python3 x-664435cf/plans/round90_counter_pin.py --lane <clone> --rev dcdd494e… --work w-c2base -> rc=2
python3 x-664435cf/plans/round90_counter_pin.py --lane <clone> --rev 664435cf… --work w-c2b    -> rc=0
python3 x-664435cf/plans/round90_counter_pin.py --selftest …                                   -> rc=0
python3 x-664435cf/plans/round90_burndown.py --lane <clone> --rev dcdd494e… --freeze-round 90  -> rc=1
python3 x-664435cf/plans/round90_burndown.py --lane <clone> --rev 664435cf… --freeze-round 90  -> rc=1
python3 x-664435cf/plans/round90_burndown.py --selftest …                                       -> rc=0
```

Output (verbatim tail lines):

```
C1 BASE: TARGET executed_rows=33 member=merge-diff-arc-agi-task located=1 executed=0 cases=0 legs=0 mismatches=0 defects=10
C1 BASE: PREDICATE R90-C1 fail        rc=1          (matches transcript: defects=10, 6 L7 lines)
C2 BASE: DEFECT SETUP unreadable plans/counter-pins-r90.json at dcdd494ef4b4
C2 BASE: PREDICATE R90-C2 could-not-evaluate         rc=2   (matches transcript)
C2 B:    RECORD-TABLE blob=163f284316141a83 matched / PINS checked=7 matched=7 mismatched=0 / PREDICATE R90-C2 pass  rc=0
C2 selftest: cases=5 red-green-ok=5  rc=0              (matches)
C3 BASE: freeze=refused oldest_pending_round=39 pending=33 malformed_unresolved=1 seeds_83_89=0 resolutions=0 checks_run=98
C3 BASE: PREDICATE R90-C3 fail  rc=1
C3 B:    identical summary, rc=1
C3 selftest: cases=7 red-green-ok=7  rc=0              (matches)
```

Deviations from `plans/…/L1/base-batteries.txt`:

- **F-1 (MINOR, deviation, location-dependent gate).** The C3 gate run from my clone location printed one extra
  defect the transcript does not contain: `DEFECT check-failed R82-V8 rc=1 'CHECK v8 fail'` (so
  `checks_run=98`, same summary, `PREDICATE R90-C3 fail`). The same command against the real lane path
  (`--lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only, `evidence/gate-real.txt`) reproduces the
  transcript exactly (no R82-V8 line). Cause: the R82-V8 check reads `origin.parent` as the fleet repo
  (`plans/round83_c2_checks.py:v8`, `R83_FLEET_REPO` default). Gate `run_check` (`plans/round90_burndown.py:196-204`)
  sets env to `PATH,HOME,LANE` only, so the variable cannot be passed. Verified: with `R83_FLEET_REPO` set in the
  calling env, the gate still prints the V8 defect (`evidence/gate-env.txt`); run directly, `R83_FLEET_REPO=<fleet>
  python3 plans/round83_c2_checks.py v8` prints `CHECK v8 ok rc=0` and without it `CHECK v8 fail rc=1`
  (`evidence/v8-env.txt`). So the freeze verdict depends on the directory the lane is cloned into. The transcript
  is correct for the real lane path; the dependence is not recorded anywhere.
- No other deviation. The C1 base defect lines are byte-identical to the transcript (L4/L8/L1 absent, six L7 lines).
  The C1 run at B gives defects=8 (L4 and L8 pass at B, as expected) — consistent by inspection of `round90_c1_replay.py:159-185`.

Freeze-round check, run from the base lane via the real path (`evidence/gate-real.txt`): `freeze=refused oldest_pending_round=39 pending=33 malformed_unresolved=1 seeds_83_89=0 resolutions=0 checks_run=98`, `DEFECT check-failed R42-R2 rc=1 ''` (the historical close that fails, as the claims say).

---

## 2. Ledger truth from git bytes at BASE

Command: `git -C <lane> show dcdd494ef4b4a6c0ae349ecb597527124ee54f91:plans/grader-population-ledger.json > ledger-base.json`
(`cmp` against the B bytes: identical), then:

```
python3 - <<EOF  (json.load; members = dict; status counts; class cells by executed/total)
members 88
status Counter({'unexecuted': 55, 'executed': 33})
git-plumbing: executed 1 of 3
serialization-schema: executed 3 of 10
file-artifact: executed 24 of 76
stdout-inspection: executed 9 of 29
subprocess-exec: executed 11 of 45
```

All six base numbers in the claims match exactly. (Evidence: `evidence/ledger-base.json`.)

After-values (the frozen C1 prediction): members 88 unchanged, executed 33 → 34; git-plumbing 1/3 → 2/3;
serialization-schema 3/10 → 4/10; file-artifact 24/76 → 25/76; stdout-inspection 9/29 → 10/29;
subprocess-exec 11/45 → 12/45. Each is base +1 in both numerator (the flipped member has exactly those five
classes; the merge-diff row is `classes: [file-artifact, git-plumbing, serialization-schema, stdout-inspection,
subprocess-exec]`, `status: unexecuted`) and the denominator is unchanged. The arithmetic is internally consistent
for a single flip. It is a single-member consistency check, not evidence that the flip happened.

- **F-2 (MINOR, frozen text, C1 prose).** The claim calls git-plumbing "the thinnest executed-or-not class cell".
  Computed from the same bytes:
  ```
  by executed fraction (ascending): filesystem-metadata 2/10=0.200, subprocess-exec 11/45=0.244, crypto-credential 3/12=0.250,
     numeric-band 3/10=0.300, serialization-schema 3/10=0.300, stdout-inspection 9/29=0.310, file-artifact 24/76=0.316,
     git-plumbing 1/3=0.333 (tied with timing-wall and shell-exec)
  by total members: signal-delivery 1, db-state 2, git-plumbing 3 (tied with process-environment)
  by executed count: db-state 1, git-plumbing 1, signal-delivery 1 (tied)
  ```
  So "thinnest" holds for none of the three measures. Recorded, not repaired.
- **F-3 (MINOR, frozen text, C1 prose).** "this is its first executed member since the ledger began" is contradicted
  by the BASE ledger: the one executed git-plumbing member is already `git-leak-recovery` (status executed). The merge-diff
  flip would be the second, not the first. Recorded, not repaired.

---

## 3. Independent derivation of the predicted vectors from the captured grader bytes

Captured grader: `git -C <lane> show dcdd494e:corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py`
→ `sha256 2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149` (matches SUBJECT_SHA; 3034 bytes).
Five test functions in definition order: test_git_repo_init, test_both_bundles_fetched, test_algo_py_exists,
test_algo_py_has_map_function, test_algo_map_function_with_test_input (matches the frozen LEGS tuple).

My derivation (from reading the grader only, before running anything): full-solution PPPPP; no-git-dir FFPPP
(.git absent → F; `git branch -a` rc 128 → F); one-branch PFPPP; algo-missing PPFEE (exists F; spec exec FileNotFoundError E
at 4 and 5); algo-syntax-error PPPEE; map-wrong-values PPPPF (first element 1≠5); test-json-corrupt PPPPE
(JSONDecodeError at json.load); map-shape-short PPPPF (len 1≠3). All eight match `plans/round90-cases.json` `predicted`.

The frozen case table is byte-identical at A and B: `git show 45171d23:plans/round90-cases.json | sha256sum` and
`git show 664435cf:plans/round90-cases.json | sha256sum` both print `7e198cd18756c0fd857fb9544f1b76a162928f8cef1f5848a1b677aa2cf6f0a4`.

Independent execution of the B probe (not a prediction, a run): `python3 x-664435cf/plans/round90_polydiff_probe.py
--lane x-664435cf --work w-probe` → rc=0; `CASE full-solution predicted=PPPPP observed=PPPPP` … all eight `predicted=observed`;
`cases=8 legs=40 mismatches=0`; `PREDICATE R90-PROBE pass`; `TOOL_SHA 2c4f0ab1e0d456416f4fe114bb47c9207a89b8a594ac80861064bad1e1ad9be3`
(= counter `TRUSTED_TOOL_SHA`). `HOST_USERNS 122865` (bwrap works on this host at measurement time).
Output: `evidence/probe-out.txt`.

- **F-4 (MINOR, frozen text, C1).** The claim's honest-limit (a) lists the first distinct vector as `PPPPPP`
  (six characters). The case table's full-solution vector is `PPPPP` (five). The distinct count is still seven
  (`PPPPP, FFPPP, PFPPP, PPFEE, PPPEE, PPPPF, PPPPE`). Recorded, not repaired.
- **F-5 (MINOR, frozen text, C1 after-line).** The predicted TARGET line reads `cases=8 legs=8`. The counter prints
  `legs = cases * 5` (`plans/round90_c1_replay.py:288`) → `legs=40` for eight cases; the probe's own summary is
  `cases=8 legs=40`. The predicted TARGET line is inconsistent with the counter's own formula. Recorded, not repaired.
- **F-6 (MINOR, frozen text, C1 legs).** The claim says `L1–L8` are the legs, but the counter's TARGET `legs=` counts
  probe legs (40). Same root as F-5.
- **F-7 (OBSERVATION, C1 host sensitivity).** `plans/round90_c1_replay.py:243-252`: when the probe re-run (L6) dies on the
  sandbox (`SetupDefect` → rc 2 with no observation block), the counter records `DEFECT L6-reproduce … produced no
  observation block` and the verdict is `PREDICATE R90-C1 fail`, not `could-not-evaluate`. A host-level outage (the
  2026-11-05 `user.max_user_namespaces=0` event in the wave bounds) would therefore read as a claim failure. Not triggered
  here (userns 122865; probe ran); code-read only (I did not change any sysctl).

---

## 4. Triage drafts (`.ufo/waves/round-90/w1/ExecC3Triage/`)

Checked at the time of this critique: the directory does not exist (`ls -d …/w1/ExecC3Triage` → "No such file or
directory"; `w1/` contains ConnectorOverlap, ExecLedgerFlip, ExecNoWork, ScribeR90, SentinelForge only). **Skipped**, sample
verification of five drafted resolution rows not possible. Not a finding against the drafts; recorded as absent.

---

## 5. C2 pin semantics (attack)

Pin ledger and checker bytes read from B; `counter-pins-r90.json` pin shas match the base/B bytes for the four
pre-existing counters (`sha256` at base `229a0edd…`, `c59e761c…`, `9a107758…` == pins; the round-90 entries are absent
at BASE, which is why C2 at BASE is rc2 SETUP). Record table: `git rev-parse dcdd494e:plans/round89-q66-records.json`
= `163f284316141a831484dacb7f69ad4cbbaadfb3`; anchor `0e6bb05f` is an ancestor of BASE (`merge-base --is-ancestor` rc 0);
`git cat-file -e d1c4f1b0:plans/round89-q66-records.json` → rc 128 (the path, not the commit, is absent there), as claimed.

Forgery fixtures: a fixture repo under `fx-c2.*` (mktemp under scratch, author `t <t@t>`) with the B `plans/` tree as
commit c1 (`82d2d09a…`), then branches d1, d2, d3 each one commit off c1. Checkers were run from each commit's own
`plans/round90_counter_pin.py` bytes (the lane-shipped checker is what a lane-tree reviewer would run), and against the
honest B checker for the control. Output: `evidence/c2-forgery.txt`.

```
d1 (ledger record_table.blob := 0*40 only; checker and counter untouched):
   RECORD-TABLE blob=163f284316141a83 matched
   PINS checked=7 matched=7 mismatched=0   PREDICATE R90-C2 pass   rc=0
d2 (plans/round90_c1_replay.py gets a trailing comment; plans/round90_counter_pin.py check() short-circuited to return 7,7,0; ledger NOT edited):
   PINS checked=7 matched=7 mismatched=0   PREDICATE R90-C2 pass   rc=0
d3 (plans/round89-q66-records.json gets a trailing line; checker RECORD_BLOB constant rewritten to its new blob; ledger NOT edited):
   RECORD-TABLE blob=474967c9b43addc8 matched   PINS checked=7 matched=7 mismatched=0   PREDICATE R90-C2 pass   rc=0
control: d2's bytes judged by the honest B checker:
   PIN-MISMATCH bytes plans/round90_c1_replay.py got=3b4d59b216e5aeb7 want=611226af23d5831c
   PINS checked=7 matched=6 mismatched=1   PREDICATE R90-C2 fail   rc=1
D4 (base plans/ bytes + B ledger, i.e. a rev whose plans bytes differ from B):
   PIN-MISMATCH absent plans/round90_c1_replay.py / round90_polydiff_probe.py / round90_burndown.py
   PINS checked=7 matched=4 mismatched=3   PREDICATE R90-C2 fail   rc=1
base rev (no ledger):   DEFECT SETUP unreadable plans/counter-pins-r90.json   PREDICATE R90-C2 could-not-evaluate   rc=2
```

So the "could-not-evaluate, not pass" requirement holds at BASE (rc2) and the B-ledger-on-base-bytes case fails closed (rc1). The
forgery cases d1–d3 pass.

- **F-8 (MAJOR, C2, UNDISCLOSED).** The checker is the unpinned root of trust. `plans/round90_counter_pin.py` is neither in the
  ledger nor in the checker's own `EXPECTED_PINS` (`round90_counter_pin.py:40-47`), so a commit that edits only the checker can make
  any pinned drift pass: d2 changes `plans/round90_c1_replay.py` (pinned sha `611226af…` → `3b4d59b2…`) and passes `rc=0` with the
  ledger untouched. The claim's disclosure names only "one commit that also rewrites the pin ledger" (`round-90-claims.md` R90-C2
  Kill rule; `round90_counter_pin.py:18-20`); the checker-rewrite route is not named, and is the cheaper route. Also not pinned by
  C2: `plans/routed_open.py` (the kill rule names it; no check enforces the kill rule — diff of base→B shows it untouched, but
  nothing measures it).
- **F-9 (MAJOR, C2, UNDISCLOSED / misdescribed).** The record-table pin is read from a hard-coded checker constant
  (`RECORD_BLOB`, line 38), not from the ledger's `record_table` entry. The ledger entry (`blob`, `anchor_commit`) is decorative:
  d1 changes only the ledger's blob to `0*40` → `pass rc=0`; d3 changes the table and the checker constant → `pass rc=0`. The
  checker's `RECORD_ANCHOR` (line 39) is never used (`grep -n RECORD_ANCHOR` returns only the definition): the anchor commit is
  never verified. The claim text says "the record table's git blob at the measured revision equals the pinned blob" and presents the
  ledger as holding it.
- **F-10 (MODERATE, C2 predicate).** The frozen predicate is a conjunction including "the selftest battery exits 0 with every declared
  red case red". The checker's `run()` (`round90_counter_pin.py:259-272`) prints `PREDICATE R90-C2 pass` from the pin check alone; the
  selftest is only run when `--selftest` is passed, and then it prints no PREDICATE line. The battery shows `PREDICATE R90-C2 pass rc=0`
  for the B tree with no selftest in that invocation. The verdict line over-claims relative to its own predicate.
- **F-11 (MINOR, frozen text, C2).** The predicted before-line says "the four pre-existing counters … are printed `PIN-OK`". The pin ledger lists three pre-existing counters (`round88_claim_figures.py`, `round89_c1_replay.py`, `round89_claim_figures.py`) plus three created this round; the record table is the fourth "pre-existing" item, not a counter. The checker never prints `PIN-OK` (`grep -n 'PIN-OK' plans/round90_counter_pin.py` → no output). The pre-existing shas match at BASE (`sha256` of `git show dcdd494e:<path>` equals the pin for all three; checked for round88, round89 replay and round89 figures). Also the predicted BASE result "exits 1 printing `PIN-MISMATCH absent`" measured rc2 `SETUP` (the brief already records this mispredict). Recorded, not repaired.
- Selftest scope (observation): T1–T5 run on synthetic fixtures with stub pinned files; none exercise the ledger record_table entry,
  the checker's own bytes, or the anchor. That is why F-8/F-9 pass the 5/5 selftest.

Scope of the disclosed residual that *is* sound: a counter-only byte drift with the checker and ledger unchanged is caught
(d2 control, rc1, `PIN-MISMATCH bytes plans/round90_c1_replay.py`), and an absent pinned path fails closed (D4 rc1).

---

## 6. C3 gate (attack) — pending counts, kill rule, checks

Pending count from git bytes at BASE (`git show dcdd494e:corpus/routed-findings.jsonl`, 133 lines, all parse):

```
status Counter({'closed': 98, 'open': 32, 'refused': 2, 'blocked': 1})
pending valid 33   (all opened 39..82; by round: 42:20, 45:4, 51:4, 39:3, 40:1, 82:1)
oldest 39
rounds 83-89 rows 0
pending list includes R82-F1 (the malformed-source row, valid JSON, status open)
```

- **F-12 (MINOR, frozen text, C3).** "resolution rows for all 27 pending rows opened ≤ 82 and for the malformed R82-F1 row"
  and "27 findings opened rounds 39–82 still sit open or blocked": measured 33 pending rows (32 valid plus R82-F1), all opened
  39–82. The "28 resolutions" after-prediction (`resolutions>=28`) is a satisfiable lower bound but the actual minimum is 33.
  The BASE gate's `pending=33` matches the measured count, so the gate is right and the prose is wrong. Recorded, not repaired.
- **F-13 (MAJOR, C3, kill rule not enforced).** The claim's kill rule: "any pending row left unresolved without a named standing
  blocker" is a kill. The gate passes such a row. Reproduction (`evidence/c3-killrule2.txt`, fixture ledger with one open row
  `opened_round=89`, no blocker, via `--file`):
  ```
  ROWS total=1 valid=1 invalid=0 superseded=0
  freeze=admitted oldest_pending_round=89 pending=1 malformed_unresolved=0 seeds_83_89=1 resolutions=0 checks_run=0
  PREDICATE R90-C3 pass
  rc=0
  ```
  The gate's own selftest blesses it (`fresh-open-admits`, rc 0 want 0). The gate's pass condition (`passed = verdict != refused and not
  defects and malformed==0`, `round90_burndown.py:330-333`) does not consult the pending set beyond the freeze rule. A tip with
  pending rows opened 83–89 and no blocker would print `PREDICATE R90-C3 pass`, and the after-prediction "pending=0" would not be
  checked by the gate. The claim's frozen predicate (no pending before 88) and kill rule (no unblocked pending) disagree; the gate implements
  only the former.
  (A blocked row with no blocker is correctly caught: `evidence/c3-killrule.txt`, `DEFECT … a blocked row must name its blocker`, rc 1.)
- **F-14 (MAJOR, C3 operability).** Location-dependent gate verdict — see F-1. The R82-V8 check passes only if the lane's parent directory
  is the fleet git repo holding commit `c839b658…` (`git cat-file -t c839b658…` → `commit` in the fleet repo). A tip measured in any other
  directory prints an extra `check-failed` and `freeze=…`/`PREDICATE` fail. The claim's after-prediction (`freeze=admitted`, `resolutions>=28`)
  is therefore a statement about the lane's location, not the revision.
- **F-15 (MODERATE, C3, measurement surface).** The gate reads the ledger from the measured revision but runs each closed row's `check`
  with `cwd=lane.root` (the working tree; `run_check`, lines 196-205, and the docstring lines 19-21 say so). The claims say "measured at revs,
  never trust prints", and the kill rule concerns "a row's check exits 0". A `check` can pass on uncommitted working-tree state while the
  ledger row at the measured rev is what is being admitted. The docstring discloses this; the claim does not.
- **F-16 (MINOR, C3, check coupling).** The R42-R2 close fails at BASE for a reason other than its own work: `routed_open.py --list` prints
  no `ROW` lines (it exits 1 before listing) whenever any row is invalid. `evidence/rop-base.txt`: `DEFECT line=125 source must read <path>:<line>`
  and `ROWS total=133 invalid=1`, and no ROW lines. The R42-R2 check requires `^ROW R42-R2\.[12] status=closed` (rows R42-R2.1 and R42-R2.2 are
  `closed` in the ledger). So this historical failure clears when R82-F1 is validly resolved, not by repairing R42-R2. Worth stating in the
  triage.
- **F-17 (MINOR, C3, flag surface).** `round90_burndown.py:398-413` `--file` is documented as selftest-only (docstring line 29) but is accepted
  from the CLI; it evaluates a working-tree ledger with working-tree sources and never reads the measured revision. A freeze could be admitted
  through it. Code-read; not exercised against a tip.

---

## 7. Claim-by-claim

- **R90-C1 (coverage) — ADMIT the mechanism and frozen vectors; NOT yet measurable at tip.** Grader bytes, case table, vectors, ledger
  base numbers and after-arithmetic all verified from git bytes; probe re-run reproduces all eight frozen vectors (F-4/F-5/F-2/F-3 are
  frozen-text errors to be recorded). The tip claim is unmeasured (no receipt at B). Kill-rule sensitivity (F-7) noted.
- **R90-C2 (calibration) — NOT ADMIT as written.** The pinned-counter drift detection is real (d2 control, D4), and BASE fails closed
  (rc2). But: the checker is unpinned and forgeable by a checker-only edit (F-8), the record-table pin is a checker constant with an
  unused anchor and a decorative ledger entry (F-9), and the PREDICATE pass line omits the selftest conjunct (F-10). An honest
  narrowed claim would be: "counters pinned by bytes in a ledger the checker reads; the checker and record-table constant are unpinned".
- **R90-C3 (operability + capability) — NOT ADMIT as written.** The BASE refusal is correct and reproducible at the real lane path (F-1
  resolved by location). But the gate passes an unblocked pending row (F-13), its freeze verdict depends on the lane's directory (F-14),
  its checks run on the working tree not the measured revision (F-15), and the frozen pending count is mis-stated (F-12).

---

## 8. Findings index (severity)

| id | sev | claim | one-line |
|---|---|---|---|
| F-1 | MINOR | C3 | transcript-vs-clone deviation; R82-V8 location dependence |
| F-2 | MINOR | C1 text | "thinnest cell" false by all three measures |
| F-3 | MINOR | C1 text | "first executed member" contradicted by git-leak-recovery |
| F-4 | MINOR | C1 text | "PPPPPP" typo (five-char vector) |
| F-5 | MINOR | C1 text | predicted TARGET `legs=8` vs counter `legs=40` |
| F-6 | MINOR | C1 text | same root as F-5 |
| F-7 | OBS | C1 | sandbox outage classified as claim failure (L6), not could-not-evaluate |
| F-8 | MAJOR | C2 | checker unpinned: checker-only edit passes drifted counter (d2); undisclosed |
| F-9 | MAJOR | C2 | record-table pin = checker constant; ledger entry decorative; anchor unused (d1, d3); undisclosed |
| F-10 | MODERATE | C2 | PREDICATE pass without the selftest conjunct |
| F-11 | MINOR | C2 text | `PIN-OK` never printed; BASE predicted rc1, measured rc2 |
| F-12 | MINOR | C3 text | 33 pending (not 27); 33 resolutions minimum (not 28) |
| F-13 | MAJOR | C3 | kill rule not enforced: unblocked open pending row → `PREDICATE pass` rc0 |
| F-14 | MAJOR | C3 | freeze verdict depends on lane directory (R82-V8 via fleet parent) |
| F-15 | MODERATE | C3 | checks run on working tree, not measured revision |
| F-16 | MINOR | C3 | R42-R2 fails via routed_open invalid-row coupling, clears with R82-F1 |
| F-17 | MINOR | C3 | `--file` is a CLI path that bypasses the measured revision |

Triage-draft sample check (item 4): skipped, `ExecC3Triage/` absent at check time (no drafts to verify).

Final per claim: C1 ADMIT (mechanism + vectors; tip unmeasured) · C2 NOT-ADMIT as written · C3 NOT-ADMIT as written.
