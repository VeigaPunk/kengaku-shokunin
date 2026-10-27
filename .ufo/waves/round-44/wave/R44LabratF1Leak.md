# R44LabratF1Leak — F1 answer-leak census over the 14 TB2 F1 tasks (pin 2fd12b88)

Seat: leaf labrat (executor), round 44. Hypothesis under test: *among the 14 F1 constant-compare tasks, at least 3 others (besides `feal-linear-cryptanalysis`) have their expected answer derivable from files published in the task directory at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.* No TB2 task, harness or verifier was run; every number below is a static fetch plus a local derivation in scratch.

## Axes named

1. **Leak surface** — which published file class carries the answer: grader (`tests/test_outputs.py`), generator/seed, solution, reference data, README prose.
2. **Derivability cost** — literal copy vs one cheap deterministic computation vs requires the intended task work.
3. **In-image reachability** — whether the leak is also inside the agent's own image (not only the public repo).
4. **Grader strictness** — exactness of the compare (exact / substring / threshold / membership) because that decides how much of a leak is enough.

## Method (observed)

- List re-derived from `.ufo/waves/round-43/build/R43ConsiderThese.md` histogram row `F1 | 14`; the 14 names read out of its table rows 9, 12, 16, 17, 26, 30, 31, 32, 43, 51, 52, 57, 80, 87.
- Tree: `curl https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1` → `.truncated=false`, **1446** blobs; the 14 task dirs hold **127** blobs / **678,336** bytes.
- Fetch: one `curl` per raw URL into scratch. Verification: recomputed git blob SHA-1 (`sha1("blob <len>\0"+bytes)`) for all 127 → **0 mismatches**. Manifest `paths.txt` sha256 `760f34f8d3f6701ccc13bf6faeed9088065951233036525c7ef778cf2a6a7b2f`. One first-pass miss (`vulnerable-secret/tests/test_outputs.py`) retried and verified.
- Classification per task: (a) the grader's deciding line; (b) every other published file that contains the answer literal or reproduces it (mechanical `grep -rnaF` of each answer token + per-task reads of README/instruction/Dockerfile/solution/generator/task-deps); (c) a measured local derivation where the channel is a computation rather than a literal.
- No `docker`, no task image, no network at grade time: "in-image" claims below are from the Dockerfile `COPY`/`rm` lines only, and are labelled `[INFERENCE]` where no container was built.

## Result table (14 rows)

`G` = grader literal (always present in F1). `NT` = published non-test channel. Quotes ≤25 words, line-exact.

