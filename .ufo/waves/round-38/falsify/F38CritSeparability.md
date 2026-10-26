# F38CritSeparability — C1/C2 separability attack (round 38, wave 2)

Tip under attack: `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. Scope: the frozen `## Separability` paragraph of
`plans/round-38-claims.md` (freeze `e0a37853`) — "Each predicate must still hold for the untouched claim."
Receipts: `.ufo/waves/round-38/falsify/F38CritSeparability/` (+ `SHA256SUMS.txt`). Scratch: `/fast/scratch/hyaku/kengaku-r38/F38CritSeparability`, deleted.

## 0. Method — five clean clones, tip verified before any write

```
S=/fast/scratch/hyaku/kengaku-r38/F38CritSeparability; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/laneX" \
  && git -C "$S/laneX" checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
git -C "$S/laneX" rev-parse --show-toplevel ; git -C "$S/laneX" rev-parse HEAD
→ /fast/scratch/hyaku/kengaku-r38/F38CritSeparability/laneX
  8c7422d7a646515d80af44844e8ecc8a1fc1d30a            (all five clones, laneA–laneE)
```

| clone | mutation | run |
|---|---|---|
| laneA | C2's package reverted (entry, S115/S116, README lines, receipt) | C1 |
| laneB | `rm -rf plans/battery38` | C2 |
| laneC | whole C2 work product deleted **and** battery38 deleted (control cross-check) | C1 |
| laneD | inconsistent revert (entry deleted, README index row kept) | C1 |
| laneE | whole C2 work product deleted, battery38 kept | C1 |

Baseline (untouched clone, laneA before mutation):
`python3 plans/round38_c1_verify.py --lane .` → `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`,
`MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`, `PREDICATE C1 fail`, `SURVIVED` = N21.
`python3 plans/round38_c2_verify.py --lane .` → `checks=7 defects=0`, `PREDICATE C2 pass`.
Baseline receipt sha256 = `5ec311a0842bfa31…` (C1) and `b2dff081efd0aa92…` (C2).

Baseline fidelity: my tip run is byte-equal to the landing receipt block
(`sed -n '4,115p' .ufo/waves/round-38/integrate/measure-final.txt` vs `base-c1.txt` → no diff, `MY-TIP-RUN-EQUALS-RECEIPT-BLOCK`).
Note that receipt was measured at `d93b7d6`, one commit before the attacked tip; between the two,
`git diff --stat d93b7d6 8c7422d7 -- plans/ corpus/ README.md SKILL.md` = `corpus/lessons/round-38.md | 77 ++++++` only, so
the receipt does carry to the tip (and my run re-measures the actual tip).

## 1. C2 with `plans/battery38` removed — predicate holds, byte-identical

```
cd laneB && rm -rf plans/battery38 && git -C . ls-files --others --exclude-standard | wc -l   → 0
python3 plans/round38_c2_verify.py --lane .
→ V1 ok listed=5 bad=0 extra=0 ; gate P1…P10 all ok (P9 ok untracked=0; P10 ok probe_rerun=byte-equal bytes=5537)
→ V2 ok ; V3 ok rows=2 bad=0 ; V4 ok cases=22 mismatches_named=0/0 bad=0 ; V5 ok ; V6 ok
→ V7 ok rows=7 tags=7 bad=0 ; checks=7 defects=0 ; PREDICATE C2 pass ; rc=0
diff base-c2.txt c2-nobattery.txt → IDENTICAL  (both sha256 b2dff081efd0aa92…)
```

C2 is not merely "still passing": its 20-line output is byte-for-byte the baseline. Removing C1's 12 fixtures changes nothing C2 reads.

## 2. C1 with C2's package reverted — measured state preserved bit-for-bit

Revert applied in laneA: deleted `corpus/knowledge/tb2-build-pmars-grader.md`,
`corpus/evidence/round38/build-pmars-probe.txt`, `corpus/SOURCES.md` rows S115/S116, and in `corpus/README.md` the index
row line 71, coverage bullet line 263, frontier bullet lines 291–306 and evidence lines 450–451.
Post-state: `knowledge_files=44`, `untracked=0`, `git status --porcelain` = exactly `M corpus/README.md`,
`M corpus/SOURCES.md`, `D …build-pmars-probe.txt`, `D …tb2-build-pmars-grader.md`.

