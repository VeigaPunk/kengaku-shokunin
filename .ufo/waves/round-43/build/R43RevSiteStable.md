# R43RevSiteStable — C1 counter verdict is site-stable under jobs / counter hash-seed / scratch root

Hypothesis (falsifiable): the round-43 C1 counter's verdict on the freeze direction module
(`.ufo/waves/round-43/claims/witness/w_near.py`, sha256 `9a044008…`, pinned `frozen-digests.txt:11`) is
invariant under `--jobs 1/8/16`, under the **counter's own** `PYTHONHASHSEED` (the counter pins
`PYTHONHASHSEED=0` only inside tool-run envs — `plans/round43_c1_verify.py:551`), and under two scratch roots.
**Confirmed: 18/18 runs byte-identical, rc=0, zero envelope violations. Runs = 18.**

## Surfaces verified before running (frozen, unedited)

- Lane clone `S/lane` = `/fast/scratch/hyaku/kengaku-r43/R43RevSiteStable/lane`; `git -C "$S/lane" rev-parse
  --show-toplevel` → `$S/lane`; clone HEAD `d33350f` (wave-1 dispatch, after freeze `02753f2`).
- `git -C "$S/lane" diff --stat 02753f260805e2e45b05af22145da00f91671364 HEAD -- plans/round43_c1_verify.py
  plans/round43_c2_verify.py .ufo/waves/round-43/claims/` → **empty** (frozen zone unchanged since the freeze
  commit; exit 0).
- `sha256sum plans/round43_c1_verify.py` → `1a1cd1f886fd4581170f83dc4a5293276fd9b981f9a6f1235d121b0cc97d6cca`
  (source lane == clone; == `frozen-digests.txt:2`). `w_near.py` → `9a044008…454c3` == `frozen-digests.txt:11`.
- The counter self-checks both tool pins every run: `PINS total=2 mismatched=0` and `PINS-AFTER mismatched=0`
  in all 18 logs.

## Method

Command template (every run inside the round-43 envelope; `$S` = scratch; `TMPDIR=$S`):

```
TMPDIR="$S" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh "$S/env" \
  env PYTHONHASHSEED=<seed> TMPDIR="$S" python3 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py \
  --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/witness \
  --work "$S/<root>/<tag>" --jobs <jobs>
```

Matrix: `--jobs ∈ {1,8,16}` × counter-process `PYTHONHASHSEED ∈ {0,1,42}` × scratch root `∈ {$S/wa, $S/wb}`
(two distinct trees) = 18 runs; driver `logs/matrix.sh` (receipt). Comparison: normalized verdict block =
all log lines except `ENVELOPE ` lines, sha256 per run, plus `diff` of the two extreme runs
(`j1_s0_wa` vs `j16_s42_wb`).

## Result — canonical verdict block (22 lines, identical in all 18 runs; digest of the block `fbe92764c14f42a6`)

```
PINS total=2 mismatched=0
FIXTURE wit-long-row tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE wit-green-erratum tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE wit-slashed-name-url tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE wit-short-commit-url tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE wit-late-claims-edit tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE wit-p2-excuse tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NA1 anchor silence killed by=wit-long-row attributed=L477 value=differs hits=1 -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have
MUTANT NA5 anchor rc-mirror killed by=wit-slashed-name-url attributed=L258 value=differs hits=1 -- plans/anchor_digest_check.py:54-56 'The task component of `<subpath>` is matched **exactly
MUTANT NA7 anchor rc-mirror killed by=wit-green-erratum attributed=L458 value=differs hits=1 -- plans/anchor_digest_check.py:112-113 'no 64-hex token on it may be outside A unless it is
MUTANT NA18 anchor rc-mirror killed by=wit-short-commit-url attributed=L154 value=differs hits=1 -- plans/anchor_digest_check.py:53-54 'a `raw.githubusercontent.com/<owner>/<repo>/<commit>/<
MUTANT NA20 anchor rc-mirror killed by=wit-green-erratum attributed=L468 value=differs hits=1 -- plans/anchor_digest_check.py:108-110 'An erratum for S<id> exempts that row's anchor token
MUTANT NA21 anchor rc-mirror killed by=wit-green-erratum attributed=L456 value=differs hits=1 -- plans/anchor_digest_check.py:108-109 'An erratum for S<id> exempts that row's anchor token
MUTANT NO5 order rc-silence killed by=wit-late-claims-edit attributed=L120 value=differs hits=1 -- plans/order_check.py:14-16 'FAIL when any file committed under `.ufo/waves/round-NN/claims
MUTANT NO7 order rc-mirror killed by=wit-p2-excuse attributed=L60 value=differs hits=1 -- plans/order_check.py:56-57 'The one P10 detail the gate prints before executing anything,
MUTANT NO22 order rc-silence killed by=wit-late-claims-edit attributed=L105 value=differs hits=1 -- plans/order_check.py:15-16 'a gate `P10` line whose detail is anything other than `receipt
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=6/6 order=3/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Equality evidence (command: `for f in "$S"/logs/*.log; do grep -v '^ENVELOPE ' "$f" | sha256sum | cut -c1-16; done`):

