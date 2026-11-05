# SentinelForge — round-90 adversarial forgeries through the production path

Seat: SentinelForge (leaf, sentinel). Base lane rev B `664435cf` (pin commit). Clone: `$S/lane`
(`S=/fast/scratch/hyaku/kengaku-r90/SentinelForge`), detached at B; every forged commit is a fixture
commit inside `$S/lane` (author `t <t@t>`). Nothing was pushed; nothing was committed in the lane.
Counter entry points used unmodified: `plans/round90_c1_replay.py`, `plans/round90_counter_pin.py`,
`plans/round90_burndown.py`, and the probe `plans/round90_polydiff_probe.py` (run as the receipt
generator). Forgeries were made by hand-edit (edit tool) or, for bulk ledger rows, by the generator
`artifacts/tools/forge_rows.py`. Raw outputs: `artifacts/outputs/`; diff of every forged commit against B:
`artifacts/patches/`.

Labels: brief forgeries 1–5 map to sections 1.1–1.5 below. Findings are H-n (HIGH), M-n, L-n.
Frozen-element defects are FE-n (reported, not repaired). Predictions that did not match are P-n.

## 0. Verdict table

| # | Forgery (fixture commit) | Counter | rc | Measured | Expected | Match |
|---|---|---|---|---|---|---|
| 0 | honest receipt + ledger flip (`259ce475`) | C1 | 0 | PASS `executed_rows=34 … executed=1 cases=8 legs=40 mismatches=0 defects=0` | positive control | yes |
| 0 | same | C2 | 0 | PASS `PINS checked=7 matched=7 mismatched=0` | positive | yes |
| 1a | consistent stamp, one fabricated vector (`f84480a8`) | C1 | 1 | `DEFECT L5-vectors no-git-dir observed=PPPPP predicted=FFPPP`; `DEFECT L6-reproduce re-run observation block differs` | L6 or L5 | yes |
| 1b | fabricated stamp hashes + HOST fields, honest vectors (`40dc3a8e`) | C1 | 0 | PASS, defects=0 | (not in brief) | extra, see M-1 |
| 1c | receipt LANE_TIP → non-ancestor commit (`42678ffc`) | C1 | 1 | `DEFECT L3-tip LANE_TIP f84480a8e8d8 is not an ancestor of 42678ffc1ef3` | L3 control | yes |
| 2a | echo probe + regenerated receipt, counter pin NOT rewritten (`f7188eef`) | C1 | 1 | `DEFECT L8-tool probe sha=7ca3576d82c3d1c6 != TRUSTED_TOOL_SHA 2c4f0ab1e0d45641` only | L8 control | yes |
| 2a | same | C2 | 1 | `PIN-MISMATCH bytes plans/round90_polydiff_probe.py got=7ca3576d82c3d1c6 want=2c4f0ab1e0d45641`; `PINS checked=7 matched=6 mismatched=1` | catch | yes |
| 2b | echo probe + `TRUSTED_TOOL_SHA` rewrite + receipt + ledger, ONE commit (`e7e3a892`) | C1 | **0** | **PASS** `executed=1 … defects=0` | PASS (r89 H3 class) | yes → H-3 |
| 2b | same | C2 | 1 | `PIN-MISMATCH bytes plans/round90_c1_replay.py got=b31e274c3449f12a want=611226af23d5831c`; `PIN-MISMATCH bytes plans/round90_polydiff_probe.py got=7ca3576d82c3d1c6 want=2c4f0ab1e0d45641`; `PINS checked=7 matched=5 mismatched=2` | catch on both bytes | yes |
| 3 | 2b + pin-ledger rewrite to new shas, ONE commit (`35e54459`) | C1 | 0 | PASS | disclosed residual | yes → H-4 |
| 3 | same | C2 | 0 | PASS `PINS checked=7 matched=7 mismatched=0` | pass (residual) | yes → H-4 |
| 3b | 2b files + checker byte-compare disabled, pin ledger byte-identical to B (`733bd397`) | C1 | 0 | PASS | — | — |
| 3b | same | C2 | **0** | **PASS** `PINS checked=7 matched=7 mismatched=0` while probe and counter bytes do NOT match their pins | claim: pin-ledger rewrite is the only route | **NO → H-1** |
| 5a | table-only: `no-git-dir` predicted FFPPP→FFPPF (`0571c28e`) | probe | 2 | `DEFECT SETUP wrong-table predicted no-git-dir`; `PREDICATE R90-PROBE setup-defect` | rc1 mismatch at case | **NO → P-2** |
| 5a | same | C1 | 1 | `DEFECT L4-table table sha=735b5c3cc812e23a != frozen 7e198cd18756c0fd`; `DEFECT L6-reproduce probe re-run rc=2 produced no observation block` | L4 byte-identity | yes |
| 5b | table AND probe constant edited to FFPPF (`31179c7b`) | probe | 1 | `CASE no-git-dir predicted=FFPPF observed=FFPPP`; `cases=8 legs=40 mismatches=1`; `PREDICATE R90-PROBE fail` | rc1 at that case | yes (this path only) |
| 5b | same | C1 | 1 | `DEFECT L4-table …`; `DEFECT L8-tool probe sha=cfbcffb83a37300e != TRUSTED_TOOL_SHA 2c4f0ab1e0d45641`; `DEFECT L6-reproduce re-run observation block differs`; defects=3 | L4 | yes |
| 4a | two pending rows closed with fabricated evidence, base checks inherited (`cc82f567`) | C3 | 1 | `check-failed R42-R3-02-fx1 rc=1` (printed twice); R45-S5-7e-fx1 NOT flagged; `freeze=refused oldest_pending_round=39 pending=31 malformed_unresolved=1 seeds_83_89=0 resolutions=2 checks_run=102` | check-failed for both | half → P-3, M-3 |
| 4b | R42-R3-02 closed with `"check":"true"` override; R42-R3-19 closed, base check (`88846f79`) | C3 | 1 | R42-R3-02 no defect (override accepted); `check-failed R42-R3-19-fx-override-two rc=1` (base check; script absent) | — | → H-2(a) |
| 4c | two pending rows `status:"refused"`, fabricated blocker (`ec3be213`) | C3 | 1 | NO defect for either; pending 33→31; `checks_run=98` | — | → H-2(b) |
| 4d | ALL 32 pending + R82-F1 + R42-R2 + R82-V8 closed, `check:"true"` (`3971a541`) | C3 | 1 | `freeze=admitted oldest_pending_round=- pending=0 malformed_unresolved=0 seeds_83_89=0 resolutions=35 checks_run=165`; ONLY defect `DEFECT line 125: R82-F1` | freeze must be refused | **H-2** |
| 4e | same, all `refused` with fabricated blocker (`a065511c`) | C3 | 1 | `freeze=admitted oldest_pending_round=- pending=0 malformed_unresolved=0 seeds_83_89=0 resolutions=35 checks_run=96`; ONLY defect `DEFECT line 125` | — | **H-2** |
| 1c-b | C3 selftest + C2 selftest at B | — | 0/0 | `cases=7 red-green-ok=7`; `cases=5 red-green-ok=5` | able-to-fail green | yes |

