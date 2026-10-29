# Round 52 wave 2 — seat W2RevConfirmations (reviewer, falsify)

Scope: independent re-read of the first two R52-C1 vacuity candidates produced by the frozen
counter. Not other seats' work. Lane bounds: leaf member, no subagent dispatch.

## Commands run

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round52_c1_grader_audit.py --lane .
D=corpus/evidence/round52/graders
grep -nF '<quote>' $D/bn-fit-modify/tests/test_outputs.py
grep -nF '<quote>' $D/build-cython-ext/tests/test_outputs.py
sha256sum $D/bn-fit-modify/tests/test_outputs.py $D/build-cython-ext/tests/test_outputs.py
grep -n '364069f8\|6549f1a8' $D/SHA256SUMS
grep -n 'def test_' <both files> | wc -l
ls corpus/knowledge/tb2-*-grader.md
```
Plus `read` of the grader bytes at ranges covering each test body.

## Counter output (frozen counter, lane tree as of this run)

```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29
  CANDIDATE bn-fit-modify class=V3 presence_only=test_bn_sample_exists,test_learned_dag_structure_exists,test_intervened_dag_structure_exists
  CANDIDATE build-cython-ext class=V2 presence_only=test_repo_cloned
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail
A5 EXCLUDED listed=1 digest_pinned=1 tasks=['sanitize-git-repo']
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail
```

Candidates 1 and 2 in the counter's CANDIDATE list (the list is alphabetical) are `bn-fit-modify`
and `build-cython-ext`. The `R52-C1 fail` and `R52-C1-A5 fail` predicates reflect the still-open
CONFIRMED and PRIOR-ART legs (no confirmations file or prior-art file is in the lane yet); they do
not bear on the two candidates checked here. Note that `CONFIRMED new=0` is measured before my
receipt is copied into the lane tree.

## Candidate 1 — `bn-fit-modify` — CONFIRMED (test-level)

File: `corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py`
sha256 `364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b` (matches `SHA256SUMS` line 3).

- `def test_bn_sample_exists():` line 13. Body lines 14–17: docstring, `bn_sample_path = Path("/app/final_bn_sample.csv")`, then
  line 17 `assert bn_sample_path.exists(), f"File {bn_sample_path} does not exist"` (grep -nF: line 17, verbatim).
- Its only assertion is artefact presence. Confirmed.
- Test-level nuance: `test_learned_dag_structure_exists` (line 20, assert line 24, verbatim) is also presence-only. The
  file as a whole is not vacuous: `test_learned_dag_structure` (line 44) and `test_sampled_data` (line 115) compare content.
  Consistent with Amendment A1's per-test unit. I did not separately verify
  `test_intervened_dag_structure_exists` (line 58) byte-wise; the counter lists it and it is outside my two-candidate scope.
- Lane-novelty check: no `corpus/knowledge/tb2-bn-fit-modify-grader.md` exists. The 12 existing `corpus/knowledge/tb2-*-grader.md` entries are: build-pmars, circuit-fibsqrt, constraints-scheduling, db-wal-recovery, feal-differential-cryptanalysis, feal-linear-cryptanalysis, git-leak-recovery, git-webserver, password-recovery, polyglot-c-py, protein-assembly, regex-log. `bn-fit-modify` is not among them, so the "never read by this lane before this round" leg holds for it.

## Candidate 2 — `build-cython-ext` — CONFIRMED (test-level)

File: `corpus/evidence/round52/graders/build-cython-ext/tests/test_outputs.py`
sha256 `6549f1a8e04b6163ec08877e6f6b9868bf94563f3a3c72ac1fba9c512c31689e` (matches `SHA256SUMS` line 8).

- `def test_repo_cloned():` line 31. Body lines 32–35:
  - line 33 `assert path.exists(), f"{path} does not exist"` (verbatim, grep -nF line 33)
  - line 34 `assert path.is_dir(), f"{path} is not a directory"` (verbatim, grep -nF line 34)
  - line 35 `assert (path / ".git").exists(), f"{path} is not a git repository"` (verbatim, grep -nF line 35)
- All three assertions are presence checks on `/app/pyknotid` and `/app/pyknotid/.git`. Confirmed.
- Test-level nuance: the file as a whole is not vacuous — `test_chelpers` (line 82), `test_ccomplexity` (94),
  `test_cinvariants_python_vs_cython` (113), `test_example_usage` (126) and `test_pyknotid_repository_tests` (140) execute or compare.
  The finding is again per-test.
- Lane-novelty check: no `corpus/knowledge/tb2-build-cython-ext-grader.md` exists.

## Verdict

Both candidates are confirmed by my independent read: each has a test function whose only assertions are
artefact presence, with located quotes that appear verbatim in the captured bytes (A1 check ii), and neither task has a prior
knowledge entry (A1/new-task leg). The weakness is per-test: each grader as a whole contains content-comparing tests.

## Receipt

- Written: `/fast/scratch/hyaku/kengaku-r52/w2-W2RevConfirmations/confirmations.json` (2 records, validated as JSON).
- Copied to: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevConfirmations/confirmations.json`.
- Fields per record: `task`, `test`, `quote`, `line`, `file`, `file_sha256`, `reader` (`W2RevConfirmations`), `confirmed: true`, `note`.

## Negative / limits

- Did not re-run the counter after my receipt; the lane's `CONFIRMED` leg reads `corpus/evidence/round52/confirmations.json`, which the L1 will
  assemble. This receipt is in my seat dir, not the lane tree.
- Did not verify candidates beyond 1 and 2, and did not read other seats' outputs.
- No installs, no git or jj commands, no lane-tree edits.
- Scratch dir `/fast/scratch/hyaku/kengaku-r52/w2-W2RevConfirmations/` removed after the copy.
