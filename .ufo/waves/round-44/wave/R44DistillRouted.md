# R44DistillRouted — routed-ledger dedupe (round 44, simplifier seat)

Seat `R44DistillRouted` (simplifier, leaf; no subagents). Date 2026-10-26. Read-only on the lane.
Lane clone `/fast/scratch/hyaku/kengaku-r44/R44DistillRouted/lane`, `git rev-parse --show-toplevel` = that path,
HEAD `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (2026-10-26 20:27:30 -0300). Every run below inside the round-44
envelope; **nothing in the lane was written** — the deliverable is this report, `groups.json` and two receipts in
`R44DistillRouted/`.

Envelope lines pasted (Q32):

```
ENVELOPE start 20:36:41 cwd=/fast/scratch/hyaku/kengaku-r44/R44DistillRouted/lane
ENVELOPE end 20:36:43 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 20:37:35 cwd=/fast/scratch/hyaku/kengaku-r44/R44DistillRouted/lane
ENVELOPE end 20:37:37 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Receipts: `R44DistillRouted/observe.txt` (sha256 `d931f451…b892`, 3 KB), `R44DistillRouted/probe_rc.sh`
(sha256 `f6cf9622…0be9`), `R44DistillRouted/groups.json` (machine-readable row→group map, sha256 `929227ed…`).

## 1. State read

```
python3 plans/routed_open.py --lane "$S/lane" --list   →  ROWS total=60 open=38 blocked=1 closed=21 refused=0
python3 plans/routed_open.py --lane "$S/lane" --observe →  OBSERVE rows=60 mismatched=0
```

Every one of the 38 open checks still fails at the tip, so no row is closable by its own check. The dedupe therefore
has to come from what each row *is*, not from a re-run. I read all 60 rows in full, then probed each open row's check
leg-by-leg and measured the three behaviours behind the executable rows (scratch_guard exit code, its selftest count,
`git_leak_probe.py --work` on an absent dir); those three measurements reproduce the rows exactly (exit 1, 36/36,
`FileNotFoundError` rc=1).

## 2. The dominant duplication: a check that pins a spelling the fix never used

15 of the 38 open rows (39 %) are not work at all. Their defect was repaired by a round-43 correction block
(`77ea425`), but the row's `check` string names the pre-correction phrasing or a bare line number instead of the span
the correction used, so `--observe` keeps them red. One ledger patch closes them — already drafted by the wave-1 seat
`R44RoutedObserve` (`.ufo/waves/round-44/wave/R44RoutedObserve/closures-patch.jsonl`, 15 rows; its patched observe
prints `open=23 blocked=1 closed=34 refused=2`).

| row | landed correction the check missed | what the check asked for |
|---|---|---|
| R42-R3-11, -12, -13, -15, -17 | `corpus/lessons/round-42.md` errata E2–E6 (`:169`, `:176`, `:182`, `:186`, `:189`) | the pre-errata sentence, verbatim |
| R42-R3-20, -23 | `corpus/QUALITY.md` C3 (`:847`) / C6 (`:865`) | `'development mode'` absent from a 69-line window it legitimately appears in |
| R42-R3-31 | `SCORECARD.md:1829` S1 ("counter that drives the gate's `uv` leg") | `'counter that invokes'` |
| R42-R3-38, -39, -40 | entry errata E1/E2/E3, spans `:296-298`, `:309-312`, `:430-432` | bare `:297`, `:311`, `:431` (0 hits each) |
| R40-R1, R42-R2 | closed children `R40-R1.1`, `R42-R2.1`, `R42-R2.2` | the parent row had no check / a stale one |
| R42-R3-14, -16 | **refused**: the row is wrong at the tip (`plans/round42_c2_verify.py:327` is the `("V7"…) ("V8"…) ("V9"…)` check list; `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile:8` is the comment, `:9`/`:10` the two `COPY` lines) | — |

Two facts worth stating separately, because they generalise: (a) a correction block is only as good as the check that
finds it — 11 of the 13 closures are a landed text block plus a check string that never got re-derived from the landed
bytes (the other 2 are row hygiene: a closed child already records the work); (b) the three entry rows would have been
green if the errata had printed the bare locator as well as the span, i.e. the cheapest repair is *both*: span in the
erratum, span in the check.

## 3. Nine groups over the 23 open rows (+1 blocked)

Ordered by fix size. `groups.json` holds the same map machine-readably. Each group is one artefact set; the "fix"
line is the whole job.