Command lines (fixture clone root, `--rev HEAD`):
- `python3 plans/round90_c1_replay.py --lane . --rev HEAD --work $S/c1-work-<tag>`
- `python3 plans/round90_counter_pin.py --lane . --rev HEAD --work $S/c2-work-<tag>`
- `python3 plans/round90_burndown.py --lane . --rev HEAD --work $S/c3-work-<tag> --freeze-round 90`
- probe (receipt generator): `python3 plans/round90_polydiff_probe.py --lane . --work $S/probe-work-<tag> > receipt.txt`
- BASE control of the gate on B (`664435cf`), same command: `rc=1`, `freeze=refused … pending=33 … seeds_83_89=0`, with `check-failed R42-R2 rc=1 ''` and `check-failed R82-V8 rc=1 'CHECK v8 fail'` (see M-4).

## 1. Forgeries in detail (recipe → commands → rc → output)

### 1.1 Forgery 1 — forged receipt (stamp consistent, vectors fabricated)

Recipe 1a (`f84480a8`, branch from honest `259ce475`): in `corpus/evidence/round90/merge-diff-probe.txt`
line 17, `CASE no-git-dir predicted=FFPPP observed=FFPPP` → `… observed=PPPPP`. Stamp fields (SUBJECT_SHA,
CASE_TABLE_SHA, TOOL_SHA, LANE_TIP, EXIT 0) left real; summary `cases=8 legs=40 mismatches=0` and
`PREDICATE R90-PROBE pass` left as they were. Commit. C1:
- rc=1. `DEFECT L5-vectors no-git-dir observed=PPPPP predicted=FFPPP`; `DEFECT L6-reproduce re-run observation block differs from the receipt`; `TARGET … mismatches=1 defects=2`; `PREDICATE R90-C1 fail`.
- Catch: L5 and L6, as predicted. A fabricated vector that equals the true probe output is not a forgery of the observation; the fabricated vectors that differ from the real run are caught by both legs.