```
cd laneA && python3 plans/round38_c1_verify.py --lane .
→ PINS total=14 mismatched=0
→ BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
→ MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
→ PREDICATE C1 fail ; rc=1
diff base-c1.txt c1-noc2.txt → no output (all 112 lines equal; sha256 5ec311a0842bfa31…)
```

The full-clone revert only deletes `corpus/README.md`, `corpus/SOURCES.md`, `corpus/evidence/round38/build-pmars-probe.txt`,
`corpus/knowledge/tb2-build-pmars-grader.md` — the tree is dirty but `untracked=0` (the gate's P9 reads only untracked files, §4).

## 3. Stronger: *all* of C2's work product deleted — still identical

laneE deletes entry, S115/S116, the four README regions, receipt, `corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`,
`corpus/evidence/round38/tb2-build-pmars/` (5 files + manifest), `plans/pkg-spec-r38.json`, `plans/build_pmars_probe.py`,
`plans/round38_c2_verify.py`; battery38 (12 modules) kept.

```
python3 plans/round38_c1_verify.py --lane .  → PINS total=14 mismatched=0
  BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
  MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0 ; PREDICATE C1 fail
diff base-c1.txt c1-c2gone-batt38kept.txt → FULL-DIFF-EMPTY-vs-baseline (sha256 5ec311a0842bfa31…)
```

The 21 kills and the N21 survivor are properties of the gate + battery38 alone: they reproduce with C2's entry, rows,
receipt, captures, dry table, spec, probe and counter all absent.

Control cross-check (laneC = C2 gone **and** battery38 gone):

```
python3 plans/round38_c1_verify.py --lane . → BATTERY fixtures=64 wrong=0 … MUTANTS total=22 killed=0 survived=22
diff .ufo/waves/round-38/claims/control-c1-nothing.txt c1-fullc2-removed.txt  (time lines masked) → only the wrapper's "exit=1"
```

i.e. the no-work state still equals the freeze control, so C2's absence never even perturbs the control line.

## 4. Finding A — the `## Separability` read-set sentence is false as written

The frozen claim says "C1 reads only the gate, the round-35 spec, the round-36/37 counters and batteries and
`plans/battery38`" / "Neither counter reads the other's work product" (`plans/round-38-claims.md`, §Separability).
Every C1 fixture package is *built by copying the lane's corpus*:

`plans/round36_c1_verify.py:55-68`
```
def copy_package(lane, spec, dest):
    """Copy the genuine round-35 package bytes named by the spec into dest (same relative paths)."""
    rels = [spec["entry"], spec["receipt"], spec["sources"], spec["readme"], *spec["frozen_instruments"]]
    …
    for p in (lane / "corpus/knowledge").glob("*.md"): shutil.copy2(p, dest / "corpus/knowledge" / p.name)
    for p in (lane / "corpus/lessons").glob("*.md"):   shutil.copy2(p, dest / "corpus/lessons" / p.name)
```
reached through `plans/round37_c1_verify.py:198-204` (`ctx.genuine_package`), so C1 transitively reads
`corpus/SOURCES.md`, `corpus/README.md`, **every** `corpus/knowledge/*.md` (including C2's entry) and `corpus/lessons/round-38.md`.

That is not merely bookkeeping: gate P8 compares the knowledge-file set with the README index set
(`plans/pkg_gate.py:252-255`, `if files != indexed: bad.append(...)`), and every fixture inherits the copied corpus.

Counterexample (laneD) — delete only the entry file, keep C2's README index row (a one-sided C2 revert):
```
python3 plans/round38_c1_verify.py --lane .  (knowledge_files=44, index row still present)
→ BATTERY fixtures=86 wrong=51 renamed_disagree=0 sidechannel=0
→ MUTANTS total=22 killed=21 survived=1 invalid=0 … ; PREDICATE C1 fail   (sha256 15685cd3823fe55e…)
FIXTURE r36-P0 expect=accept declared=- observed_rc=1 observed_defects=P8 WRONG
FIXTURE p23-p2-receipt-deleted expect=reject declared=P2 observed_rc=1 observed_defects=P2,P8 WRONG
51/51 WRONG rows carry P8 in `observed_defects` (10×P6,P8  8×P5,P8  7×P7,P8  6×P4,P8  4×P8  4×P3,P8 …)
```

So C2-side editing changes C1's battery-validity line (`wrong=0` → `wrong=51`) and therefore C1's admission, while
leaving the mutant count untouched (21/1). The numbers I measured in §2–§3 are inert only because the revert was
*consistent* with the P8 invariant; the frozen sentence claims independence of the read set, which the code contradicts.

Direction: the coupling is **adversarial only** — no state was found in which C2's presence makes C1 pass easier
(contrapositive tested in §3: deleting everything of C2 leaves 21/1 unchanged). So this is a claim-text defect (fixable,
one sentence), not a laundering path.

## 5. Finding B — C2's predicate depends on the worktree's untracked state, including C1's artifacts

C2's V2 runs the gate with `--require-clean-tree` (`plans/round38_c2_verify.py:122-123`), and that clause is
untracked-only (`plans/pkg_gate.py:259-266`):
```
r = subprocess.run(["git", "-C", str(p.root), "ls-files", "--others", "--exclude-standard"], …)
left = [x for x in r.stdout.splitlines() if x]; return not left, f"untracked={len(left)} first=…"
```

Probe 1 — an untracked file under C1's dir (laneC, tipped tree otherwise pristine):
```
mkdir -p plans/battery38; echo 'FIXTURES = []' > plans/battery38/zz_untracked.py
python3 plans/round38_c2_verify.py --lane .   (untracked=1)
→ gate: P9 DEFECT untracked=1 first=plans/battery38/zz_untracked.py
→ V2 DEFECT spec=frozen gate=frozen gate_exit=1 ; checks=7 defects=1 ; PREDICATE C2 fail
```
Probe 2 — an untracked file *outside* battery38 (laneB, `plans/zz_untracked_sep.py`): same
`P9 DEFECT untracked=1`, `checks=7 defects=1`, `PREDICATE C2 fail`. So the sensitivity is to any uncommitted file,
C1's fixtures included — the freeze control shows the same mechanism (`control-c2-nothing.txt`: `P9 DEFECT untracked=11`).

At the attacked tip `untracked=0` and C2 passes; but "C1 can pass with C2 absent and vice versa" holds only while the
worktree is committed. An executor's uncommitted battery38 module reds C2 for a reason unrelated to the build-pmars grader.

## 6. Non-findings (tested, held)

- C1 reads none of `corpus/evidence/round38/*`, `plans/pkg-spec-r38.json`, `plans/build_pmars_probe.py`,
  `plans/round38_c2_verify.py` — proven by static literal scan of both counters and by the full-deletion run (§3).
- C1's 14 pins name no C2 file (`plans/pkg_gate.py`, `plans/round35/36/37…` only); deleting C2 leaves `mismatched=0` in every run.
- `plans/battery38/*.py` contains no path to any C2 artifact (`grep -rn "evidence/round38\|plans/build_pmars\|pkg-spec-r38" plans/battery38/` → no output), matching §1.
- The N21 survivor is stable in all three C1 states (baseline, literal revert, full C2 deletion): `survived=1`, the same `MUTANT N21 … SURVIVED` line. C2's presence neither supplies nor hides that kill.

## 7. Impacted axes and smallest safe correction

Axes: **calibration (C1)** — the claim overstates C1's read-set and hides a corpus-invariant dependency;
**coverage (C2)** — its admission is gated on a clean worktree, a condition on C1's commit hygiene. No measured
number changes; both are one-sentence corrections, below the bar for rejecting an admission.

Correction for the round-38 errata (the claims file is frozen at `e0a37853` and must not be edited in place):
1. Replace "C1 reads only …" with: C1's fixture packages copy the lane's `corpus/README.md`, `corpus/SOURCES.md`,
   every `corpus/knowledge/*.md` and `corpus/lessons/*.md`, so C1's battery validity also witnesses the gate's
   files==index invariant; an inconsistent landing of *any* knowledge entry reds C1's battery (`wrong>0`) though not
   its mutant count.
2. Add to C2's limits: V2 runs `--require-clean-tree`, which counts untracked files only, so C2 must be measured on a
   committed worktree; uncommitted executor output (e.g. a battery38 module) reds V2/P9.

## 8. No-harm

No lane file, index, jj state or fleet-root file was written; all writes are in the five scratch clones, the report
dir and the receipts dir. Scratch `/fast/scratch/hyaku/kengaku-r38/F38CritSeparability` removed after copying receipts.
No tool installed; no pacman transaction attempted.

VERDICT: separable-yes
