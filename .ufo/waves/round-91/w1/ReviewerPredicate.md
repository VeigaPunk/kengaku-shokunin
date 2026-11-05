# ReviewerPredicate — round-91 frozen claims and instruments, attacked (read-only)

Seat: ReviewerPredicate (leaf, no subagents). Lane: kengaku-shokunin @ master `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0` (confirmed via `scripts/hyaku/jj-lane.sh state` and `git rev-parse master`; local=remote, ahead=0 behind=0). All commands ran against a `git clone --shared` of the lane at `a8de3e69` in `$S/lane`, `S=/fast/scratch/hyaku/kengaku-r91/ReviewerPredicate` (removed on exit; no tree left on disk). No mutating git/jj command touched the lane; the only lane writes are this findings file.

Diagnostics note: no `lsp` device is mounted in this seat's tool inventory and no language server answered these paths; findings below rest on direct file reads at pinned revisions and on executed commands (grep only as literal fallback). Nothing below is semantic-index output.

Verdicts at the measured tip `a8de3e69`:

| Claim | Verdict | Measured command (exit) |
|---|---|---|
| R91-C1 | **UNMET** — instrument defect, not evidence (F1) | `python3 plans/round91_c1_replay.py --lane $S/lane --rev a8de3e69… --work $S/c1-tip` → exit 1 |
| R91-C2 | **PASS** as predicted, one frozen mispredict (F8) | `python3 plans/round91_counter_pin.py --lane $S/lane --rev a8de3e69… --work $S/c2-tip` → exit 0 |
| R91-C3 | **UNMET** — the move is absent from the tree (F2) + gate defects F3/F5/F6/F7 and false repair sentence F4 | `python3 plans/round91_burndown.py --lane $S/lane --rev a8de3e69… --work $S/c3-tip --freeze-round 92` → exit 1 |
| R91-F1 (companion) | **PASS** | `python3 plans/round91_f1_counter.py --lane $S/lane --work $S/f1` → exit 0 |

---

## F1 — CRITICAL — C1 counter fails at the measured tip on its own pinned probe's receipt format (predicate–implementation identity break)

Frozen predicate L5 (`plans/round-91-claims.md:53`): "**L5 every case's receipt-observed vector equals its frozen predicted vector**". Frozen predicate sentence (`:54`): "pass iff legs L1–L9 all pass at the measured revision, and the TARGET line prints `executed=1` only in that case".

Code implementing it: `plans/round91_c1_replay.py:82,86` —
```python
for token in line.split()[1:]:
    if "=" in token:
        key, _, value = token.partition("=")
...
cases.append((parts.get("id", "?"), parts.get("predicted", "?"), parts.get("observed", "?")))
```
The pinned probe writes the case id as a **bare positional token**, not `id=` (`plans/round91_modernize_probe.py:165-166`):
```python
rows.append("CASE %s predicted=%s observed=%s ok=%s %s"
            % (case["id"], case["predicted"], observed, ok, classes))
```
Receipt (`corpus/evidence/round91/modernize-probe.txt`, OBSERVATIONS block): `CASE full-pass predicted=PP observed=PP ok=True …` — the token `full-pass` carries no `=`, so `parts.get("id","?")` yields `"?"` for all ten cases.

Measured at tip:
```
$ python3 plans/round91_c1_replay.py --lane $S/lane --rev a8de3e69…33c8f0 --work $S/c1-tip   (exit 1)
TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10 legs=20 mismatches=10 defects=10
DEFECT L5 receipt names unknown case ?          (×10)
PREDICATE R91-C1 fail
```
Every observed vector equals its frozen predicted vector (`plans/round91-cases.json`: PP/FP/FP/FP/FP/PP/FP/EP/PF/FP — all ten agree with the receipt), L6's re-run over the extracted tree reproduced the receipt observation block with zero differences (no L6 defect), and L1/L2/L3/L4/L7/L8/L9 all pass — the sole failing leg is L5, failing on the id token. The counter gates a clause the frozen predicate never states (each receipt CASE line must carry an `id=` key=value token and jointly name exactly the table's case ids); structurally, this counter can never pass any receipt its own pinned probe emits. This is the round-90 M5 "predicate-implementation gap" class recurring inside the round whose Mistakes §2 claims to close it. Per the frozen kill rule ("any leg L1–L9 failing at the measured tip makes the claim unmet"), R91-C1 is unmet as measured; the defect is the instrument's parse, not the evidence.

