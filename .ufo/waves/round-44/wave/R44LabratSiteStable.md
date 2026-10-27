# R44LabratSiteStable — C1 counter verdict vs site (jobs / hash seed / work root)

**Assignment.** Hypothesis: the verdict of `plans/round44_c1_verify.py` on the pre-freeze witness battery
`.ufo/waves/round-44/claims/witness/` (`w_u.py`) is invariant under `--jobs 1/8/16`, the counter's own
`PYTHONHASHSEED`, and two different `--work` roots. Run each combination in a clone inside the round-44 envelope and
diff the MUTANT/summary lines.

**Answer: INVARIANT.** 30 envelope-wrapped executions across 30 distinct configurations; all 30 print a
byte-identical verdict body (18 lines, sha256 `d1a24537d9c156365c8bae6c3cb97d0562c867cf067090fad80f4a81418af601`),
exit 0, and every envelope reports the `~/.local/bin` content digest unchanged. No run diverged in a single
MUTANT, FIXTURE, BATTERY, MUTANTS, MUTANTS-BY-TOOL, ADVERTISED, PINS, PINS-AFTER or PREDICATE line, and the
per-mutant attribution site is the same everywhere (U5 `L522`, U6 `L522`, U7 `L539`, U9 `L384`, U14c `L161`, all
`value=differs hits=1`).

## Method

- Clone (rule): `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
  `git -C "$S/lane" rev-parse --show-toplevel` -> `/fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/lane`.
  Inputs actually measured: counter `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad`,
  witness `f3855ae1c1dbf37357233995cb25318254a482f7ee69fdea90edc13648a60bd8` (`receipts/inputs-sha256.txt`).
- Every run: `envelope.sh "$S/env/<tag>" [env PYTHONHASHSEED=<seed>] /usr/bin/python3
  "$S/lane/plans/round44_c1_verify.py" --lane "$S/lane" --battery-dir
  "$S/lane/.ufo/waves/round-44/claims/witness" --work "$S/w<A|B>" --jobs <1|8|16>`, stdout+stderr to
  `$S/out/<tag>.txt`, then the verdict lines (`^FIXTURE|MUTANT|BATTERY|MUTANTS|ADVERTISED|PINS|PREDICATE`) were
  extracted and hashed. Helper: `$S/one.sh`; scratch `S=/fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable`.
- Diff: all 30 extracted verdict bodies hash to the same value; `awk` over the run table shows one unique hash,
  30/30 `exit=0`, 0 non-zero exits.

## Run matrix (30 executions, 30 receipts)

| axis | values | count |
|---|---|---|
| `--jobs` | 1, 8, 16 | 3 |
| counter `PYTHONHASHSEED` | `0`, `1`, `424242`, unset (randomised) | 4 |
| `--work` root | `$S/wA`, `$S/wB` | 2 |
| full cross product | | 24 (`j<jobs>-s<seed>-w<A|B>`) |
| repeat of `jobs=8 seed=0 wA` | `repeat-r1`, `repeat-r2`, `repeat-r3`, `baseline-b2` | 4 |
| `--lane .` from inside the clone with a third root `$S/wC` | `rel-lane-wC` | 1 |
| deeper work root `$S/deep/x/y/wD`, jobs=16, seed=1 | `deep-work-wD` | 1 |

Table with start/end times, exit and per-run verdict hash: `receipts/runs.tsv` (30 rows, one hash column value).

Identical body (all 30 runs, verbatim; also `receipts/verdict-body.txt`):

```
PINS total=2 mismatched=0
FIXTURE u3-row-path-binds tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u5-sixty-three-hex tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
FIXTURE u6-sixty-five-hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u7-twin-captures tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9-dirty-erratum tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u14c-odd-claims-name tool=order expect=error declared=- observed_rc=2 observed=- ok
MUTANT U5 anchor silence killed by=u5-sixty-three-hex attributed=L522 value=differs hits=1 -- plans/anchor_digest_check.py:88 ...
MUTANT U6 anchor silence killed by=u6-sixty-five-hex attributed=L522 value=differs hits=1 -- plans/anchor_digest_check.py:88 ...
MUTANT U7 anchor rc-mirror killed by=u7-twin-captures attributed=L539 value=differs hits=1 -- plans/anchor_digest_check.py:98-99 ...
MUTANT U9 anchor rc-mirror killed by=u9-dirty-erratum attributed=L384 value=differs hits=1 -- plans/anchor_digest_check.py:106-107 ...
MUTANT U14c order error killed by=u14c-odd-claims-name attributed=L161 value=differs hits=1 -- plans/order_check.py:26-27 ...
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=4/4 order=1/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

