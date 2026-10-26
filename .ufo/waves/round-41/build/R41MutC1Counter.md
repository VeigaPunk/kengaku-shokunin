# R41MutC1Counter — mutation-testing the round-41 C1 counter itself

Seat: mutation-tester, kengaku round 41 wave 1 (2026-10-26). Scratch `/fast/scratch/hyaku/kengaku-r41/R41MutC1Counter` (removed at end). Receipts in `.ufo/waves/round-41/build/R41MutC1Counter/`.

## Method

Every committed control was **reproduced in my clone, then re-run 15 more times with one single-line mutant of the counter** in place of the pristine counter. A control *catches* a counter mutant iff the run's stdout+exit no longer reproduces that control's receipt. `⚑` = the control's verdict/exit flips; otherwise the catch is a pinned-line difference only.

- Counter under test: `plans/round41_c1_verify.py`, sha256 `8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8` (== `claims/frozen-digests.txt:2`).
- Mutants: `KM01`–`KM15`, each replacing exactly one unique source substring (count asserted = 1; generator + hashes: `R41MutC1Counter/mutant-hashes.txt`).
- Envelope for **every** counter run (per orchestrator rule):
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 <counter> --lane <lane> --work $S/w` (the counter adds its own nested sandboxes; nothing outside scratch was written).
- Controls reproduced (control → lane/battery → invocation): nothing → pristine clone, no `plans/battery41`; no-mutants → clone + witness copy in `plans/battery41` + counter patched by the committed ed-script (`233a234`); witness-as-battery → clone + `claims/witness/{w_receipts,w_sources}.py` in `plans/battery41`; tool-edited → witness clone + one appended line in `plans/tip_receipts.py`; hostile → **the real lane** with `--battery-dir` on a copy of `claims/hostile` (the committed receipt's `lane_read=FileNotFoundError` is only reproducible when the hidden lane is the real lane the hostile module names; reproduced byte-identically that way).

**Fidelity (pristine counter vs committed receipts):** all five byte-identical — `diff claims/control-c1-<c>.txt out/<c>__pristine.out` → empty for nothing / no-mutants / witness-as-battery / tool-edited, and for hostile after the lane fix (`repro-*-pristine.txt`). Do-nothing exit 1, no-mutants exit 1, witness exit 0, tool-edited exit 1, hostile exit 1 — all as committed.

## Table: counter mutants vs committed controls

| Mutant | Guard (counter line) | `old -> new` | caught-by (lines, ⚑=verdict flip) | Verdict |
|---|---|---|---|---|
| KM01 | `exhibits` pair branch (:440) | `mut[0] == b` → `mut[0] == a` | witness-as-battery (28, ⚑ 0→1); tool-edited (24) | **caught** |
| KM02 | `exhibits` rc-silence (:442) | `ref[0] == 1` → `ref[0] == 0` | witness-as-battery (12, ⚑) | **caught** |
| KM03 | `exhibits` rc-mirror (:444) | `ref[0] == 0` → `ref[0] == 1` | witness-as-battery (14, ⚑); hostile (6: T13 killed→SURVIVED) | **caught** |
| KM04 | `exhibits` error (:446) | `in (0, 1)` → `in (2,)` | witness-as-battery (16, ⚑) | **caught** |
| KM05 | `exhibits` silence (:449) | `cls not in mut[1]` → `cls in mut[1]` | witness-as-battery (16, ⚑) | **caught** |
| KM06 | `path_ok` traversal (:351) | `return ".." not in tok` → `return True` | — none — | **survived** → D1 |
| KM07 | `WORK_TOKEN` (:115) | `^\{WORK` → `^\{work` (tokens never match) | witness-as-battery (34, ⚑); tool-edited (14); hostile (10) | **caught** |
| KM08 | floors sum (:640) | `sum(FLOORS) == TOTAL` → `>=` | — none — | **survived** (equivalent, see D3) |
| KM09 | `fingerprint` content digest (:344) | `content = sha256(...)` → `content = ""` | — none — | **survived** → D5 |
| KM10 | sidechannel scan (:473) | `if hits:` → `if False:` | hostile (3: `SIDECHANNEL` line + `sidechannel=1→0`; exit stays 1) | **caught** (line-level) |
| KM11 | build type check (:309) | drop `not isinstance(argv, list)` | — none — | **survived** → D6 |
| KM12 | `PINS-AFTER` (:634) | `!= dig` → `== dig` | witness-as-battery (6, ⚑ 0→1); nothing (2); hostile (2). tool-edited blind: `mismatched=1` unchanged | **caught** |
| KM13 | `good` drops `not after` (:642) | remove `not after and` | — none — | **survived** → D4 |
| KM14 | null run (:575) | `if res != ref[...]` → `if False:` | — none — | **survived** → D7 |
| KM15 | `TOTAL = 23` (:123) | → `TOTAL = 24` | witness-as-battery (4, ⚑ 0→1) | **caught** |

Per-cell evidence (changed-line counts + first changed line + rc pairs): `R41MutC1Counter/matrix-catch-digest.txt`; command: `diff out/<control>__pristine.out out/<control>__<KM>.out` over the 60 matrix runs (15 mutants × 4 non-patched controls; the no-mutants control is itself a patched counter and was run once, byte-identical).

**Score: 9 of 15 mutants are caught by at least one committed control; 6 survive.** At strict verdict/exit granularity: 8/15 (KM10's only catch is the hostile receipt's `SIDECHANNEL`/`sidechannel` lines; the hostile control still exits 1 through its 22 survivors, so its *exit* does not depend on the scan).

## Surviving guards — one drafted extra control each (receipts in `R41MutC1Counter/`)

- **KM06 `path_ok` → D1 `d1_path_escape.py`**: battery fixture whose argv carries `--work {WORK}/../esc`. Pristine: `SETUP ... breaks the contract`, exit 2. Under KM06: token accepted, run completes, exit 1 (`D1__pristine.txt`, `D1__KM06.txt`) — **catches**.
- **KM09 fingerprint digest → D5 concurrent writer**: a process outside the counter appends nothing but flips one byte (same size) of `fx/w_receipts/f000/lane/README.md` once `variants/` exists. Pristine: `TAMPERED w-t02-no-evidence ...`, `tampered=1`, fail, exit 1. Under KM09: `tampered=0`, pass, exit 0 (`D5__pristine.txt`, `D5__KM09.txt`) — **catches**. This is the real multi-tenant-host threat; no in-sandbox battery can reach it (fixture dirs are read-only during tool runs), so the committed set *cannot* contain it.
- **KM11 build type check → D6 `d6_tuple.py`**: `build()` returns `()`. Pristine: child `TypeError`, SETUP refusal, exit 2. Under KM11: empty tuple accepted, exit 1 (`D6__pristine.txt`, `D6__KM11.txt`) — **catches**.
- **KM13 `good` without `not after` → D4 concurrent writer**: mid-run append to the clone's `plans/tip_receipts.py` during an otherwise-green witness run (the round-40 `~/.local/bin` shim scenario, one lane over). Pristine: `PINS-AFTER mismatched=1`, `PREDICATE C1 fail`, exit 1. Under KM13: `PINS-AFTER mismatched=1` printed but ignored, `PREDICATE C1 pass`, exit 0 (`D4__pristine.txt`, `D4__KM13.txt`) — **catches**; the append-only copy was restored (`cmp` with the pristine clone → identical).
- **KM14 null run → D7 `d7_nulldet.py`**: ten receipts fixtures whose probe passes/fails at random, so the second unmodified run differs. Pristine: 5 × `NULL ... differs on a second unmodified run`, `null_detected=5`. Under KM14: `null_detected=0`, no NULL lines (`D7__pristine.txt`, `D7__KM14.txt`) — **catches at pinned-line level**; exit stays 1 in both because the random fixtures also set `wrong=10`, an overlap inherent to the guard (only genuine nondeterminism triggers it).
- **KM08 floors sum → D3, equivalence proof instead of a control**: whenever `good`'s other conjuncts hold, `killed == TOTAL`, `per_tool[t] == [FLOORS[t], FLOORS[t]]` for both tools, and the per-tool kills sum to `killed`, so `sum(FLOORS.values()) == TOTAL` is already implied; `== ⇒ >=` makes KM08 unable to flip any verdict, and `floors_ok` is used nowhere else. Demonstrated: a swapped-FLOORS counter (`{"receipts": 10, "sources": 13}`) fails identically with and without KM08 — receipts byte-identical (`D3__floorswap-pristine.txt`, `D3__floorswap-KM08.txt`). Per the freeze kill rule this is reported as a limit (a redundant, equivalent guard), not relabelled.

## Findings beyond the table

1. **The green control carries the counter.** Five of the nine catches (and every verdict flip) come from `control-c1-witness-as-battery` alone: it is the only committed control that expects exit 0, so it is the only one that detects guard mutations that create false negatives. The four fail-expecting controls only detect false positives, and KM12 shows they are partially blind even to those (tool-edited's `PINS-AFTER mismatched=1` is invariant under inversion).
2. **Line-level vs verdict-level.** KM10 and the non-witness catches of KM03/KM07/KM12 change pinned receipt lines without flipping any exit. If admission compares only `PREDICATE`/exit, the committed set catches 8/15; comparing full receipts (what the receipts pin) catches 9/15. Either way the six survivors need the drafted controls above.
3. **Host-write guards are only exercisable from outside.** KM09/KM13 survived because nothing inside the counter's own sandbox can write a fixture tree or a pinned tool; the drafted D4/D5 use a concurrent out-of-band writer, which is exactly the incident class round 40 recorded (`R40CritC1Counter`'s `~/.local/bin` shim).
4. **Mid-session lane change absorbed.** The L1 landed 7 `plans/battery41` modules (48 fixtures) into the lane while this probe ran. All committed-control reproductions had been cloned from the pre-landing tip, so the matrix is unaffected; the hostile control, re-run on the landed lane, stayed byte-identical to the committed receipt — first stability evidence for that control across a battery landing.

## Restoration evidence

- Lane tools/counter unchanged: `sha256sum` on the real lane after all runs — `round41_c1_verify.py` `8835a94b…`, `tip_receipts.py` `e4f49714…`, `sources_adopt.py` `38492bf1…` (== `claims/frozen-digests.txt`); all mutated counters were scratch copies under `$S/counters/`.
- `lane_w/plans/tip_receipts.py` restored after D4 (`cmp` with pristine clone → identical); no git/jj command was ever run against the real lane; nothing outside `build/R41MutC1Counter/` and scratch was written; scratch removed (`rm -rf -- /fast/scratch/hyaku/kengaku-r41/R41MutC1Counter`).
- No tool installs were needed (bwrap, python3, git, coreutils only).

VERDICT: c1-counter-mutants-caught-9/15