Recipe 1b (`40dc3a8e`): stamp `CASE_TABLE_SHA` → `000…0`, `TOOL_SHA` → `111…1`, `HOST_PYTHON` → `Python 2.7.18`; vectors honest. Commit. C1 rc=0 `executed=1 … defects=0`, `PREDICATE R90-C1 pass`. C2 rc=0. The counter never reads `TOOL_SHA`, `CASE_TABLE_SHA`, `HOST_*`, `WORKTREE` or `COMMAND`; see M-1.

Recipe 1c (`42678ffc`): `LANE_TIP` → `f84480a8e8d89c20e3ea22a5725eddaf007371e9` (a real commit that is not an ancestor of the honest tip). C1 rc=1, `DEFECT L3-tip LANE_TIP f84480a8e8d8 is not an ancestor of 42678ffc1ef3`, `defects=1`.

### 1.2 Forgery 2 — forged probe + counter pin rewrite (r89 H3 class)

2a control (`f7188eef`, from B): the probe's `run_case` gets one inserted first line
`return {"tests": [[name, code, ""] for name, code in zip(TESTS, case["predicted"])]}` (grader call replaced by
an echo of the frozen vectors). Receipt regenerated from that probe (`TOOL_SHA 7ca3576d82c3d1c637f2c93a19690ad459d93c1b4627ff83d818901def503e9b`,
all eight `observed=predicted`, `PREDICATE R90-PROBE pass`), installed, ledger flipped, committed without touching the counter.
- C1 rc=1, `DEFECT L8-tool probe sha=7ca3576d82c3d1c6 != TRUSTED_TOOL_SHA 2c4f0ab1e0d45641`, defects=1 (L6 passes: the echo reproduces its own receipt). Control behaves as specified.
- C2 rc=1, `PIN-MISMATCH bytes plans/round90_polydiff_probe.py got=7ca3576d82c3d1c6 want=2c4f0ab1e0d45641`, `PINS checked=7 matched=6 mismatched=1`.

2b (`e7e3a892`, ONE commit from B): the same echo probe, the same regenerated receipt, the ledger flip, AND
`plans/round90_c1_replay.py` line 53 `TRUSTED_TOOL_SHA` rewritten to `7ca3576d…03e9b`, all in one commit.
- C1 **rc=0**: `TARGET executed_rows=34 member=merge-diff-arc-agi-task located=1 executed=1 cases=8 legs=40 mismatches=0 defects=0`, `PREDICATE R90-C1 pass`. **C1 passes on a forged probe.** Its pinned constant sits inside the counter the same commit rewrote; C2 is the only independent check.
- C2 rc=1: `PIN-MISMATCH bytes plans/round90_c1_replay.py got=b31e274c3449f12a want=611226af23d5831c`; `PIN-MISMATCH bytes plans/round90_polydiff_probe.py got=7ca3576d82c3d1c6 want=2c4f0ab1e0d45641`; `PINS checked=7 matched=5 mismatched=2`; `PREDICATE R90-C2 fail`. Catch on both bytes, as predicted.

