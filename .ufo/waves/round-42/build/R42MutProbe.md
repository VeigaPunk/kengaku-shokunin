# R42MutProbe — mutation-testing the C2 probe, receipt and captures against the frozen counter

Seat R42MutProbe (mutation-tester, leaf; no subagents, no installs). 2026-10-26. Detector: the frozen
`plans/round42_c2_verify.py` (digest `270097fdf1d25ee8…`), run exactly as the predicate runs it:
`python3 plans/round42_c2_verify.py --lane <clone> --work $S/w`, every run inside the Q32 envelope.
Target: `plans/fibsqrt_probe.py` (`fc58bf3f1780aaef…`), its receipt `corpus/evidence/round42/fibsqrt-probe.txt`
(`2a54ca8a76619a17…`) and the grader captures. Question: do V2's P10 rerun, V4 and V5 catch each mutant?

## 0. Envelope (Q32) — every run

Every counter/probe/fixture run in this report executed inside:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

with `date +%T` before/after and `ls -A /home/vgpnk/.local/bin | sha256sum` before/after on every run
(`ENVELOPE …` lines in every receipt under `receipts/`). Of the 16 counter runs, 15 show before==after
(`763032563d3739aa` through 17:49, `77408cab9a10361a` from 17:51 on — the listing itself changed once between
17:49:54 and 17:51:58, from outside any of my sandboxes). One run (M1b, end 17:49:54) recorded
before=`763032563d3739aa` after=`77408cab9a10361a` **CHANGED**: the path was
read-only (`--ro-bind`) inside my sandbox, so the listing change was written from outside it (concurrent seat
activity; none of my commands install anything). The final restored-bytes run (17:51:58) shows
before==after==`77408cab9a10361a`. Scratch: `$S=/fast/scratch/hyaku/kengaku-r42/R42MutProbe` (trap-cleaned);
`TMPDIR=$S/w`; nothing over 50 MB anywhere near /tmp; no receipt file over 1 MiB (largest 10 KB).

## 1. Where the mutations lived

All mutants were applied to a disposable scratch clone (`git clone -q --shared <lane> $S/lane`, toplevel
verified `= $S/lane`, at tip `fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`). **The real lane was never written**:
post-run digests of all eight touched paths equal the freeze pins — probe `fc58bf3f1780aaef`, counter
`270097fdf1d25ee8`, gate `ea63882240e67e99`, spec `e836c425fec93421`, receipt `2a54ca8a76619a17`, dry table
`9ee60af69ba3dc9f`, sim.c `700645ac6156cdc8`, test_outputs.py `6117b8edb7d567b3` (commands+outputs in
`receipts/`, §5). Per-mutant protocol: apply (assert the old string occurs exactly once) → record sha256 →
run the frozen counter → restore pristine bytes → sha256-verify restoration.

**Timeline note:** when I cloned (17:31) the lane tip `fda71ae` did not yet carry the C2 entry/SOURCES/README/
PROVINCE surfaces, so the pristine counter was red there (V4/V7/V9 short-circuit on the absent entry — code
`round42_c2_verify.py:164-167,207-210,283-287`). To get a green baseline I greened **the clone only** with the
wave-1 drafts as a fixture: `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (snapshot of seat R42PkgEntry's
draft), the S125–S127 SOURCES rows, README index row + coverage bullet + §Frontier sub-bullet and the PROVINCE
block, all taken unmodified from `R42PkgEntry/integration-drafts.md` (snapshot at `receipts/assemble.py`; the
new entry file was `git add`-ed in the clone so P9's untracked-file check stays green). Mid-experiment the L1
landed the package (tip `ff14d76` → `508434ad…`), and a **bare** clone of the landed tip (no fixture of mine)
passes on its own: `receipts/BARE2.txt` — `P10 ok probe_rerun=byte-equal bytes=4212 … checks=9 defects=0 /
PREDICATE C2 pass`. All mutant runs below were on `fda71ae`+fixture; every byte the counter reads is
digest-pinned, and M7 was re-run on the bare landed tip (§3) to confirm the catch transfers.

## 2. Baseline (pristine bytes)

`receipts/BASELINE.txt` (17:34:58→17:36:07, 69 s wall):

```
V1 ok listed=9 bad=0 extra=0        V6 ok census_exit=0
V2 ok spec=frozen gate=frozen gate_exit=0      V7 ok rows=7 tags=7 bad=0
V3 ok rows=3 bad=0                  V8 ok order_exit=0 result=PASS
V4 ok cases=16 mismatches_named=0/0 bad=0      V9 ok case_rows=16/16 bad=0
V5 ok probe=frozen dry_byte_equal=True
    gate: P10 ok probe_rerun=byte-equal bytes=4212
