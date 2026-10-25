# F35RunC1 — C1 coverage counter (round 35 wave 2 falsify)

Seat: F35RunC1 (executor). Target: re-run `python3 plans/round35_c1_verify.py --lane .`
twice in the lane and twice in a fixture clone at dfee6fff631ebc5f623ba4506e5c7992a215401c
(copy nothing; committed bytes alone). Any lane-vs-clone difference is a finding.

## Lane runs (2)

Repo: /home/vgpnk/Projects/shokunin/kengaku-shokunin (HEAD dfee6fff631ebc5f623ba4506e5c7992a215401c).
Command: `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round35_c1_verify.py --lane .`

Run 1 output (exit 0):

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

Run 2 output (exit 0): byte-identical to run 1 (same 9 lines, `EXIT=0`).

## Fixture clone runs (2)

Fixture recipe followed:

```
D=$(mktemp -d /tmp/k35f-XXXX)          # /tmp/k35f-3ULg
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '*'
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
```

Verified before running: `git -C "$D/lane" rev-parse --show-toplevel` → `/tmp/k35f-3ULg/lane`
(= `$D/lane`); `rev-parse HEAD` → `dfee6fff631ebc5f623ba4506e5c7992a215401c`;
`git status --porcelain` → empty. No fixture commits were needed.

Command: `cd "$D/lane" && python3 plans/round35_c1_verify.py --lane .`

Run 1 output (exit 0):

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

Run 2 output (exit 0): byte-identical. (V6 ran in `--file` mode in the clone, as the
script routes any non-fleet lane path to `validate --file <lane>/corpus/SOURCES.md`.)

## Committed-bytes check (inputs to the counter)

sha256 of six counter input files, lane vs clone: all SAME —
`plans/round35_c1_verify.py`, `plans/tb2_grader_probe.py`, `corpus/SOURCES.md`,
`corpus/README.md`, `corpus/knowledge/tb2-protein-assembly-grader.md`,
`corpus/evidence/round35/tb2-grader-probe.txt`.
Tracked files under `corpus/evidence/round35/tb2-eval/`: 7 in lane, 7 in clone; sha256
lists identical file-for-file (covers SHA256SUMS, test_outputs.py, and captures; V1 also
self-checked SHA256SUMS digests in both trees).

Lane-only untracked files at run time: `.ufo/waves/round-35/falsify*.json/.ready*` and the
falsify report dir itself — none referenced by any check (V1–V6 read only corpus/, plans/, and
the fleet census script).

## Findings

None. No lane-vs-clone difference; no dependency on uncommitted files; the clone passes on
committed bytes alone.

Tooling: no tools installed or updated (python3/git pre-existing; no pacman/uv/npx changes).

VERDICT: c1-lane-pass-clone-pass