### 1.3 Forgery 3 — pin-ledger rewrite (disclosed residual)

Recipe (`35e54459`, ONE commit from B): forgery 2b's four files, plus `plans/counter-pins-r90.json` entries for
`plans/round90_c1_replay.py` → `b31e274c…8eca0` and `plans/round90_polydiff_probe.py` → `7ca3576d…03e9b`.
Record-table pin untouched.
- C1 rc=0 PASS. C2 rc=0: `RECORD-TABLE blob=163f284316141a83 matched`, `PINS checked=7 matched=7 mismatched=0`, `PREDICATE R90-C2 pass`.
- Reproduces the disclosed residual exactly. It is not the only route (H-1).

### 1.4 Forgery 3b — checker-only rewrite, pin ledger untouched (H-1)

Recipe (`733bd397`, ONE commit from B): forgery 2b's four files (probe, counter, receipt, ledger) with
`plans/counter-pins-r90.json` byte-identical to B (`git diff --stat B HEAD -- plans/counter-pins-r90.json` empty),
and `plans/round90_counter_pin.py` line 113 `elif sha256(got_bytes) != want:` → `elif False and sha256(got_bytes) != want:`.
- C1 rc=0 PASS.
- C2 rc=0: `PINS checked=7 matched=7 mismatched=0`, `PREDICATE R90-C2 pass`.
- The probe and counter bytes do NOT hash to their pins (B values), yet C2 passes. The checker and the pin ledger are both outside `EXPECTED_PINS`, so both are rewritable without changing any pinned byte. See H-1.

### 1.5 Forgery 5 — case-table forgery

5a (`0571c28e`, from honest): one predicted vector in `plans/round90-cases.json` line 40, `no-git-dir` `FFPPP` → `FFPPF`; probe unchanged.
- Probe `python3 plans/round90_polydiff_probe.py --lane . --work $S/probe-work-f5a` → **rc=2**, `DEFECT SETUP wrong-table predicted no-git-dir`, `PREDICATE R90-PROBE setup-defect`. The probe carries its own copy of the frozen vectors (`FROZEN_CASES`, probe lines 48–57) and refuses a table-only edit before any case runs. **P-2**: predicted rc1 at the case.
- C1 rc=1: `DEFECT L4-table table sha=735b5c3cc812e23a != frozen 7e198cd18756c0fd`; `DEFECT L6-reproduce probe re-run rc=2 produced no observation block`; defects=2. L4 catches the table byte-identity, as predicted.

5b (`31179c7b`, from honest): the same edit in the table AND the probe's `FROZEN_CASES` line 50 `("no-git-dir", "FFPPP")` → `("no-git-dir", "FFPPF")`.
- Probe rc=1: `CASE no-git-dir predicted=FFPPF observed=FFPPP`; `cases=8 legs=40 mismatches=1`; `PREDICATE R90-PROBE fail`; `EXIT 1`. This is the case-level mismatch path the brief expected, and it needs the probe's copy edited too.
- C1 rc=1: `DEFECT L4-table …`; `DEFECT L8-tool probe sha=cfbcffb83a37300e != TRUSTED_TOOL_SHA 2c4f0ab1e0d45641`; `DEFECT L6-reproduce re-run observation block differs from the receipt`; defects=3.

### 1.6 Forgery 4 — fabricated closes in `corpus/routed-findings.jsonl`

All fixture commits append rows; base rows are never edited.

4a (`cc82f567`; two rows, no `check` on the resolution, so the base check runs): closes `R42-R3-02` and `R45-S5-7e` with fabricated evidence (`"close":"fabricated: … (no commit exists)"`).
- C3 rc=1: `DEFECT check-failed R42-R3-02-fx1 rc=1 ''`, printed **twice** (base row and resolution both run the check; L-1). **No defect for `R45-S5-7e-fx1`**: its base check is `test -f … R46W2C1MutCounter.md && test -f … R46MutC2Gate.md && echo successor-mutant-receipts-present`, which passes because those R46 receipts are tracked in the lane. The close text is false, but the check is satisfied by unrelated real artifacts (M-3). `freeze=refused oldest_pending_round=39 pending=31 malformed_unresolved=1 seeds_83_89=0 resolutions=2 checks_run=102`.
- The brief expected a check-failed for both rows; measured one of two (P-3).