The claims' After prediction (`:52`: `executed=1 … mismatches=0 defects=0` … exit 0) is falsified; the do-nothing BASE control matches its prediction exactly: `TARGET executed_rows=34 … executed=0 cases=0 legs=0 mismatches=0 defects=9`, `PREDICATE R91-C1 fail`, exit 1.

## F2 — CRITICAL — C3's triage/burn-down never landed: ledger byte-identical at BASE and tip, 30 old rows still open

`git diff --stat 59764383 a8de3e69 -- corpus/routed-findings.jsonl` prints nothing (213 lines at both; no round-91 rows exist — max `opened_round` is 89). The move's promised resolutions ("the 29 open seeds opened 83–87 and 89", claims `:117` region) are absent: measured at tip,
```
$ python3 plans/round91_burndown.py --lane $S/lane --rev a8de3e69… --work $S/c3-tip --freeze-round 92   (exit 1)
ROWS total=213 valid=212 invalid=1 superseded=34
freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3
PREDICATE R91-C3 fail
```
The frozen After (`:124`) predicts `freeze=admitted pending=<open rows opened in round 91 only> … resolutions>=35`; the tree holds 30 effectively-open rows opened 82–89 (the 29 seeds verbatim, plus `R82-F1-R90`) and 34 resolutions (all landed in round 90). The claims' BASE prediction also mispredicts two cells: `malformed_or_invalid_unresolved>=1` measures **0** (R82-F1's invalid prose source is already superseded by the round-90 row R82-F1-R90, so the r90 "PASS IS UNREACHABLE" fix clears it at BASE too), and `pending>=29` measures 30. BASE and TIP gate output is identical except F4's v8 defect. R91-C3 is unmet at the measured tip — an honest refusal, but the claim's central move is not in the tree.

## F3 — CRITICAL — C3's selftest clause is printed in the claims but never computed nor gated by the gate (r90 M5 class, unclosed in C3)

Claims After (`:124`) says the tip run prints `SELFTEST cases=9 red-green-ok=9`; the frozen predicate (`:125`) makes "the selftest battery green with every red case red for its named reason" a pass clause. The gate's default predicate path never runs it: `--selftest` is a separate early-return branch (`plans/round91_burndown.py:393,398-399`) and `passed` (`:304-306`) has no selftest term. Measured tip run: **no SELFTEST line printed** (see F2 output). The explicit flag run is green —
```
$ python3 plans/round91_burndown.py --work $S/st --selftest   (exit 0)
SELFTEST cases=13 red-green-ok=13
```
— and the counts disagree three ways: claims predict 9, the docstring says "Ten fixture ledgers" (`:311`), the battery has 13 cases. The C2 checker closed M5 for itself ("the selftest battery run in the same invocation", `round91_counter_pin.py:129-133` — verified in-path); the C3 gate did not.

## F4 — HIGH — R82-V8 repair sentence is false to the tree on both halves