| # | task | G line (answer literal) | NT class | NT evidence (file:line — quote) | cost |
|---|---|---|---|---|---|
| 1 | `chess-best-move` | `test_outputs.py:25` — `sorted(["g2g4", "e2e4"])` | generator + README | `environment/make.py:118` — `"r1bq1r2/1p3pp1/p1n1p3/3nPkbP/8/P1N5/1P2QPP1/R1B1K2R w KQ - 0 16"`; `README.md:21` — "there are two valid checkmate moves (`g2g4` and `e2e4`)" | **measured**: 1-line mate search on the published FEN |
| 2 | `code-from-image` | `test_outputs.py:28-30` — `bee26a133f…ce3defe` | solution + README | `solution/solve.sh:27,30,33` — `SALT = b"0000TBENCH-SALT"`; `H = sha256(h0, h0[:10], SALT)`; `README.md:32` full hash | **measured**: recompute from published `code.png` |
| 3 | `count-dataset-tokens` | `test_outputs.py:8` — `expected_output = "79586"` | README | `README.md:21` — "the correct integer token count (79586)" | literal |
| 4 | `crack-7z-hash` | `test_outputs.py:25` — `content == "honeybear"` | data + solution + README | `environment/task-deps/secrets.7z` (7zAES, 215 B); `solution/solve.sh:31` — `7z x -p1998`; `README.md:24,28` — `"honeybear"` / "password is \"1998\"" | **measured**: extract archive with published password |
| 5 | `feal-linear-cryptanalysis` | `test_outputs.py:4-103` (100 constants), `:122` `assert c in data` | generator | `environment/task-deps/gen.py:12` — `keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]`; `:18-28` seeded hash chain | **measured earlier** (`feal-linear-probe.txt:11,12` = pass) |
| 6 | `fix-git` | `test_outputs.py:19` md5(a)==md5(b), refs `:28,:37` = `/app/resources/patch_files/*` | in-image reference + solution | `environment/Dockerfile:9` — `COPY resources /app/resources`; `environment/setup.sh:8-9` — `cp /app/resources/patch_files/about.md …` | copy two shipped files |
| 7 | `fix-ocaml-gc` | `test_outputs.py:19` — `"40 tests passed" in tests_contents` | solution + README | `solution/solve.sh:8` — `sed -i '650s/Whsize_hd(hd)/wh/' …/shared_heap.c`; `README.md:26` | apply published one-line patch `[INFERENCE]` (no OCaml build run) |
| 8 | `gcode-to-text` | `test_outputs.py:17` — `"flag{gc0d3_iz_ch4LLenGiNg}"` | README only | `README.md:36` — "contains exactly the expected flag: `flag{gc0d3_iz_ch4LLenGiNg}`"; no literal in `text.gcode` (grep 0 hits) | literal from README; geometry needs the intended render |
| 9 | `log-summary-date-ranges` | `test_outputs.py:8-23` — `EXPECTED_ROWS` (15 counts) | generator | `environment/log_generator_deterministic.py:72-74` — `seed = date.year*10000+…`; `random.seed(seed)`; `Dockerfile:12-13` deletes it from the image | **measured**: re-ran generator → 15/15 exact |
| 10 | `mteb-leaderboard` | `test_outputs.py:11` — `"GritLM/GritLM-7B"` | README | `README.md:24` — "the correct model name: `GritLM/GritLM-7B`" | literal |
| 11 | `mteb-retrieve` | `test_outputs.py:11` — `"MTEB: Massive Text Embedding Benchmark"` | README | `README.md:33` — "matches the expected value: \"MTEB: Massive Text Embedding Benchmark\"" | literal |
| 12 | `password-recovery` | `test_outputs.py:18` — `"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses` | generator (build script) + README | `environment/setup.sh:25` — `echo "PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54" > …`; `:30` — `# Split after "PASSWORD=8XdP5"`; `README.md:31`; `Dockerfile:18` `rm /app/setup.sh` | literal |
| 13 | `sqlite-db-truncate` | `test_outputs.py:8-17` soln, `:31` `score > 6` | data | `environment/trunc.db` (4096 B, ships via `Dockerfile:6`, published); raw `testword` scan yields all pairs; `README.md:38` gives one pair | **measured**: 8/8 pairs, 0 parser deps |
| 14 | `vulnerable-secret` | `test_outputs.py:21` — `FLAG{b4ff3r_0v3rfl0w_m4st3r_k3y_2024}` | source + README | `environment/vulnerable.c:6-11` `encrypted_key[]`, `:15` `const unsigned char xor_key = 0x42`; `README.md:28` full flag; `Dockerfile:23` `rm vulnerable.c` | **measured**: XOR the published array |

**Counts.** G (grader literal): **14/14**. Any published non-test channel: **14/14**. Recomputable from a published artefact (generator/solution/data/source, i.e. no literal copy needed): **10/14** (rows 1, 2, 4, 5, 6, 7, 9, 12, 13, 14). README prose states the answer verbatim: **10/14** (rows 1, 2, 3, 4, 7, 8, 10, 11, 12, 14). Inside the agent's own image without `/tests`: **1 confirmed by Dockerfile lines** (row 6) `[INFERENCE: no image built]`. `no-leak`: **0**.

## Measured derivations (with envelope lines)

All derivation scripts write only into `/fast/scratch/hyaku/kengaku-r44/R44LabratF1Leak/env`; each run was wrapped in the round-44 envelope. Receipts copied to `.ufo/waves/round-44/wave/R44LabratF1Leak/receipts/`.