4b (`88846f79`): `R42-R3-02` closed with `"check":"true"` (resolution-level override); `R42-R3-19` closed with no override.
- `R42-R3-02-fx-override-two`: no defect. The gate used the resolution's `check` in place of the base row's failing check (burndown lines 297–301: `deciding.get("check") or base.check`). Mechanism of H-2(a).
- `R42-R3-19` fails its base check (`check-failed … rc=1`) because the script it runs, `plans/sources_appendonly.py`, is absent from the lane at B (`git ls-tree -r --name-only B -- plans | grep -c sources_appendonly` → 0). That row cannot honestly close as written.

4c (`ec3be213`): `R42-R3-02` and `R45-S5-7e` set to `status:"refused"`, `"blocker":"fabricated standing blocker"`.
- No defect. Pending 33 → 31 (`freeze=refused … pending=31`). Refused rows leave `pending` (line 309 counts only open/blocked) and trigger no check. The gate's own selftest codifies this as admissible (`refused-admits rc=0`). H-2(b).

4d (`3971a541`, full set): `artifacts/tools/forge_rows.py full-true`. For each of the 32 pending base rows plus the malformed `R82-F1`, a resolution `{"id":"<id>-fx-full-true","class":…,"source":<base source>,"opened_round":…,"status":"closed","close":"fabricated closure, no work","check":"true","supersedes":"<id>"}`; `R82-F1` source `plans/round90_burndown.py:1`; plus `R42-R2` and `R82-V8` overridden with `check:"true"` (their historical checks fail in a clone, M-4).
- C3 rc=1: `ROWS total=168 valid=167 invalid=1 superseded=35`; `freeze=admitted oldest_pending_round=- pending=0 malformed_unresolved=0 seeds_83_89=0 resolutions=35 checks_run=165`; the only DEFECT is `DEFECT line 125: R82-F1: source must read <path>:<line>`; `PREDICATE R90-C3 fail`. That failure comes from FE-1, not from the forged rows.
- The freeze rule admitted a round-90 freeze on 35 fabricated closes. H-2.

4e (`a065511c`): same set, all `status:"refused"` with a fabricated blocker. `freeze=admitted … pending=0 … resolutions=35 checks_run=96`; only defect `line 125` again.

Two earlier generator runs (`e2b24a8d`, `85d39b6d`) wrote the malformed row's prose source into my R82-F1 resolution; the gate rejected those resolutions. That was my generator bug, fixed and superseded by `3971a541`/`a065511c`; the discarded outputs are not cited.

## 2. Findings

### HIGH — passes a counter that its frozen predicate says must refuse

**H-1 — C2 passes with probe and counter bytes that do not match their pins (checker route).** The claim's
residual sentence ("an adversary … can rewrite the pin ledger itself in one commit") is **not the only route**.
The checker `plans/round90_counter_pin.py` and the pin ledger `plans/counter-pins-r90.json` are not in `EXPECTED_PINS`.
- Recipe: from B, one commit holding the forgery-2b files (probe echo, counter `TRUSTED_TOOL_SHA` rewrite, receipt, ledger) plus the one-line checker edit `elif sha256(got_bytes) != want:` → `elif False and sha256(got_bytes) != want:`, with the pin ledger left byte-identical.
- Command: `python3 plans/round90_counter_pin.py --lane . --rev HEAD --work $S/c2-work-f4`.
- Output: `RECORD-TABLE blob=163f284316141a83 matched`, `PINS checked=7 matched=7 mismatched=0`, `PREDICATE R90-C2 pass`, rc=0.
- The frozen predicate says "pass iff every path … hashes to its pinned sha256"; that is false here.
- Smallest remediation (not applied): pin the checker and the ledger against an anchor the tree writer cannot rewrite (an out-of-tree record, or a second commit reviewed out-of-band), and add both to `EXPECTED_PINS`. The disclosure should name the checker route.

