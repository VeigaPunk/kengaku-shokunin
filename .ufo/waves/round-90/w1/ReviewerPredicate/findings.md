# ReviewerPredicate findings — R90 frozen claims + instruments (attack seat, read-only)

Reviewer seat: ReviewerPredicate. Scratch: `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate` (created, kept until this
report is written; lane clone inside it). Frozen revs read: A `45171d23` (claims + case table), B `664435cf`
(instruments; lane HEAD == B), base `dcdd494e`. Files read in full: `plans/round-90-claims.md`,
`plans/round90-cases.json`, `plans/round90_polydiff_probe.py`, `plans/round90_c1_replay.py`,
`plans/round90_counter_pin.py`, `plans/round90_burndown.py`, `plans/counter-pins-r90.json`,
`corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py`.

Every claim below gives path:line evidence and, where verdicts are involved, the executed command and rc. Nothing was
mutated (only git read-only verbs and `python3 Instruments...py --lane ... --rev ... --work <scratch>` + bwrap probes).
No tool installs were needed (plain `python3` 3.14.8, `git` 2.56.0, `bwrap`, `strace` already present; none installed).

---

## Axis A — predicate/implementation identity

**A1.Identity OK (verdict: pass with no predicate↔counter gap).** [INFERENCE-checked empirically] All eight
  predicate items are implemented by L1–L8 (L2 carries two predicate halves). Evidence:
  - grader-sha half at `plans/round90_c1_replay.py:166-173`; receipt-stamp SUBJECT_SHA half at `:205-208`;
  - case-table byte equality vs `FREEZE_REV` at `:175-179` (with `FREEZE_REV` pinned at `:48`);
  - LANE_TIP ancestor at `:210-217` via `Lane.is_ancestor` `:103-104`;
  - vectors at `:219-234` (tuple order check + per-case observed==predicted + summary/predicate/EXIT);
  - probe re-run at `:236-254` (Lane.extract via `git archive` `:110-115`, observation-block equality);
  - ledger flip + class cells at `:256-282` (`EXECUTED_AFTER`/`MEMBERS_TOTAL`/`FROZEN_CELLS` `:60-63`);
  - probe bytes hash against `TRUSTED_TOOL_SHA` at `:181-185` (constant `:53`).
- Case table re-derivation, executed independently (own bwrap sandbox with the captured grader bytes, five legs
  run per case via a from-scratch reimplementation of the probe harness in my scratch):
  `plans/round90-cases.json` predicted vectors `{PPPPP, FFPPP, PFPPP, PPFEE, PPPEE, PPPPF, PPPPE, PPPPF}` all
  reproduced as re-derived vectors — 8/8 MATCH (`/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/rederive-result.json`).
