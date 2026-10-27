# R44CritSeparability — separability critic report

Round 44 (hyaku run 9), wave item R44CritSeparability. Claims frozen at `plans/round-44-claims.md` (freeze
5f16ed0; first probe run 45dc0bc). Question: does each counter pass with the other's work wholly absent and fail
without its own? Any shared input?

## Method

1. Read both counters in full (`plans/round44_c1_verify.py` 939 lines, `plans/round44_c2_verify.py` 554 lines)
   and inventoried every file each reads (code reading).
2. Grepped each counter for tokens of the other's world (C1 for `corpus|feal|probe|pkg|grader|SOURCES|
   PROVINCE|readme|knowledge|receipt|.ufo|witness-run`; C2 for `battery|anchor_digest|w_*|witness|MUTANTS|
   round44_c1`).
3. Empirical, both directions, all runs inside the round-44 envelope:
   - R1/R2: C1 on a clone **with** the C2 package vs a clone with the C2 package deleted (entry, captures,
     receipt, dry table, spec, gate, probe).
   - R3: C2 on a pristine clone (battery44 absent).
   - R4: C2 on a clone with a planted `plans/battery44/` module (untracked).
   - R5: C2 on a clone with a planted generic untracked file (control for R4).

## What C1 reads (code inventory)

- `plans/anchor_digest_check.py`, `plans/order_check.py` — lanes, digest-pinned (`TOOLS`/`PINS`, lines 126-133;
  read at `main()` line 799).
- `plans/battery44/*.py` (or `--battery-dir`) — `BATTERY_REL` line 125; `build_battery` line 707.
- Its own file (slices Ctx/load/build_module_child, `builder_source()` line 431).
- `WR = ".ufo/waves/round-44/claims/witness-run.txt"` (line 146) appears ONLY inside MUTANTS label strings — never
  opened (no read/open call on it).
- Everything else is built from nothing inside bwrap: fixtures' repos are created by `ctx.init`/`ctx.git` inside
  the empty fixture dir; tools run with the lane and `plans/` hidden (`Runner.hidden`, line 611).
- No read of: corpus/knowledge, captures, receipt, dry table, pkg-spec-r44.json, pkg_gate.py, feal probe,
  SOURCES, README, PROVINCE, claims.md, `.ufo/` files. (grep confirms: only docstring/label text.)

## What C2 reads (code inventory)

- `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/` captures + SHA256SUMS (`CAP`/`CAPTURES`, v1, v10,
  v11).
- `plans/pkg-spec-r44.json`, `plans/pkg_gate.py` (pinned, executed: v2), `plans/feal_linear_probe.py` (pinned,
  executed: v5), `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt` (pinned: v5).
- `plans/order_check.py` (executed: v8), `plans/round-44-claims.md` (passed as `--claims` to order_check: v8).
- `corpus/SOURCES.md` (v3, v6 census), `PROVINCE.md` + README (v9), spec's `entry` (the C2 knowledge entry), spec's
  `receipt`.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`CENSUS`, v6).
- No reference anywhere to `plans/battery44`, the anchor tool, the C1 counter, or witness modules (grep: only the
  string `anchor_digest` as a v3 defect label).

## Shared inputs

- **`plans/order_check.py`** — the only file read/executed by both counters (C1: pinned tool under test; C2:
  v8 execution). It is a frozen tool, not a work product of either counter.
- `plans/round-44-claims.md` — C2 only (via order_check). Not read by C1.
- The lane repo itself — both counters take `--lane`, but over disjoint subtrees; C1 never touches the lane's git
  state (its git calls are inside fixture dirs or bounded by ceiling inside scratch).
- Environment-level: C2's v2 gate runs `pkg_gate.py package --require-clean-tree`, whose P9 (`c_clean_tree`,
  pkg_gate.py:259-265) flags **any untracked file** via `git ls-files --others`. So uncommitted battery44 modules
  would make C2's V2 DEFECT while the wave is in flight — a generic worktree-cleanliness channel, not a content
  read, inert at the landing measurement (clean clone of committed tip).

## Empirical results (all runs enveloped; PATH-dir digest unchanged in every run)

### R1/R2 — C1 with vs without the C2 package

Battery: freeze witness `claims/witness/w_u.py` (documented control: witness-as-battery → C1 pass in dev mode;
used because `plans/battery44` does not exist yet in the lane — checked `git ls-files` and glob: absent).

R1 (clone A, C2 package present):
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/env1 /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/env1 --bind /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/env1/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/laneA --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/witness --work /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/w1
ENVELOPE start 20:34:06 cwd=/home/vgpnk/Projects/shokunin
...
ENVELOPE end 20:34:09 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

R2 (clone B, C2 package deleted: `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`,
`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/`, `feal-linear-probe.txt`,
`feal-linear-dry-cases-freeze.txt`, `plans/pkg-spec-r44.json`, `plans/pkg_gate.py`,
`plans/feal_linear_probe.py`):
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/env2 /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/env2 --bind /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/env2/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/laneB --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/witness --work /fast/scratch/hyaku/kengaku-r44/R44CritSeparability/w2
ENVELOPE start 20:34:11 cwd=/home/vgpnk/Projects/shokunin
...
ENVELOPE end 20:34:15 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Counter output (all lines except the ENVELOPE header/start/end) is **byte-identical** (`diff` clean). Both exit
0. Key lines (identical in both):
```
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=4/4 order=1/1
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```
Receipts: `c1-full-laneA.txt` sha256 `87a60dd07e20e1f651970e4f47b89d9aa6a7cd640a5c273ab951405b47b52c1d` (2651 B);
`c1-nopkg-laneB.txt` sha256 `42390b4813da16a3f8ee8e1d2ab51106093aad290a5b501e370bf047bfdeb0cf` (2651 B).
C1 is independent of the whole C2 package. C1 fails without its own work: freeze control
`claims/control-c1-nothing.txt` (`BATTERY fixtures=0`, `killed=0 survived=5`, PREDICATE fail).

### R3/R4/R5 — C2 without battery44, with battery44 planted, with generic untracked file

All three exit 1, `PREDICATE C2 fail`, `checks=11 defects=7`. Verdict lines identical:

```
V1 ok listed=11 bad=0 extra=0
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=9 bad=['S138:row', ..., 'S146:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
V8 ok order_exit=0 result=PASS
V9 DEFECT receipt, entry, PROVINCE.md or README absent
V10 DEFECT receipt or entry absent
V11 DEFECT entry absent
checks=11 defects=7
PREDICATE C2 fail
```

Every defect traces to C2's own package: the knowledge entry (`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`,
spec `entry`) does not exist yet and SOURCES lacks rows S138-S146 (v3). V4/V7/V9/V10/V11 short-circuit on the
missing entry; V2 is the gate rejecting for the same reason (entry absent + SOURCES rows absent). Receipt and
captures are present and pass (V1, V5, V6, V8).

The ONLY difference between R3, R4 and R5 is inside the V2 gate's P9 clean-tree line:

- R3 pristine: `P9 ok untracked=0 first=0`, `gate: defects=5`
- R4 battery44 planted: `P9 DEFECT untracked=1 first=plans/battery44/sep-placeholder.py`, `gate: defects=6`
- R5 generic untracked file planted: `P9 DEFECT untracked=1 first=untracked-probe.txt`, `gate: defects=6`

So planting `plans/battery44/` changes C2 exactly as planting any unrelated untracked file does — through the
generic `git ls-files --others` cleanliness gate (pkg_gate.py:259-265), not through any read of battery44 content.
At the landing measurement (clean clone of the committed tip) this channel is inert. C2 fails without its own
package (7 defects) regardless of battery44 presence.

Receipts: `c2-pristine-laneC.txt` sha256 `8c9773bd3b78416133ccec77e989660eaa8cefd94bb9c044a879a2e0ca816ed8`
(1787 B); `c2-battery44-planted-laneD.txt` sha256 `e79a65d60bdbfc3a14475df2bcf3ffae40cd3feabce9c8b2b4c2cd69c8a4fcf5`
(1824 B); `c2-untracked-file-laneE.txt` sha256 `b026b8184ec4cf1ade9453808dfb33a0b16c8142a6d646daba1fdf0960ecdbe4`
(1809 B).

## Findings

1. **C1 passes with C2's work wholly absent** — empirically byte-identical 5/5 kill output with and without the
   C2 package; code reading shows C1 reads nothing of C2's world.
2. **C1 fails without its own work** — no battery44 ⇒ fixtures=0, 5 survivors (freeze control).
3. **C2 fails without its own work** — entry + SOURCES rows absent ⇒ 7 defects (verified now).
4. **C2 is content-insensitive to battery44** — the only observable effect of planting battery44 is the generic
   P9 untracked-file gate, reproduced by an unrelated untracked file; not a read of battery44.
5. **Shared inputs: exactly one file — `plans/order_check.py`** (frozen tool, read/run by both; not a work
   product of either counter). Plus the environment-level worktree-cleanliness gate (inert at measurement).

## VERDICT: separable-yes-shared-inputs-1
