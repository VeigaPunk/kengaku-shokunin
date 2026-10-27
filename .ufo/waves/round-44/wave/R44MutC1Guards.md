# R44MutC1Guards — mutation test of the round-44 C1 counter (`plans/round44_c1_verify.py`)

Seat: R44MutC1Guards (leaf, no subagents). Round 44 wave, 2026-10-26.
Target: the round-43 mutation set (M01–M15, single-line mutants of the C1 counter's guards,
`R43MutC1Counter` table) re-run against the round-44 counter `plans/round44_c1_verify.py`
(guards carried from round 43 plus the new F1–F6 fences), with the committed round-44 controls
(`.ufo/waves/round-44/claims/c1_controls.sh`: control-c1-*.txt receipts, hostile f1–f6, witness
`witness/w_u.py`). The frozen lane file was never modified: every mutant is a scratch copy
(`/fast/scratch/hyaku/kengaku-r44/R44MutC1Guards/mut/<id>.py`), digest recorded per run.

## Method

- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane`;
  `git -C $S/lane rev-parse --show-toplevel` = `$S/lane`; clone HEAD `5e3d3aa06c6b7000929ac3e62563a39159c4501f`.
  Counter digest in the clone `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad` =
  `claims/frozen-digests.txt` line for `plans/round44_c1_verify.py`; both tools match their PINS
  (`11bb2cad…`, `948d5e1d…`). So the clone's counter/tools are byte-identical to the frozen ones.
- Mutants: `rig/gen_mutants.py` applies round-43's M01–M15 at the same guards, translated to the
  round-44 counter text (`old -> new` asserted unique, every copy `py_compile`-clean; sha256 in
  `mut/SHA256SUMS` — recreating below). Counts: 15 mutants, single replacement each.
- Detector = the committed round-44 control set, reproduced by `rig/driver.sh` (each control on its
  own fresh mirror of the counter copy, mirroring `c1_controls.sh` semantics):
  witness, do-nothing, standing batteries (battery42+battery43 as battery44), witness-as-battery,
  no-mutants, span={1} (leg f), SITE_EQUAL→True (leg g), tool-edited, direction mislabel,
  hostile f1–f6 (round-44 half only; the round-43 counter half never runs the mutated counter).
  Every control invocation runs inside `claims/envelope.sh` (lines pasted below); outputs land in
  `$S/out-<mutant>/<control>.txt`.
- Compare (`rig/compare.sh`): per control, diff the normalized mutant output against the normalized
  pristine baseline (ENVELOPE/DIFF lines and scratch-dir/fixture-root random names stripped).
  Caught = ≥1 committed control's observable output changes. Survived = no control changes. The
  `value` control for M01 is inconclusive by construction (its patch anchor IS the mutated line; the
  patch assert fails — same as round 43).
- Baseline validation: the pristine base run reproduces every committed receipt — `witness`,
  `nothing`, `standing`, `wab`, `nomut`, `span`, `value`, `edited`, `mislabel` MATCH; the hostile
  f1–f6 runs reproduce the receipts' round-44 halves exactly (same SETUP refusal category and
  message, modified only by scratch-dir naming: e.g. f2 `--lane rev-parse --show-toplevel=… is
  outside the fixture`, f4 `--lane git hung`, f6 `SIDECHANNEL … tokens=inspect` + `--lane
  rev-parse --show-toplevel=…`).
- Environment note: the landing tip now carries `plans/battery44/` (10 modules, L1 battery seats).
  The committed `nothing` receipt was produced when no battery44 existed. The driver therefore runs
  `nothing` against a clean mirror lane (no battery44), preserving the control's semantics
  (fixtures=0). All other controls pass an explicit battery dir or their own mirror, so the lane's
  battery44 does not enter any measurement.

## Mutants (id | guard | old -> new)

| id | guard (round-44 line) | mutant |
|---|---|---|
| M01 | L153 `SITE_EQUAL` | `return tuple(mut_sites) == tuple(ref_sites)` → `return True` |
| M02 | L882 reference trace 1 | the traced reference run → `r_sites = 0, frozenset(), frozenset(), ()` (run dropped) |
| M03 | L883 reference trace 2 | `r_sites2 = runner.run(...)` → `r_sites2 = r_sites` (stability self-comparison) |
| M04 | L852 newline-count validity | `or old.count("\n") != new.count("\n") \` → `or False \` |
| M05 | L533 `symlink_breach` | `if p.is_symlink() and not p.resolve().is_relative_to(d):` → `if False:` |
| M06 | L568 `order_argv_breach` blob branch | `if got[0] == 0 and got[1] != "blob":` → `if False:` |
| M07 | L514 `repo_breach` toplevel branch | `ok = p == repo if what.endswith("toplevel") else …` → `ok = True if …` (toplevel check vacuous) |
| M08 | L521 `repo_breach` worktree branch | `if val:` → `if False:` |
| M09 | L694 `exhibits` silence conjunct | drop `cls in set(fx["defects"])` |
| M10 | L927 floors sum | `sum(FLOORS.values()) == TOTAL` → `True` |
| M11 | L902 unattributed accounting | `unattributed += 1` → `survived += 1` |
| M12 | L383 fingerprint content term | `content = file_sha256(p)` → `content = ""` |
| M13 | L719 sidechannel scan | `if hits:` → `if False:` |
| M14 | L921 PINS-AFTER | `after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]` → `after = []` |
| M15 | L837 null run | `if res != ref[fx["fid"]]:` → `if False:` |

## Results

Caught = ≥1 committed round-44 control's output changes vs the pristine baseline (scratch names
normalised). "Inconclusive" = the control's own patch anchor is the mutated line (M01 vs `value`).

| id | guard | verdict | caught by (observed change) |
|---|---|---|---|
| M01 | SITE_EQUAL (L153) | **caught** | `witness`/`wab`/`edited`: all kills → `UNATTRIBUTED … last=site-record-equal`, `killed=5→0`; `value` inconclusive (patch anchor is this line) |
| M02 | reference trace 1 (L882) | **caught** | `witness`/`wab`/`edited`/`value`: kills → `UNATTRIBUTED … last=site-record-unstable` (empty first record vs real second record) |
| M03 | reference trace 2 (L883) | **survived** | no control changes (records stable; see draft d03) |
| M04 | newline-count validity (L852) | **survived** | no control changes (no table row has unequal newline counts; see draft d04) |
| M05 | `symlink_breach` (L533) | **survived** | no control changes — no round-44 control carries a symlink fixture (round-43's h5 is not in the round-44 control set; see draft d05) |
| M06 | `order_argv_breach` blob branch (L568) | **survived** | no control changes — the round-44 controls either use blob paths or are refused earlier by the argv-shape leg (F3); no control reaches the blob branch with a directory-at-HEAD substitute (see draft d06) |
| M07 | `repo_breach` toplevel branch (L514) | **survived** | no control changes — the round-44 hostile refusals for f1/f2/f4/f6 come from `lane_breach` (which runs before `repo_breach`); `repo_breach`'s toplevel branch is never reached (see draft d08 note) |
| M08 | `repo_breach` worktree branch (L521) | **survived** | no control changes — same reason: `repo_breach`'s `if val:` branch unreached (see draft d08) |
| M09 | `exhibits` defects conjunct (L694) | **survived** | no control changes — every committed fixture declares exactly the classes it observes, so dropping the conjunct changes no hit/attribution (see draft d09) |
| M10 | floors sum (L927) | **survived (equivalent-in-context)** | no control changes — within `good`, `sum(FLOORS.values()) == TOTAL` is implied by `per_tool==[FLOORS,FLOORS]` ∧ `len(MUTANTS)==TOTAL`; no control can isolate the term (see draft d10) |
| M11 | `unattributed += 1` (L902) | **caught** | `span`/`value`: `unattributed=5` → `survived=5 unattributed=0` |
| M12 | fingerprint content term (L383) | **survived** | no control changes — no committed control produces a fixture-tree content change between the two fingerprints (fixture dirs are read-only during every tool run; see draft d12) |
| M13 | sidechannel scan (L719) | **caught** | `f6`: the `SIDECHANNEL hb-…/f6_above.py tokens=inspect` line disappears (the committed f6 module carries `inspect` in its docstring) |
| M14 | PINS-AFTER (L921) | **caught** | `edited`: `PINS-AFTER mismatched=1` → `mismatched=0` |
| M15 | null run (L837) | **survived** | no committed control produces a null second-unmodified-run difference (tools deterministic; see draft d15) |

Tally: **caught 5 / survived 10** (survivors: M03 M04 M05 M06 M07 M08 M09 M10 M12 M15).
No mutant produced a false pass of a should-fail control other than through the recorded lines; no
control regressed to accepting an escape vector (f1–f6 still refuse under every mutant).

Round-43 comparison: the round-43 set caught M01 M02 M05 M06 M07 M11 M13 M14 (8/15). Under the
round-44 control set M05, M06 and M07 are no longer covered (the round-43 h5/h6/h4 controls are
gone; f1–f6 exercise `lane_breach`/F3/F5 before `repo_breach`'s branch checks), and M13 is still
caught — now by f6's sidechannel token. Draft red controls for the ten survivors below.

## Draft controls for the surviving guards (this seat's report dir only; not frozen)

All demonstrated on the seat scratch (receipts copied to `R44MutC1Guards/receipts/`):

- **d03 — reference-trace stability** (`receipts/d03-*.txt`): the stability check needs a reference
  whose traced site record differs between two runs. Attempted vector: outer `PYTHONHASHSEED`
  variation (0/1/7) — measured NEGATIVE: pristine and M03 print `killed=5` under every outer seed
  (the counter pins `PYTHONHASHSEED=0` inside every tool run; no traced span line of either pinned
  tool holds a hash-order-sensitive local). With these two tools the double trace is always stable;
  the guard is defense-in-depth. A future control would need a third tool (or tracer-visible
  nondeterminism) — named as a limit, not a defect.
- **d04 — newline-count validity** (`receipts/d04-*.txt`): a counter copy whose `MUTANTS` table
  gains row `XNL1` (one-line `old`, two-line semantics-swapping `new`). Pristine
  counter: `MUTANT XNL1 … invalid`, `invalid=1`, exit 1. M04 counter: `MUTANT XNL1 … killed
  by=u5-sixty-three-hex attributed=L522 value=differs`, `killed=1`, exit 0. The check is
  demonstrably load-bearing.
- **d05 — symlink breach** (`receipts/d05-*.txt`): fixture `d5-symlink-outside` — a committed repo
  whose working tree holds a symlink resolving outside d. Pristine counter: `SETUP … escapes its
  directory: symlink repo/corpus/link-out -> …` (exit 2). M05 counter: `FIXTURE
  d5-symlink-outside … ok` (accepted).
- **d06 — order argv blob branch** (`receipts/d06-*.txt`): fixture `d6-receipt-is-directory` — an
  order fixture whose `--receipt` names a DIRECTORY at HEAD. Pristine counter: `SETUP … escapes its
  directory: --receipt corpus/evidence/round7/x is a tree at HEAD, not a blob` (exit 2). M06
  counter: fixture admitted (`FIXTURE d6-receipt-is-directory … WRONG`: the tool exits 1, not the
  declared 2 — the branch is off regardless).
- **d08 — `repo_breach` worktree branch** (`receipts/d08-*.txt`): no committed round-44 control
  reaches the branch (the f-refusals fire in `lane_breach`/F3/F5 first). Hostile fixture
  `d8-bare-worktree`: `.git/config` carries `core.bare=true` + `core.worktree=<outside host>`;
  measured (seat scratch): `git rev-parse --show-toplevel` fails rc=128 while
  `git config --get core.worktree` returns the outside path — the ONLY reachable worktree-branch-only
  state. Pristine counter: `SETUP … escapes its directory: repo/core.worktree=…` (exit 2). M08
  counter: `FIXTURE d8-bare-worktree … ok`. (Incidental: the module's source contains `core.`, so
  both runs also print `SIDECHANNEL … tokens=core.`, `sidechannel=1` — a separate token-scan
  exercise.) For the toplevel branch alone, a fixture whose repo is inside d but whose
  `--lane`-adopted repo has a worktree above d is refused by `lane_breach` before `repo_breach`;
  a control would need the repo walk to see `rev-parse --show-toplevel` resolve outside while
  `lane_breach` stays silent (not constructible with the round-44 breach order — named as a limit).
- **d09 — `exhibits` defects conjunct** (`receipts/d09-*.txt`): anchor fixture `d9-underdeclared`
  (row with a 63-hex anchor token; fixture declares `defects: []`, so the counter marks it WRONG).
  Pristine `--only U5`: `MUTANT U5 … SURVIVED exhibits=none`. M09 counter: `MUTANT U5 … killed
  by=d9-underdeclared` — a kill on a class the fixture never declared.
- **d10 — floors sum term (redundancy demo, M10 equivalent-in-context)** (`receipts/d10-*.txt`):
  `FLOORS` patched to `{"anchor": 6, "order": 4}` (sum 10 ≠ TOTAL 5). Pristine AND M10 counters
  both print `PREDICATE C1 fail` — the `per_tool==[FLOORS,FLOORS]` term fails whenever the sum term
  would, so no control can isolate `sum(FLOORS.values()) == TOTAL`; within `good` it is implied by
  `per_tool==[FLOORS,FLOORS]` ∧ `len(MUTANTS)==TOTAL`. The term is redundant defense; its mutant is
  equivalent-in-context, reported as a limit, not a defect.
- **d12 — fingerprint content term** (`receipts/d12-*.txt`): counter patched so a content-only
  rewrite (byte reversal of each fixture's `lane/corpus/SOURCES.md`, same length/size/mode) happens
  between the two fingerprints. Pristine: `TAMPERED u3-row-path-binds fixture tree changed during
  the run` ×5, `tampered=5`, exit 1. M12 counter: `tampered=0`, exit 0. (The order fixture
  `u14c` carries no SOURCES.md, so 5 of 6 fixtures change.)
- **d15 — null run** (`receipts/d15-*.txt`): counter patched so the second "unmodified" copy is
  actually U5-mutated. Pristine: `NULL u5-sixty-three-hex differs on a second unmodified run`,
  `null_detected=1`, exit 1. M15 counter: no NULL line, `null_detected=0`, exit 0.

## Envelope lines (QUALITY Q32)

Every measurement ran inside `claims/envelope.sh`; every run below shows
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` — no `INVALID`
measurement, no re-run needed. Representative lines (paths abbreviated, `<COUNTER>` = counter copy
under test, `<LANE>` = clone lane):

