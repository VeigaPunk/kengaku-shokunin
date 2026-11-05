# ExecC3Triage: routed-findings triage (drafts)

Receipts: `receipts/`. Draft rows: `resolutions.jsonl` (34), `seed-rows.jsonl` (46, report-only seeds).

Seat: ExecC3Triage (leaf, read-only on the lane). Item: draft resolution rows for `corpus/routed-findings.jsonl`. The ledger was not edited.

## Measured state

- Lane HEAD at measurement: `a2b22609` (round-90 C1 receipt and ledger row landed). B `664435cf` is an ancestor. Gate run at `--rev HEAD`.
- Gate at HEAD, lane working tree (`receipts/gate-at-HEAD-lane.txt`): `ROWS total=133 valid=132 invalid=1 superseded=0`; DEFECT line 125 (R82-F1 malformed); DEFECT invalid-row-unresolved R82-F1; DEFECT check-failed R42-R2 rc=1; `freeze=refused oldest_pending_round=39 pending=33 malformed_unresolved=1 seeds_83_89=0 resolutions=0 checks_run=98`; `PREDICATE R90-C3 fail`, rc 1. This matches the BASE measurement, so the 33 and the two structural defects are confirmed.
- Pending inventory = 33, exactly as expected: 39x3 (R39-R2, R39-R3, R39-R4), 40x1 (R40-R5), 42x20, 45x4 (R45-S5-7b..e), 51x4 (R51-R1..R4), 82x1 (R82-F1). No other DEFECT line exists in the lane run. `R82-V8` shows a clone-only check failure (see Instrument notes), not a lane defect.
- Drafts were validated, not just written: `resolutions.jsonl` (34) and `seed-rows.jsonl` (46) were appended as commits in a scratch clone (`6786c924` then `8ba6bada`, scratch-only, author t) and the gate was run on that clone. Gate selftest 7/7 red-green (`receipts/selftest.txt`).

## Draft outcome (what the gate reads from the drafts)

| Scope | Result |
|---|---|
| 34 resolutions only (`resolutions.jsonl`) | `freeze=refused oldest_pending_round=51 pending=5 malformed_unresolved=1 seeds_83_89=0 resolutions=34 checks_run=109` ; rc 1 |
| 34 resolutions + 46 seeds (`seed-rows.jsonl`) | `freeze=refused oldest_pending_round=51 pending=37 malformed_unresolved=1 seeds_83_89=46 resolutions=34 checks_run=117` ; rc 1 |

Statuses for the 33 pending: **6 closed, 23 refused, 4 blocked, 1 open**. R42-R2 is a 34th resolution (supersede of a closed row whose check fails).

Pending after drafts: 4 blocked (R51-R1..R4, owned by kama, protocol and operator/integrator) and 1 open (R82-F1). Freeze refusal is therefore honest, not a drafting artifact.

## Headline findings for the L1 (read first)

1. **C3 pass is unreachable under the frozen gate, even with zero pending.** `plans/round90_burndown.py` appends `DEFECT line N: <id>: <reason>` for every malformed base line unconditionally (`evaluate`, lines 255-257), and `passed` requires no defects (line 330). The ledger is append-only, so line 125 stays malformed forever. Reproduced in a fixture (`receipts/fixture-malformed-superseded.txt`): one malformed row superseded by a closed resolution, pending 0, malformed_unresolved 0, `freeze=admitted`, and still `PREDICATE R90-C3 fail`, rc 1. Not repaired (frozen instrument). The claim's own predicate ("exits 0 with freeze=admitted ... no malformed row left unresolved") cannot be satisfied as written.
2. **23 refusals rest on the lane's own recorded `accepted-risk` dispositions** (dated 2026-10-26 to 2026-10-28, all `next: kengaku round 52 backlog` or a re-open condition). I quote them; I did not judge them correct. Re-measurement shows each defect still present. Mass refusal makes the gate's count green-able without fixing anything, so the L1 should decide consciously whether the refusals stand, and the claim text should say so.
3. **6 closes, two of which are judgment closes:** R42-R3-33 and R42-R3-37 close a finding whose residual is explicitly carried in a frozen record (round-43 claims:79; the unrun feal image). Both are marked in the row notes. Leaving them open is the conservative alternative.
4. **Four rows cannot be closed by any honest evidence today, and their checks pass for the wrong reason:** R45-S5-7c and R42-R3-09 (passing check = defect present), R51-R3 and R51-R4 (passing check = still absent). Closing on those checks would be fabrication-class. The gate has no way to tell.
5. **R82-F1 is a lane-owned item that was never done.** The routed fix (QUOTE_RE, round 83) did not land: no commit touches plans/anchor_line_check.py after f58c0d6a (round 58); cited=72 is unchanged; the four blind-spot rows are unparsed. The drafted supersede carries the well-formed source (`corpus/lessons/round-82.md:72`) and is status **open**. This is the one row the L1 can actually fix in this round.
6. **The R42-R2 closed row's check does not pass today.** Its check greps `routed_open.py --list` for `ROW R42-R2.x` lines the instrument never prints. The work (scratch_guard, registry row) did land; the drafted supersede pins those and passes rc 0.
7. **Frozen-text figure off:** the claim says "27 findings opened rounds 39-82 still sit open or blocked". Measured: 33 (39x3, 40, 42x20, 45x4, 51x4, 82). Recorded as a mispredict, not repaired.

## Draft files

- `resolutions.jsonl`: 34 rows, the ledger's own schema plus `supersedes`. Ids `<base>-R90`. Every `close` has concrete evidence; every `blocker` names the recorded disposition or the standing owner.
- `seed-rows.jsonl`: 46 rows for rounds 83-89 (NOT for resolutions.jsonl, per the assignment). Opened-round counts 83:2, 84:9, 85:8, 86:4, 87:6, 88:4, 89:13. Statuses 14 closed, 29 open, 3 blocked. All 46 pass the gate's source/schema validation in the clone.
- `receipts/`: every command output this report cites (gate runs, per-row check runs, probe batches 1-7, section dumps, selftest, fixture).

## Numbered verdicts

Fields per finding: current status | ran | observed | drafted status | drafted evidence or blocker (full text in the draft file, id shown) | drafted check.

