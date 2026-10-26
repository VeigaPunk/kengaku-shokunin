# R39MutProbe — mutation probe of `plans/git_leak_probe.py` sensitivity (round 39 wave 1, C2)

Seat R39MutProbe, 2026-10-26. Frozen probe digest `4961a50f28ae…` (= `PROBE_SHA256` in
`plans/round39_c2_verify.py`). All work ran on scratch copies under
`/fast/scratch/hyaku/kengaku-r39/R39MutProbe/` (removed at the end; receipts copied to
`build/R39MutProbe/`). The lane file was never written: `plans/git_leak_probe.py` sha256
before = after = `4961a50f28ae85e8d8b687d3623aef29b59d4db14c0e62e5244e48cfef8cf68c`
(`MANIFEST.txt`: `lane_probe_before` / `lane_probe_after`).

## Method (one baseline + 7 single-point mutants)

- Scratch: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
  `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane` verified; `TMPDIR=$S`; `--work "$S/w"`.
- **Baseline:** `python3 $S/probe/pristine.py --lane $S/lane --work $S/w` → rc=0, elapsed 1s,
  stdout sha256 `d7f3a465ccc4…` = frozen receipt `corpus/evidence/round39/git-leak-probe.txt`
  sha256 `d7f3a465ccc4…`; `diff -u` empty (`BASELINE_BYTE_EQUAL_TO_FROZEN_RECEIPT`). The frozen
  receipt reproduces byte-for-byte on this host, so every mutant verdict below is attributable.
- Detector legs, per mutant:
  1. **receipt diff** vs pristine stdout (`diff -u`, saved as `xN.diff`);
  2. **P10 leg**, simulated exactly from the gate source `plans/pkg_gate.py:267-285` (`c_rerun`):
     defect iff fresh rc != 0 OR fresh stdout not byte-equal to the receipt file. The gate itself
     was not executed against a mutant — that needs the mutant committed in a clone, forbidden by
     the fixture rules — so `c_rerun`'s two conditions were applied to the mutant's actual rc/stdout.
  3. **V4/V7 legs**: the frozen counter bytes (`plans/round39_c2_verify.py`, copy sha256
     `5c722dc188d1…`) executed unchanged by a driver against a scratch lane holding the frozen spec
     (`f62163ce…`), the frozen dry table (`e92a5d6d…`), the receipt under test, and a synthetic
     entry whose `## Requirement map` labels are exactly what V7 derives from the FROZEN receipt
     (recover-secret=enforced, secret-gone=partly, files-untouched=enforced,
     messages-untouched=partly). **Control:** frozen receipt → `v4 ok cases=25 … bad=0`,
     `v7 ok rows=4 tags=4 bad=0` (`control.det`).
  4. **V5 legs**: mutant file digest vs `PROBE_SHA256`; and `--dry` stdout vs the frozen dry table.
- All 7 grade runs + 7 dry runs executed concurrently in one call; wall time 1.6s total.

## Mutant table

| id | site (probe line) | old → new | receipt | P10 | V4 | V7 | V5 digest | V5 dry | verdict |
|----|---|---|---|---|---|---|---|---|---|
| x1 | 183 | `print("TEST " + name + " F error=" + type(e).__name__)` → `print("TEST " + name + " P")` | differs | defect | defect | defect | defect | equal | killed |
| x2 | 215 | `"1" if case.setup else "0"` → `"0"` (setup skipped for every case) | differs | defect | defect | defect | defect | equal | killed |
| x3 | 213 | drop `"GIT_CONFIG_NOSYSTEM": "1", ` from the case env | byte-equal | pass | ok | ok | defect | equal | survived behaviorally |
| x4 | 169-170 | `if stage("recipe", …):` + `sys.exit(3)` → bare `stage("recipe", …)` | byte-equal | pass | ok | ok | defect | equal | survived behaviorally |
| x5 | 198 | `"--bind", str(work / "app"), "/app"` → `"--ro-bind", …` | differs | defect | defect | defect | defect | equal | killed |
| x6 | 98,103 | recipes of `untouched` ↔ `echo-only` swapped | differs | defect | defect | defect | defect | equal | killed |
| x7 | 103,110 | recipes of `echo-only` ↔ `clean-echo` swapped (added control) | byte-equal | pass | ok | ok | defect | equal | survived behaviorally |

