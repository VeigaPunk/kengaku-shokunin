# SentinelReceiptsR80 — receipt integrity and scope audit

Axes: coverage (six located replays), calibration (honest provenance). Read-only audit; no remediation or gate judgment.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`.
Measured master: `6669fe72e59718acc1a0f32a92849a544b0b2f1c` (output of `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`). All measurements below pin this commit, not the concurrently changing worktree.
Base: `dce7c275381c669e6489f1b795b1505d0824c262`.

## Findings

### Medium — mint provenance can name a tree other than the executed checkout

Command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:plans/round80_c1_remint.py`.
Observed code: line 83 checks `git status --porcelain` once; line 87 takes `git rev-parse master`, not HEAD; line 97 starts the member loop; lines 134–135 unconditionally emit that tip and `WORKTREE clean`; line 146 writes each receipt inside the loop.
Exploit path [INFERENCE, not executed]: invoke the driver in a clean detached checkout or other branch whose HEAD differs from master. It executes worktree tools while stamping master; both commits may still be ancestors of the eventual measured tip. A single clean entry check also does not establish per-probe cleanliness after earlier receipts are written.
Impact: `LANE_TIP` is not reliably the executed checkout; `WORKTREE clean` is only an entry-time assertion, not independently authenticated historical state. This is a producer provenance weakness, NOT evidence that the six existing observations were forged. All six existing tool hashes match tip and stamped-commit tools.
Smallest remediation: stamp HEAD and ensure the executed snapshot equals that commit; run measurements before writing receipts (or in a separate clean snapshot), then publish. This report does not change frozen requirements or gates.

### Informational — historical cleanliness is not recoverable from a commit alone

All six stamps say `WORKTREE clean`. Git commits preserve trees, not the original process's status output. Therefore original mint-time cleanliness cannot be independently certified from these bytes. Current shared worktree status was dirty, but that is later concurrent work and does not prove a false mint-time stamp.
Command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain`.
Observed output at audit start:
```
 M plans/round80-restamp.json
?? .ufo/waves/round-80/w1.ready
?? .ufo/waves/round-80/w1.ready.dispatched
?? corpus/evidence/round80/r79-c1-after.txt
?? corpus/evidence/round80/r79-c2-after.txt
```

## Independent hash and ancestry checks

One shared clone only:
```
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane
# rc 0, done.
git -C /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane rev-parse --show-toplevel
# /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane
git -C /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane checkout --detach 6669fe72e59718acc1a0f32a92849a544b0b2f1c
# rc 0, HEAD is now at 6669fe72
```
For each member below, ran `sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/<historical>` and `sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/<tool>` using its frozen table paths. Exact digest outputs (both equal their receipt stamps):

### cancel-async-tasks
```
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round61/cancel-async-probe.txt
3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round61/cancel-async-probe.txt
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round61_c1_cancel_probe.py
92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round61_c1_cancel_probe.py
```
### chess-best-move
```
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round55/chess-best-move-probe.txt
de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round55/chess-best-move-probe.txt
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round55_c3_chess_probe.py
7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round55_c3_chess_probe.py
```
### distribution-search
```
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round58/kl-probe.txt
3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round58/kl-probe.txt
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round58_c2_kl_probe.py
51c192f2f98186acb439cb69c2e0370860c362e3bdcb267afea93cd547fa6760  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round58_c2_kl_probe.py
```
### largest-eigenval
```
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round57/eigen-probe.txt
463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round57/eigen-probe.txt
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round57_c2_eigen_probe.py
4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round57_c2_eigen_probe.py
```
### openssl-selfsigned-cert
```
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round59/openssl-probe.txt
ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round59/openssl-probe.txt
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round59_c1_openssl_probe.py
6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/round59_c1_openssl_probe.py
```
### protein-assembly
```
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round35/tb2-grader-probe.txt
2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/corpus/evidence/round35/tb2-grader-probe.txt
$ sha256sum /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/tb2_grader_probe.py
acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0  /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane/plans/tb2_grader_probe.py
```

For EACH of the six receipts, command:
`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 6250e94b2adaff8cd22d32f7ab45024f092e3235 6669fe72e59718acc1a0f32a92849a544b0b2f1c`
returned rc 0, no output. Each stamp has this same ancestor. Comparing `git show 6250e94b2adaff8cd22d32f7ab45024f092e3235:<tool>` with pinned-tip tool bytes gave equality for all six.

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --name-only af51132d8919cedd14d3d3407ae5abc966d5d427 6669fe72e59718acc1a0f32a92849a544b0b2f1c -- plans/round80_probes.json` returned rc 0, empty output.
All six COMMANDs name the table's instrument, expected argument shape and member-specific scratch paths; protein uses the frozen `uv run --no-project --with biopython python3` prefix. Those shared remint-work paths are historical command metadata, not paths used by this seat.

## Fresh observation comparisons (two members)

Both run concurrently from `/fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/lane` with `TMPDIR=/fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80`, `PYTHONDONTWRITEBYTECODE=1`; only own scratch receives output. Exact commands and stdout:

```
$ python3 plans/round55_c3_chess_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/chess-best-move.work --receipt /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/chess-best-move.txt
CASE both-lowercase-two-lines predicted=P observed=P rc=0
CASE both-space-separated predicted=P observed=P rc=0
CASE reversed-order predicted=P observed=P rc=0
CASE single-move-only predicted=F observed=F rc=1
CASE uppercase-white predicted=F observed=F rc=1
CASE extra-decoy-move predicted=F observed=F rc=1
CASE duplicate-move predicted=F observed=F rc=1
CASE whitespace-padded predicted=P observed=P rc=0
CASE empty-file predicted=F observed=F rc=1
CASE crlf-line-endings predicted=P observed=P rc=0
CASE instruction-example-h1h8 predicted=F observed=F rc=1
CASE fullwidth-unicode-digit predicted=F observed=F rc=1
cases=12 observed_pass=5 observed_fail=7 mismatches=0
PREDICATE R55-C3 pass
```
Exit 0; stderr ''; complete OBSERVATIONS block equality after removing only frozen `REV <commit>` lines: True.

```
$ python3 plans/round58_c2_kl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/distribution-search.work --receipt /fast/scratch/hyaku/kengaku-r80/SentinelReceiptsR80/distribution-search.txt
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE sol predicted=P/P/P/P observed=P/P/P/P ok
CASE uniform predicted=P/P/P/F observed=P/P/P/F ok
CASE kb-only-m7 predicted=P/P/P/F observed=P/P/P/F ok
CASE minzero predicted=P/P/F/F observed=P/P/F/F ok
CASE negatom predicted=P/P/F/F observed=P/P/F/F ok
CASE nanatom predicted=P/P/F/F observed=P/P/F/F ok
CASE sumdrift predicted=P/P/F/P observed=P/P/F/P ok
CASE wrongvocab-m5 predicted=P/F/P/F observed=P/F/P/F ok
CASE twod predicted=P/F/P/P observed=P/F/P/P ok
CASE maxover predicted=P/P/F/F observed=P/P/F/F ok
CASE tolbnd predicted=P/P/P/P observed=P/P/P/P ok
CASE intcounts predicted=P/P/F/P observed=P/P/F/P ok
cases=12 legs=48 mismatches=0 setup=0 predicted_u=0
PREDICATE R58-C3 pass
```
Exit 0; stderr ''; complete OBSERVATIONS block equality after removing only frozen `REV <commit>` lines: True.

No mismatch or hand-edit signal found in either full block. The other four observations were not independently replayed by this seat; their provenance/hash checks alone do not prove execution.

## Historical and scope sweep

Command:
```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --name-status dce7c275381c669e6489f1b795b1505d0824c262 6669fe72e59718acc1a0f32a92849a544b0b2f1c -- corpus/evidence/round35/ corpus/evidence/round55/ corpus/evidence/round57/ corpus/evidence/round58/ corpus/evidence/round59/ corpus/evidence/round61/
```
Output empty, rc 0: no historical receipt edits in any of the six directories.

Command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --name-only dce7c275381c669e6489f1b795b1505d0824c262 6669fe72e59718acc1a0f32a92849a544b0b2f1c`.
Filtering resulting paths for exact `MANIFEST.json` or `templates/` / `scripts/` prefixes yielded `[]`. No such edits.

Command used for the content corpus: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --unified=0 dce7c275381c669e6489f1b795b1505d0824c262 6669fe72e59718acc1a0f32a92849a544b0b2f1c`. Python inspected added lines (excluding `+++`) with:
- credentials: PEM private-key headers, AWS AKIA/ASIA key shapes, long sk- tokens, and quoted password/api_key/access_token/secret assignments → 0 hits;
- `/tmp(?:/|\b)` → 4 hits, all assignment text in wave dispatch/spec saying NOT to use temporary evidence; no new evidence pointer;
- write-like statements (`write_text|write_bytes|open\(|rm -|git -C|cd |--lane |--receipt `) followed by fleet-root paths or `../` → 6 hits, all dispatch/spec assignment text, not write operations.
Whole changed-file scanning additionally surfaced older README temporary references and existing registry checks; base-to-tip added-line inspection excludes these inherited bytes. No credential or new forbidden write found by this bounded sweep.

## Limits and disposition

Cannot certify original worktree cleanliness, human edit history, absence of arbitrary-format secrets, or runtime writes by other processes outside this lane from committed lane bytes. No operating-system audit log was available; no sibling or fleet-root mutation was performed to test a scenario. Did not run C1/C2 counters, mutate fixtures, judge claims, or invoke another runtime. `resume_continuity_v1` is not on this assigned receipt surface.
All exercised commands exited 0; no replay failure occurred. Two full replay blocks, all twelve digests, six ancestor checks, historical directory immutability and bounded forbidden-content/path sweeps resisted the performed checks. Provenance weakness above remains static-analysis evidence, not an operational exploit demonstration.
No tools installed or updated. Only this report was written in the lane; scratch clone and outputs are deleted before yield.

Self-evaluation: accuracy 4 (historical state unknowable); completeness 4 (two replays, required minimum; four not replayed); clarity 4 (explicit inference/observation separation); actionability 4 (producer fix identified, not authorized); conciseness 4 (full replay/hash evidence retained). Overall 4.0; original mint process records would improve provenance confidence.