### G1 — land the rider patch set (4 rows) · high confidence · in flight
`R39-R2`, `R42-R3-26`, `R42-R3-27`, `R42-R6`.
All four are one tool contract each, already patched red→green:
`.ufo/waves/round-44/wave/R44RoutedRiders/red-green-receipt.txt` shows before `rc=1 Traceback`, after
`rc=2 SETUP --work … is not …`; `SELFTEST ok=36/36` → `37/37`; `landed-check.txt` re-runs the four ledger checks at
`rc=2 / rc=2 / grep_rc=0 / reported=37`, with the round-39 C2 gate green after the re-pin (`checks=7 defects=0`).
Fix: apply the four patches **plus** `01b` (the re-pin) and rewrite `SKILL.md:661-665` — that sentence still says
"`plans/git_leak_probe.py` … is not edited — create `--work` first", which the patch falsifies. Evidence for the
original defect, measured here: `git_leak_probe.py --work <absent>` → `rc=1` with `FileNotFoundError … absent/k39-glr-*`;
`scratch_guard.py check` on a `chmod 000` sentinel → `rc_direct=1` while the docstring promises 2 (`:17-18`).

### G2 — one carried-residuals register (3 rows) · high confidence
`R39-R4`, `R40-R5`, `R42-R5`.
The same defect written three times, once per round's spot-check: each carries the F39 triad (`F39LedgerTip` D1,
`F39MutDirection`, `F39OrderGateMut` fail-open) plus residuals, and each check points at one item
(`mutant_direction_check.py`, measured `exit 2 SETUP … missing=R37_REL,battery38_fixtures,attributed,FAMILY
non_6_tuple_rows=14`). Fix: **one register** — a section of `corpus/lessons/round-44.md` naming each residual by id,
owner and round — and one check that greps it; retire the three bundle rows. Two register items are code and must not
hide inside a bundle: `plans/mutant_direction_check.py:91-101` (refuses any non-round-38 list — one fix, teach it the
round-44 list) and `plans/order_check.py` fail-open (freeze-held, → G8).

### G3 — negative proof for the inherited a–c repairs (1 row) · medium confidence
`R42-R1` (the closed `R40-R1` points here). No red hostile control exists for repairs a (fd-bound variant),
b (`--unshare-ipc`), c (`--tmpfs /run`); the counter itself argues the vectors are unreachable because
"Both tools execute no fixture code" (`plans/round42_c1_verify.py:30-31`). Fix: one receipt that *proves* that claim
(enumerate every subprocess both tools can spawn) or carries a red module for whichever repair is reachable, and pin
the `uv` assumption (`:108` PATH keeps `/usr/local/bin`). A limit to test, not a regression — but one receipt, not
three rounds of carriage.

### G4 — one control set for the round-42 survivor calibration (2 rows) · medium confidence · partial
`R42-R3-34`, `R42-R3-35`. Round 44 already landed the fence controls (`claims/control-c1-hostile-f1..f6.txt`, each
`SETUP … escapes its directory` / `git hung`, `exit=2`), the `h` symlink and `i` argv-blob legs with their hostile
modules. What remains of both rows is one artefact: a per-mutant **restore control** (relabel a carried direction →
`SURVIVED exhibits=0>1`) and one red module for each substitute fixture shape (`b-xo1-receipt-is-directory`,
`b-xo3-emptied-directory`, `b-x13-staged-manifest`); the token-scan stays a named limit.

### G5 — close the two plan rows the round-44 freeze superseded (2 rows) · high confidence
`R42-R3-33`, `R42-R3-37`. Ledger-only. `R44RoutedPlan` judged 33 satisfied (round-44 froze 5 id-bound mutants,
`claims/witness-run.txt` `MUTANTS total=5 killed=5 survived=0`) and 37 superseded (no `cheat-clock-seed` on the round-44
claim surface). Fix: two check swaps + close evidence.

### G6 — land the two QUALITY draft tools with `--lane` (2 rows) · high confidence
`R42-R3-18`, `R42-R3-19`. Q33/Q34's Check lines name `plans/carried_direction_diff.py` and
`plans/sources_appendonly.py`; neither exists, and the drafts that would become them read the lane positionally
(`.ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py:13` `LANE = sys.argv[1] if len(sys.argv) > 1 else "."`),
so `--lane .` is taken as a path. Fix: land both with `--lane` accepted (one commit), or rewrite both Check lines to
the draft path — `corpus/QUALITY.md:829-844` (C1/C2) already states this as the owed fix.

