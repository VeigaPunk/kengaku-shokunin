# E14CaptureIdentity — round 55 w1 seat report

## Assignment
Byte-identity receipt for the R55-C3 capture: prove on committed bytes that the in-repo
chess-best-move grader capture is byte-identical to upstream terminal-bench-2 at pin
2fd12b88aafdd04a52c298e3940bcb189f9766d6, and cross-check the runner identity against the
held regex-log runner (S109).

## What I ran
1. `sha256sum` on the three in-repo captures (lane repo, base-tip tree):
   - corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py → `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` (971 B)
   - corpus/evidence/round52/graders/chess-best-move/tests/test.sh → `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` (608 B)
   - corpus/evidence/round52/graders/regex-log/tests/test.sh → `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` (608 B)
   - exit 0. All three equal the frozen claim values.
2. Read-only GETs to raw.githubusercontent.com/harbor-framework/terminal-bench-2/<pin>/…
   (first attempt used a wrong `tasks/` prefix → 404; corrected to repo-root layout
   `chess-best-move/…` confirmed via the git trees API). Fetched chess-best-move
   tests/test_outputs.py, tests/test.sh, instruction.md, task.toml; plus regex-log/tests/test.sh.
   All curls exit 0.
   - upstream test_outputs.py  `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` (971 B)
   - upstream chess test.sh    `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` (608 B)
   - upstream regex-log test.sh `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` (608 B)
   - upstream instruction.md    `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` (260 B)
   - upstream task.toml         `d8f01d3c84ed5836edbb49c6c3b3cc7b5b96d951cf01a0987467c9206fb22f9e` (849 B)
3. `cmp -s` byte-compares in-repo vs upstream: all three pairs IDENTICAL (stronger than hash equality).
4. `curl -fsS https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88aafdd04a52c298e3940bcb189f9766d6`
   → sha `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, committer date 2026-04-30T05:53:30Z,
   message "Add task metadata to task manifests". Pin exists. exit 0.

## Verdict
- pair 1 (test_outputs.py in-repo ↔ upstream at pin): MATCH
- pair 2 (chess tests/test.sh in-repo ↔ frozen sha 4770437e…): MATCH
- pair 3 (runner-identity cross-check: chess test.sh == regex-log test.sh in-repo, both == upstream at pin): MATCH
- pin existence confirmed via GitHub API.

All three sha256 pairs match; zero mismatches. The C3 kill rule (c) (upstream identity
check fails at the pin) does NOT fire.

## Files written
- .ufo/waves/round-55/w1/E14CaptureIdentity/identity.txt (the receipt)
- .ufo/waves/round-55/w1/E14CaptureIdentity/report.md (this file)
- .ufo/waves/round-55/w1/E14CaptureIdentity.md (seat report per contract)

## Defects found
None in the scoped bytes. (Note for L1, not a defect: my first fetch guessed a `tasks/`
path prefix and got 404s; the repo layout is task dirs at root — corrected immediately,
no impact on the receipt.)

## Dead ends
- 404 on `tasks/chess-best-move/...` raw URLs — wrong path guess, resolved via trees API.

## Tooling
No installs/upgrades performed (curl, sha256sum, cmp, python3 all present). Read-only
network GETs only. No git mutations. Scratch dir /fast/scratch/hyaku/kengaku-r55/E14CaptureIdentity
removed after copying the receipt into the wave dir.
