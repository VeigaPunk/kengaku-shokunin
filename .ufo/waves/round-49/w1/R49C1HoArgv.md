# R49C1HoArgv — benign argv shape probes

Axis: **calibration** (honest-fixture acceptance/classification).

## Freeze and scope

The committed stage-1 freeze was verified before measurement: `9d2900af41e4d1fc6022eff99010436fde6dbd93` exists in the lane tree, is an ancestor of lane tip `af88aab193e6034cb9b386472064e3c18fa90128`, and its `plans/round-49-claims.md` SHA256 equals the lane file (`7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83`). The measurement clone was checked out at the freeze revision. Fence SHA256: `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

No stage-2 v3 counter/population was present at this freeze, so this is **not a scored R49-C1 run**. I used the round-48 v2 harness only as an unscored per-fixture strace diagnostic with explicit testing overrides; its final predicate is expected to fail because the hostile directories were deliberately empty and this module adds a different population. No R49 admission is claimed.

## Findings

### In-d `..` normalization and environment-token values

The measured probes below were `ADMIT benign touches=0` under the diagnostic harness, as the frozen C1 contract says an admission with zero outside touches is `BENIGN-ADMIT`:

- `repo/../repo`, `x/y/z/../../../repo`, `./repo`, `repo/`, absolute in-d path with and without dot-dot, lane `.` / `sub/../` when `d` itself is a repository.
- Caller-expanded environment token resolving to `repo`; literal `$LANE`, `%LANE%`, and `~` directory names inside `d`; Unicode in-d lane name.
- Valid anchor option placement with `--evidence-ref` before `--lane`; repeated valid `--lane` and `--verbose` forms.
- Fixed-order `order` arguments with in-d `./` and dot-dot spellings in their values.

Representative verbatim receipt lines:

```text
FENCE-RUN honest honest/ho49_argv_shapes.py a01-dotdot-same ADMIT benign touches=0 calls=503 -- ADMIT
FENCE-RUN honest honest/ho49_argv_shapes.py a02-dotdot-phantom ADMIT benign touches=0 calls=503 -- ADMIT
FENCE-RUN honest honest/ho49_argv_shapes.py a08-env-dollar-literal ADMIT benign touches=0 calls=503 -- ADMIT
FENCE-RUN honest honest/ho49_argv_shapes.py a09-env-expanded ADMIT benign touches=0 calls=503 -- ADMIT
FENCE-RUN honest honest/ho49_argv_shapes.py a12-opt-before-lane ADMIT benign touches=0 calls=503 -- ADMIT
FENCE-RUN honest honest/ho49_argv_shapes.py o02-order-dotdot ADMIT benign touches=0 calls=510 -- ADMIT
FENCE-RUN honest honest/ho49_argv_shapes.py o05-order-value-dotdot ADMIT benign touches=0 calls=510 -- ADMIT
```

The fixed `order` tool's required shape is enforced as frozen contract, so option reordering is rejected by the fence. Independent invocation of `order_check.py` with reordered options returned semantic exit 1 (not argparse usage error), confirming its argparse accepts the permutation. Thus the fence's exact-order restriction is an **honest over-refusal** relative to the underlying tool parser, not an outside-access leak:

```text
FENCE-RUN honest honest/ho49_argv_shapes.py o03-order-reorder-GAP BREACH clean touches=0 calls=426 -- BREACH order argv is not the contract shape ['--lane', '--claims', '--receipt']
TOOL-ARGV o03-order-reorder-GAP rc=1 argparse_error=0 stderr=-
FENCE-RUN honest honest/ho49_argv_shapes.py o06-order-eq-GAP BREACH clean touches=0 calls=426 -- BREACH order argv is not the contract shape ['--lane', '--claims', '--receipt']
TOOL-ARGV o06-order-eq-GAP rc=1 argparse_error=0 stderr=-
```

The analogous anchor forms are also accepted by `argparse` but refused by `_argv`'s exact-token parser: `--evidence-ref=index`, `--lane=repo`, and unambiguous abbreviation `--lan repo`. Their direct tool runs reached semantic `USAGE` failures, not argparse failures; the harness reported each fence refusal with zero touches. This demonstrates conservative over-refusal, not an escape:

```text
FENCE-RUN honest honest/ho49_argv_shapes.py a17-evref-eq-GAP BREACH clean touches=0 calls=426 -- BREACH anchor argv token '--evidence-ref=index' is not an exact option
FENCE-RUN honest honest/ho49_argv_shapes.py a18-lane-eq-GAP BREACH clean touches=0 calls=426 -- BREACH anchor argv token '--lane=repo' is not an exact option
FENCE-RUN honest honest/ho49_argv_shapes.py a19-abbrev-GAP BREACH clean touches=0 calls=426 -- BREACH anchor argv token '--lan' is not an exact option
TOOL-ARGV a17-evref-eq-GAP rc=2 argparse_error=0 stderr=USAGE: no staged file under corpus/evidence/ — cannot resolve any digest
TOOL-ARGV a18-lane-eq-GAP rc=2 argparse_error=0 stderr=USAGE: no committed file under corpus/evidence/ — cannot resolve any digest
TOOL-ARGV a19-abbrev-GAP rc=2 argparse_error=0 stderr=USAGE: no committed file under corpus/evidence/ — cannot resolve any digest
```

The most concrete parser inconsistency: the fence admits `--lane ../outside --lane repo` after the dict overwrites the first value, even though its docstring says every argv value stays inside `d`. `argparse` likewise uses the final duplicate value, so this probe did **not** demonstrate an outside touch or actual escape. Record as an unvalidated contract-scope concern, not a security gap:

```text
FENCE-RUN honest honest/ho49_argv_shapes.py a13-dup-outside-dropped ADMIT benign touches=0 calls=503 -- ADMIT
TOOL-ARGV a13-dup-outside-dropped rc=2 argparse_error=0 stderr=USAGE: no committed file under corpus/evidence/ — cannot resolve any digest
```

True outside-normalizing paths (`../outside-repo`, `repo/../../outside`) and a normalized lane that is not a discovered repo were refused with zero touches. Environment-looking strings are passed literally by the fence: if a matching directory exists in `d`, admission is benign; a nonexistent `$UNSET_NAME` lane is refused.

## Exact commands and observed outputs

1. `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` → `Cloning into 'lane'... done.`
2. `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C1HoArgv/lane`.
3. `git -C "$S/lane" checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git -C "$S/lane" rev-parse HEAD` → `9d2900af41e4d1fc6022eff99010436fde6dbd93`.
4. `git -C "$S/lane" merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 af88aab193e6034cb9b386472064e3c18fa90128 && echo FREEZE-IS-ANCESTOR-OF-TIP` → `FREEZE-IS-ANCESTOR-OF-TIP`.
5. `git show 9d2900af41e4d1fc6022eff99010436fde6dbd93:plans/round-49-claims.md | sha256sum` and `sha256sum .../plans/round-49-claims.md` → both `7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83`.
6. `python3 /fast/scratch/hyaku/kengaku-r49/R49C1HoArgv/probe_acceptance.py` → `rc=0`; selected observed lines are quoted above. The driver ran the official `anchor_digest_check.py` and `order_check.py` against built scratch fixtures; no external source was opened.
7. `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py --lane "$S/lane" --work "$S/work" --refusals "$S/empty-refusals" --sealed "$S/empty-sealed" --honest "$S/honest" --jobs 8 --seed 4c1a` → `COUNTER_RC=1`, with:

```text
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
TREE clean
PINS total=82 mismatched=0
FENCE source=/fast/scratch/hyaku/kengaku-r49/R49C1HoArgv/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
HONEST fixtures=145 admitted=132 refused=13 read=0 hung=0 build_errors=0
BENIGN total=132
PREDICATE R48-C1 fail
```

The 13 refusals include both deliberate negative controls and the order/argv over-refusal probes. The failed predicate is not interpreted as an R49 result: overrides intentionally supplied empty hostile populations and a different honest module count.

## Limits and source record

The r49 stage-2 v3 counter was not available at the stage-1 freeze, so these per-fixture classifications are diagnostic results under the prior v2 harness, not the eventual R49 counter's committed receipts. The direct `argparse` probes establish parser acceptance, but do not exercise a successful full gate result; anchor returns semantic no-evidence usage errors on the small fixture. The `order` permutation reaches semantic return 1. The out-and-back `order` case `o04` was malformed for a fixture rooted at `d` and is not used as evidence. The local run had a harmless `PAD-OVERFLOW` because the single module contributed 41 fixture children; it does not affect individual fence verdicts, but do not reuse this module unmodified as a committed population without splitting the fixtures across bounded modules.

Sources opened: local lane artifacts only; no external URL was opened, so no URL/access-date/quote source citation applies.

REV measured: `9d2900af41e4d1fc6022eff99010436fde6dbd93` (uncommitted clone clean at run; no tree-bytes because clean). Scratch cleanup was performed after copying results into this report.

VERDICT: benign in-d dot-dot and environment-token shapes classified `BENIGN-ADMIT`/`touches=0`; option order plus `=`/abbreviation syntax expose real honest over-refusal relative to the gated tools' argparse grammar. No outside-access gap was demonstrated; the duplicate-option drop is a documented contract concern only. No C1/C2 admission claimed.
