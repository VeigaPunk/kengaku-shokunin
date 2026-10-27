# R44RoutedPlan — routed rows review (critic, round 44 wave)

Seat: `R44RoutedPlan` (critic, leaf; no subagents). Date 2026-10-26. Lane clone at
`/fast/scratch/hyaku/kengaku-r44/R44RoutedPlan/lane` (HEAD `5e3d3aa06c6b7000929ac3e62563a39159c4501f`,
2026-10-26 20:27:30 -0300, "round-44: v2 wave spec + validated dispatch (68 seats)"); toplevel asserted =
`$S/lane`. Nothing in the lane was written; the two prescribed checks ran inside the round-44 envelope
(`claims/envelope.sh`, Q32), `local_bin_content_before=after=328be01808ba022f unchanged`.

Target rows (ledger `corpus/routed-findings.jsonl`): R42-R3-33..37 (`.ufo/waves/round-42/falsify/F42CritPlanNext.md`
D1–D5), R40-R1, R40-R5 (`corpus/lessons/round-40-verifier-spotcheck.md` §5), R39-R4
(`corpus/lessons/round-39-verifier-spotcheck.md:136`). All are judged at the lane tip against the round-43/44 frozen
claims (`plans/round-43-claims.md`, `plans/round-44-claims.md`), the round-44 claims controls
(`.ufo/waves/round-44/claims/`), and the round-44 counter source (`plans/round44_c1_verify.py`).

## Verdict table

| row | class | verdict | check command (re-run to decide closure) |
|---|---|---|---|
| R42-R3-33 | plan-mutant-numerator | **satisfied** (superseded by an explicit, bounded list) | `grep -n 'MUTANTS total=5 killed=5' .ufo/waves/round-44/claims/witness-run.txt` |
| R42-R3-34 | plan-missing-restore-control | **still open** | `grep -c "rc-mirror', 'direct'," .ufo/waves/round-44/claims/c1_controls.sh` → 1 |
| R42-R3-35 | plan-missing-refusals | **still open** (partial: legs h/i + F1–F6 landed; X13 + token-scan residual) | `ls .ufo/waves/round-44/claims/hostile/` (f1–f6 only) |
| R42-R3-36 | plan-class-from-unfrozen-probe | **still open** (overclaim resolved; prior-art receipt unfiled) | `ls corpus/evidence/round43/ | grep -q 'prior-art'` → fails |
| R42-R3-37 | plan-host-dependent-cheat | **superseded** (clock-seed cheat off the claim surface) | `grep -n 'cheat-clock-seed' plans/round-44-claims.md` → no output |
| R40-R1 | c1-counter-soundness | **satisfied** (F1–F4 all in the round-42+ counter; R40-R1.1 closed) | `grep -nE -- '--unshare-ipc|--tmpfs /run|--ro-bind-data|def path_ok' plans/round44_c1_verify.py` |
| R40-R5 | carried-residuals-bundle | **still open** (4 of 5 items; W04 census line now verified) | `git log --format=%h --follow -- plans/order_check.py` → 34158b0 only |
| R39-R4 | carried-residuals-bundle | **still open** ((a)/(d)/(e); (b)/(c)/(f) closed) | `python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py` → SETUP, exit 2 |

## Per-row findings

### R42-R3-33 (F42CritPlanNext D1) — SATISFIED
Defect: the round-43 plan's calibration numerator "20 rc-witnessed survivors (R41PlanNext §2.4)" was unbound (≤9
directional; 9 unwitnessed; L164/L181 rc-equivalent). At the tip neither the round-43 nor the round-44 freeze uses
that list. Round-43 froze 9 near-variants and disclosed "9 witnessed of 20" (`plans/round-43-claims.md:78-79`).
Round-44 froze 5 named mutants with directions re-derived before freeze through the counter
(`plans/round-44-claims.md:27-41`): `claims/witness-run.txt` prints `MUTANTS total=5 killed=5 survived=0
invalid=0 null_detected=0 unattributed=0`, every kill `value=differs`. The remaining `u = 18` rows and the "17
reachable `round_close.py` survivors (§A.3)" are carried as named limits — "a third tool the counter does not
mutate" (`plans/round-44-claims.md:66-69`) — never as mutation mutants; `R43PlanNext` §A.3 tallies exactly 17
"R" survivors. The D1 harm (freezing unwitnessed mutants as calibration) is gone; the present list is id-bound.
The stale "20 rc-witnessed" sentence survives only in historical records (`SCORECARD.md:1791` round-43 planned
block; `F42CritPlanNext.md:56-67`), not in any live freeze.
Check: `grep -n 'MUTANTS total=5 killed=5' .ufo/waves/round-44/claims/witness-run.txt`.