checks=9 defects=0
PREDICATE C2 pass
```

A mutant counts **killed** iff its run's defect set grows over this baseline (all runs: `PREDICATE C2 fail`).

## 3. Mutant table — 12 mutants, 12 killed

| id | point (file:line) | old → new | counter deltas vs baseline | P10 note | verdict |
|----|-------------------|-----------|----------------------------|----------|---------|
| M1a | probe:122 | `for x in lit[1:]:` → `for x in lit[2]:` (typo → slice dropped) | V2 DEFECT, V5 DEFECT | `fresh probe exit=1 stderr='Traceback…'` — probe dies at import (probe:144→122, `TypeError: 'int' object is not iterable`, full trace `receipts/M1-grade-err.txt`); even `--dry` dies | killed |
| M1b | probe:122 | `for x in lit[1:]:` → `for x in lit[2:]:` (true off-by-one) | V2 DEFECT, V5 DEFECT | `fresh probe output is not byte-equal to the receipt` | killed |
| M2 | probe:274 | `overall()`: `"pass" if letters=="P"*3 else "fail"` → inverted | V2 DEFECT, V5 DEFECT | `not byte-equal` (every CASE line's `predicted=`/`observed=` swap; summary counts swap) | killed |
| M3 | probe:216-217 | harness `except AssertionError: print(… " F")` → `" P"` | V2 DEFECT, V5 DEFECT | `not byte-equal` (assertion-failing tests print P: nop PPF→PPP …) | killed |
| M4 | probe:141 | `text()`: `eol.join(lines) + eol` → `eol.join(lines)` | V2 DEFECT, V5 DEFECT | `not byte-equal` — see §4; fresh run flips `lookup-28-padded-32000` PFP→PPP, `mismatches=0→1` (`receipts/M4-grade.txt`) | killed |
| M5 | receipt:7 | nop `tests=PPF` → `tests=PFF` (observed/summary/match untouched) | V2 DEFECT, **V9 DEFECT** (`case table … equal=False`); **V4 blind** | `not byte-equal` | killed |
| M6 | receipt:24 | summary `observed_pass=7` → `6` | V2 DEFECT, **V4 DEFECT** (`summary disagrees with the CASE lines`); V9 blind | `not byte-equal` | killed |
| M7 | receipt:7 | nop `regrade=same` → `regrade=DIFF:FFF` | **V2 DEFECT only**; V4/V7/V9 all blind (no check parses `regrade=`) | `not byte-equal` | killed |
| M8 | receipt:19-20 | swap padded-31999/padded-32000 CASE lines | V2 DEFECT, V4 DEFECT (`case ids differ from the frozen table`), V9 DEFECT (entry table vs receipt order) | `not byte-equal` | killed |
| M9 | receipt:11 | lookup-28 `match=yes` → `match=NO` | V2 DEFECT, V4 DEFECT (`summary disagrees`, mismatches 0 vs 1); V9 blind | `not byte-equal` | killed |
| M10 | capture sim.c:1 | `#include <stdio.h>` → `#include <stdio.h>/*m*/` | **V1 DEFECT** (`bad=['sim.c']`), V2 DEFECT | `fresh probe exit=2 stderr='SETUP capture sim.c missing or not at its pinned digest'` (the probe's own PINS refuse before any grading) | killed |
| M11 | capture test_outputs.py:1 | canary line `.` → `!` | V1 DEFECT (`bad=['test_outputs.py']`), V2 DEFECT | `fresh probe exit=2 stderr='SETUP capture test_outputs.py …'` | killed |