```
# baseline witness (pristine counter, clone lane, witness battery)
ENVELOPE start 20:41:56 cwd=/fast/scratch/hyaku/kengaku-r44/R44MutC1Guards
ENVELOPE end 20:42:00 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
# f4 (pristine): exit=2 after the 30 s hang, same digest pair, unchanged
# every mutant control run: same digest pair, unchanged (none invalidated)
```

Full `ENVELOPE <argv>` lines are in each receipt file (out-<V>/<control>.txt and drafts/out/*).

## Receipts (copied into `wave/R44MutC1Guards/receipts/`)

- `base/` — pristine baseline, all 15 controls.
- `<mutant>-<control>.txt` — decisive control output per caught mutant (M01/M02 witness; M11 span;
  M13 f6; M14 edited).
- `drafts/` — every draft run (d03 d04 d05 d06 d08 d09 d10 d12 d15) with the draft fixture modules.
- `rig/` — `gen_mutants.py`, `driver.sh`, `compare.sh`, `drafts.sh`, `mut/SHA256SUMS` (rerunnable).
- Mutant counter copies and per-mutant full control sets stay in scratch (`$S/mut/`, `$S/out-*`)
  and are deleted with the scratch at cleanup; the rig regenerates them.

## Limits

- "Caught" is output-level: a control whose text changes counts; no control regressed to accepting
  an escape vector. M07/M08 are not merely uncovered but unreachable under the round-44 committed
  controls (f-refusals fire in `lane_breach` first) — draft d08 documents the reachable worktree
  state; the toplevel branch alone has no constructible control (named as a limit).
- M10 is equivalent-in-context (proved above), not merely uncovered — reported as a limit per the
  round's own equivalence rule.
- M03's stability check has no constructible trigger with the two pinned tools (measured negative
  under outer seed variation); the draft is a spec plus the negative measurement.
- The round-44 control set no longer covers M05/M06/M07 (covered in round 43 by h4/h5/h6, which
  are not part of the round-44 committed set): the drafts d05/d06/d08 are red controls for them.
- The `nothing` control had to be run against a clean mirror because the landing tip now contains
  `plans/battery44/`; the committed receipt predates that (disclosed in Method).

VERDICT: c1-guards-caught-5/15
