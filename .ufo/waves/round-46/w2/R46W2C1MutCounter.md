# R46W2C1MutCounter — C1 counter mutation probe

Axes: calibration counter sensitivity; control discrimination; restoration integrity.

## Setup and pristine

Read the frozen claims file including its `Freeze amendments` section. Scratch clone checks:

```text
TOP=/fast/scratch/hyaku/kengaku-r46/R46W2C1MutCounter/lane
HEAD=42d5043afac952fcb43bf4798757785dd258cf85
```

Pinned counter SHA-256 before mutation: `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`. The pristine command was run inside the required envelope:

```text
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" python3 plans/round46_c1_verify.py --lane . --work "$S/pristine-work" --jobs 8
```

Actual output: exit `0`; `PINS total=65 mismatched=0`; `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=32 contradicted=0`; `PREDICATE C1 pass`. Envelope: `start 02:46:10`; `end 02:46:20 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged`. Full receipt: `receipts/pristine.txt`.

For each mutant below, the same counter invocation was run against its related frozen hostile fence control (`--fence` points into the scratch clone), then against the landed fence with default options. Baseline and restored control runs use byte-identical pristine counter files. Every run used the required envelope; all envelope endings reported `unchanged`, and none returned exit 4 / `INVALID`.

## Results

`before` is the pristine counter digest; `mutant` is the measured mutant copy's digest; every mutant copy was restored and re-hashed to the pristine digest (`ef19380e…`). The `control` column reports the actual `PREDICATE C1` on pristine / mutant / restored runs. The table's final `landed` column is the mutant run against the repaired default fence.

| Mutant (single behavior change) | Matched frozen control | Control output pristine / mutant / restored | Landed-fence mutant result | Killed by |
|---|---|---|---|---|
| Name hiding: default `SystemRandom()` replaced with predictable `random.Random(0)` | `keyed_name.py` | `fail / fail / fail` | `pass`, exit 0 | None; survives |
| Tamper detection: disable empty/NUL-hole/execve-less trace-log guard | `b1_log_erasure.py` | `fail / fail / fail` | `pass`, exit 0 | None; survives |
| Root-wide counting: `_outside` recognizes only `p == root`, not descendants | `b3_module_read.py` | `fail / fail / fail` | `pass`, exit 0 | None; survives |
| Stat tracing: remove `STAT_FAMILY` from `TRACED` | `b5_stat_channel.py` | `fail / fail / fail` | `pass`, exit 0 | None; survives |
| Pending-open decode: skip unfinished calls remaining at end of trace | `b6_killed_open.py` | `fail / fail / fail` | `pass`, exit 0 | None; survives |
| Exit-status verdict: derive BREACH/ADMIT from fence stdout (`_out`) rather than harness status | `b4_stdout_spoof.py` | `fail / fail / fail` | `fail`, exit 1 | Landed default C1 predicate (pristine passes; this mutant fails) |

All five surviving landed-fence runs printed the expected totals, `CALIBRATION advertised=32 contradicted=0`, and `PREDICATE C1 pass`. The exit-verdict mutant printed `REFUSALS total=20 clean=0 leaked=20`, `SEALED total=12 clean=0 leaked=12`, `CALIBRATION advertised=32 contradicted=32`, `PREDICATE C1 fail`.

**Control finding:** no frozen hostile-fence control discriminated any mutant: each matched control returned `PREDICATE C1 fail` on pristine, mutant, and restored bytes. The controls did not show mutation-specific output changes; the keyed controls are still rejected, but the result is the same generic leaked-fixture failure. The landed-fence predicate killed only the stdout/status mutation. Thus the name-hiding, tamper, root-wide, stat-tracing and pending-open regressions survive the measured acceptance detector.

Control receipts and landed-fence receipts (all complete ENVELOPE output, kept under the report subdirectory):
- `receipts/name-pristine.txt`, `name-mut.txt`, `name-restored.txt`, `name-default-mut.txt`
- `receipts/tamper-mut.txt`, `tamper-restored.txt`, `tamper-default-mut.txt`
- `receipts/root-pristine.txt`, `root-mut.txt`, `root-restored.txt`, `root-default-mut.txt`
- `receipts/stat-pristine.txt`, `stat-mut.txt`, `stat-restored.txt`, `stat-default-mut.txt`
- `receipts/pending-pristine.txt`, `pending-mut.txt`, `pending-restored.txt`, `pending-default-mut.txt`
- `receipts/exit-pristine.txt`, `exit-mut.txt`, `exit-restored.txt`, `exit-default-mut.txt`

The retained `receipts/counter-*.py` files are all restored snapshots. Their measured final SHA-256 values, as well as the lane counter after restoration, were `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`. Mutant SHA-256 values observed before restoration: name `e214ed0926152175accb5df390477fd347936d5bfcdc716ee66412be8e30a75b`; tamper `3cd1ac5bcba7e540aa8879040d3b58a96140c0bdc9a14206b8f77c5f7c2bc9e0`; root `cd4e2936e9dbb15d137b6900ef3912807f675095f9b9a8356b753fdfeba989c6`; stat `b83113242bb2bcd86d05283dce9bbb59be9e6f864d6bca6c54979b875abae643`; pending `9ed10e3a802b843598726a3e6496b9d55f146b5c9020d7f23f37352316bd4d3b`; exit `52fe65fdbe5e35648f3e36658d45a0938ebfae7d9a1d6c0d809935604e43da20`.

## Restoration / handling note

An initial edit-tool call was mistakenly anchored to the lane's same-named tracked path rather than the scratch copy. I immediately restored that single line to the pinned bytes; subsequent isolated checks confirmed the lane counter SHA-256 was `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`. All later mutations were made only to unique copies under this report's `receipts/` directory and restored. Scratch cleanup completed via the mandated guard: `DELETE path=/fast/scratch/hyaku/kengaku-r46/R46W2C1MutCounter resolved=/fast/scratch/hyaku/kengaku-r46/R46W2C1MutCounter bytes=606736523 size=578.6MiB` (initial) and again after the landing checks: `DELETE path=/fast/scratch/hyaku/kengaku-r46/R46W2C1MutCounter resolved=/fast/scratch/hyaku/kengaku-r46/R46W2C1MutCounter bytes=606456674 size=578.4MiB`.

No tools installed or updated.

VERDICT: c1-counter-mutants-killed-1/6