### 1. R39-R2
- Current status: open (opened 39, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: probe still raises FileNotFoundError at plans/git_leak_probe.py:258 for an absent --work (re-run in a mktemp dir).
- Drafted status: **refused** (`R39-R2-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "re-open when the probe's digest pins are re-frozen (plans/round39_c2_verify.py PROBE_SHA256, plans/pkg-spec-r39.json frozen_instruments; SKILL.md:664)". Re-measured 2026-11-05 at a2b22609: plans/git_leak_probe.py:258 still raises FileNotFoundErro…
- Drafted check: none (drafted status is not closed)

### 2. R39-R3
- Current status: blocked (opened 39, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1 (0 `"order` rows in corpus/defects.jsonl, 5 rows). Pin still holds: plans/ledger_tip.py:72 binds corpus/defects.jsonl; plans/round40_c1_verify.py:98 pins ledger_tip.py.
- Drafted status: **refused** (`R39-R3-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "re-open when corpus/defects.jsonl is unpinned from plans/ledger_tip.py:6-7,72-73 and plans/round40_c1_verify.py:98". The pin still holds today: plans/ledger_tip.py:72 binds ("corpus/defects.jsonl","plans/defect_ledger.py"); plans/round40_c1_verif…
- Drafted check: none (drafted status is not closed)

### 3. R39-R4
- Current status: open (opened 39, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 2); surface read at HEAD
- Observed: `check` rc2 SETUP: plans/round39_c1_verify.py is not a round-38-list counter. plans/order_check.py unchanged since 34158b0 (sha 948d5e1d).
- Drafted status: **refused** (`R39-R4-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "split per residual: re-open (a) plans/order_check.py fail-open mid-scan (last commit 34158b0) and (e) plans/mutant_direction_check.py's round-38-only loader as their own rows in the round each instrument is re-frozen". Re-measured 2026-11-05 at a…
- Drafted check: none (drafted status is not closed)

### 4. R40-R5
- Current status: open (opened 40, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1. `git log 34158b0..HEAD -- plans/order_check.py` empty; R39-R3/R39-R4/F39LedgerTip D1 still open.
- Drafted status: **refused** (`R40-R5-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: `git log 34158b0..HEAD -- plans/order_check.py` is empty; the carried items R39-R3, R39-R4 and F39LedgerTip D1 are unchanged; check rc 1. The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 5. R42-R1
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1. Markers for repairs present; plans/battery42/ exists now; no `command -v uv` or /usr/local/bin/uv in plans/ or plans/battery42/ (uv assumption unpinned).
- Drafted status: **refused** (`R42-R1-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: the code markers the row's check greps for are present in plans/round42_c1_verify.py (--unshare-ipc, --ro-bind-data, def path_ok, unattributed), and plans/battery42/ now exists (a_cla…
- Drafted check: none (drafted status is not closed)

### 6. R42-R3
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1. Filler-control half present (control-c2-filler.txt:1-3). `grep -rln 'pulls/|state=closed|merged=' plans/*.py` no hits.
- Drafted status: **refused** (`R42-R3-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: the filler-control half is landed (.ufo/waves/round-42/claims/control-c2-filler.txt:1-3 red-as-required); the open half is not: `grep -rln 'pulls/|state=closed|merged=' plans/*.py` re…
- Drafted check: none (drafted status is not closed)

### 7. R42-R5
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 2); surface read at HEAD
- Observed: `check` rc2 SETUP: plans/round42_c1_verify.py not a round-38-list counter (missing=R37_REL,battery38_fixtures,attributed,FAMILY non_6_tuple_rows=14).
- Drafted status: **refused** (`R42-R5-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: check exits 2 SETUP: plans/round42_c1_verify.py is not a round-38-list counter (missing=R37_REL,battery38_fixtures,attributed,FAMILY non_6_tuple_rows=14); plans/order_check.py unchang…
- Drafted check: none (drafted status is not closed)

### 8. R42-R6
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1. Chmod-000 sentinel: `plans/scratch_guard.py check` prints reason=sentinel-unreadable and exits 1 (uid 1000). selftest ok=36/36, no unreadable case.
- Drafted status: **refused** (`R42-R6-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: a chmod-000 sentinel makes `plans/scratch_guard.py check` print CHECK red reason=sentinel-unreadable and exit 1 (uid 1000); `--selftest` prints SELFTEST ok=36/36 and has no check-sent…
- Drafted check: none (drafted status is not closed)

### 9. R42-R3-02
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: SKILL.md has no ':238'.
- Drafted status: **refused** (`R42-R3-02-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: SKILL.md has no ':238' (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 10. R42-R3-05
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: knowledge entry line 350 still cites test_outputs.py:26-52.
- Drafted status: **refused** (`R42-R3-05-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: corpus/knowledge/tb2-circuit-fibsqrt-grader.md:350 still cites test_outputs.py:26-52 (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 11. R42-R3-06
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: corpus/README.md:75 sources cell unchanged.
- Drafted status: **refused** (`R42-R3-06-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: corpus/README.md:75 sources cell still reads 'S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88)' (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 12. R42-R3-07
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: SKILL.md:862 still reads 'equal to the receipt row'.
- Drafted status: **refused** (`R42-R3-07-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: SKILL.md:862 still reads 'equal to the receipt row' (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 13. R42-R3-08
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: plans/pkg_gate.py:276 still has `--with biopython==1.85`.
- Drafted status: **refused** (`R42-R3-08-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: plans/pkg_gate.py:276 still runs `uv run --no-project --with biopython==1.85`; plans/fibsqrt_probe.py has no biopython import (grep 'biopython|uv' matches prose at line 44 only). chec…
- Drafted check: none (drafted status is not closed)

### 14. R42-R3-09
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0, but it passes BECAUSE the defect clause "and pytest's cache" is present (knowledge line 328). Presence-test of the defect: not close evidence.
- Drafted status: **refused** (`R42-R3-09-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: corpus/knowledge/tb2-circuit-fibsqrt-grader.md:328 still reads "and pytest's cache". NOTE: this row's check passed today (rc 0) only because it asserts the defect clause is present; i…
- Drafted check: none (drafted status is not closed)

### 15. R42-R3-18
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: plans/carried_direction_diff.py and plans/sources_appendonly.py absent; `git log --all` empty for both.
- Drafted status: **refused** (`R42-R3-18-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: plans/carried_direction_diff.py and plans/sources_appendonly.py do not exist; `git log --all` on both paths is empty (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 16. R42-R3-19
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: sources_appendonly.py absent, so the `--lane .` invocation cannot run.
- Drafted status: **refused** (`R42-R3-19-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: plans/sources_appendonly.py is absent, so the `--lane .` invocation cannot run (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 17. R42-R3-26
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: chmod-000 sentinel exits 1, check requires 2.
- Drafted status: **refused** (`R42-R3-26-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: a chmod-000 sentinel still exits 1 from `plans/scratch_guard.py check` (check requires exit 2; rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 18. R42-R3-27
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: `--selftest` ok=36/36, check requires >=37.
- Drafted status: **refused** (`R42-R3-27-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: `--selftest` reports SELFTEST ok=36/36 (check requires >= 37; rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 19. R42-R3-32
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: corpus/lessons/round-42.md has no `measure-final.txt:938`.
- Drafted status: **refused** (`R42-R3-32-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: corpus/lessons/round-42.md has no `measure-final.txt:938` citation (check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 20. R42-R3-33
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0: plans/round-43-claims.md:79 reads '9 witnessed of 20 ... stay carried' (the honest numerator, with the 9 unwitnessed carried).
- Drafted status: **closed** (`R42-R3-33-R90`)
- Drafted evidence or blocker: Numerator corrected in the frozen round-43 plan: plans/round-43-claims.md:79 reads '(`F42CritPlanNext` D1: 9 witnessed of 20) stay carried', i.e. the honest count replaces '20 rc-witnessed'. Scope of this close: the misstatement is corrected. The 9 unwitnessed survivors are NOT claimed witnessed; ro…
- Drafted check: `cd "$LANE" && grep -qF '9 witnessed of 20' plans/round-43-claims.md` (rc0 today)

### 21. R42-R3-34
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0 only because NA7 exists in one control (control-c1-direction-mislabel.txt:7-8). Per-mutant restore controls not present.
- Drafted status: **refused** (`R42-R3-34-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: round-43 has one NA7 control (.ufo/waves/round-43/claims/control-c1-direction-mislabel.txt:7-8), but the routed item is per-mutant restore controls for the u=18 branch, which are not …
- Drafted check: none (drafted status is not closed)

### 22. R42-R3-35
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: no xo|x13|substitut file in .ufo/waves/round-43/claims/ (25 files).
- Drafted status: **refused** (`R42-R3-35-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: no XO3/X13 substitute-shape red control exists in .ufo/waves/round-43/claims/ (25 files, none matching xo|x13|substitut; check rc 1). The lane declined the work; no fix landed.
- Drafted check: none (drafted status is not closed)

### 23. R42-R3-36
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: corpus/evidence/round43/ holds no prior-art receipt.
- Drafted status: **refused** (`R42-R3-36-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`; recorded next: "kengaku round 52 backlog". Re-measured 2026-11-05 at a2b22609: corpus/evidence/round43/ holds no prior-art receipt (files: feal-dry-cases-freeze.txt, feal-probe.txt, tb2-feal-differential-cryptanalysis/; check rc 1). The lane declined the work; n…
- Drafted check: none (drafted status is not closed)

### 24. R42-R3-37
- Current status: open (opened 42, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0: host=libc-rand flagged at knowledge entry lines 48, 291, 346 and plans/feal_probe.py:194. Image re-derivation still unrun.
- Drafted status: **closed** (`R42-R3-37-R90`)
- Drafted evidence or blocker: Host dependence flagged where the claim is made: corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:48, :291 and :346 read `host=libc-rand` / `flagged host=libc-rand`; plans/feal_probe.py:194 carries host="libc-rand" on cheat-clock-seed; round-43 claims §C2 names it a host fact (per row)…
- Drafted check: `cd "$LANE" && grep -q 'host="libc-rand"' plans/feal_probe.py && grep -q "libc.srand" plans/feal_probe.py && grep -q "host=libc-rand" corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (rc0 today)

### 25. R45-S5-7b
- Current status: open (opened 45, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0: round-46 C3 lint refuses dict literal (`lint= ['{', '}']`); PRED_LINT_TOKENS at plans/round46_c3_verify.py:629.
- Drafted status: **closed** (`R45-S5-7b-R90`)
- Drafted evidence or blocker: Routed item landed in the round-46 C3 lint: plans/round46_c3_verify.py:629 PRED_LINT_TOKENS includes "{" and "}"; lint_block (line 641) refuses a dict literal. Re-run today: `lint= ['{', '}']`, check exit 0.
- Drafted check: `python3 -c 'import importlib.util,sys;from pathlib import Path;p=Path(sys.argv[1]);s=importlib.util.spec_from_file_location("c3",p/"plans/round46_c3_verify.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);b="def predict(text):\n    table = {\"x\": True}\n    return table.get(text, False)\n";l=m.lint_block(b);print("lint=",l);sys.exit(0 if "{" in l else 1)' "$LANE"` (rc0 today)

### 26. R45-S5-7c
- Current status: open (opened 45, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0 echoes 'unpinned-uv-fetch-present': plans/pkg_gate.py:276 still runs the unpinned uv fetch. A passing check here means the defect is PRESENT.
- Drafted status: **refused** (`R45-S5-7c-R90`)
- Drafted evidence or blocker: recorded disposition `accepted-risk`. Re-measured 2026-11-05 at a2b22609: plans/pkg_gate.py:276 still runs the unpinned `uv run --with biopython==1.85` fallback. NOTE: this row's check passed today (rc 0) because it matches the defect and echoes 'unpinned-uv-fetch-present'; a passing check here mean…
- Drafted check: none (drafted status is not closed)

### 27. R45-S5-7d
- Current status: open (opened 45, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0: plans/fixture_fence.py:221 refuses `{T}/../../etc` as a placeholder.
- Drafted status: **closed** (`R45-S5-7d-R90`)
- Drafted evidence or blocker: Brace-prefix item re-run today against a non-lane option: plans/fixture_fence.py:221 refuses `--evidence-ref {T}/../../etc` with 'is a placeholder the fence cannot resolve' (check printed that message; exit 0).
- Drafted check: `python3 -c 'import importlib.util,sys;from pathlib import Path;p=Path(sys.argv[1]);s=importlib.util.spec_from_file_location("ff",p/"plans/fixture_fence.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);v,e=m._argv(Path("."),"anchor",["--evidence-ref","{T}/../../etc"]);print("err=",e);sys.exit(0 if v is None and "placeholder" in (e or "") else 1)' "$LANE"` (rc0 today)

### 28. R45-S5-7e
- Current status: open (opened 45, owner kengaku, disposition accepted-risk)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0: both round-46 mutant receipts exist and are tracked at HEAD.
- Drafted status: **closed** (`R45-S5-7e-R90`)
- Drafted evidence or blocker: Successor mutant receipts are tracked at HEAD: `git ls-files` lists .ufo/waves/round-46/w2/R46W2C1MutCounter.md and .ufo/waves/round-46/w1/R46MutC2Gate.md (both present, 6292 and 4209 bytes).
- Drafted check: `test -f "$LANE/.ufo/waves/round-46/w2/R46W2C1MutCounter.md" && test -f "$LANE/.ufo/waves/round-46/w1/R46MutC2Gate.md" && echo successor-mutant-receipts-present` (rc0 today)

### 29. R51-R1
- Current status: open (opened 51, owner kama, disposition routed)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1: `curl :45669/v1/models` returns nothing; :1234 returns 200; PROVINCE.md:15 records ABSENT 2026-11-04.
- Drafted status: **blocked** (`R51-R1-R90`)
- Drafted evidence or blocker: routed to owner kama (serving-plane health and flag authority, per the row's next). The row's check fails today: `curl -s -m5 http://127.0.0.1:45669/v1/models` returns nothing; PROVINCE.md:15 records ABSENT 2026-11-04 (round-76 resolver: 000 for :45669). Only :1234 answers (HTTP 200). Standing block…
- Drafted check: none (drafted status is not closed)

### 30. R51-R2
- Current status: open (opened 51, owner protocol, disposition routed)
- Ran: base `check` (rc 1); surface read at HEAD
- Observed: `check` rc1, mis-scoped: `../*-shokunin/corpus/routed-findings.jsonl` matches only this lane's own ledger (133 disposition hits).
- Drafted status: **blocked** (`R51-R2-R90`)
- Drafted evidence or blocker: routed to owner protocol (fleet routed-finding ledger schema: owner + disposition + next). The row's check is mis-scoped: `../*-shokunin/corpus/routed-findings.jsonl` expands to this lane's own ledger only (133 "disposition" hits), so rc 1 is not evidence about any sibling. Standing blocker: the fle…
- Drafted check: none (drafted status is not closed)

### 31. R51-R3
- Current status: open (opened 51, owner unowned:integrator, disposition routed)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0 because the three trees are still ABSENT (state, not decision). PROVINCE.md:12,13,16 and round-51 receipt paths.txt agree.
- Drafted status: **blocked** (`R51-R3-R90`)
- Drafted evidence or blocker: routed to owner unowned:integrator; operator decision: restore or retire the three declared trees. Re-measured today: ABSENT ~/Projects/webzites/repos/llm-wiki, ~/archive/bench-arena, ~/Projects/bounties/ledger/telemetry.jsonl; PROVINCE.md:12,13,16 record the dated ABSENT verdicts; receipt corpus/ev…
- Drafted check: none (drafted status is not closed)

### 32. R51-R4
- Current status: open (opened 51, owner kama, disposition routed)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0 because :34113 still returns 000 (ABSENT record). PROVINCE.md:14. systemctl --user not reachable from this shell.
- Drafted status: **blocked** (`R51-R4-R90`)
- Drafted evidence or blocker: routed to owner kama: whether the qwen-coder unit is retired. Re-measured today: curl http://127.0.0.1:34113/health returns 000 (the row's check passes on that state, which is the ABSENT record, not the decision). PROVINCE.md:14 records it. `systemctl --user` could not be queried from this shell (no…
- Drafted check: none (drafted status is not closed)

### 33. R82-F1
- Current status: open (opened 82, owner kengaku, disposition routed)
- Ran: base `check` (rc 0); surface read at HEAD
- Observed: `check` rc0 but vacuous: ANCHORLINE cited=72 (unchanged since R82), live=0. S260/S261/S265/S266 unparsed; QUOTE_RE at plans/anchor_line_check.py:67; source cell malformed (prose).
- Drafted status: **open** (`R82-F1-R90`)
- Drafted evidence or blocker: Well-formed source: corpus/lessons/round-82.md:72 is the '## Corrections' heading that carries the R81-V discharges (the base row's prose cell is replaced by a real path:line). Status is open, not closed, because the routed fix never landed: plans/anchor_line_check.py:67 QUOTE_RE still requires `:N …
- Drafted check: none (drafted status is not closed)

### 34. R42-R2
- Current status: closed row, check FAILS at HEAD (rc1)
- Ran: base `check` run in lane and clone; children R42-R2.1/.2 checked
- Observed: Closed row, check rc1 at HEAD: `routed_open.py --list` prints no `ROW R42-R2.x` lines (output: DEFECT line=125 + ROWS total=133 invalid=1). Children verified: scratch_guard selftest 36/36 rc0; SKILL.md:640 row present.
- Drafted status: **closed (supersede)** (`R42-R2-R90`)
- Drafted evidence or blocker: Children verified today at a2b22609: R42-R2.1 plans/scratch_guard.py present, `python3 plans/scratch_guard.py --selftest` prints SELFTEST ok=36/36 rc0; R42-R2.2 SKILL.md:640 registry row `scratch-root-guard` present. The original R42-R2 check is defective, not the work: `python3 plans/routed_open.py…
- Drafted check: `cd "$LANE" && test -f plans/scratch_guard.py && python3 plans/scratch_guard.py --selftest >/dev/null 2>&1 && grep -qs 'scratch-root-guard' SKILL.md` (rc0 today)


## Seed drafts (rounds 83-89; in seed-rows.jsonl, not in resolutions.jsonl)

### 35. R83-V1
- Current status: no ledger row (seed; opened 83, class `admission-timing`, source `corpus/lessons/round-83-verifier-spotcheck.md:92`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R83-V1-R90`)
- Drafted evidence or blocker: Correction appended: corpus/lessons/round-84.md:33 (`## Corrections (R83-V1, R83-V2)`). Entry held, not re-admitted: corpus/lessons/round-85.md:31 ('stays held on Q13'). The conditional re-admission is not made (see R84-V4).
- Drafted check: none

### 36. R83-V2
- Current status: no ledger row (seed; opened 83, class `freshness`, source `corpus/lessons/round-83-verifier-spotcheck.md:93`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R83-V2-R90`)
- Drafted evidence or blocker: Partial: entry header repaired and re-verified: corpus/knowledge/tb2-code-from-image-offline.md:3 carries 'recheck: 2026-11-04 ... cadence monthly'; correction corpus/lessons/round-84.md:34. Not verified: the report/SCORECARD assertions routed as superseded (no R83-V2 reference in SCORECARD.md or LOG.md outside spot-checks).
- Drafted check: none

### 37. R84-V1
- Current status: no ledger row (seed; opened 84, class `uncommitted-round-evidence`, source `corpus/lessons/round-84-verifier-spotcheck.md:111`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R84-V1-R90`)
- Drafted evidence or blocker: Committed at 99a7cb3b ('inherited round-84 evidence committed (R84-V1)'); tracked at HEAD (git ls-files): .ufo/waves/round-84/w1-results.json, w1/CriticR84.md, w1/CriticR84/critique.md, w1/CriticR84/report.txt.
- Drafted check: `cd "$LANE" && git ls-files --error-unmatch .ufo/waves/round-84/w1-results.json >/dev/null 2>&1`

### 38. R84-V2
- Current status: no ledger row (seed; opened 84, class `freeze-hygiene`, source `corpus/lessons/round-84-verifier-spotcheck.md:112`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R84-V2-R90`)
- Drafted evidence or blocker: Not landed: `git cat-file -e b12a9d46:plans/round84-cases.json` rc 128 (verified 2026-11-05); the case table is still absent from the freeze commit; no fail-closed anchor located.
- Drafted check: none

### 39. R84-V3
- Current status: no ledger row (seed; opened 84, class `forged-receipt-control`, source `corpus/lessons/round-84-verifier-spotcheck.md:113`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R84-V3-R90`)
- Drafted evidence or blocker: Not landed: plans/round84_c1_replay.py has no forged or correct-vector control (grep rc 1).
- Drafted check: none

### 40. R84-V4
- Current status: no ledger row (seed; opened 84, class `q13-checker-shape`, source `corpus/lessons/round-84-verifier-spotcheck.md:114`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **blocked** (`R84-V4-R90`)
- Drafted evidence or blocker: Operator / gate-owner ruling pending: fleet L0 question /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:297 ('kengaku | round-84 | Q13 checker shape blocks ...') has no answer; plans/gate_timing_check.py:241-243 still accepts only falsify/wave2.
- Drafted check: none

### 41. R84-V5
- Current status: no ledger row (seed; opened 84, class `quality-criterion`, source `corpus/lessons/round-84-verifier-spotcheck.md:115`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R84-V5-R90`)
- Drafted evidence or blocker: Q61 criterion present: corpus/QUALITY.md:1320; introduced by commit 99a7cb3b ('Q61 criterion (R84-V5)').
- Drafted check: none

### 42. R84-V6
- Current status: no ledger row (seed; opened 84, class `writer-collision`, source `corpus/lessons/round-84-verifier-spotcheck.md:116`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R84-V6-R90`)
- Drafted evidence or blocker: Repaired at 99a7cb3b ('entry writer repair (R84-V6)'): corpus/knowledge/tb2-code-from-image-offline.md:4 reads `writer: kengaku-L1-round83-admission`; plans/gate_timing_check.py:55 WRITER_RE is `^writer:` under re.MULTILINE (line-start anchored).
- Drafted check: none

### 43. R84-V7
- Current status: no ledger row (seed; opened 84, class `expansion-overclaim`, source `corpus/lessons/round-84-verifier-spotcheck.md:117`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R84-V7-R90`)
- Drafted evidence or blocker: Correction appended: corpus/lessons/round-84.md:64 (`expansion: unchanged`); corpus/lessons/round-85.md:64-66 carries the same correction.
- Drafted check: none

### 44. R84-V8
- Current status: no ledger row (seed; opened 84, class `carried-red-gate`, source `corpus/lessons/round-84-verifier-spotcheck.md:118`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R84-V8-R90`)
- Drafted evidence or blocker: Not evidenced fixed: plans/round82_c1_plans_registry.py:167 still emits 'SELFTEST-FLAG:%s'; no flag fix located; registry gate not re-run in this pass.
- Drafted check: none

### 45. R84-V9
- Current status: no ledger row (seed; opened 84, class `c2-definition-horizon`, source `corpus/lessons/round-84-verifier-spotcheck.md:119`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R84-V9-R90`)
- Drafted evidence or blocker: Prospective: a successor freeze must define its before against an existing revision or price the future-file condition at freeze. No successor freeze exists to test; the original future file (corpus/lessons/round-84.md) now exists, so the condition is historical.
- Drafted check: none

### 46. R85-V1
- Current status: no ledger row (seed; opened 85, class `c1-battery-probe-fixtures`, source `corpus/lessons/round-85-verifier-spotcheck.md:184`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V1-R90`)
- Drafted evidence or blocker: No closure located: no successor battery or revision-bound receipt for flip_ledger or the new probe's selftest found in this pass (plans/round85_c1_replay.py present, not re-audited).
- Drafted check: none

### 47. R85-V2
- Current status: no ledger row (seed; opened 85, class `c1-provenance-control-sizing`, source `corpus/lessons/round-85-verifier-spotcheck.md:185`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V2-R90`)
- Drafted evidence or blocker: No successor freeze located that prices indistinguishable copies or binds host/revision stamps.
- Drafted check: none

### 48. R85-V3
- Current status: no ledger row (seed; opened 85, class `c2-frozen-obligations`, source `corpus/lessons/round-85-verifier-spotcheck.md:186`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V3-R90`)
- Drafted evidence or blocker: No closure located for V8/V2/V3/V6/V7/V9 substantive repairs; not re-audited in this pass.
- Drafted check: none

### 49. R85-V4
- Current status: no ledger row (seed; opened 85, class `c2-default-worktree`, source `corpus/lessons/round-85-verifier-spotcheck.md:187`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V4-R90`)
- Drafted evidence or blocker: Not landed: plans/round85_c2_debt.py:412 `Tree(lane, "worktree", "worktree")` remains the no-`--rev` path.
- Drafted check: none

### 50. R85-V5
- Current status: no ledger row (seed; opened 85, class `registry-revision-blindness`, source `corpus/lessons/round-85-verifier-spotcheck.md:188`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V5-R90`)
- Drafted evidence or blocker: No fix located: the round-82 plans-registry gate (plans/round82_c1_plans_registry.py) not re-run; the tip-reading claim not re-verified.
- Drafted check: none

### 51. R85-V6
- Current status: no ledger row (seed; opened 85, class `scope-guards-stamp-integrity`, source `corpus/lessons/round-85-verifier-spotcheck.md:189`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V6-R90`)
- Drafted evidence or blocker: No closure located for SentinelR85 S1/S2/S4/S6 in this pass.
- Drafted check: none

### 52. R85-V7
- Current status: no ledger row (seed; opened 85, class `report-counting-amendment-attribution`, source `corpus/lessons/round-85-verifier-spotcheck.md:190`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R85-V7-R90`)
- Drafted evidence or blocker: No closure located: no successor report with the SOURCES counting command and hash-bound amendment accounting found.
- Drafted check: none

### 53. R85-V8
- Current status: no ledger row (seed; opened 85, class `wave-metadata-operator`, source `corpus/lessons/round-85-verifier-spotcheck.md:191`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **blocked** (`R85-V8-R90`)
- Drafted evidence or blocker: Operator clarification pending: run-15 precedence over the canonical section-2 seat bands (corpus/lessons/round-85-verifier-spotcheck.md:191). No answer located in the lane or the fleet L0 file.
- Drafted check: none

### 54. R86-V1
- Current status: no ledger row (seed; opened 86, class `dead-evidence-pointer`, source `corpus/lessons/round-86-verifier-spotcheck.md:236`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R86-V1-R90`)
- Drafted evidence or blocker: Not landed: no correction names W1/ExecGatesR86/gate-receipt.txt (grep empty in LOG.md and round-86..89 lessons). LOG.md:3317 still cites .ufo/waves/round-86/L1/outside-gates.txt, absent (ls rc 2). LOG.md:3350 records the dead path as a defect only.
- Drafted check: none

### 55. R86-V2
- Current status: no ledger row (seed; opened 86, class `correction-sweep-conformance`, source `corpus/lessons/round-86-verifier-spotcheck.md:64`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R86-V2-R90`)
- Drafted evidence or blocker: Not landed: no erratum naming the superseded report lines 7 ('zero dead seats') and 242 ('naming the two incomplete seats above') located; must-fix item 2 (line 242) is the same debt.
- Drafted check: none

### 56. R86-V3
- Current status: no ledger row (seed; opened 86, class `stale-case-set-wording`, source `corpus/lessons/round-86-verifier-spotcheck.md:246`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R86-V3-R90`)
- Drafted evidence or blocker: Corrected: corpus/README.md:941 now reads 'eight case shapes, six schema-drift and two controls'; appended correction LOG.md:3342 (R87-C2 live case-set wording). LOG.md:3300 keeps the frozen wording, per the LOG rule.
- Drafted check: `cd "$LANE" && ! grep -qs 'eight frozen schema-drift cases' corpus/README.md`

### 57. R86-V4
- Current status: no ledger row (seed; opened 86, class `members-1-literal`, source `corpus/lessons/round-86-verifier-spotcheck.md:249`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R86-V4-R90`)
- Drafted evidence or blocker: Successor counts executed rows: plans/round87_c1_replay.py:262 prints `TARGET executed_rows=... member=... located=... executed=...`.
- Drafted check: `cd "$LANE" && grep -qs 'TARGET executed_rows=' plans/round87_c1_replay.py`

### 58. R87-V1
- Current status: no ledger row (seed; opened 87, class `l2-seats-not-dispatched`, source `corpus/lessons/round-87-verifier-spotcheck.md:125`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **blocked** (`R87-V1-R90`)
- Drafted evidence or blocker: Standing L0 question: fleet /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:312 ('kengaku | round-87 | Wave w1 ... no w1.ready.dispatched marker') has no answer.
- Drafted check: none

### 59. R87-V2
- Current status: no ledger row (seed; opened 87, class `figure-mispredict-q66-check`, source `corpus/lessons/round-87-verifier-spotcheck.md:126`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R87-V2-R90`)
- Drafted evidence or blocker: Q66 counter-side check landed as plans/round88_claim_figures.py (present); errata appended: LOG.md:3346 ('Correction to the frozen claim text (appended, not an edit)' for the defects=7 BASE figure).
- Drafted check: none

### 60. R87-V3
- Current status: no ledger row (seed; opened 87, class `lesson-spotcheck-pointer`, source `corpus/lessons/round-87-verifier-spotcheck.md:127`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R87-V3-R90`)
- Drafted evidence or blocker: Pointer appended in the round-88 lesson: corpus/lessons/round-88.md:16 cites corpus/lessons/round-87-verifier-spotcheck.md (committed 801b903a).
- Drafted check: `cd "$LANE" && grep -qs 'round-87-verifier-spotcheck' corpus/lessons/round-88.md`

### 61. R87-V4
- Current status: no ledger row (seed; opened 87, class `q66-able-to-fail`, source `corpus/lessons/round-87-verifier-spotcheck.md:128`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R87-V4-R90`)
- Drafted evidence or blocker: Shown able to fail: corpus/lessons/round-88.md:83 reports Q66 10 mutants, 6 killed, 4 survived.
- Drafted check: none

### 62. R87-V5
- Current status: no ledger row (seed; opened 87, class `axis-verdict-in-scorecard`, source `corpus/lessons/round-87-verifier-spotcheck.md:129`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R87-V5-R90`)
- Drafted evidence or blocker: No SCORECARD round section located stating the axis verdict beside the held score; not re-audited in this pass.
- Drafted check: none

### 63. R87-V6
- Current status: no ledger row (seed; opened 87, class `stale-lane-clause`, source `corpus/lessons/round-87-verifier-spotcheck.md:130`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R87-V6-R90`)
- Drafted evidence or blocker: Not evidenced in this pass.
- Drafted check: none

### 64. R88-1
- Current status: no ledger row (seed; opened 88, class `registry-rows-missing`, source `corpus/lessons/round-88-verifier-spotcheck.md:68`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R88-1-R90`)
- Drafted evidence or blocker: Registry rows present: SKILL.md:754 round88-fixgit-probe, SKILL.md:755 round88-c1-replay, SKILL.md:756 round88-claim-figures.
- Drafted check: `cd "$LANE" && grep -qs 'round88-c1-replay' SKILL.md && grep -qs 'round88-claim-figures' SKILL.md`

### 65. R88-2
- Current status: no ledger row (seed; opened 88, class `frozen-selftest-count-drift`, source `corpus/lessons/round-88-verifier-spotcheck.md:69`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R88-2-R90`)
- Drafted evidence or blocker: Not landed: no correction entry for 'four SELFTEST pass lines' vs five located in LOG.md or the round-89 lesson.
- Drafted check: none

### 66. R88-3
- Current status: no ledger row (seed; opened 88, class `attack-wave-findings`, source `corpus/lessons/round-88-verifier-spotcheck.md:70`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R88-3-R90`)
- Drafted evidence or blocker: Partially landed, not closed: the forged-probe pin (C1, TRUSTED_TOOL_SHA) and the external counter pins (C2) landed at 664435cf (B). The remaining C2 items and the round-88 list at corpus/lessons/round-88.md (Routed to round 89) are not re-verified; see R89-A2-1..A2-5.
- Drafted check: none

### 67. R88-4
- Current status: no ledger row (seed; opened 88, class `untracked-wave-handoff`, source `corpus/lessons/round-88-verifier-spotcheck.md:71`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R88-4-R90`)
- Drafted evidence or blocker: Tracked at HEAD: .ufo/waves/round-88/w1-results.json (committed at c3f81f72).
- Drafted check: `cd "$LANE" && git ls-files --error-unmatch .ufo/waves/round-88/w1-results.json >/dev/null 2>&1`

### 68. R89-D1
- Current status: no ledger row (seed; opened 89, class `frozen-element-d-unimplemented`, source `corpus/lessons/round-89-verifier-spotcheck.md:110`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R89-D1-R90`)
- Drafted evidence or blocker: Closed by the R90-C2 pin landing: plans/counter-pins-r90.json (commit 664435cf, ancestor of HEAD) pins plans/round89-q66-records.json to blob 163f284316141a831484dacb7f69ad4cbbaadfb3 anchored at 0e6bb05f (git cat-file -e rc 0). plans/round90_counter_pin.py at HEAD: 'RECORD-TABLE blob=163f2843... matched', 'PINS checked=7 matched=7 mismatc…
- Drafted check: `cd "$LANE" && grep -qs '163f284316141a831484dacb7f69ad4cbbaadfb3' plans/counter-pins-r90.json`

### 69. R89-D2
- Current status: no ledger row (seed; opened 89, class `control-name-drift`, source `corpus/lessons/round-89-verifier-spotcheck.md:111`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-D2-R90`)
- Drafted evidence or blocker: Correction not yet appended: LOG.md:3405 records `selftest-removed-from-path` vs `selftest-in-path` as 'Recorded as Mistake 10; the operator rules'. The correction note is owed in the round-90 LOG entry (L1 append).
- Drafted check: none

### 70. R89-D3
- Current status: no ledger row (seed; opened 89, class `before-count-two-ways`, source `corpus/lessons/round-89-verifier-spotcheck.md:112`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-D3-R90`)
- Drafted evidence or blocker: Correction not yet appended: grep '1 of 3 measured' in LOG.md and the round-89 lesson returns nothing; SCORECARD.md:4169 still reads '1 of 4 red'. The correction entry is owed.
- Drafted check: none

### 71. R89-D4
- Current status: no ledger row (seed; opened 89, class `gate-no-reject-row`, source `corpus/lessons/round-89-verifier-spotcheck.md:113`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-D4-R90`)
- Drafted evidence or blocker: Pending this round's lesson: corpus/lessons/round-90.md absent (ls rc 2). The round-89 lesson ## Gate (corpus/lessons/round-89.md:18) lists admissions; no reject row located for the ScribeR89 non-admission.
- Drafted check: none

### 72. R89-D5
- Current status: no ledger row (seed; opened 89, class `mistake-9-counter-pin`, source `corpus/lessons/round-89-verifier-spotcheck.md:114`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **closed** (`R89-D5-R90`)
- Drafted evidence or blocker: Closed by the R90-C2 external pin ledger (plans/counter-pins-r90.json at 664435cf; checker rc 0 at HEAD). Residual disclosed by C2 itself: one commit that rewrites the pin ledger can still move the pins.
- Drafted check: `cd "$LANE" && grep -qs '163f284316141a831484dacb7f69ad4cbbaadfb3' plans/counter-pins-r90.json`

### 73. R89-D6
- Current status: no ledger row (seed; opened 89, class `scorecard-c2-limitation`, source `corpus/lessons/round-89-verifier-spotcheck.md:115`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-D6-R90`)
- Drafted evidence or blocker: Not landed: SCORECARD.md:4169 (R89-C2 row) carries no limitation on the record-table pin; 'pins the claim population at commit B' is not in SCORECARD.md. The correction row is owed (this round).
- Drafted check: none

### 74. R89-A2-1
- Current status: no ledger row (seed; opened 89, class `pin-by-ancestry-and-blob`, source `corpus/lessons/round-89.md:116`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-1-R90`)
- Drafted evidence or blocker: Partially landed: byte and blob pins landed at 664435cf (checker PINS 7/7; record-table blob matched). Ancestry of the pins to the freeze commit is not in the C2 predicate (bytes and blob only); not closed.
- Drafted check: none

### 75. R89-A2-2
- Current status: no ledger row (seed; opened 89, class `c2-after-figures`, source `corpus/lessons/round-89.md:117`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-2-R90`)
- Drafted evidence or blocker: Not landed: no after-figure check located; the ids=8 to ids=9 case at plans/round-85-claims.md:106 not re-tested.
- Drafted check: none

### 76. R89-A2-3
- Current status: no ledger row (seed; opened 89, class `surviving-mutants`, source `corpus/lessons/round-89.md:118`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-3-R90`)
- Drafted evidence or blocker: Not evidenced: C1 M1-M5, M7 and C2 N1, N4, N6 kill status not re-measured; .ufo/waves/round-89/w1/MutTesterR89/mutants.md not re-run.
- Drafted check: none

### 77. R89-A2-4
- Current status: no ledger row (seed; opened 89, class `frozen-text-corrections`, source `corpus/lessons/round-89.md:119`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-4-R90`)
- Drafted evidence or blocker: Partially recorded: LOG.md:3405 lists the frozen-text defects as Mistake 10 (not repaired; operator rules). Correction entries are owed (R89-D2, R89-D6).
- Drafted check: none

### 78. R89-A2-5
- Current status: no ledger row (seed; opened 89, class `sentinel-L1-L6`, source `corpus/lessons/round-89.md:120`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-5-R90`)
- Drafted evidence or blocker: Not evidenced: SentinelR89 hostile-case items (120 s stall, empty or '.' paths, prior counters run from the working tree not BASE blobs) not re-tested in this pass.
- Drafted check: none

### 79. R89-A2-6
- Current status: no ledger row (seed; opened 89, class `host-userns-in-receipt`, source `corpus/lessons/round-89.md:121`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-6-R90`)
- Drafted evidence or blocker: Not verified in this pass whether the probe receipt records user.max_user_namespaces.
- Drafted check: none

### 80. R89-A2-7
- Current status: no ledger row (seed; opened 89, class `scout-candidate-set`, source `corpus/lessons/round-89.md:122`)
- Ran: grep/ls/git on the cited surface (batches 4-7 and the section dumps in receipts/)
- Observed: seed text: see drafted evidence below
- Drafted status: **open** (`R89-A2-7-R90`)
- Drafted evidence or blocker: Routed candidate list (24 unexecuted members, .ufo/waves/round-89/w1/ScoutR89/next.md), not a defect. Round 90 executed one candidate (merge-diff-arc-agi-task). L1 to decide whether this is a finding at all.
- Drafted check: none


## Instrument notes (frozen or lane-owned; reported, not repaired)

- **I1 - unconditional DEFECT for a superseded malformed row** (`plans/round90_burndown.py` `evaluate`, lines 255-257 append it regardless of supersede; line 330 `passed` requires no defects). Reproduced in `receipts/fixture-malformed-superseded.txt`. Consequence: R90-C3's "exit 0" branch is unreachable under the append-only rule.
- **I2 - checks run in the lane working tree, not at `--rev`.** `run_check` uses `cwd=lane_root` and a fixed env (`PATH`, `HOME`, `LANE`). R82-V8's check (`plans/round83_c2_checks.py:166-171`) resolves the fleet root as `origin.parent`. In the lane it prints `CHECK v8 ok` (rc 0); in a clone under scratch it prints `CHECK v8 fail` (rc 1). The gate's verdict therefore depends on where the checkout lives. Not a lane DEFECT at HEAD (the lane-run gate lists three DEFECT lines, none for R82-V8).
- **I3 - `checks_run` double-counts a superseded closed finding.** One loop visits base and resolution rows (`evaluate` lines 295-304); both run the same check. Baseline clone at HEAD: 98. With 6 closed supersedes: 109 = 98 + (5 x 2 + 1). Seeds add 8 closed checks: 117.
- **I4 - R42-R2's original check is defective.** `routed_open.py --list` prints no `ROW R42-R2.x` lines. Not repaired; the drafted supersede uses the landed artifacts.
- **I5 - R51-R2's check is mis-scoped.** `../*-shokunin/corpus/routed-findings.jsonl` expands to this lane's own ledger only.
- **I6 - selftest gap.** The seven gate selftest cases do not cover a malformed row superseded by a closed resolution, which is the case I1 breaks.
- **I7 - check-pass is not close evidence, and the gate cannot tell.** R45-S5-7c and R42-R3-09 pass because the defect is present; R51-R3 and R51-R4 pass because the state is still absent; R82-F1's check passes because the parser is blind. Any closed row citing these checks would be fabrication-class. Recommend the L1 keep close evidence to the routed artifact, not the check.
- **I8 - frozen prose figure.** Claims text: "27 findings opened rounds 39-82". Measured: 33. Recorded, not repaired.

## What was not verified (limits)

- Seed rows drafted as **open** mean: no closure evidence was located in this pass. They do not prove absence of a landed fix. Not exhaustively audited: R85-V1..V7, R86-V1/V2 beyond the grep, R87-V5/V6, R88-2/3, R84-V8/V9, R89-A2-2..A2-6.
- R51 rows are host-state dependent; re-measured on 2026-11-05 only. `systemctl --user` was unavailable (no DBUS session) so the qwen-coder unit state rests on PROVINCE.md and the :34113 probe.
- The two judgment closes (R42-R3-33, R42-R3-37) are flagged in their rows; the L1 may reject them and leave them open.
- Not re-run: the C1 counter, the C2 checker beyond a single HEAD run, and any lane instrument (out of seat scope).

## Suggested checks for the main agent after the L1 integrates

1. `python3 plans/round90_burndown.py --lane . --rev <tip> --work <w> --freeze-round 90` and `--selftest` (selftest 7/7 today).
2. Run the gate from a clean clone so checks do not read the lane working tree (I2).
3. Expect `freeze=refused` until R51-R1..R4 and R82-F1 change status; expect DEFECT line 125 regardless (I1).

## Installs, host changes, cleanup

- Installs or upgrades: none. Tools used: python3, git, sh, curl. No pacman, no sysctl, no host service change, no write outside the wave dir and scratch.
- Scratch: clones `lane`, `base`, `fx.*`, work dirs under `/fast/scratch/hyaku/kengaku-r90/ExecC3Triage`; receipts copied into `receipts/` before removal; scratch removed at seat end (`rm -rf` on the scratch root).
- Fixture commits (`6786c924`, `41d93f45`, `8ba6bada`, fixture repo) exist only in scratch, never in the lane.