1. **`log-summary-date-ranges` — the published generator alone reproduces all 15 grader counts.** Copied the published generator, changed only `output_dir` to scratch, ran it (164 files), counted `[ERROR]/[WARNING]/[INFO]` per date file, applied the four ranges + total.
   - `files 164` / `rows==EXPECTED True of 15` / all 15 rows `OK` (e.g. `['total','INFO','56621'] == ['total','INFO','56621']`).
   ```
   ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratF1Leak/env /fast/scratch/hyaku/kengaku-r44/R44LabratF1Leak/env --bind /fast/scratch/hyaku/kengaku-r44/R44LabratF1Leak/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r44/R44LabratF1Leak/der/derive_logsummary.py
   ENVELOPE start 20:36:43 cwd=/home/vgpnk/Projects/shokunin
   ENVELOPE end 20:36:44 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
   ```
2. **`crack-7z-hash` — published archive + published password = the grader constant.**
   - `archive sha256 a2e13fcbb4c2c8e92b1bf9d78ec91376705d1f5631d5bd4de64f82aa0553b773`, `7z rc 0`, `content 'honeybear' … match True`.
   ```
   ENVELOPE start 20:36:49 cwd=/home/vgpnk/Projects/shokunin
   ENVELOPE end 20:36:51 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
   ```
3. **`code-from-image` — the answer is a hash of the published image, no OCR.** Reproduced `solve.sh:27-33` (`h0=sha256(png)`, `H=sha256(h0+h0[:10]+b"0000TBENCH-SALT")`).
   - `image bytes 95041` / `computed bee26a133f103b9ecda444c70ec22cafef6e31a3de7af6d047974dc90ce3defe` / `match True`.
   ```
   ENVELOPE start 20:36:49 cwd=/home/vgpnk/Projects/shokunin
   ENVELOPE end 20:36:51 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
   ```
4. **`chess-best-move` — the FEN published in `make.py:117-118` fixes the answer.** `uv run --with chess` (ephemeral, cache inside the envelope) enumerated legal moves and checkmate-in-one.
   - `checkmate-in-one moves ['e2e4', 'g2g4']` / `grader expects ['e2e4', 'g2g4'] match True`.
   ```
   ENVELOPE start 20:37:10 cwd=/home/vgpnk/Projects/shokunin
   ENVELOPE end 20:37:12 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
   ```
5. **`sqlite-db-truncate` — the shipped/published `trunc.db` carries all eight graded pairs; the grader passes at 7.**
   - `trunc.db bytes 4096 testword hits 9`; `pairs [{"testword02":10.0} … {"testword09":0.5}]`; `matching grader pairs 8 of 8; grader passes at score>6 -> True`.
   ```
   ENVELOPE start 20:37:43 cwd=/home/vgpnk/Projects/shokunin
   ENVELOPE end 20:37:45 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
   ```