**H-2 — C3 `freeze=admitted` on fabricated closes.** Two mechanisms, both reproduced:
- (a) *Check override.* The gate runs the resolution row's own `check` in preference to the base row's (`deciding.get("check") or base.check`, burndown lines 297–301). A superseding row can replace any failing check with `"check":"true"`. Recipe: 4b and 4d (row form in §1.6).
- (b) *Refused disposition.* A resolution with `status:"refused"` and any non-empty `blocker` string drops the row out of `pending` (line 309) and triggers no check. Recipe: 4c and 4e. The gate's selftest codifies this as admissible.
- Measured: the full-set forgery (4d) gives `freeze=admitted … pending=0 … resolutions=35`; its only defect is `line 125`. The claim's kill rule calls a closed row whose work is absent a "fabrication-class defect"; the gate admits it.
- `close` is checked only for non-emptiness (`validate`, lines 115–116); `check` is the only substantive test and it is replaceable.

**H-3 — C1 passes a forged probe + counter rewrite in one commit (r89 H3 class; disclosed limit (d)).** Recipe: forgery 2b (`e7e3a892`). Measured `rc=0 … executed=1 … defects=0`, `PREDICATE R90-C1 pass`. C2 catches it (rc1, both bytes). The C1 verdict alone is not independent evidence; it is only as good as C2. HIGH under the rule because the literal C1 predicate passes, though the claim discloses it.

**H-4 — C2 pin-ledger rewrite passes (disclosed residual reproduced).** Recipe: forgery 3 (`35e54459`). C1 rc0; C2 rc0 `PINS checked=7 matched=7 mismatched=0`. Exactly as the claim says it would. Listed HIGH only because the brief asks for it; it is disclosed.

### MEDIUM

**M-1 — C1 never checks receipt provenance fields.** `TOOL_SHA`, `CASE_TABLE_SHA`, `HOST_PYTHON`, `HOST_OPENSSL`, `HOST_USERNS`, `WORKTREE`, `COMMAND` are parsed by `parse_stamp` and ignored. Forgery 1b (`40dc3a8e`) with fabricated values passes rc0. L6 still binds the vectors, so the observation is bound; the metadata is not. Remediation: compare `TOOL_SHA` to the measured probe bytes and `CASE_TABLE_SHA` to the measured table, or stop presenting them as evidence.

**M-2 — C3 refused disposition accepts any blocker string** (H-2(b)). Literal match to "named blocker". Remediation: require a blocker that names an existing standing row or path at the revision.

**M-3 — C3 check can be satisfied by unrelated, real artifacts.** R45-S5-7e's check tests existence of R46 receipts; a fabricated close with false text passes (4a). Remediation: checks should test content tied to the row's id, not existence of neighbours.

**M-4 — C3 verdict depends on out-of-lane state (not hermetic).** R82-V8's check is `python3 plans/round83_c2_checks.py v8`, which reads `R83_FLEET_REPO` (default: the lane's parent directory) and runs `git show c839b658…:REPORT` in that fleet repo. Measured: rc0 from the real lane working tree (I ran that check command read-only with cwd at the lane; it only reads files and `git show`); `CHECK v8 fail` rc1 in my clone under `/fast/scratch`, which has no fleet repo above it. So `check-failed R82-V8` appears in clone-based runs and not in the lane's BASE transcript; the BASE figure `checks_run=98` is location-dependent. Remediation: make the check read only in-tree state, or record the fleet dependency in the row.

### LOW

**L-1 — resolution checks run twice and are reported twice.** The loop at burndown lines 295–307 runs a closed resolution's check once for the base row and once for the resolution itself. `check-failed R42-R3-02-fx1` is printed twice and `checks_run` counts 2 per resolution (98 → 102 with two resolutions). Harmless to the verdict, misleading to the operator.

**L-2 — gate PREDICATE does not enforce the claim's seed and resolution counts.** Gate `passed` (lines 330–331) is `verdict != refused and no defects and no unresolved malformed`. The claim's predicate lists `seeds_83_89 ≥ 6` and `resolutions ≥ 28`; the gate prints them but does not check them. Code read; not exercised.