Every row: `checks≥1 defects≥1`, `PREDICATE C2 fail`, exit 1 (receipts `M*.txt`). M7 was re-run on the bare
landed tip `508434ad` with no fixture: `V2 DEFECT … not byte-equal`, `checks=9 defects=1`, `PREDICATE C2 fail`
(`receipts/M7-bare2.txt`) — the catch does not depend on my fixture. **VERDICT basis: killed 12/12.**

### M1b deep-dive (the requested `lookup()` equality-chain off-by-one)

Dropping literal index 1 leaves bit 1 unconstrained in every value's AND chain, so each chain matches `v` and
`v⊕2`. A scratch simulation of the circuit semantics predicted 6 wrongly-answered graded inputs —
`1680, 1682, 11448, 11450, 43680, 43682` (the x²−1/x²+1 pairs of 41², 107², 209²) — and unchanged letters for
`lookup-27-drop-48401` and `lookup-28-bitflip-41`. The direct fresh probe run confirms exactly that
(`receipts/M1b-grade.txt`, diff vs receipt): 7 CASE lines flip — `lookup-28`, `lookup-28-plus-examples`,
`lookup-28-padded-31999`, `lookup-28-comment-lines`, `lookup-28-reversed-lines`, `lookup-28-crlf` PPP→PPF and
`lookup-28-padded-32000` PFP→PFF — `cases=16 observed_pass=7→1 observed_fail=9→15 mismatches=0→7`. V5 catches
it twice over: the digest pin, and the `--dry` byte-compare (`gates_lines` 1195→1167, 1151→1124, 1279→1249,
1196→1168, 2390→2362 …; `receipts/M1b-dry.txt`).

### M4 deep-dive (gates generator, corrected prediction)

I predicted P10 would be byte-equal here (stdout carries no gate bytes). Wrong, and the experiment corrected
it: the padded case lists end with `""` elements, so `join(lines)` without the final newline leaves the file
one `splitlines()`-counted line short — `lookup-28-padded-32000`'s file now has 31999 lines, test 2 flips F→P,
the fresh stdout says `tests=PPP predicted_tests=PFP match=NO … observed=pass`, `mismatches=0→1`
(`receipts/M4-grade.txt`). P10 catches it behaviorally; V5 catches it via digest and via the dry table's
`gates_lines` 32000→31999.

## 4. The two code-reading questions

**`match=` compares letters exactly — yes, with one named blind spot.** `letters = "".join(got[t][0] for t in
TESTS)` (probe:345) takes the first character of each verdict token in TESTS file order; `match = letters ==
c.predicted` (probe:351) is exact string equality, no normalization. The exception class (probe:340 `parts[3]`)
is carried for display only (probe:347 `errs`) and is **not** part of the comparison: `F` and
`F error=IsADirectoryError` match alike — visible in the receipt's own `gates-is-directory` line
(`tests=PFF … test_gates_file_size:error=IsADirectoryError … match=yes`, receipt:22). A grader failing the same
test by a different exception class is invisible to `match=` (and to V4/V9, which parse the same letters).

**`regrade=` really regrades the same end state — yes.** One harness process per case (probe:266) runs STAGE,
then `for tag in ("TEST", "REGRADE")` (probe:210) over the same `/app` end state built once in `run_case`
(probe:244-261); nothing is rebuilt or reset between the loops; test 3 recompiles `./sim` itself on each call.
The verdict uses only the TEST letters (probe:345-348); REGRADE letters surface only as
`regrade=same|DIFF:<letters>` (probe:353,356) and the `regrade cases=16 differ=0` footer — reported, never
used, as the docstring promises. Empirically: the baseline P10 rerun (a full fresh double-grading of all 16
cases) reproduced the receipt byte-for-byte (`bytes=4212`), and the receipt's footer says `differ=0`. Flip
side (M7): the receipt's `regrade=` column has **no structural checker** — V4/V7/V9 do not parse it — so its
integrity rests entirely on P10's byte-compare, which does fire.

## 5. Restoration evidence

Mutated → restored sha256 (full values in `receipts/driver-results.json`):