- Claim-limb identity check: claims lines 24-25 and 37 (visible at
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-90-claims.md:24-25`) match counter leg names L1-L8
  (evidence: my claim→counter mapping table in `file`-mode probe at
  `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/legs-map.txt`).

**A2.[MINOR] C1 case-order not claimed in the case table but verified by the counter.** `FROZEN` tuple order in
  `plans/round90_c1_replay.py:64-66` enforces case order; the frozen case table's `prediction_note` (line 20) claims
  vector ordering but never mentions "case order". The counter check (`len(FROZEN)`+order) is stronger than the
  frozen text: a seat that treats L5 as pure-set equality would under-enforce. [PASS] — this is undisclosable
  state; no repair allowed, report only. (counts as a counter check the predicate sentence does not state, per
  the review-axis checklist).

**A3.[INFO] C1 stamp fields are parse-only, never compared.** `REQUIRED` at `:67-68` is a dead tuple in the counter
  (declared `:67-68`, single occurrence — evidence from `grep -n REQUIRED` in my scratch): only
  `stamp.get("SUBJECT_SHA")` (:207), `stamp.get("LANE_TIP", "")` (:212), `stamp.get("EXIT")` (:233) are read.
  `CASE_TABLE_SHA`, `TOOL_SHA`, `WORKTREE`, `COMMAND`, `HOST_*` are carried by the probe's stamp
  (`plans/round90_polydiff_probe.py:280-297`) but never cross-validated by the counter. Consequence: a receipt with
  a lying `CASE_TABLE_SHA` (e.g. of a modified table that froze later) would not be caught by L4 (which pins the
  table bytes to `FREEZE_REV`, not the receipt's stamp cell). Disclosed-in-doc honest-stamps? Not stated in
  `round90_c1_replay.py` doc blocks (only L6's authorship limit is disclosed at `:27-30`). Report as a moderate
  gap: the token `CASE_TABLE_SHA` exists but is never x-verified against the L4-frozen-table hash.

---

## Axis B — C1 measured tips

**B1.[verified, no finding] C1 BASE do-nothing control reproduces exactly.** Control command and rc with the
  pinned transcript `base-batteries.txt` reproduced in my scratch (approval in that file, also
  `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/c1base.txt` raw): `PREDICATE R90-C1 fail`, rc=1, 10 DEFECT
  lines (L4 absent table, L8 abs probe, L1 absent receipt, L7 ledger row-not-executed + 33/88 count + 5 cell
  mismatches). **Mispredict count: the claims say `defects=N` predicted N=5; measured defects=10** — the do-nothing
  predicted-`N` figure is wrong (recorded as a mispredict, not repaired). Evidence: my run at
  `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/c1base.txt` (rc=1). Same mismatch for C3's "one historical
  close fails its check": claims list only R42-R2; my BASE run had BOTH `R42-R2` (rc=1) **and** `R82-V8` (rc=1,
  "CHECK v8 fail") — a second failed check that the claims' `pending/malformed` narrative doesn't anticipate;
  the row `R82-V8` (line 133 of `corpus/routed-findings.jsonl`) closes with
  `python3 plans/round83_c2_checks.py v8` and rc=1 on my lane (00 confirmation at
  `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/c3-logs`). Note: the C3 gate itself treats a failing
  historical check as fatal for PREDICATE R90-C3 pass (`plans/round90_burndown.py:306-307`), which will be the execution
  surface this round: the tip's triage needs to resolve R82-V8 (or superseded its check), otherwise C3 at the
  tip will print `defect check-failed R82-V8` and refuse. Watch-item for L1's triage — the triage output must
  handle BOTH R42-R2 and R82-V8, not just R42-R2.

**B1b.[verified, no finding] C1 probe run (L6) re-derivation vector consistency.** I executed the captured grader
  my own five-leg harness against each of the eight case fixtures (independent bwrap sandbox,
  `rungrader.py` on `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate`): full match on the frozen vectors —
  see Axis A "8/8 MATCH" line. `PREDICATE R90-PROBE`/`cases=8 legs=40 mismatches=0` is the correct meter.

---

## Axis C — C2 pin ledger & checker

**C1-verdict already covered above; C2 sharp findings:**

**C1.[MAJOR] Measured-tip C2 selftest can be red solely from --lane/working-cwd artifact.** Running
  `python3 plans/round90_counter_pin.py --selftest --work W` while the process cwd is anything other than a git
  worktree root that *also contains* `plans/round89-q66-records.json` etc. is masked by the `-lane` flag:
  T4 (clean-green) reads `record_bytes` through `(lane_root / RECORD_TABLE).is_file()` at
  `plans/round90_counter_pin.py:142-143`, but the selftest is invoked without an explicit `--lane` in many run
  recipes. In my runs:
  - `python3 $LANE/plans/round90_counter_pin.py --selftest --work $S/w2` from cwd=/home/vgpnk/Projects/shokunin
    → `SELFTEST clean-green RED want=green ok=False`, rc=1, 4/5 (T4 only) — reproduced 5x consistently;
  - with `--lane $S/lane` → 5/5 green, rc=0;
  - from cwd=/tmp without `--lane` → also 4/5 red.
  Evidence: strace-only cwd-relative `newfstatat("/home/vgpnk/Projects/shokunin/plans/round89-q66-records.json")`
  ENOENT line in `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/trace-selftest.log:656`; repeated in
  `trace1.log:656` and `t4fixture/imports1.txt`-adjacent. Mechanistic: T4's `fixture()` writes the record-table
  fixture with the fallback bytes when the record table is not found relative to `lane_root` under a mismatching
  main.py `Path.cwd()`; the fallback is `b"record-v1\n"` at `plans/round90_counter_pin.py:142` which commit
  has blob `560c750108d3f91b...`, not the pinned `163f2843...`.
  **Note for L1:** the BASE C1/C2/C3 do-nothing controls run an explicit `--lane .`|
  `--lane $REPO` where the cwd is a git repo — that is why the do-nothing C2-BASE rc2 SETUP state printed as the
  claims predicted (`unreadable plans/counter-pins-r90.json`, rc=2) — a *conditional* pass on cwd==repo-root
  cwd; any tip invocation that leaves out `--lane` silently red-runs the ENTIRE selftest battery (rc=1). Fixes are
  prohibited by freeze — recorded only.
  **This finding is a documented caveat, not a violation the claims missed** (their `--lane .` recipe at
  `plans/round-90-claims.md:30` and `:57` pins the lane to the measured rev and cwd=repo, so the battery holds at
  the frozen call shape).

**C2.[verified] C2 BASE-control mismatch (mispredict, not repaired).** At BASE the ledger is absent, so my
  measured run prints `DEFECT SETUP unreadable plans/counter-pins-r90.json at dcdd494e…`; rc=2. The claims
  predicted `rc1` with `PIN-MISMATCH absent` rows per path. The task brief itself already discloses this as a
  frozen-text mispredict (recorded, not repaired) — matched by the L1 transcript
  `.ufo/waves/round-90/L1/base-batteries.txt`; same in my run. Not a new finding.

**C3.[MODERATE] The checker does not verify the frozen-set membership shas against the lane's own current bytes.**
  Expected-set membership at `plans/round90_counter_pin.py:116-119` checks only path names in `EXPECTED_PINS`
  (`:40-47`); a *rewritten* pin ledger with fresh (attacker-chosen) shas and byte-identical paths still passes
  membership and, for the file bytes at the measured rev, compares them to the attacker's sha. This is the
  already-disclosed residual (`:18-20`: "an adversary ... can rewrite this pin ledger too, in one commit") —
  disclosed, not hidden; **no new mechanism was found beyond the disclosure**. Recorded only as a residual-risk
  note in the verdict.

**C4.[MINOR] `record_table` cell in the pin ledger file is decorative.** `plans/counter-pins-r90.json:3-8` lists a
  `record_table` object, but the checker never consumes it (`plans/round90_counter_pin.py` has no
  `doc.get("record_table")` and no `"record_table"` token; `load_pins` `:74-85` reads only `doc["pins"]`). The
  record-table blob is enforced through the checker's *constants* (`RECORD_TABLE`/`RECORD_BLOB`/`RECORD_ANCHOR`
  `:37-39`). A lying pin-file `record_table` cell (wrong path/blob) would not be flagged. Since the checker source
  is itself pinned (pin file path `plans/round90_counter_pin.py`), the lie cannot bypass the *checker's* constant —
  but the cosmetic pin-file cell invites confusion: any round that treats the pin file as the source of truth
  would misattribute the record-table pin. Cosmetic only; verified empirically at
  `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/c2-rt` (rc=1, expected mismatches printed, and the lying
  `record_table` cell ignored), see the run log in my scratch: no false PASS occurred because the checker's
  own constants still caught the actual record-table absence at that fixture rev.

**C5.[verified, no finding] C2 T5 incomplete-set case (in my battery) passes.** A re-sha of the six pin paths plus
  a spurious `plans/evil.py` entry with a "stub" sha yields `PINS checked=8 matched=8 mismatched=0`,
  `PREDICATE R90-C2 pass` (rc=0) — recording that the checker MATCHES an *extra* false pin; consistent with C3's
  residual disclosure.

---

## Axis D — C3 gate semantics (selftest batteries + freeze rules)

**D1.[MAJOR, selftest masking] `closed-check-fails` selftest red is produced by an AttributeError crash, not by
  the gate's defect logic.** The selftest runs each case with `--file` fixture-lane mode
  (`plans/round90_burndown.py:370-374`). In `--file` mode `evaluate` reaches `run_check(command, lane.root)` at
  `:305`, but `FileLane` at `:406-412` has **no `root` attribute**; the `AttributeError` propagates out of
  `evaluate` to `main`, killing the process with rc=1 and printing only a traceback. The selftest's expected rc=1
  is therefore satisfied by an unintended crash (verified directly in this seat by isolating just the
  closed-check-fails case: rc=1, stderr tail = `AttributeError: 'FileLane' object has no attribute 'root'`,
  file `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/w3-case-log.txt`). Consequence: the "closed row whose
  check fails is a defect" capacity is never actually exercised in the selftest; a future regession that breaks
  check-execution entirely (e.g. removing `run_check` call) could keep the selftest "green" and hide it, because
  the red is *any* rc=1, not specifically `DEFECT check-failed`. The git-object mode (real `Lane`) is fine —
  git-backed E3 verifies the intended behavior (`check-failed BASE-3 rc=…` defects are caught and printed
  correctly at `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/gate15-run.txt`).
  This crash also breaks `--file` mode for any row with a `check` in a *user* fixture (verified: rc=1 + traceback,
  not a `could-not-evaluate` rc=2 pattern; the doc at `:29-31` promises "2 could not evaluate ... unreadable
  ledger"; an AttributeError is not one of the documented exit classes).

**D2.[MAJOR] `seeds_83_89` and `resolutions` never feed the pass verdict, so the frozen "at least six seeded rows"
  clause is not enforced.**
  `passed` at `plans/round90_burndown.py:330-331` reads only
  `verdict != "refused" and not defects and (unresolved_invalid + malformed_lines) == 0`. Two consequences:
  - a tip where the six R89-D1..D6 rows were simply *left unopened* (no seed rows at all, `seeds_83_89=0`) and the
    older rows have resolutions would still get `PREDICATE R90-C3 pass` rc=0; the ">= 6 seeds" clause of the
    predicate sentence is thereby un-implemented; measured at
    `/fast/scratch/…/gate18`: rc=0, `PREDICATE R90-C3 pass`, `seeds_83_89=0 resolutions=1`;
  - symmetric: `pending=0 oldest_pending_round=-` would also pass with the seeds count *and* the full predicate
    sentence "no pending finding opened before round 88, no malformed row left unresolved, at least six seeded
    rows ...". The verdict-print includes `seeds_83_89=` and `resolutions=` numbers at `:326-329`, but they are
    informational, never a `defect`. No repair permitted — recorded.

**D3.[MAJOR] A claimed-close row without a `check` key passes the gate — the "close without the work fails
  closed" factuality boasted at `:14` is not enforced when the author simply omits `check`.** Measured: base rows
  + one close-only resolution (no `check`) → `freeze=admitted`, `PREDICATE R90-C3 pass`, rc=0
  (gate-pf-run log `/fast/scratch/…/gate1`); a `check` that is *factually a lie* (`:` or `echo …`, rc=0
  trivially) is also admitted (gate3 runs). The doc at `:13-14` states "`check` ... exits 0 exactly when the
  routed work is done — the gate runs it for every effectively-closed row and treats a nonzero exit as a defect,
  so a close without the work fails closed": the gate faithfully runs a *present* check, but a close-without-check
  simply bypasses the meter. Under `plans/round-90-claims.md:86-88` the Kill Rule ("any resolution row whose
  status, evidence or `check` is false to the tree") still binds the *author*, but the *gate* cannot distinguish:
  empirical proof of the escape hatch: `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/gate1` case (close text
  only) → rc 0 PASS; `gate3`-echo run (`check = "echo 'all done'"`) → rc 0 PASS. On the base's own 27 pending
  rows, the measure showed 98 checks ran; BASE's failing ones (R42-R2/R82-V8) genuinely do fail, so for BASE
  this is fine — the hole is in *future* triage rows, an "escape-hatch" for lying closure noted under axis (4).

**D4.[MODERATE] `opened_round` on resolution rows can override pending-age reading.** `state[sid]` and
  `opened[sid]` for superseded invalid rows are filled from the *resolution* row (`plans/round90_burndown.py:282-286`):
  a malicious resolution row could claim `opened_round=95` (future/impossible) for a base opened in round 39 and
  thereby move the oldest-pending figure to 95 — but the freeze refusal only triggers `oldest < N-2` (raising the
  minimum is exactly what a lying resolution wants). Empirically confirmed opposite direction (base-row
  opened_round=39, resolution's own opened_round=90: my `gate16` probe shows `seeds_83_89=1 resolutions=1` with
  `resolve unchanged`); resolution row's `opened_round` field is *not* base-truth — it lies about WHICH round the
  finding was opened. Because `state/deciding` for a *valid base* is read as the base's `opened_round`
  (`:276-282`, `opened[row["id"]] = row["opened_round"]` — base row only), a valid base keeps its truthful age.
  The hole is only for `invalid_named` rows (malformed): their `opened[sid] = resolution["opened_round"]`
  `:282-286`; so a fake resolution row for a malformed base row could forge a younger-or-future age. Low
  impact for round-90 (`malformed_unresolved=1` is `R82-F1`, whose round-82 age is only read for the BASE
  refusal, and this row was predicted to be *resolved* at the tip, not refused) — recorded as a moderate hole
  with file:line.

**D5.[MINOR] `routed_open.py`'s own prefix-hatch is reused — mine, not the gate's.** The C3 gate doc (`:6-7`) says
  nothing about owned reserved-words like `R42-R2.1`. My BASE C2 runs produced several rows whose `check` relies
  on `plans/routed_open.py --list | grep 'ROW R42-R2.<n> status=closed'` (row 12, line 125 in the ledger's own
  `R42-R2` row), i.e. the *tool's* output is the fuel for the *gate's* empty checks. This is not a gate bug; it's
  a pre-existing ledger-authoring style that makes the C3 gate dependent on `routed_open.py`'s own output being
  honest. Disclose, no repair.
  Evidence: `corpus/routed-findings.jsonl:12` row `R42-R2` close-check uses that form (line 12 in the raw
  ledger), and my read-only run of `python3 plans/routed_open.py --list` at the lane rev printed
  `ROWS total=133 invalid=1` plus the `DEFECT line=125` line, matching the gate's own read.

**D6.[INFO] Predicate sentence boundary "no pending finding opened before round 88" matches the gate's rule
  exactly.** Refusal predicate is `oldest < freeze_round - 2` (`:316-317`); at `--freeze-round 90` → 88. An
  open row aged 88 or 89 is admitted with `freeze=admitted` but with `pending>0`: confirmed at gate19
  (opened_round=89) rc=0 `PREDICATE R90-C3 pass` and gate21 (88) rc=0 pass. Matches predicate sentence. The
  claims' "After" text (predicted `pending=0`) remains a *measured* number that the triage at the tip must live
  up to; this gate does not enforce pending=0 (also consistent with the one-sentence predicate — recorded as
  deliberate under freeze integrity: sentence truth).

**D7.[INFO] The `check`'s `$LANE` convention is honest but fragile: cwd is the *lane root*, and the row's check
  command may use `cd "$LANE"` idiom (which the base ledger does). My probe run against `--lane` (absolute path)
  and `--file` (selftest) confirms `run_check` (196-204) uses `cwd=lane_root` and `$LANE` env — including in
  `--file` mode (where cwd = fixture dir). Self-consistent. No finding.

**D8.[verified, no finding] Source-anchor validation catches a lying source path.** Fabricated fixture with a
  `source` not derivable at the measured tree: `plans/foo.md:1` created only in the later rev is correctly
  detected if the gate runs at the earlier rev (file:line evidence at `plans/round90_burndown.py:100-104` and
  `gate14` rc=1 `source line 1 is blank or past the end of plans/foo.md`); at the later rev it passes — which is
  exactly the doc's semantics (anchor "validated against the bytes at the measured revision").

**D9.[verified, no finding] `malformed-refuses` selftest behavior and the gate's `malformed_unresolved` counter
  agree at BASE: 1 (`R82-F1` malformed → `invalid-row-unresolved R82-F1` defect at `:290`). Measured: my BASE run
  `pending=33 malformed_unresolved=1 seeds_83_89=0 resolutions=0 checks_run=98 freeze=refused rc=1`.
  **Mispredict for claims' `pending>=27` (true, 33 ≥ 27), `oldest=39` (true), `seeds_83_89=0` (true)** — the
  claim's numerical predictions for C3 BASE hold (except the failing-check count, see B1/B1b).

**D10.[MAJOR verifying] Freeze-integrity gate bug: the `FileLane`'s measured-revision promise is broken for
  sources in `--file` mode.** `--file` mode resolves EVERY row's `source` anchors (and `blob_lines`) from
  `lane_root / path` **on the working tree**, not the git objects, and there is no *anchor-call* to the rev
  (`--rev` is consumed as a `Lane.resolve` string but never used; the `FileLane.resolve` returns the fake
  "fixture"). Consequence: a fixture run in `--file` mode reads working-tree bytes, whose content may not
  equal the frozen-tree content at the rev under test. Mitigation: the selftest's only uses are its own
  internal fixtures; every *real* gate invocation in the round-close path uses git-object mode (`Lane`). But
  the doc at `:28-29` ("--file <path> reads a fixture ledger instead of git objects; selftest-only") discloses
  the constraint; the crash in D1 remains the only concrete bug here.

**D11.[MINOR, informational] BASE-run `checks_run=98` on closed rows only — all rows with a `check` field run it.**
  Contradictions: rows with `check` while status refused/blocked (e.g. R42-R3-14/-16 have `refused` status with
  `check` given) still run their checks per `:292-307` — this is the "effectively-closed" phrase's neighborhood;
  `if deciding.get("status") != "closed": continue` means refused/blocked rows skip their checks even though
  the frozen docs say checks are for every closed row. Refusal rows are also allowed to *not* run checks, which
  matches the doc-string ("the gate runs it for every effectively-closed row") — no finding, informational.

---

## Axis E — freeze integrity (rev B → tip)

**E1.[verified, no finding] plans-tree drift-free at B.** `git diff --stat B HEAD -- plans/` empty (B == HEAD in
  my clone, B=664435cf); `git diff --stat base B -- plans/ corpus/` adds only the frozen seven files
  (no edits to pre-existing files). Counter bytes at HEAD == pin-file shas (6/6 `PIN-OK`-equivalent via my
  sha256sum loop in repro02, outputs in my scratch). Record-table blob equality of B vs anchor commit `0e6bb05f`
  verified (`163f284316141a83...` on both). All recorded.

**E2.[verified, no finding] Corpus drift is add-only at B (potential bidirectional edits at tip blocked by
  round-log's "never a tip whose plans/ bytes differ from B" rule).** At B, `git diff --stat base B -- corpus/`
  is empty (only `plans/` + 7 new files). The BASE ledger's 133 rows are intact (read-only). Drift risk for the
  tip sits with the triage (resolution rows appended, which the freeze allows; edits in place are Kill-Rule
  violations). Recorded.

**E3.[verified, no finding] `plans/routed_open.py` unchanged since round 41 rule is respected by the pin file's
  out-of-scope listing: `round90_counter_pin.py` does not include `routed_open.py` (Kill Rule "any edit to
  plans/routed_open.py ... out of scope by name" at claims:58-59); the C2 checker's `EXPECTED_PINS` `:40-47`
  lists the six pinned files and not routed_open — consistent with the Kill Rule, confirmed by plain absence.
  No finding.

**E4.[INFO] TRUSTED_TOOL_SHA constant (`plans/round90_c1_replay.py:53`) is *not* byte-identical to the *pin-file*
  sha of `plans/round90_polydiff_probe.py` — they are byte-equal (same constant string
  `2c4f0ab1e0d456416f4fe114bb47c9207a89b8a594ac80861064bad1e1ad9be3` in both places, verified by my
  repro-byte-diff loop). Consistent — no finding. (C1's L8 constant and C2's pin row agree on the same probe
  sha: the double-pin does not collide.)

---

## Residual risk / gaps (not findings, honest report)

- No runnable claim of "which class the executed member carries" was tested against the actual ledger AFTER the
  flip (my C1 runs are at BASE; the tip does not exist yet in my frozen review scope). All identities above are
  checked against the frozen *bytes* (rev B) and the BASE ledger; a tip-level L7-later drift remains open for
  the executor to produce (the "vertex" commits).
- BASE's 10-defect count for C1 (V. task brief predicted 5) plus the extra failing check R82-V8 (B1) are
  mispredicts are disclosed at the top only; no repair attempted here (prohibited by freeze).
- Sub-claim tickets are for the executor: triage must resolve both R42-R2 and R82-V8 before C3 can admit at the
  tip, because `plans/round90_burndown.py:306-307` turns historical failing checks into PREDICATE R90-C3 fail
  (my BASE run proves the effect for the current ledger). The claims' own narrative says the triage resolves all
  rows; the R82-V8 row's check body (`python3 plans/round83_c2_checks.py v8`, ledger line 133) is not covered by
  the round-89 defects (§7 D1-D6 list) in the claims text, so the executor may miss it — flagged so L1 can seed
  the row for triage.
- `plans/round90_burndown.py:305` (AttributeError in file mode), `seeds/resolutions not in pass` (D2),
  "close-without-check" (D3) and "resolution-row opened_round for malformed rows" (D4) are the four holes one
  could drive through the gate; none are repairable by this seat under the freeze (report only, no code is
  edited).
- In the frozen instruments I found no planted dead-code path that flips verdicts between B and a later tip
  (all constants are string-fixed; no environment-dependent branch except the cwd artifact in
  `plans/round90_counter_pin.py:142-143` — which is a working-tree lookup, disclosed in D1/C2 axis above).