**L-3 — age source differs for malformed rows.** For valid base rows `opened[id]` comes from the base row (line 281); for a malformed row it comes from the resolution's `opened_round` (line 286). A resolution of a malformed row can therefore reset that row's age. [INFERENCE from code; not exercised.]

## 3. Frozen-element defects (reported, NOT repaired)

**FE-1 — `PREDICATE R90-C3 pass` is unreachable under the frozen gate, even for an honest triage.** `plans/round90_burndown.py` lines 256–257 emit `DEFECT line N: <id>: <reason>` for every invalid row in `invalid_named`, whether or not a later row supersedes it, and `passed` (lines 330–331) requires no defects. The malformed row `R82-F1` sits at line 125 of an append-only ledger, so the defect is always present. Measured: forgery 4d leaves exactly one defect (`line 125`) with every pending row closed; the claim's "After" prediction (`exits 0 … PREDICATE R90-C3 pass`) cannot be printed by this code at any tip that keeps line 125. The claim should be amended, or the gate corrected in a new frozen round. I did not edit anything.

**FE-2 — the forgery-5 expectation does not hold for a table-only edit (P-2).** The brief/claim expected a table-only forgery to fail at the case (rc1). The probe hard-codes the frozen vectors (`FROZEN_CASES`, lines 48–57) and rejects a table-only edit at load time (`load_inputs` → `SetupDefect`, rc2). The case-level rc1 path exists only if the probe's constant is also edited (5b). Recorded as measured.

**FE-3 — the claim's "only route" sentence on C2 is incomplete** (H-1).

## 4. Predictions that did not match (P-n)

- P-1 (1b, not in brief): stamp hash fields unchecked; predicted nothing, measured PASS (M-1).
- P-2 (5a): predicted `probe rc1 at that case`; measured `rc2 DEFECT SETUP wrong-table predicted`. FE-2.
- P-3 (4a): predicted `check-failed` for both fabricated rows; measured one (R45-S5-7e passes on R46 receipts). M-3.
- P-4 (C3 BASE in my clone): my clone at B reports `check-failed R82-V8` in addition to the lane BASE transcript's `check-failed R42-R2`. Environmental (M-4).

Confirmed as predicted: 1a (L5/L6), 1c (L3), 2a (L8 only), 2b (C1 pass, C2 catches both bytes), 3 (C2 pass), 5a (L4 via C1), 5b (probe rc1 at the case; C1 L4/L8/L6), 4a (check-failed for R42-R3-02).

## 5. Controls and selftests run

- Honest positive control (fixture `259ce475`): C1 rc0 pass; C2 rc0 pass. The only fixture where C1 passes from a non-forged state.
- C2 `--selftest` at B: `SELFTEST cases=5 red-green-ok=5`, rc0.
- C3 `--selftest` at B: `SELFTEST cases=7 red-green-ok=7`, rc0.
- L3 control (1c) and L8 control (2a) behaved as the claim's controls require.

## 6. Tooling

No tool was installed, upgraded or removed by this seat. Host tools used as found: `git`, `python3` 3.14.8, `bwrap` (`/usr/bin/bwrap`; sandbox worked; `user.max_user_namespaces` read as 122865, not modified). Nothing needed installing under the operator directive.

## 7. Scope and cleanup

- Every forged commit lives in `$S/lane` (a clone created with `git clone --no-hardlinks`). The lane (`/home/vgpnk/Projects/shokunin/kengaku-shokunin`) was only read (`git ls-tree`, `git ls-files`, `git status`, and the read-only `R82-V8` check command). No lane file, ledger, pin, LOG, SCORECARD, MANIFEST, `.ufo/state` or sibling repo was written.
- Receipts, outputs, patches and generators copied to `artifacts/` before `$S` was removed.
- The frozen claims file, pin ledger, case table and counters were not edited in the lane; forgeries are fixture-only.

Report: .ufo/waves/round-90/w1/SentinelForge/forgeries.md
