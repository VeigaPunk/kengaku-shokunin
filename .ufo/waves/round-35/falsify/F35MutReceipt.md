# F35MutReceipt — mutation probe of the C1 receipt/probe/capture chain (round 35, wave 2)

Seat: F35MutReceipt (mutation-tester, leaf). Date: 2026-10-25.
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin at tip `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master).
Attacked invariant: the frozen C1 predicate — `python3 plans/round35_c1_verify.py --lane .` prints `checks=6 defects=0` / `PREDICATE C1 pass`, exit 0 — stays green only when the receipt, the probe, and the capture are genuine and mutually consistent.

**Answer to the tasking question: none of the four assigned mutants survive — 4/4 killed.** One adjacency mutant beyond the assignment (M5) survives and is reported as a coverage finding, not a contract change.

## Method

Fixture per the round recipe: `mktemp -d /tmp/k35f-XXXX`; `git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"`; `git -C "$D/lane" sparse-checkout set --no-cone corpus/SOURCES.md corpus/README.md "corpus/knowledge/**" "corpus/lessons/**" "corpus/evidence/round35/tb2-eval/**" corpus/evidence/round35/tb2-grader-probe.txt plans/round35_c1_verify.py plans/tb2_grader_probe.py`; `git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c`; `git -C "$D/lane" rev-parse --show-toplevel` verified equal to `$D/lane` before any write (TOPLEVEL-OK, both instances). No fixture commits were needed (working-tree mutations only, restored by `cp` from pristine copies); no git state mutation anywhere; the lane itself was only read, plus one authorized read-only counter run.

Pristine reference hashes (identical in both fixture instances — same commit bytes):

```
2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8  receipt.txt     (corpus/evidence/round35/tb2-grader-probe.txt)
acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0  probe.py        (plans/tb2_grader_probe.py)
44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582  test_outputs.py (corpus/evidence/round35/tb2-eval/test_outputs.py — equals the pinned digest)
```

Counter environment: system python3 has no Biopython, so the counter's own V5 fallback ran the probe as `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` (uv 0.13.0, already installed — no tools were installed or upgraded for this seat). Verified working before any mutant.

## Incident (recorded per KengakuR35's instruction)

My first fixture `/tmp/k35f-PcHd` (plus marker `/tmp/k35f-mutreceipt-D.txt`) was deleted mid-probe by a command I never ran. Seat F35LogDraft confessed on IRC: it ran `rm -rf /tmp/k35f-*` (a glob) after finishing its seat, sweeping live sibling fixtures — a violation of the fixture rule (`rm -rf` only the exact `$D`). Impact: the M2 mutant had been applied but not yet measured; M1 had already been measured and restored in that fixture, so no evidence was lost. Recovery: fixture rebuilt fresh as `/tmp/k35f-Z8MZ` (same commit, TOPLEVEL-OK, pristine hashes identical, baseline re-verified green); pristine copies and hashes moved out of `/tmp` into this seat's scratch (`falsify/F35MutReceipt/scratch/pristine/`) so a repeat wipe cannot destroy evidence. M1 was re-run in the rebuilt fixture so all four mutants carry evidence from the same fixture instance. Broadcast warning sent to all peers; F35LogDraft confirmed it will scope future cleanups to its exact `$D`.

## Baselines

Lane (read-only, authorized): `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round35_c1_verify.py --lane .` →

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
exit=0
```

Fixture 1 (`/tmp/k35f-PcHd`, pre-incident): first run showed `V6 DEFECT census exit 1` — diagnosed: the census `validate --file` mode checks every `used-by` path exists on disk, and the initial sparse set lacked the other 41 knowledge files + lessons. Widened sparse to `corpus/knowledge/**` + `corpus/lessons/**` (42 knowledge files present) → green (`checks=6 defects=0`, `PREDICATE C1 pass`, `exit=0`).

Fixture 2 (`/tmp/k35f-Z8MZ`, rebuilt post-incident, full sparse set from the start): green — identical output, `checks=6 defects=0`, `PREDICATE C1 pass`, `exit=0`.

Baseline green in both instances ⇒ every verdict below is a kill/survive, not a baseline-inconclusive.

## Mutants

### M1 — flip one `observed=` value in the receipt

Mutation (fixture receipt, line 3): `case=valid-balanced predicted=pass observed=pass match=yes` → `case=valid-balanced predicted=pass observed=fail match=yes` (single field flip; summary line untouched).

Mutant hash: `8417d9ac0896a2abb1748924b53ff20f1c5985dfde1b15d638f853cd58d79fe4` (byte-identical in both fixture instances).

Counter (`cd "$D/lane" && python3 plans/round35_c1_verify.py --lane .`):

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 DEFECT fresh probe output differs from receipt (exit 0)
V6 ok
checks=6 defects=1
PREDICATE C1 fail
exit=1
```

Verdict: **KILLED** — V5 byte-compares a fresh probe run against the receipt (plans/round35_c1_verify.py:170-171); any hand edit to the receipt diverges. (Same V5 message observed in fixture 1 pre-incident.)

Restoration: post-restore sha256 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` = pristine. ✓

### M2 — probe skips a case

Mutation (fixture `plans/tb2_grader_probe.py`, `build_cases`): deleted the `("uppercase", valid.upper() + "\n", "pass", "file holds only the sequence (case is not specified)"),` tuple — the probe now runs 17 cases instead of 18. Receipt untouched.

Mutant hash: `83df4f5316b822e7da0e2a2d7d0a46be7af993790229aaf6fd48498f95a97207`.

Counter:

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 DEFECT fresh probe output differs from receipt (exit 0)
V6 ok
checks=6 defects=1
PREDICATE C1 fail
exit=1
```

Verdict: **KILLED** — the fresh 17-case run cannot byte-match the committed 18-case receipt (case lines and the `cases=17 …` summary both differ).

Restoration: post-restore sha256 `acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0` = pristine. ✓

### M3 — prediction flip + receipt regenerated from the changed probe

Mutation (fixture `plans/tb2_grader_probe.py` line 98): `("uppercase", valid.upper() + "\n", "pass", …)` → `("uppercase", valid.upper() + "\n", "fail", …)` — prediction now contradicts the grader's actual verdict. Receipt then REGENERATED from the changed probe (`uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane . > corpus/evidence/round35/tb2-grader-probe.txt`, probe exit 1 by design, plans/tb2_grader_probe.py:164), so receipt and probe are mutually byte-consistent — the strongest form of this mutant.

Mutant probe hash: `11d3e3b88eef8a67624073e6517f808a928718d798597fc7ec7baa59dce491b3`; regenerated receipt hash: `b7faa075085e647ae1dcc60f31a6a3e9713b29ff3dfd31333976a687fc76aede`. Regenerated receipt carries `case=uppercase predicted=fail observed=pass match=NO` and summary `cases=18 observed_pass=5 observed_fail=13 mismatches=1`.

Counter:

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 DEFECT summary not green: cases=18 observed_pass=5 observed_fail=13 mismatches=1
V6 ok
checks=6 defects=1
PREDICATE C1 fail
counter-exit=1
```

Verdict: **KILLED** — the byte-compare passes (receipt was regenerated), but V5's independent green-summary anchor fires (plans/round35_c1_verify.py:172-175 requires `mismatches=0`). A second, redundant anchor exists behind it: the knowledge entry must carry the fresh summary line verbatim (:176-178) — `corpus/knowledge/tb2-protein-assembly-grader.md:20` holds `cases=18 observed_pass=5 observed_fail=13 mismatches=0`, so the `mismatches=1` summary would also fail that check had the green check been absent. Two independent anchors, both tripwired.

Restoration: probe and receipt restored; post-restore hashes `acd7d38d…` and `2359d906…` = pristine. ✓

### M4 — capture `test_outputs.py` replaced with a one-line-different copy

Mutation (fixture `corpus/evidence/round35/tb2-eval/test_outputs.py` line 57): `assert 5 <= len(linker) <= 20, (` → `assert 5 <= len(linker) <= 21, (` — a behavior-changing one-line difference (the `linker-21aa` case would flip fail→pass if the grader ran).

Mutant hash: `a6d472da54f5c360776561bc7bd849a099a972dfd648ea36ae78a092bb887b21`.

Counter:

```
V1 DEFECT listed digest mismatch or missing file: test_outputs.py
V2 ok
V3 DEFECT quote not on test_outputs.py:57-57: assert 5 <= len(linker) <= 20, (
V4 ok
V5 DEFECT fresh probe output differs from receipt (exit 2)
V6 ok
checks=6 defects=3
PREDICATE C1 fail
counter-exit=1
```

Verdict: **KILLED** — three independent defenses fired: V1's SHA256SUMS digest pin (:65-66), V3's located-quote table (the entry quotes the original line 57 verbatim from the capture; the mutated bytes no longer contain it, :134-135), and V5 (the probe REFUSEs a non-pinned grader digest and exits 2, plans/tb2_grader_probe.py:142-144, so the fresh output differs from the receipt).

Restoration: post-restore sha256 `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` = pinned digest. ✓

### M5 (adjacency, beyond the four assigned) — probe metadata string mutated, receipt regenerated

Purpose: quantify what V5's anchoring actually covers. Mutation (fixture `plans/tb2_grader_probe.py` line 97): the `requirement=` prose of `valid-balanced` gained ` TAMPERED` (not a prediction, not the summary). Receipt regenerated from the changed probe (probe exit 0 — `mismatches` unaffected).

Mutant probe hash: `0ee9c4177ceb8c0b447f8faa709fb45842a42c8d991dc6e11c2b33a9845540e9`. Regenerated receipt line: `case=valid-balanced predicted=pass observed=pass match=yes … requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt TAMPERED'`.

Counter:

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
```

Verdict: **SURVIVED** — coverage finding. V5 anchors (a) byte-freshness of the receipt against a fresh probe run and (b) the summary line's greenness + its verbatim presence in the entry. Nothing anchors the per-case `requirement=` prose (or the `assertion=` strings) to `instruction.md` or to the entry's claims: a tampered probe plus a regenerated receipt keeps the frozen predicate green as long as `mismatches=0` and the summary line is unchanged. This is a boundary of the counter's anchoring, reported as found; the frozen predicate is not mine to change.

## Verdict table

| Mutant | Mutation point | Counter result | Verdict |
|---|---|---|---|
| M1 | receipt `observed=` field flip | V5 `fresh probe output differs from receipt` | killed |
| M2 | probe skips a case (18→17) | V5 `fresh probe output differs from receipt` | killed |
| M3 | probe prediction flip + receipt regenerated | V5 `summary not green: … mismatches=1` | killed |
| M4 | capture `test_outputs.py` one-line-different | V1 + V3 + V5 (3 defects) | killed |
| M5 (adjacency) | probe `requirement=` string + receipt regenerated | all green | **survived** (coverage finding) |

Assigned mutants: 4/4 killed. The receipt chain's defenses are real: byte-freshness (V5), green-summary + entry-carry anchors (V5), digest pin (V1), and quote-verbatim anchoring (V3). The one gap found (M5) is metadata-prose anchoring, outside the assigned mutation set.

## Restoration evidence

After the final mutant (M5) was restored, all three files hashed back to pristine (`acd7d38d…`, `2359d906…`, `44a05a24…`), the counter run green again (`checks=6 defects=0`, `PREDICATE C1 pass`), `git -C "$D/lane" status --porcelain` empty, and the fixture removed (`test ! -e` verified). The lane was never written to.

Tooling: nothing installed or upgraded (uv 0.13.0 already present; used as-is).

VERDICT: receipt-mutants-killed-4/4