Claims (`:117`): "`R82-V8`'s path-dependent check repaired (`plans/round83_c2_checks.py` derives the fleet root from the lane root's parent, **not `origin.parent`**; the resolution row's check **passes from a clone cwd**)". Measured:
- The file is byte-identical to its round-83 landing: `git diff ddb903a8 a8de3e69 -- plans/round83_c2_checks.py` is empty (and C2's pin at `0c61136d…` pins those unchanged bytes).
- `plans/round83_c2_checks.py:168` is literally `fleet=Path(os.environ.get('R83_FLEET_REPO',str(origin.parent))).resolve()` with `origin=Path(os.environ.get('R83_ORIGIN_REPO',str(ROOT))).resolve()` (`:167`, `ROOT = Path.cwd()` `:22`) — the derivation **is** `origin.parent`, the exact expression the sentence denies.
- `python3 plans/round83_c2_checks.py v8` from the clone cwd → `CHECK v8 fail`, exit 1; from the real lane cwd → `CHECK v8 ok`, exit 0. Corroborated inside the gate: the clone run defects `DEFECT check-failed R82-V8 rc=1 'CHECK v8 fail'`; the real-lane run (same revision, same ledger bytes) does not.

The check remains path-dependent in exactly the way the claim says was repaired; it passes only from the real lane (or with `R83_ORIGIN_REPO`/`R83_FLEET_REPO` exported, which the row's check command `python3 plans/round83_c2_checks.py v8` does not do).

## F5 — HIGH — the claims' After state is unreachable from the tip ledger: v2 gate retroactively defects round-90 rows

Measured (both clone and real-lane runs):
```
DEFECT override-unjustified R42-R2
DEFECT override-unjustified R42-R3-33
DEFECT override-unjustified R42-R3-37
```
The round-90 resolution rows carry override checks without `override_reason` (legal under the round-90 gate); the v2 gate now classifies any differing check on a superseding row as an override requiring a reason (`plans/round91_burndown.py:241-243`). Append-only (kill rule: "any edit to a pre-existing ledger row in place") means these three defects can only be cleared by new supersede rows — none exist — so `freeze=admitted` is unreachable from this ledger even if all 30 pending rows were resolved. The claims' After prediction (`:124`) and the claims' own "admitted" target are self-contradictory with the frozen override rule given this data.

## F6 — MEDIUM — C3 gate windows disagree with the frozen predicate sentence (latent identity break)

Predicate (`:125`): "no effectively-open finding opened **before round 91**" and "seeded rows with `opened_round` in **83–90**". Gate: refuse iff `oldest < freeze_round - 2` (`plans/round91_burndown.py:277`) = 90 at N=92, so an effectively-open row `opened_round=90` prints `freeze=admitted` while violating the predicate sentence; seeds count `83 ≤ opened_round ≤ freeze_round−1` = **91** (`:272,275`), so a round-91 row counts toward the gate's seed clause but not the predicate's 83–90; the printed field is `seeds_83_91` where the After line predicts `seeds_83_90>=46` (measured `seeds_83_91=46`: count matches, label does not). Latent today — no rows with `opened_round` 90 or 91 exist — but the gate's PREDICATE line can print `pass` contrary to the frozen sentence.

## F7 — MEDIUM — "every effectively-closed row's check exiting 0" is vacuous for closed rows without a check

`plans/round91_burndown.py:253-255`: `command = override_cmd or base_cmd; if not command: continue` — a closed finding with no `check` runs zero checks and raises nothing; "check passed" is indistinguishable from "no check exists". Seven closed base rows carry no check (R83-V1, R84-V1, R84-V5, R84-V6, R84-V7, R87-V2, R87-V4). Measured `checks_run=114` against the frozen prediction `checks_run>=117` (`:124`) — a mispredict partly caused by this silent skip.

## F8 — MEDIUM — C2: pass as predicted; frozen C-count mispredicts (6 predicted, 8 measured); unused RED_CASES

```
$ python3 plans/round91_counter_pin.py --lane $S/lane --rev a8de3e69… --work $S/c2-tip   (exit 0)
PIN-OK ×16 … PINS checked=16 matched=16 mismatched=0
SELFTEST cases=8 red-green-ok=8
PREDICATE R91-C2 pass
$ python3 plans/round91_counter_pin.py --lane $S/lane --rev 59764383… --work $S/c2-base   (exit 2)
DEFECT SETUP unreadable plans/counter-pins-r91.json
PREDICATE R91-C2 could-not-evaluate
```
K=16 matches the frozen 13+3 prediction exactly; the BASE control matches its prediction exactly (fail-closed, no awk zero, no substitute). But the After line (`:84`) predicts "C as 6 fixture cases" — measured C=8 (7 red + clean-green; hardcoded `selftest_cases = 8` at `plans/round91_counter_pin.py:130`; docstring "Eight fixture repos" `:185`). Per red case verified red **for its named reason** (child lines: rc and defect text both matched for counter-byte-mutated, path-absent, tampered-pin, blob-mutated, absent-pin-ledger rc=2, self-pin-mismatch, blob-anchor-missing; clean-green green). The self-pin leg is genuinely able to fail (case 7 plants a stale checker at the self path whose committed bytes match their own pin — the RUNNING checker then mismatches). Minor: `RED_CASES` (`:148`) is declared and never referenced — the named-reason list is not machine-connected to the battery.

## F9 — LOW — frozen-text factual errors (reported, not repaired, per the file's own rule)

- Claims `:35,38` cite `test_modernized_code_runs` at "lines 16–42" and `test_dependency_file_exists` at "lines 45–48"; the pinned bytes define them at lines **11** and **46** (`grep -n 'def test' corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py`). The round-91 lesson's Gate records the correct lines ("`def` at lines 11 and 46"), so the error is isolated to the claims file. No leg consumes line numbers (L2 pins the whole-file sha `0c24195f…`), so no claim verdict changes.
- Claims `:58`: "the ten cases yield three distinct predicted vectors (`PP`, `FP`, `PF`)" — the frozen table has **four** (`script-hangs` is `EP`, `plans/round91-cases.json`), contradicting the same Move paragraph's "a timeout class (E leg)". Count-unit error of the round-90 M3 class, in prose only.

## F10 — LOW — dead weight in the pinned instruments

`plans/round91_c1_replay.py:238-241`: inner `def host(...)` is never called (and its conditional expression would run each subprocess twice); `plans/round91_counter_pin.py:148`: `RED_CASES` unused (F8). Neither affects a verdict.

## F11 — INFO — item 6: `refused`/`blocked` absorption under the decided-state mapping

The mapping is implemented as frozen: `pending` = effective status `open` only (`:287` region); `blocked` parked and validated to carry non-empty `owner` **and** `blocker` (`validate`, `:117-119`); `refused` decided, validated to carry a non-empty `blocker`. Absorption is mechanically available by design: any effectively-open row (including all 30 still open) leaves the pending set via one supersede row with `status:"refused"` + any non-empty blocker string, or `blocked` + any non-empty owner string; neither is age-checked and the gate cannot verify a blocker's truthfulness — the kill rule's "false to the tree … fabrication-class defect" is enforceable only by review, not by the machine. No live violation exists in the tree (ledger byte-identical to BASE, F2). The adjacent age-window mismatch is F6.

## What holds (calibration evidence, not defect)

- **C2 end-to-end as predicted**: 16/16 pins (13 sha + 3 blob) match at tip including the checker's own running bytes; in-path selftest green; every red case red for its named reason; BASE exits 2 fail-closed. Blob anchors verified at abbreviated commits (`45171d23`, `cd0c116e`).
- **C1's evidence is sound despite F1**: L1–L4, L6–L9 all pass at tip; the L6 re-run of the pinned probe from the extracted tree reproduced the receipt observation block exactly; `legs=20` matches the frozen formula 10×2; BASE control exit 1 with fail-closed defects only.
- **R82-F1 closure is real**: `python3 plans/round91_f1_counter.py` (exit 0) — `PARSED S260=1,S261=2,S265=1,S266=2`; `ANCHORLINE rows=274 cited=84 … live=0` rc=0 over the real registry (was `cited=72 … live=0` blind before the repair); `WRONG-LINE-CAUGHT True` (the repair retains the true positive on a sha-bound fixture capture); `plans/anchor_line_check.py --selftest` 6/6 (rc=0).
- **Burndown selftest battery** (explicit flag): 13/13 red-green-ok, every case red/green for its named reason, including `override-with-reason-base-fails-admits` (base failure printed, not gated — as the claims state) and `seed-starved-refuses`.
