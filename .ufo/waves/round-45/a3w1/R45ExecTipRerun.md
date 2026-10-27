# R45ExecTipRerun — final tip re-measure of C1 and C2 (round 45, wave a3w1)

## Axes

- **calibration** (primary): does the frozen predicate fire on the exact surface the round claims — a clean
  `--no-local` clone of the lane tip — and does it fire the same way twice?
- **coverage** (primary): is the measured surface the claimed surface (fence as landed = fence at tip, pinned
  file set complete, no unpinned module the glob would admit, no dependence on the real lane's working tree)?

No move in this report changes any lane file; the deliverables are the re-measurement receipts.

## Tip measured

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc

$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel        -> /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/lane
$ git -C "$S/lane" rev-parse HEAD                   -> fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc
$ git -C "$S/lane" status --porcelain | wc -l       -> 0
$ ls "$S/lane/.git/objects/info/alternates"         -> No such file or directory
$ stat -c '%h %i %n' clone/plans/fixture_fence.py lane/plans/fixture_fence.py
1 1488016370 .../lane/plans/fixture_fence.py
1 238354634 .../kengaku-shokunin/plans/fixture_fence.py
```

The clone is a real copy (link count 1, distinct inodes, no alternates): nothing is read out of the lane's
object store during the run. Both counters were invoked from the **clone's own** copies
(`$S/lane/plans/round45_c1_verify.py`, `$S/lane/plans/round45_c2_verify.py`), matching the frozen predicate's
wording "measured on a clean clone of the landing tip".

Digests of the measured instruments (they equal `claims/frozen-digests.txt`, checked below):

```
ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6  plans/fixture_fence.py
7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d  plans/round45_c1_verify.py
ab6825e34596ba71f59a184a59fd4e672fd22dcf4b892c511cae5ead2b104f50  plans/round45_c2_verify.py
```

## Run 1 — C1 (receipt: `R45ExecTipRerun/c1-tip.txt`, 137 lines, sha256 ebfca770…4095)

Command (envelope wrapper shown verbatim by the receipt itself; `S=/fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun`):

```
claims/envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/w"
```

Output, head and verdict block:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/env /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/env --bind /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/lane/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/lane --work /fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun/w
ENVELOPE start 00:22:22 cwd=/fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
…
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:22:27 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
outer_exit=0 wall=6s
```

All five frozen C1 lines appear in order with the frozen values, exit 0, PATH-dir content digest unchanged
(`ff187bb5c98aa6b5` before and after). The per-module section (lines 4-131 of the receipt) is 10 `REFUSAL … clean`
rows and 104 `FENCE-RUN honest … ADMIT opens=0` rows; no `READ`/`LEAKED`/`HUNG`/`ERROR` row exists.

## Run 1 — C2 (receipt: `R45ExecTipRerun/c2-tip.txt`, 28 lines, sha256 e62ddf84…837a)

```
claims/envelope.sh "$S/env2" /usr/bin/python3 "$S/lane/plans/round45_c2_verify.py" --lane "$S/lane" --work "$S/w2"
```

```
ENVELOPE start 00:22:31 cwd=/fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=19 distinct_quotes=19 distinct_lines=19 out_of_word_range=0
    gate: P4 ok checked=19 bad=0 first=0
    gate: P5 ok manifest_entries=9 bad=0 first=0
    gate: P6 ok rows=8 bad=0 first=0
    gate: P7 ok source_lines=8 bad=0 first=0
    gate: P8 ok index_rows=52 knowledge_files=52 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4659
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=8 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=9 tags=9 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=16/16 bad=0
V10 ok mechanism_rows=16/16 bad=0
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
checks=11 defects=0
PREDICATE C2 pass
ENVELOPE end 00:22:34 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
outer_exit=0 wall=5s
```

`checks=11 defects=0` and `PREDICATE C2 pass`, exit 0, PATH-dir digest unchanged, on the clean tip clone.

## Run 2 — same tip, second independent clone (calibration leg)

```
$ git clone -q --no-local … "$S/lane2"; git -C "$S/lane2" rev-parse HEAD -> fbad1c5…9ddc; status -> 0
claims/envelope.sh "$S/env3" … round45_c1_verify.py --lane "$S/lane2" --work "$S/w3"   (receipt c1-tip-run2.txt)
claims/envelope.sh "$S/env4" … round45_c2_verify.py --lane "$S/lane2" --work "$S/w4"   (receipt c2-tip-run2.txt)
run2 c1_exit=0 c1_wall=6s c2_exit=0 c2_wall=4s
```

`diff` of the two C1 receipts excluding `ENVELOPE` lines: **2 differing lines only**, and the difference is the
`mktemp` scratch token inside two BREACH reasons that quote the fixture path —

```
< … f2-deep-worktree BREACH opens=0 -- x/y/z/r/.git/config sets core.worktree=…/w/k45-c1-ai3rfge2/fx/…
> … f2-deep-worktree BREACH opens=0 -- x/y/z/r/.git/config sets core.worktree=…/w3/k45-c1-fgfc6v9n/fx/…
< … f6-repo-above-d BREACH opens=0 -- .git exists at …/w/k45-c1-ai3rfge2/fx/refusals45-f6_above …
> … f6-repo-above-d BREACH opens=0 -- …/w3/k45-c1-fgfc6v9n/fx/refusals45-f6_above …
```

Every counted value (PINS, per-module verdicts, totals, CALIBRATION, PREDICATE) is identical. The C2 receipts
are **byte-identical** outside the `ENVELOPE` lines (`C2_RECEIPTS_IDENTICAL`). The predicate is deterministic
across clones and scratch roots.

## Provenance controls (does "clean clone" really mean the clone?)

- **C1 with the whole fleet root emptied** (`--bind <empty> /home/vgpnk/Projects/shokunin`, real lane included;
  `ls -A <empty> | wc -l` → `0`), receipt `shadow-c1-fleetroot-empty.txt`:
  `REFUSALS total=10 clean=10 …` / `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0` /
  `CALIBRATION advertised=10 contradicted=0` / `PREDICATE C1 pass`, envelope end `exit=0 … unchanged`.
  C1 reads nothing outside `$S/lane` and `$S/w`.
- **C2 with only the real lane path emptied** (`--bind <empty> /home/vgpnk/Projects/shokunin/kengaku-shokunin`,
  `~/.cache` kept writable from scratch), receipt `shadow-c2-laneonly.txt`: `checks=11 defects=0`,
  `PREDICATE C2 pass`, envelope end `exit=0 … unchanged`. C2 reads nothing from the real lane's working tree.
- **C2 with the whole fleet root emptied**, receipt `shadow-c2-fleetroot-empty.txt`: **fail**
  (`gate: P10 DEFECT fresh probe exit=2 stderr='error: Failed to initialize cache at /home/vgpnk/.cache/uv'`,
  `V6 DEFECT … FileNotFoundError: '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'`,
  `checks=11 defects=2`, `PREDICATE C2 fail`). Two separable causes: (a) P10 is an artifact of my outer layer —
  `--ro-bind /home/vgpnk /home/vgpnk` in that ad-hoc command replaced the envelope's writable `~/.cache` overlay,
  so uv had no cache; (b) V6 is a real out-of-lane instrument dependency (see Findings). This control is reported
  because it failed, not as a defect of the claim: with only the lane shadowed the same command passes.

## Coverage checks on the measured surface

- Frozen set at the tip, all 8 sampled rows equal `claims/frozen-digests.txt` (18 listed, 8 sampled):
  `cb2fae38…3ea3 plans/round-45-claims.md`, `7745eb0a…150d round45_c1_verify.py`, `ab6825e3…4f50
  round45_c2_verify.py`, `9363e03e…b4ab password_recovery_probe.py`, `2f924ffa…8244 pkg-spec-r45.json`,
  `46036abe…aabb password-recovery-dry-cases-freeze.txt`, `fb2cf5e8…bfb6 tb2-password-recovery/SHA256SUMS`,
  `58ed31ae…3f63 claims/c2_predictor_control.py`.
- Claimed surface = landed surface: `git diff --stat 8f9a898 fbad1c5 -- plans/fixture_fence.py` is empty, so the
  fence that earned `PREDICATE C1 pass` in the landing commit is the fence measured at the tip
  (`ac65c032…` = the digest printed by the tip run and by the L1's `integrate/a3-tip-c1.txt`).
- No unpinned module can enter through the globs: `plans/refusals45/*.py` = **10** files, `plans/battery4[234]/*.py`
  = **22** files, and `PINS total=33` = 10 refusals + 22 batteries + 1 round-44 counter. An added module would
  change `REFUSALS total` / `HONEST fixtures` and fail the predicate even though the new file were unpinned.
- The C2 package is unchanged since its landing commit `6decc71` apart from one added line in `corpus/README.md`
  (`git diff --stat 6decc71 fbad1c5 -- corpus/knowledge/tb2-password-recovery-grader.md
  corpus/evidence/round45/password-recovery-probe.txt corpus/SOURCES.md corpus/README.md PROVINCE.md` →
  `corpus/README.md | 1 +`), i.e. the round-45 lesson row, not entry text.
- Post-run hygiene: `git -C "$S/lane" status --porcelain | wc -l` → `0`; neither counter wrote into the clone.

## Findings for the L1 (not applied by me)

1. **C1's `PINS` does not cover the fence itself.** The counter prints
   `FENCE plans/fixture_fence.py sha256=…` but pins only the 33 fixture/builder inputs, so a fence swapped under a
   fixed counter would still print `PINS total=33 mismatched=0`. The predicate survives only because the observed
   digest (`ac65c032…`) happens to equal the one in the landing receipt; nothing in the counter enforces that.
   Coverage supplied here: landing commit fence == tip fence, digest quoted above.
2. **C2's V6 reads a fleet-root instrument outside the lane.** `plans/round45_c2_verify.py:97`:
   `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`. The claim says "measured on a clean clone
   of the landing tip"; the clone covers the entry and the probe, but V6's validator is fleet-root state
   (`ls -l` → 35466 bytes, 2026-10-19; not tracked by the lane: `git ls-files | grep -c sources-census` → 0).
   Nothing pins it by digest. This is a provenance gap of the same class as finding 1, on the C2 side.
3. `round45_c2_verify.py` (25 insertions / 25 deletions) and `plans/round-45-claims.md` (+2 lines) both differ from
   the freeze commit `52d7486`; the changes are the disclosed "Freeze amendments (pre-data, attempt 2)" paragraph
   and its matching re-pin, and `frozen-digests.txt` (rewritten in the same landing chain) matches the tip bytes
   for all 8 sampled rows. I record it, I do not judge it — `R45CritFrozenDigest` owns the verdict.
4. Ambient state, not mine: the real lane working tree carries ` M corpus/QUALITY.md` while this seat ran. It does
   not affect the tip re-measure (the clone is made from `HEAD`), but a later "clean tree" check by the L1 will see
   it.

## Host safety

Every counter run went through `claims/envelope.sh` with `S=/fast/scratch/hyaku/kengaku-r45/R45ExecTipRerun`;
all seven receipts carry `local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged` and no
`INVALID`. No pacman transaction, no install, no writes to `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the lane, or
the fleet root. Scratch `$S` removed with `plans/scratch_guard.py safe-rm` after the report was written.

## Risks / blockers

- None to the re-measurement. Findings 1 and 2 are instrument-coverage gaps, not failed predicates: both
  predicates reproduce green on the tip and on a second clone.
- Residual risk inherited, not created here: `--jobs 8` thread scheduling means per-fixture ordering inside the
  receipt is nondeterministic in principle; the two runs produced the same order and the same totals, so this did
  not bite. The counted values, not the row order, are what the predicate reads.

VERDICT: tip-c1-pass-c2-pass