6. **`vulnerable-secret` — XOR the published source array with the published key.** Decoded `encrypted_key[]` (`vulnerable.c:6-11`) with `0x42` (`:15`): `b'FLAG{b4ff3r_0v3rfl0w_m4st3r_k3y_2024}\x00'` — byte-identical to `test_outputs.py:21`. (Plain read + `struct`; no envelope needed since nothing was written; output re-checked inside the sqlite/envelope run's bwrap namespace by identical byte compare.) `[INFERENCE: python XOR done in the fleet shell, not under bwrap — read-only computation]`
7. **`feal-linear-cryptanalysis`** — not re-run here (frozen probe, cannot be modified): `corpus/evidence/round44/feal-linear-probe.txt:11` `CASE decrypt-public-keys … observed=pass`, `:12` `CASE replay-public-gen … observed=pass`, `:24` `cases=14 observed_pass=8 observed_fail=6 mismatches=0`.

## Novel findings (beyond "the grader contains the constant")

- **N1 — the answers are re-published in prose that carries no canary.** `grep -c 'BENCHMARK DATA SHOULD NEVER APPEAR\|canary'` over all 14 `README.md` and all 14 `instruction.md` returned **0** for every file, while the graders all open with the canary. 10/14 READMEs state the expected answer literally (rows 1, 2, 3, 4, 7, 8, 10, 11, 12, 14). The "do not train on this" marker protects the file that holds the assertion, not the file that holds the answer.
- **N2 — the only in-image shortcut is `fix-git`, and it is a copy.** `Dockerfile:9` ships the grader's own reference (`/app/resources/patch_files/*`), `setup.sh:8-9` is left at `/app/setup.sh` (never removed) and contains the exact `cp` that produces the graded bytes, and the grader compares md5 of those two files (`test_outputs.py:19,28,37`). No git forensics needed: two `cp`s, one commit. `[INFERENCE: image not built; from Dockerfile/setup.sh lines]`
- **N3 — "deleted from the image, published in the repo" is a cosmetic anti-cheat, twice.** `feal-linear` (`Dockerfile:13-14` `rm orig_plaintexts.txt`, `rm gen.py`) and `log-summary-date-ranges` (`Dockerfile:12-13` `rm -f /app/log_generator_deterministic.py`) both delete a deterministic generator that is published, and in both cases the generator alone reproduces the graded answer — measured for log-summary (15/15), measured earlier for feal (`gen.py` keys + counter hash chain, probe `:11-12`).
- **N4 — four "reasoning" tasks are a fixed transform of a published artefact** (chess FEN→mate search, code-from-image `sha256(image‖salt)`, crack-7z `7z x -p1998`, vulnerable XOR-0x42). Each is ≤6 lines with no task-specific skill; all four measured above.
- **N5 — grader strictness is looser than the class name suggests.** `feal-linear` `:122` accepts each constant as a *substring of the whole file* (no line, count or order check; 100 wrong-key decoys still pass — probe `:15`); `count-dataset-tokens:11` is `in actual_output` (a superset file passes); `password-recovery:18` is list membership over an unbounded file (brute-force list passes); `sqlite-db-truncate:31` is `score > 6` of 8; `fix-ocaml-gc:19` is a string in a log, guarded only by `tests/test.sh:25-28` regenerating it.
- **N6 — `gcode-to-text` is the one task where the published artefact does not hand over the answer cheaply.** The flag is in no file of the tree except `README.md:36` and the grader (`grep -rn 'gc0d3'` = 2 hits). My own top-layer projection of the published `text.gcode` (47,315 extruding points, 894 in the top 2.9 mm) produced no legible glyphs, and the side/height projections show a slanted solid only — so here the non-test leak really is the README prose, not the data.

## Risks / limits (stated, not hidden)

- No TB2 task, harness or verifier was executed and no image was built: rows 6 and 7 are read off Dockerfile/`solve.sh` lines (`[INFERENCE]` for runtime effect).
- `mteb-leaderboard` / `mteb-retrieve` / `count-dataset-tokens` answers were not recomputed (network, HF datasets, mteb results repo); their leak is the literal in README/grader only.
- README is published but is *not* copied into the task image by any Dockerfile in the 14; "public repo" and "in-image" are kept separate above for that reason.
- Verdict counts any published task-dir file, per the assignment's own parenthetical that lists "the answer in the tests" as a qualifying leak; the stricter non-test count is 14/14 as well, and the compute-only count is 10/14.

## Files

- Written (lane): `.ufo/waves/round-44/wave/R44LabratF1Leak.md`, `.ufo/waves/round-44/wave/R44LabratF1Leak/receipts/{log-summary-derive,crack-7z-derive,code-from-image-derive,chess-derive,sqlite-derive}.txt` (5 receipts, 20 KB total).
- Lane corpus/plans/state: **no changes** (read-only seat; no git/jj command run in the lane, no clone).
- Scratch `/fast/scratch/hyaku/kengaku-r44/R44LabratF1Leak` (fetched tree, `files/`, derivation scripts) deleted via `scratch_guard.py safe-rm` at the end of this seat.
- No tool installed or upgraded; `uv run --with chess` was ephemeral (cache inside the envelope scratch).

VERDICT: f1-answer-leaks-14/14
