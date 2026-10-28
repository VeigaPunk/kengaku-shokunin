# C1ScoutAgreement — R52-C1 empirical probe (wave 1)

Seat: `C1ScoutAgreement`. Read-only. No `labels.json` written. No lane-tree edit. No tool install.

## Axes

1. Sample coverage — every sorted index that is a multiple of 5, then the requested 15.
2. Label fidelity — class assigned from claims §C1 prose, not from the counter regexes.
3. Counter fidelity — class taken from the frozen counter's `classify()` / `collect()` record, not from its `CANDIDATES` line.
4. Separability — whether those classes name distinguishable grader phenomena, not only regex partitions.

## Selection

`plans/round52-tasks.json` has 89 tasks. JSON key order equals sorted-name order (checked). Sorted index multiple of 5 yields **18** tasks (indices 0, 5, …, 85), not 15. The seat asked for 15 and for an agreement count out of 15, so the scored set is the first 15 of that rule (indices 0–70). The other three (75, 80, 85) were fetched and classified the same way and agree as well; they are an appendix, not the denominator.

Primary grader for every scored task is `tests/test_outputs.py`. The `environment/tests/test_outputs.py` fallback was not needed (those tasks are `break-filter-js-from-html`, `circuit-fibsqrt`, `schemelike-metacircular-eval`, none of which fall on a multiple of 5).

Pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Bytes fetched from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<path>`.

## Result

**Agreement 15/15. Disagreements: none.** Full multiple-of-5 rule: 18/18, also none.

Scored distribution: V2=9, V3=5, V0=1, V1=0, V4=0.

| idx | task | my label | counter | agree | deciding bytes |
|---:|---|---|---|---|---|
| 0 | adaptive-rejection-sampler | V2 | V2 | yes | L7 `import subprocess`; L73 `subprocess.run` |
| 5 | build-pov-ray | V2 | V2 | yes | L5 `import subprocess`; L15 `subprocess.run` |
| 10 | cobol-modernization | V2 | V2 | yes | L7 `import subprocess`; L55 `subprocess.run` |
| 15 | count-dataset-tokens | V3 | V3 | yes | L9 `Path("/app/answer.txt").read_text()`; no behaviour token |
| 20 | dna-assembly | V2 | V2 | yes | L5 `import subprocess`; L21 `subprocess.run` in `calc_tm` |
| 25 | feal-linear-cryptanalysis | V3 | V3 | yes | L120 `open("/app/plaintexts.txt").read()`; L122 `assert c in data`; no behaviour token |
| 30 | fix-ocaml-gc | V3 | V3 | yes | L15 `exists()` and L17 `read_text()`; content fires before V1 |
| 35 | headless-terminal | V2 | V2 | yes | L2 `import subprocess`; L6 `import requests`; L127 `requests.get` |
| 40 | largest-eigenval | V0 | V0 | yes | no presence/content/behaviour token; 3 `def test_` lines so not V4 |
| 45 | make-mips-interpreter | V2 | V2 | yes | L4 `import subprocess`; L17 `subprocess.Popen` |
| 50 | mteb-leaderboard | V3 | V3 | yes | L12 `open("/app/result.txt")`; L15 `.strip()`; no behaviour token |
| 55 | overfull-hbox | V2 | V2 | yes | L18 `os.system('apt install …')`; L20 `os.system("/usr/bin/pdflatex …")` |
| 60 | polyglot-rust-c | V2 | V2 | yes | L7 `import subprocess`; L24 `os.popen("rustc …")` |
| 65 | pytorch-model-cli | V2 | V2 | yes | L3 `import subprocess`; L43 `subprocess.run` |
| 70 | raman-fitting | V3 | V3 | yes | L17 `open(result_path)`; L18 `json.load(f)`; no behaviour token |

Appendix (same rule, past the requested 15): sam-cell-seg idx 75 V2/V2 (`subprocess.run` L172); sqlite-with-gcov idx 80 V2/V2 (`subprocess.run` L12); video-processing idx 85 V2/V2 (`subprocess.run` L28 in `_test_jump_analyzer_video`).

Feature bits (presence / content / behaviour / `def test_` count) also matched on all 18. Claims-literal regexes were the §C1 prose, not the counter's compiled patterns. Counter labels came from `classify()` on the fetched bytes and from `collect()` records of a scratch-lane run of the copied counter.

## Does the scheme separate?

**As a regex partition, yes, on this sample.** Three classes appear and they are not the same cut: V2 files contain a behaviour token (`subprocess`, `os.system`, `os.popen`, `Popen`, `requests`); V3 files contain a content token and no behaviour token; the one V0 file contains neither, and has 3 test functions so it is not V4.

**As a vacuity triage, no, not on this sample.**

- V1 and V4, the frozen triage queue, are empty here (0/15).
- The only V0, `largest-eigenval` (`cdc58e3a…`, 3951 bytes), is not a vacuous grader. It imports the candidate (`from eigen import find_dominant_eigenvalue_and_eigenvector`, L21), checks `A @ eigenvec ≈ eigenval * eigenvec` (L63–67), checks dominance against `np.linalg.eigvals` (L76–80), and times the candidate in a `ProcessPoolExecutor` (L7, L92). `concurrent.futures.ProcessPoolExecutor` is not in the behaviour marker list, and `np.allclose` / `assert` are not content markers under §C1. Three `def test_` lines (L50, L71, L85) also keep it out of V4. V0 here means "unmarked", not "otherwise weak".
- First match is file-level, so a behaviour token anywhere in the file hides presence-only tests. Read examples: cobol L11–18 and L21–31 only `Path.exists`, while L55 `subprocess.run` forces V2; pytorch L12–27 are three `assert *.exists()` tests, while L43 `subprocess.run` forces V2; mteb L6–7 is presence-only, while L12 `open(` forces V3; headless L68 `assert not path.exists()` sits in a file that also calls `requests.get` (V2). The classes separate files. They do not separate vacuous tests from checking tests inside one file.
- `overfull-hbox` is V2 because the marker is a session fixture (`os.system` at L18 and L20), not inside a `def test_`. The tests themselves compare file text. §C1 applies to the file bytes, so the label is correct under the frozen rule and still not "the tests execute something".

## Counter vs claims prose (observed, did not flip a label)

The counter's compiled patterns are not the prose. On these 18 files none of the extras changed a boolean feature or a class:

- content adds `assert.*\bin\b` (counter L36). It would also match feal L122 `assert c in data`, but feal already matches prose `open(` at L120, so it stays V3 either way.
- presence adds `os.path.isfile` and a leading word boundary. No scored file needed that extra.
- behaviour is `curl ` with a required trailing space, not bare `curl`. No scored file contains `curl`.
- test count is `^\s*def\s+test_` rather than a substring count of `def test_`. Counts matched on all 18, including largest-eigenval (3 source defs; the `@pytest.mark.parametrize` over sizes 2–10 is not 27 functions under either rule).

## What the counter run actually printed

Scratch lane had only these 18 captures (no `SHA256SUMS`, no confirmations, no prior-art). Command:

```
python3 plans/round52_c1_grader_audit.py --lane /fast/scratch/hyaku/kengaku-r52/C1ScoutAgreement/lane
```

Exit 1, as expected for a partial capture set. Its `CLASS V0=72` is **not** a population result: 71 of those V0s are absent captures forced to V0 by `collect()` (`error: capture absent`). The 18 fetched records are V2=12, V3=5, V0=1, which matches the table above (the extra 3 V2s are the appendix).

The script that ran is not the pre-amendment text. Lane HEAD when measured was `07ea2084053f5112ea797a653e6a3a96e8cf4a64`, not the claims base tip `30801b479e3418c11089b8586178b6960216f364`. Worktree counter sha256 `e43ff9e7cd2242ce62b561fbae67e41cb478be156d03ffc412972cdf7593e6be` matched the scratch copy and the HEAD blob (`git hash-object` = `git rev-parse HEAD:plans/round52_c1_grader_audit.py` = `a8df59b79d96377b53aa47a22a251b0c04135fef`). Amendment A1 in `plans/round-52-claims.md` (and the counter's `classify_tests`) moves the *candidate* unit to per-test `P1`. The file-level `class` field is unchanged, and that field is what this comparison used. The run's `CANDIDATES` line (mteb-leaderboard, pytorch-model-cli, raman-fitting, sam-cell-seg) is the A1 presence-only-test queue, not the frozen §C1 V1/V4 queue. This seat did not re-label under A1.

## Digests (fetched primary graders)

| task | bytes | sha256 |
|---|---:|---|
| adaptive-rejection-sampler | 9249 | `547dc6e107f034f41703722aeceb6d0236e3fb69116fc3f2fbaba11884de352f` |
| build-pov-ray | 5157 | `64d6ce107503714ada346e5606832ee886be9950971cf81523e73d8ba28e8d37` |
| cobol-modernization | 3027 | `009180a7092583fc8143bb3ffc3957923aa0d61d0aac3a471f76eeb4aae54a88` |
| count-dataset-tokens | 467 | `5c11065dc97e9266c960548165f15797a8c99c72026173a65ebef0cc924a2212` |
| dna-assembly | 14105 | `5c2d0fd2e5f6303263e9750f67acda7db491ef04841832b4fc62bcfb61b08924` |
| feal-linear-cryptanalysis | 2914 | `f59ebc7218a648582483cee02556c3bc1235e186301376bc3be066ed106ed9f9` |
| fix-ocaml-gc | 809 | `e6031cd07c9962f024f2ae232d0645126bd399df0cd8d3df6a46475b68aa4959` |
| headless-terminal | 3676 | `c6998195e29efb64f41f903b6a727059c4f0ee267f730cd7ffca5c1f7d99ab78` |
| largest-eigenval | 3951 | `cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce` |
| make-mips-interpreter | 3646 | `f1748ff20bfd670af1e1cb935647503eb176a4a14dd15f20935264ad7e4a98f6` |
| mteb-leaderboard | 537 | `b28f8fc8b7614801305813c402be52f4be1e75de6658ecdfdf9383aa793892cf` |
| overfull-hbox | 3752 | `09756f87d1a29df533e86c5c7d5fd14f64acb17b03cabb55921bb2890d368e5d` |
| polyglot-rust-c | 1638 | `baed5e4d0cc0e5809ff41a7df1815d18c65c708a3a3f264428e1cda11ce692f9` |
| pytorch-model-cli | 3181 | `370702c57a4e0c85f70ee37a5c357ae3a5df8480a275bb6263b0376f2f6c093b` |
| raman-fitting | 2029 | `171fae772ccf262aec8ddac5bd2c6c731eed842421f5d8439a330b158c9f8c13` |
| sam-cell-seg | 10136 | `908c4b6aa44e12b6c429c221b92eaa6b150880b9b3d74d9d5ef6869a570f4fd4` |
| sqlite-with-gcov | 2166 | `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` |
| video-processing | 4950 | `09b32dd6eb55db1ca024f63b4bb7ddc8b81dbd6003408892c175c0b3ffd17d30` |

## Commands

- Read `plans/round-52-claims.md` (full, then §C1 and Amendment A1 re-read) and `plans/round52_c1_grader_audit.py`.
- Sorted-index extract: `python3` over `plans/round52-tasks.json` (89 keys, insertion order == sorted, 18 multiples of 5).
- Fetch: `curl -fsSL` of the 18 primary paths into `/fast/scratch/hyaku/kengaku-r52/C1ScoutAgreement/lane/corpus/evidence/round52/graders/`, `xargs -P 8`. Counter and population copied with `cp -a` and `cmp`'d identical to the lane files at copy time.
- Class comparison: imported the scratch copy and applied claims-literal regexes beside `mod.classify`.
- Counter run: `python3 plans/round52_c1_grader_audit.py --lane <scratch lane>` → exit 1.
- Read-only git identity: `git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git hash-object`, `git diff --stat` on the counter and claims file. No mutation.

## Files produced

- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutAgreement.md`
- Same text: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutAgreement/report.md`
- Scratch tree removed after the report was written. No `labels.json`. No installs (pacman guard; nothing needed).

## Unresolved

- Raw GitHub bytes were not independently checked against the pin's git tree object (no `git clone` of terminal-bench-2). Digests above are of the bytes that were classified.
- Lane HEAD had moved off the claims base tip before this seat measured it. The counter compared against is the A1-era file, whose file-level `classify()` still implements the §C1 table.