## Envelope lines (QUALITY Q32)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/env/j1-sunset-wB /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/env/j1-sunset-wB --bind /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/env/j1-sunset-wB/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/lane/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/lane --battery-dir /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/lane/.ufo/waves/round-44/claims/witness --work /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/wB --jobs 1
ENVELOPE start 20:34:10 cwd=/home/vgpnk/Projects/shokunin
...
ENVELOPE end 20:34:15 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/env/rel ... -- /usr/bin/python3 plans/round44_c1_verify.py --lane . --battery-dir .ufo/waves/round-44/claims/witness --work /fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/wC --jobs 8
ENVELOPE start 20:36:10 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable/lane
ENVELOPE end 20:36:13 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

All 30 runs: `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`, `exit=0` (zero exit-4
`INVALID` envelopes, so no re-run was needed). Full receipts of four representative runs are in
`receipts/full-j1-sunset-wB.txt`, `receipts/full-j16-s424242-wB.txt`, `receipts/full-rel-lane-wC.txt`,
`receipts/full-deep-work-wD.txt`.

## Axis-liveness controls (the null result is not a dead axis)

`receipts/seed-axis-control.txt` — the counter's own interpreter honouring the varied seed:

```
PYTHONHASHSEED=0 hash(seed-probe)=4488536522357565246
PYTHONHASHSEED=1 hash(seed-probe)=-7215174363294950837
PYTHONHASHSEED=424242 hash(seed-probe)=2370684542585505117
PYTHONHASHSEED=unset run1 hash(seed-probe)=4483937406767392349
PYTHONHASHSEED=unset run2 hash(seed-probe)=-3220678929372137386
```

Three explicit seeds give three different string hashes and the unset case randomises per process, so the seed axis
is live and the counter stayed invariant anyway. The jobs axis reaches the counter's pool directly
(`round44_c1_verify.py:676` `with concurrent.futures.ThreadPoolExecutor(self.jobs) as ex:`) and `--jobs` is a plain
`add_argument("--jobs", type=int, default=8)` (`:773`); no cap or clamp. Seed isolation is one-way here: tool runs are
pinned to `PYTHONHASHSEED=0` by the counter itself (`:618`), so only the parent counter's dict/set ordering is varied.

## Cross-site corroboration

The verdict body is also byte-identical to the frozen L1 receipt produced on the *source lane* with the L1 work root
(`/fast/scratch/hyaku/kengaku-r44/L1/ctl/w1`) — same hash `d1a24537d9c15636…`
(`sha256sum .ufo/waves/round-44/claims/witness-run.txt` = `d94c0ef0b51f70015912b6c87de892189df3f8d4d8b372ee907b82279ef02f8a`).
So the counter's verdict on this battery is stable across three independent sites (clone × 2 work roots × deep root ×
source lane), two argv shapes (absolute `--lane` and `--lane .`), 3 concurrency levels, and 4 hash-seed states.

## Limits and risks (named, not hidden)

1. **Concurrency saturation.** The witness battery has 6 fixtures, so `--jobs 8` and `--jobs 16` both saturate at 6
   concurrent tool runs; only `--jobs 1` versus the saturated point is a distinct concurrency regime. A battery with
   ≥16 fixtures would be needed to exercise 16 genuinely concurrent runs. (No such battery was built: the seat may
   not author `plans/battery44` work and duplicating the witness module would collide fixture ids.)
2. **What "stable" is measured on.** Equality is on the printed verdict (MUTANT attribution line number, `value=`,
   `hits=`, fixture lines, counters), not on the private locals digests. The tracer normalises only
   `/rtmp/tNNNNNN` and `/work/wNNNNNN` inside the scratch root (`:183`), leaving the `mkdtemp` component in the
   hashed text; leg g therefore compares mutant vs reference *within one root*, which stayed stable, and the output
   proved invariant across roots, but the digests themselves were not compared cross-root (they are never printed).
3. **Verdict value.** `PREDICATE C1 n/a (non-default battery or mutant subset)` — this is dev-mode evidence for the
   witness-battery control, not the frozen lane predicate (`--battery-dir` omitted). It says nothing about
   `plans/battery44`, which this seat did not build.
4. The counter's own `PINS`/`PINS-AFTER` and `BATTERY ... sidechannel=0` lines were identical in all 30 runs, so the
   tools and witness module were unmodified throughout (matches `receipts/inputs-sha256.txt`).

## Artifacts

- `receipts/runs.tsv` — 30 rows: tag, envelope start/end, exit, digest line, verdict-body hash (16 hex).
- `receipts/verdict-body.txt` — the one 18-line body all runs printed.
- `receipts/full-{j1-sunset-wB,j16-s424242-wB,rel-lane-wC,deep-work-wD}.txt` — full envelopes.
- `receipts/seed-axis-control.txt`, `receipts/inputs-sha256.txt`.
- No lane file was written; scratch `S=/fast/scratch/hyaku/kengaku-r44/R44LabratSiteStable` removed with
  `scratch_guard.py safe-rm` after the receipts were copied here.

VERDICT: site-stable-confirmed-runs-30