### R42-R3-34 (F42CritPlanNext D2) — STILL OPEN
D2 demanded per-mutant restore controls for the `u=18` branch (a hostile module replaying a carried direction cell
that must turn the predicate red). Round-44 still has exactly one: U7 relabelled `rc-mirror` → `rc-silence`
(`.ufo/waves/round-44/claims/control-c1-direction-mislabel.txt`: `MUTANT U7 anchor rc-silence SURVIVED
exhibits=0>1,rc-mirror`; `c1_controls.sh` patch #9 is the only such patch). U5/U6/U9/U14c have no per-mutant
restore control; `plans/round-44-claims.md:40-41` names only this one control. The freeze's witness battery
(`witness/w_u.py`) demonstrates reachability for all five, but the D2 red non-vacuity control per mutant is not
present. Never claimed closed in the ledger note; still true at tip.
Check: `grep -c "rc-mirror', 'direct'," .ufo/waves/round-44/claims/c1_controls.sh` → 1.

### R42-R3-35 (F42CritPlanNext D3) — STILL OPEN (partial)
Round-43 landed leg h (symlink escape refusal) and leg i (order argv blobs: "an order fixture is refused unless
its `--claims` and `--receipt` each name a BLOB at HEAD" — `plans/round44_c1_verify.py:58-60`, covering the
XO1/XO3 substitute shapes) plus R1–R4 pins with hostile controls h1–h6, and round-44 added fences F1–F6 each with
a red hostile module (`.ufo/waves/round-44/claims/hostile/`: f1_gitfile, f2_deep, f3_abbrev, f4_fifo,
f5_alternates, f6_above; each open under the round-43 counter `exit=1` and refused by SETUP under round 44
`exit=2`, e.g. f1 `--lane rev-parse --absolute-git-dir=… is outside the fixture`, f6 `--lane rev-parse
--show-toplevel=… is outside the fixture`). Residuals named in D3 remain: the X13 staged-manifest shape (anchor)
has no red control — the anchor tool still accepts `--evidence-ref index` (`plans/anchor_digest_check.py:570`,
choices `head|index`) and F3's anchor argv shape allows it, so the round-42 X13 vector remains expressible — and
the token scan stays a heuristic ("the token scan is a heuristic, so non-author review of battery44 stays part of
admission", `plans/round44_c1_verify.py:105-107`; `plans/round-44-claims.md:66`).
Check: `ls .ufo/waves/round-44/claims/hostile/` (f1–f6 only; no X13 control).

### R42-R3-36 (F42CritPlanNext D4) — STILL OPEN (residual)
The overclaim half is resolved: the round-43/44 class sentences carry no novelty assertion — "The class sentence
carries no novelty claim (prior art: wave item)" (`plans/round-44-claims.md:104`); probe (`plans/feal_linear_probe.py`),
dry table and receipt are frozen (`corpus/evidence/round44/feal-linear-dry-cases-freeze.txt`,
`feal-linear-probe.txt`). The dated prior-art receipt is still unfiled: the ledger's own check
`ls corpus/evidence/round43/ | grep -q 'prior-art'` fails (round43 evidence = `feal-dry-cases-freeze.txt`,
`feal-probe.txt`, `tb2-feal-differential-cryptanalysis/` only; round44 likewise has none), and the pinned image is
still never pulled ("the image is never pulled", `plans/round-44-claims.md:101`). The wave item stands.
Check: `ls corpus/evidence/round43/ | grep -q 'prior-art'` (fails).	 in the envelope: `PRIOR-ART-ABSENT`.

### R42-R3-37 (F42CritPlanNext D5) — SUPERSEDED
The host-RNG cheat `cheat-clock-seed` (libc srand/rand) is off the whole claim surface at the tip. Round-43's
probe already disclosed it as a host fact ("`cheat-clock-seed` is a host fact (`host=libc-rand`, `F42CritPlanNext`
D5)", `plans/round-43-claims.md:100-101`) and no claim relied on it. Round-44's C2 is a different task
(feal-linear-cryptanalysis) whose receipt cases are RNG-independent (public gen.py keys, public hash-chain replay,
constants copy, decoys — `corpus/evidence/round44/feal-linear-probe.txt`); nothing in the round-44 freeze asserts a
host-drawn 5/5. The host stand-in itself remains an explicitly named limit ("host python3/gcc stand in for the
image's python 3.13 (`uvx`) and Debian gcc; the image is never pulled", `plans/round-44-claims.md:100-101`). The
D5 residual (re-derivation in `alexgshaw/feal-differential-cryptanalysis:20251031`, image never pulled) has no
claim depending on it.
Check: `grep -n 'cheat-clock-seed' plans/round-44-claims.md` → no output.

### R40-R1 (c1-counter-soundness) — SATISFIED
The four R41SentinelCounter fences rout to the round-42 counter are all in the current counter: F1 (mutant variant
readable from inside a tool run) → "variant bound by fd and the store hidden" (`plans/round44_c1_verify.py:36-37`,
`--ro-bind-data <fd> <slot>` at :356); F2 (AF_UNIX) → `--tmpfs /run` + `--unshare-net` (:342-343); F3 (SysV
IPC) → `--unshare-ipc` (:343); F4 (relative argv escape) → "relative argv tokens resolved against the fixture
dir" (:37) via `path_ok` (:388-399) plus `GIT_CEILING_DIRECTORIES` (F6, :26). The ledger already records the
closure: `R40-R1.1` status=closed "round-42 counter freezes all five F41C1Hardened repairs plus attribution:
plans/round42_c1_verify.py:20-30, code :311 (--ro-bind-data fd), :302 (--unshare-ipc, --tmpfs /run), :343
(path_ok), :504 (relative-token contract), :635 (unattributed)". Rounds 43/44 carry these unchanged.
Check: `grep -nE -- '--unshare-ipc|--tmpfs /run|--ro-bind-data|def path_ok' plans/round44_c1_verify.py`.

### R40-R5 (carried-residuals-bundle) — STILL OPEN
Items at tip:
- W04 census line (D3): **now verified** — round-41 census prints the W04 count: `claims/census-before.txt` and
  `integrate/census-after.txt` each print 15 `W04` rows (round-41 lesson: "Report census lines print the W04
  count (D3). Instruction to the L1's report", `corpus/lessons/round-41.md:94`).
- order class: still blocked (separate row R39-R3; `corpus/defects.jsonl` pinned).
- F39LedgerTip D1 (clone-mode rows that cannot fail): still carried — named through round-42 lessons
  (`corpus/lessons/round-42.md:170-172`: not even named in the round-42 claims), absent from rounds 43/44 claims.
- F39MutDirection (R39-R4, below): open; prescribed check still exits 2.
- F39OrderGateMut fail-open: `plans/order_check.py` unedited since `34158b0` (`git log --format=%h --follow --
  plans/order_check.py` → one commit); round-44 pins it unchanged (`948d5e1d…`, `plans/round-44-claims.md:29-30`).
- `round40_c2_verify.py --work` traceback: fixed (`plans/round41_c2_verify.py:286,290` creates `--work`).
Check: `git log --format=%h --follow -- plans/order_check.py` → `34158b0` only.

### R39-R4 (carried-residuals-bundle) — STILL OPEN
Per the ledger note: closed at tip are (b) Q30 wired (`plans/round_close.py:14` runs `order_check.py`), (c)
`tip_receipts.py` derives the round-39 receipt, (f) C1 soundness repairs landed (`plans/round41_c1_verify.py`,
carried through rounds 42–44). Still open at tip: (a) `plans/order_check.py` unedited since `34158b0`, fail-open
mid-scan (same evidence as R40-R5); (d) `F39LedgerTip` D1 carried; (e) the row's prescribed check still refuses
any non-round-38 list: `python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py` →
`SETUP counter plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,…`, exit 2
(run in the envelope below).
Check: `python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py` → SETUP, exit 2.

## Envelope receipt (Q32) for the two prescribed checks

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44RoutedPlan/env /fast/scratch/hyaku/kengaku-r44/R44RoutedPlan/env --bind /fast/scratch/hyaku/kengaku-r44/R44RoutedPlan/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash -c ls corpus/evidence/round43/ | grep -q "prior-art" && echo PRIOR-ART-PRESENT || echo PRIOR-ART-ABSENT; python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py; echo "rc=$?"
ENVELOPE start 20:36:42 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedPlan/lane
PRIOR-ART-ABSENT
SETUP counter plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,attributed non_6_tuple_rows=7; this check reads the round-38 MUTANTS rows (id, clause, dir, adv, old, new) and its battery38 loader only
rc=2
ENVELOPE end 20:36:43 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

VERDICT: plan-rows-closable-3-of-8