| mutant | file | mutated | restored |
|--------|------|---------|----------|
| M1a | fibsqrt_probe.py | `e0e44b1221e7326a…` | `fc58bf3f1780aaef…` ✓ |
| M1b | fibsqrt_probe.py | `21800ff4a4c5bfb6…` | `fc58bf3f1780aaef…` ✓ |
| M2 | fibsqrt_probe.py | `8419acac398b485b…` | `fc58bf3f1780aaef…` ✓ |
| M3 | fibsqrt_probe.py | `1e54a4f72a22b127…` | `fc58bf3f1780aaef…` ✓ |
| M4 | fibsqrt_probe.py | `ced13388320460cd…` | `fc58bf3f1780aaef…` ✓ |
| M5 | fibsqrt-probe.txt | `4a786ff98f450b0b…` | `2a54ca8a76619a17…` ✓ |
| M6 | fibsqrt-probe.txt | `e734a5177d121b48…` | `2a54ca8a76619a17…` ✓ |
| M7 | fibsqrt-probe.txt | `13d0a5d6432a1221…` | `2a54ca8a76619a17…` ✓ (both clones) |
| M8 | fibsqrt-probe.txt | `eb16806f9737db2d…` | `2a54ca8a76619a17…` ✓ |
| M9 | fibsqrt-probe.txt | `27d653ada3fdec08…` | `2a54ca8a76619a17…` ✓ |
| M10 | sim.c | `147ffae95d6ec6fd…` | `700645ac6156cdc8…` ✓ |
| M11 | test_outputs.py | `f5b7eeeaef69b580…` | `6117b8edb7d567b3…` ✓ |

Final restored-bytes counter run (`receipts/RESTORED.txt`, 17:51:58): `P10 ok probe_rerun=byte-equal
bytes=4212 … checks=9 defects=0 / PREDICATE C2 pass`. The real lane's eight touched-path digests re-measured
after everything: all equal the freeze pins (§1). One invalid run is disclosed: my first "bare" M7 attempt
(`receipts/` keeps no copy) ran a sed-generated script whose `cd $S/lane` substitution missed, so it re-ran the
baseline on the fixture clone — detected because P10 reported `bytes=4212` where the tampered receipt would
have been 4216; redone correctly as `M7-bare2.txt`.

## 6. Findings for the counter (calibration notes, not defects)

1. **V5's digest pin is a universal catch for any probe-byte mutant** — including mutants whose `--dry` output
   is unchanged (M3: dry byte-equal, caught by the pin alone). The behavioral layer (P10) is what separates
   crash/letters mutants from stdout-silent ones; here both layers fired on every probe mutant.
2. **V4 does not read the `tests=` letters** (its regexes take `observed=`, the `match=NO` count and the
   summary): a letters-only receipt tamper (M5) passes V4 and is caught by V9 (the entry's case table is a
   second copy of the letters) plus P10.
3. **The `regrade=` column is guarded only by P10** (M7: V4/V7/V9 all blind; P10 fires on both the fixture
   clone and the bare landed tip).
4. **Capture mutants are stopped by digest pins before any grading** (V1 manifest + the probe's own PINS →
   SETUP exit 2), so the counter never measures how a mutated grader would score — by design; consistent with
   the claims' "host gcc stands in" limit. Also V5's `--dry` path returns before the pin check, so V5 stays
   ok under capture mutants (observed in M10/M11).
5. **P9 (clean tree) checks untracked files only** (`git ls-files --others`, gate:259-265): mutations of
   tracked files (probe, receipt, captures, README…) are invisible to it — P10 is the live guard for
   tracked-file tampering; my fixture's new entry file had to be `git add`-ed to keep P9 green.
6. Q32: one envelope run recorded a `~/.local/bin` listing change mid-run (§0) — written from outside my
   read-only sandbox; all other runs before==after.

Receipts: `.ufo/waves/round-42/build/R42MutProbe/receipts/` (16 counter runs, 4 direct-run artifacts, driver
ledger, scripts). Every number above carries its command in those files.

VERDICT: probe-mutants-caught-12/12