Mutant file digests (all ≠ `4961a50f…`, so V5's digest leg fires for every one):
x1 `4fc5f4d8…`, x2 `b85b03ab…`, x3 `b327c1e3…`, x4 `980bb685…`, x5 `0b325f8c…`,
x6 `eac1b91a…`, x7 `c396df30…` (`MANIFEST.txt`).

## Per-mutant evidence

**x1 — harness maps every exception to P** (generic `except Exception` branch, AssertionError→F kept).
`x1.diff`: `CASE flag-is-directory … tests=FPPPP → PPPPP`, `observed=fail → pass`, `match=yes → NO`,
the `error=IsADirectoryError` suffix disappears; summary `observed_pass=13→14 observed_fail=12→11
mismatches=0→1`. Detection: P10 defect (fresh stdout ≠ receipt); `x1.det`: `v4 DEFECT … bad=
["mismatch cases not named in the entry: ['flag-is-directory']"]`, `v7 DEFECT … bad=['recover-secret:
labelled enforced, receipt derives partly']`. Killed on all three behavior legs.

**x2 — setup skipped for every case.** grade rc=2; receipt is a 4-line prefix (`x2.txt`):
`untouched` FFFFF, `oracle-solve-sh` FFFFF, `echo-only` PFFFF — all three `match=NO` — then
`x2.err`: `SETUP case echo-reflog-expire did not yield five test verdicts (rc=3)` /
`STAGE recipe rc=128` (first bare `git -C /app/repo …` recipe dies without the setup-built repo).
Detection: P10 defect (rc=2); `x2.det`: `v4 DEFECT … ['case ids differ from the frozen table',
'summary line count != 1', "mismatch cases not named in the entry: ['untouched', 'oracle-solve-sh',
'echo-only']"]`, `v7 DEFECT` (secret-gone derives enforced ≠ labelled partly; messages-untouched
derives enforced ≠ partly; two cite defects). Killed.

**x3 — GIT_CONFIG_NOSYSTEM dropped.** Receipt byte-equal to pristine; `--dry` byte-equal. Host
check (command in transcript): `/etc/gitconfig` ABSENT, `/usr/etc/gitconfig` ABSENT — there is no
system git config on this host for the flag to exclude, so the receipt cannot be sensitive to it.
P10 would pass (fresh mutant output byte-equal to the frozen receipt); V4 ok; V7 ok (`x3.det`).
Survivor at the behavior layer; caught only by V5's digest pin.

**x4 — recipe failures ignored.** Receipt byte-equal; `--dry` byte-equal. No frozen recipe exits
non-zero (the pristine run produced 25 verdicts at rc=0), so the `sys.exit(3)` branch is dead code
on this corpus and the probe's own error path (exit 2) is never exercised by its 25 frozen cases.
P10 would pass; V4 ok; V7 ok (`x4.det`). Survivor at the behavior layer; V5 digest only.

**x5 — /app bound read-only.** grade rc=2 after `empty-app` (the only `setup=False` case, which
grades FFFFF normally); `x5.err`: `SETUP case untouched did not yield five test verdicts (rc=3)` /
`STAGE setup rc=1` — challenge-setup.sh cannot write a read-only /app. Detection: P10 defect
(rc=2); `x5.det`: `v4 DEFECT … ['case ids differ from the frozen table', 'summary line count != 1']`,
`v7 DEFECT … ['secret-gone: no receipt case violates it', … 'messages-untouched: labelled partly,
receipt derives enforced', …]`. Killed.

**x6 — recipe swap, discriminating pair (`untouched` ↔ `echo-only`).** `x6.diff`:
`untouched … tests=FPPPP → PPPPP, observed=fail → pass, match=NO`; `echo-only … tests=PPPPP →
FPPPP, observed=pass → fail, match=NO`; summary counts unchanged (13/12) but `mismatches=0→2`.
Detection: P10 defect; `x6.det`: `v4 DEFECT … ["mismatch cases not named in the entry:
['untouched', 'echo-only']"]`, `v7 DEFECT … ['recover-secret: labelled enforced, receipt derives
partly']`. Killed.

**x7 — recipe swap, null pair (`echo-only` ↔ `clean-echo`; added control beyond the six assigned
mutations, probing the swap class's null direction).** Receipt byte-equal: both swapped recipes
yield PPPPP and neither the receipt nor the dry table prints recipe text, so no receipt-level
check can tell which recipe ran. P10 would pass; V4 ok; V7 ok (`x7.det`). Survivor at the
behavior layer; V5 digest only.

## Findings (coverage)

1. **Counter-level catch: 7/7.** V5's digest pin (`plans/round39_c2_verify.py` `v5`: probe not at
   `PROBE_SHA256` → defect) fires for every byte change, so the C2 counter as specified catches
   all seven mutants. The VERDICT line counts this level.
2. **Receipt-behavior layer catch: 4/7** (x1, x2, x5, x6). For x3, x4, x7 the receipt is
   byte-identical: P10's fresh-run byte-compare passes, V4 and V7 pass — the digest pin is the
   only thing standing. If the probe were ever re-frozen carrying one of these defects (digest
   updated), no counter check would notice.
3. **V5's dry byte-compare leg adds nothing for any mutant:** `--dry` output is byte-equal to the
   frozen dry table for all seven (it prints no recipes, no env, no sandbox flags). Recipe
   identity (the x6/x7 class) is pinned by the file digest alone.
4. **x4:** the probe's failure path (setup/recipe rc → exit 2, "never a verdict") is dead code on
   its own frozen corpus — all 25 recipes exit 0 — and no counter check can exercise it.
5. **x3:** the `GIT_CONFIG_NOSYSTEM=1` isolation claim is untestable on this host (no system
   gitconfig exists); the receipt cannot be sensitive to it here.

## Limits

- Single host: git 2.56.0, bwrap 0.11–0.13 (0.13.1), no `/etc/gitconfig`; the task image is never
  pulled (the same limits the claims file names for the probe).
- P10 simulated from `plans/pkg_gate.py:267-285` conditions applied to actual mutant rc/stdout;
  the gate was not run against a mutant (would require committing in the scratch clone, forbidden
  by the fixture rules).
- The synthetic entry is a detection fixture, not the L1 entry; on the frozen receipt it passes
  V4/V7 (control), which is what makes the mutant DEFECTs attributable rather than baseline noise.
- Scratch copies were disposable per the tasking ("in a copy, never the lane file"); deleted after
  the evidence copy; lane bytes verified unchanged before/after.
- x7 is an added control, not one of the six assigned mutations; it was chosen to test whether the
  recipe-swap class has a null direction (it does).

VERDICT: probe-mutants-7/7