- 18/18 blocks digest `fbe92764c14f42a6`, 22 lines each. `diff <(grep -v '^ENVELOPE ' j1_s0_wa.log)
  <(grep -v '^ENVELOPE ' j16_s42_wb.log)` → empty ("IDENTICAL").
- The block is byte-identical to the frozen recorded run: `diff <(grep -v '^ENVELOPE '
  "$S/logs/j16_s0_wa.log") .ufo/waves/round-43/claims/witness-run.txt` differs only by the frozen file's own
  three ENVELOPE wrapper lines (L1's receipt carries them inline); the 22 counter lines match exactly, i.e.
  every killing fixture, attributed span line and `value=differs` reproduces the freeze witness run.
- Per-run envelope exits: all `exit=0`; dev-mode counter exit code 0 in all 18 (`logs/rc.txt`: every line
  `rc=0`).

## ENVELOPE lines (Q32), one per run

Full bwrap command line (identical across runs except `PYTHONHASHSEED`, `--work`, as captured verbatim in each
receipt under `logs/<tag>.log`):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43RevSiteStable/env /fast/scratch/hyaku/kengaku-r43/R43RevSiteStable/env --bind /fast/scratch/hyaku/kengaku-r43/R43RevSiteStable/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- env PYTHONHASHSEED=<seed> TMPDIR=$S python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py --lane $S/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/witness --work $S/<root>/<tag> --jobs <jobs>
```

| run | ENVELOPE start | ENVELOPE end (exit, `~/.local/bin` content digest before/after) |
|---|---|---|
| j16_s0_wa | 19:16:15 | 19:16:19 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j1_s0_wa | 19:16:47 | 19:16:51 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j1_s0_wb | 19:16:53 | 19:16:57 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j1_s1_wa | 19:16:59 | 19:17:03 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j1_s1_wb | 19:17:05 | 19:17:10 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j1_s42_wa | 19:17:11 | 19:17:16 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j1_s42_wb | 19:17:17 | 19:17:22 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j8_s0_wa | 19:17:24 | 19:17:28 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j8_s0_wb | 19:17:30 | 19:17:35 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j8_s1_wa | 19:17:36 | 19:17:41 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j8_s1_wb | 19:17:43 | 19:17:47 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j8_s42_wa | 19:17:49 | 19:17:53 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j8_s42_wb | 19:17:54 | 19:17:58 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j16_s0_wb | 19:17:59 | 19:18:03 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j16_s1_wa | 19:18:05 | 19:18:08 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j16_s1_wb | 19:18:10 | 19:18:13 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j16_s42_wa | 19:18:15 | 19:18:18 exit=0 328be01808ba022f / 328be01808ba022f unchanged |
| j16_s42_wb | 19:18:20 | 19:18:24 exit=0 328be01808ba022f / 328be01808ba022f unchanged |

`grep -l INVALID "$S"/logs/*.log` → no match: no measurement invalidated; the PATH-dir content digest
(`328be01808ba022f`) also equals the digest recorded in the freeze-time witness run, so `~/.local/bin` content
did not change at any point across the session.

## Durations (no site-dependent timing anomaly)

`jobs=1` ≈ 4–5 s, `jobs=8` ≈ 4–5 s, `jobs=16` ≈ 3–4 s per run (from the ENVELOPE start/end pairs above);
wall for the 17-run remainder 98.59 s (`bash matrix.sh`, timed by the shell).

## Verdict

The hypothesis is **confirmed**: verdict invariant across all 18 combinations — same `MUTANTS total=9
killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`, same `MUTANTS-BY-TOOL anchor=6/6 order=3/3`,
same per-mutant kill attributions (fixture + span line + `value=differs`, hits=1). No diff on any compared
line; the counter's development-mode verdict on the frozen witness battery does not depend on scheduler
parallelism, the counter process's own hash seed, or the scratch location.

## Residual risk and gaps

- Both scratch roots sit under the same filesystem (`/fast/scratch/hyaku/kengaku-r43/R43RevSiteStable/wa|wb`);
  a different mount or a path-length-sensitive failure mode is not covered (the counter resolves `--work` with
  `.resolve()` and refuses a lane-inside work dir — `round43_c1_verify.py:720-729` — which bounds the path
  effect).
- Seeds {0,1,42} exercise the counter's own dict/set iteration; they do not cover every Python hash
  randomization state.
- Three runs each at jobs=1/8/16 and the byte-comparison of full stdout blocks (not sampling) — but only the
  22 stable output lines were compared; wall-clock timing is reported, not asserted invariant.
- The lane tip has advanced past the freeze commit (`d33350f` vs `02753f2`); the frozen-diff check above shows
  the frozen zone untouched, and the counter's own PINS/PINS-AFTER held `mismatched=0` throughout.

Receipts: 18 per-run logs + `rc.txt` + `matrix.sh` under
`.ufo/waves/round-43/build/R43RevSiteStable/logs/` (64,073 bytes total, largest file well under 1 MiB;
sha256 of two extremes `35563bf0a0331bf0` (j1_s0_wa.log), `a0dc0f19b32acdc8` (j16_s42_wb.log) — they differ
only in the ENVELOPE command/timing lines).

VERDICT: site-stable-confirmed-runs-18