### G7 — measured-true, misdescribed: one correction pass (6 rows) · high confidence
`R42-R3-02`, `-05`, `-06`, `-07`, `-09`, `-32`. Every one is a behaviour already measured, described one token
wrong; each replacement string is in hand, so it is one commit and six greps:

| row | site at the tip | edit |
|---|---|---|
| R42-R3-02 | `SKILL.md:600` (only `:178-184` hit) | add `plans/round42_c2_verify.py:238` for V7 (`return False, "receipt or entry absent"`) |
| R42-R3-05 | entry `:350` `test_outputs.py:26-52` | `:26-53` — `isqrt` ends `:53`, next `def` `:56` |
| R42-R3-06 | `corpus/README.md:75` `S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88)` | move S128 out: `S128 (OpenAgents issue #9645, tier B)` — `:272` already reads `(+ S128, tier B prior art)` |
| R42-R3-07 | `SKILL.md:699-700` "equal to the receipt row by row" | the triple comparison: `CASE_ROW` (`plans/round42_c2_verify.py:84`) captures id, letters, verdict only |
| R42-R3-09 | entry `:328` "…and pytest's cache" | drop the clause in an appended erratum (the fibsqrt probe never invokes pytest) |
| R42-R3-32 | `corpus/lessons/round-42.md:146` names `measure-final.txt`, never `:938` | append E8 naming `integrate/measure-final.txt:938` (`ENVELOPE end 17:52:40 … CHANGED`) |

Note the row's own locator is stale in two of these (`R42-R3-07` cites `SKILL.md:684-685`; the sentence is at `:699`)
— a dedupe pass that trusts the note's line number edits the wrong place.

### G8 — freeze-held repairs: schedule, do not code (2 rows) · high confidence
`R42-R3-08`, `R39-R3`. `plans/pkg_gate.py:276` still runs the probe under
`["uv","run","--no-project","--with","biopython==1.85","python3"]` while `plans/fibsqrt_probe.py` imports stdlib only;
`plans/pkg_gate.py` is pinned in the round-44 freeze again (it was frozen in round 43 for the same row), and
`corpus/defects.jsonl` is pinned by `plans/ledger_tip.py:6-7,72-73`. Both rows name the pin as the blocker, not owner
absence: the fix is a round in which the pinned file is editable, and until then the rows are correctly `blocked`.

### G9 — source-surface state reader and its first receipt (2 rows) · medium confidence · in flight
`R42-R3`, `R42-R3-36`. No `plans/*.py` reads a tier-B row's live state (`grep -rln 'pulls/|state=closed|merged='` →
no file), and `corpus/evidence/round43/` holds no prior-art receipt. Both asked for the same thing on the same surface:
a `plans/` tool that reads a PR/issue state, with its first dated receipt at
`corpus/evidence/round43/prior-art-feal-differential.txt`. Two artefacts, one commit; the row checks then differ only
in which of the two they grep.

## 4. Arithmetic

| axis | before | after the map |
|---|---|---|
| rows in ledger | 60 | 60 |
| open | 38 | 23 open + 1 blocked, in **9** groups |
| disposed by one existing patch | 0 | 15 (13 closed, 2 refused) |
| groups a fix must be written for | 38 rows ≈ 38 fixes | 9 fix-units |
| rows per fix-unit | 1.0 | 2.7 (24 rows / 9 groups), 3.0 over the seven multi-row groups (21 rows) |

Coverage check (`groups.json` vs the ledger, computed): `open covered True`, `missing []`,
`dupes []`, `blocked covered True`.

## 5. What I did not merge, and why

- **R42-R3-08 vs R42-R1** — both name `pkg_gate.py`'s `uv` leg, but one is a frozen-pin schedule item and the other a
  counter-repair proof receipt; one commit cannot close both. Kept apart (G8 vs G3).
- **The `order_check.py` fail-open residual** sits inside G2's register but its repair is freeze-held; folding it into
  G2's fix would let the register read closed while the tool is unchanged. Named in both places, fixed in G8's round.
- **G9 is the weakest merge** (two artefacts, one commit). If the L1 prefers one row per artefact, split it into
  `plans/source_state.py` and the prior-art receipt — no other group depends on the split.

## 6. Tradeoff

The map's gain is that 9 artefacts replace 23 rows of work and 15 rows vanish outright; the cost is that G2 and G4
each still hide a code change behind a register/control word (`mutant_direction_check.py`, the restore control). I kept
those visible rather than dissolving them, because a register that names a residual while the residual's tool is
unchanged is exactly the duplicate-authority pattern this seat exists to remove.

VERDICT: routed-groups-9-from-38
