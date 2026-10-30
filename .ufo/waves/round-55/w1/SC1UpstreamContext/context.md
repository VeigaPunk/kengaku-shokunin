# SC1UpstreamContext — upstream context for `chess-best-move` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`

Seat role: scout (coverage axis). Read-only upstream GETs only. No git/jj mutation, no lane file
edited by this seat. All fetches against `harbor-framework/terminal-bench-2` at the frozen pin.

Repo alias note: `laude-institute/terminal-bench-2` is a **301 redirect** to
`harbor-framework/terminal-bench-2` (`api.github.com/repos/laude-institute/terminal-bench-2`
→ `{"full_name":"harbor-framework/terminal-bench-2","id":1063848495,"default_branch":"main"}`);
raw.githubusercontent resolves the old path to the same bytes (HTTP 200, identical sha256s).

---

## 1. Task tree listing at the pin

`GET https://api.github.com/repos/harbor-framework/terminal-bench-2/contents/chess-best-move?ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6`
→ **HTTP 200, 8100 bytes JSON**. Entries:

| type | size | name | blob/tree sha |
|---|---|---|---|
| file | 177 | `.gitignore` | `ecd089e8ac7767b9bdb6f3ac247c8d033f7565ab` |
| file | 1909 | `README.md` | `1893475fa37ab3448cda1389512d64d9993bfc30` |
| dir | 0 | `environment/` | `f3ded5972699a62a0c18620ad866d1aab78d6820` |
| file | 260 | `instruction.md` | `a4af733ba3fba7e241977652939632001a1d162d` |
| dir | 0 | `solution/` | `57ba2dd859050f8d3c277909cbc14702df27f232` |
| file | 849 | `task.toml` | `c8a3d165efd8bac363de2c5e8a42cad058932412` |
| dir | 0 | `tests/` | `c9f4a73cd05333b46577ed6311e08fa01ce6b19d` |

Sub-tree contents (same endpoint, `?ref=` pin):

- `environment/` → `Dockerfile` (512 B, blob `129e56ddb57d3000d672f24bed61911c9f39102f`), `make.py` (3651 B, blob `5a3643467b558ca8c28e4b2a3904b8c8dd10faf3`)
- `tests/` → `test.sh` (608 B, blob `cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57`), `test_outputs.py` (971 B, blob `6ec2300aaac167ebd547a9ccfe00abc6af410a75`)
- `solution/` → **`solve.sh` (7555 B, blob `2abc5c3c2069c0db5ba6105b420e0c04c8764572`)** — names only, as scoped

Whole-repo tree at the pin (`GET .../git/trees/2fd12b88…?recursive=1` → HTTP 200, 453 523 bytes,
`"truncated": false`, **1038 blob entries**): **89 top-level task directories** + 3 root files
(`.gitignore`, `LICENSE`, `README.md`) = **92 top-level entries**. Task-dir names are at the repo
root — there is **no `tasks/` prefix** (a fetch with that prefix 404s). Full task list saved as
`upstream-tasks.txt` in this seat's dir.

File-level sha256 (recomputed from the fetched bytes):

| file | bytes | sha256 |
|---|---|---|
| `tests/test_outputs.py` | 971 | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` |
| `tests/test.sh` | 608 | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| `instruction.md` | 260 | `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` |
| `task.toml` | 849 | `d8f01d3c84ed5836edbb49c6c3b3cc7b5b96d951cf01a0987467c9206fb22f9e` |
| `solution/solve.sh` | 7555 | `53b5c5e2278ca915b0930eedfd44565ca84ef21c7346fd6601434484cf76151f` |
| `environment/make.py` | 3651 | `46b95008df62fac7ca7fd7260baf36519de5718b91a4bde485c8d9b7d37f17c1` |
| `environment/Dockerfile` | 512 | `d5697e7a11399e45f105bf43f40e5c95746d6a8601965ea6935a52b59bbbfa2b` |
| `README.md` | 1909 | `bdf339ea1848c81e884f0f811803ecdeaa3dc741e997bda53841f2816fbafd18` |
| `.gitignore` | 177 | `9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953` |

### Byte-identity against the lane's captured bytes (independent of seat E14CaptureIdentity)

- `chess-best-move/tests/test_outputs.py`: upstream sha256 **==** lane capture
  `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` sha256
  (`a540714e…f286`), and `cmp` reports **byte-identical**. → the frozen R55-C3 kill rule (c)
  (upstream identity at the pin) is not fired by this evidence.
- `chess-best-move/tests/test.sh`: upstream sha256 **==** lane capture sha256 (`4770437e…c334`),
  byte-identical.
- Cross-check: upstream `regex-log/tests/test.sh` at the same pin is **also**
  `4770437e…c334` — i.e. the runner really is byte-identical to the held S109 runner, which is
  exactly what amendment A1 relies on when it drops the third SOURCES row.
- Independent sweep: **all 89** upstream `tests/test_outputs.py` were fetched (390 556 B total)
  and compared byte-for-byte with the lane capture. **0 differ.** The only task with no local
  capture file is `sanitize-git-repo` — and its upstream sha256
  (`57e4904177acac5807b51f7c32444bde1968ba0445855fa4333d9eb73865b59e`) equals the sha already
  recorded in `corpus/evidence/round52/graders/SHA256SUMS:158`, consistent with the lane's
  deliberate GH013 push-protection exclusion (`EXCLUDED.md`); the bytes are **not** present in the
  repo, as documented. The lane's 89-task capture therefore carries no unrecorded byte drift.

## 2. `task.toml` summary

`GET .../raw.../chess-best-move/task.toml` → HTTP 200, 849 bytes, sha `d8f01d3c…2f9e`.

- `schema_version = "1.1"`, `artifacts = []`
- `[task] name = "terminal-bench/chess-best-move"`; description: *"Evaluates the agent's ability to
  analyze a chess position from an image, use a chess engine to find the best move(s), and handle
  multiple valid solutions."*; `keywords = ["games"]`
- `[[task.authors]]` → **Nicholas Carlini** `<nicholas@carlini.com>`; `[metadata] author_name` /
  `author_email` the same
- `[metadata] difficulty = "medium"`, **`category = "games"`**, `tags = []`
- `expert_time_estimate_min = 45.0`, `junior_time_estimate_min = 180.0`
- `[verifier] timeout_sec = 900.0`; `[agent] timeout_sec = 900.0`; `[environment]
  build_timeout_sec = 600.0`
- `[environment] docker_image = "alexgshaw/chess-best-move:20251031"`, `cpus = 1`,
  `memory_mb = 2048`, `storage_mb = 10240`, `gpus = 0`, `allow_internet = true`,
  `mcp_servers = []`
- `[verifier.env]`, `[environment.env]`, `[solution.env]` all empty

Every field the frozen claim names (difficulty medium, games category, author, timeouts) is present
and matches.

## 3. `solution/` dir

**Exists**, one file: `solution/solve.sh` (7555 B). Names only were in scope, so the script body was
not analysed for the report; the single grep of its byte stream for the graded artefact path shows
it writes `/app/move.txt` (`solve.sh:229 move_path = Path("/app/move.txt")`) — noted only as the
existence of an oracle, not used as any oracle source for R55-C3.

## 4. Neighbours: which other tasks carry a `move.txt`-style token artefact

**No other task at the pin carries a `move.txt`-style artefact.** Evidence:

- Grepping the full recursive tree (1038 blobs) for any path containing `move` returns **only**
  `chess-best-move/*` (9 entries) and `extract-moves-from-video/*` (7 entries) — no upstream
  *file* named `move.txt` exists in the repo (the artefact is agent-written at runtime).
- Grepping all **94** upstream `tests/test_outputs.py` blobs (89 task graders + 5
  `environment/tests/` variants) for the string `move.txt` returns exactly **one** hit:
  `chess-best-move/tests/test_outputs.py:22 move_file = Path("/app/move.txt")`.
- The upstream instruction set (all 89 `instruction.md` fetched, 86 332 B) mentions `move.txt` in
  **one** task only — `chess-best-move/instruction.md:1`.

Nearest neighbours, by graded-artefact class (all from the lane's own capture, each verified
byte-identical to upstream at the pin):

| task | artefact | comparison | class |
|---|---|---|---|
| `chess-best-move` | `/app/move.txt` | `sorted(move) == sorted(["g2g4","e2e4"])` — order-insensitive **full-multiset equality** over whitespace-split tokens | **new to this lane** |
| `extract-moves-from-video` | `/app/solution.txt` | Levenshtein similarity ≥ 90 % against an embedded Zork walkthrough | similarity, not equality |
| `password-recovery` | `/app/recovered_passwords.txt` | `split("\n")` line **membership** of one constant (r45) | line membership |
| `feal-linear-cryptanalysis` | `/app/plaintexts.txt` | whole-file **substring** search for 100 decimals (r44) | substring membership |
| `count-dataset-tokens` | `/app/answer.txt` | substring `"79586"` | substring |
| `gcode-to-text` | `/app/out.txt` | `read_text().strip() == "flag{…}"` | exact single value |
| `crack-7z-hash` | `/app/solution.txt` | `content == "honeybear"` | exact single value |
| `mteb-retrieve`, `mteb-leaderboard` | `/app/result.txt` | exactly one line, exact value | exact single value |
| `code-from-image` | `/app/output.txt` | `startswith("bee26a")` + further asserts | prefix + asserts |
| `db-wal-recovery` | `/app/recovered.json` | `ids == sorted(ids)` — **ordering**, not multiset equality | ordering |
| `sparql-university` | query output | `", ".join(sorted(countries))` — sorted *display* | display formatting |

`chess-best-move` is the **only** grader in the entire 94-grader upstream set that compares an
agent-written token file by **order-insensitive full-multiset equality**: a scan for
`sorted(…) == sorted(…)` across all 94 upstream graders yields exactly one hit
(`chess-best-move/tests/test_outputs.py:25`), and no upstream grader uses `collections.Counter`.
The three other `sorted(` users are the `db-wal-recovery` ordering check and two `sparql-university`
display joins. This supports the frozen claim's assertion that the artefact class is new to this
lane (r45's line-membership is a strictly weaker relation: a superset answer passes there, whereas
here a duplicate or an extra token breaks equality).

Other chess-adjacent upstream tasks exist but do **not** grade a move-token file:
`regex-chess` (agent writes `/app/re.json`, regex pairs; the grader compares **FEN** strings, not
moves), `winning-avg-corewars` (parses a simulator's stdout), `extract-moves-from-video` (Zork
text moves, similarity-scored).

## 5. Supporting upstream detail (context only, not claim-bearing)

- `instruction.md` (260 B, single line): *"The file chess_board.png has an image of a chess board.
  It is currently white to move. Write the best move for white to play to /app/move.txt in the form
  [src][dst], for example, e2e4 or h1h8. If there are multiple winning moves, print them all, one
  per line."* — the quote S202 cites is verbatim in it, and its sha256 matches the sha already
  recorded in the lane's S202 row.
- `environment/make.py` renders the board from FEN
  `r1bq1r2/1p3pp1/p1n1p3/3nPkbP/8/P1N5/1P2QPP1/R1B1K2R w KQ - 0 16` (PIL + Noto Sans Symbols).
- `environment/Dockerfile`: `FROM ubuntu:24.04`, `WORKDIR /app`, installs `python3-pip` and
  `pillow==11.2.1`, downloads `NotoSansSymbols2-Regular.ttf` to `/fonts/noto.ttf`, copies `make.py`
  in, runs it, then removes it.
- The task's `tests/test.sh` is **not** task-specific: **30 of the 89** upstream tasks share the
  byte-identical runner sha `4770437e…c334` (the regex-log runner shape). The remaining 59 each
  carry a distinct runner sha. So S109's runner semantics are genuinely shared ground, not a
  chess-only coincidence — this strengthens amendment A1's drop decision.

## 6. Independent re-derivation of the frozen 12-case prediction table

To test the R55-C3 kill rule (b) ("the oracle derives from anything but the captured grader's own
assertions"), the upstream grader's assertion was re-parsed from the **upstream bytes**
(`assert sorted(move) == sorted(["g2g4", "e2e4"])`, target list `['g2g4','e2e4']`) and each of the
12 frozen cases in `plans/round55_c3_chess_probe.py` was evaluated by the grader's own expression
`content.strip().split()` then `sorted(...) == sorted(target)`, with no sandbox and no lane
instrument. Result: **12/12 observed verdicts equal the frozen predictions, mismatches = 0**
(P cases: both-lowercase-two-lines, both-space-separated, reversed-order, whitespace-padded,
crlf-line-endings = 5; F cases: single-move-only, uppercase-white, extra-decoy-move,
duplicate-move, empty-file, instruction-example-h1h8, fullwidth-unicode-digit = 7).

This is a *static* re-derivation: it does not execute the grader, so it does not by itself certify
the probe's receipt. The receipt
`corpus/evidence/round55/chess-best-move-probe.txt` (present in the working tree, written by
another seat) already shows `cases=12 observed_pass=5 observed_fail=7 mismatches=0` /
`PREDICATE R55-C3 pass`, consistent with this re-derivation.

## 7. Defects / observations for the L1 (reported; this seat edited none of them)

1. **`PROVINCE.md` round-55 paragraph understated the remainder — FIXED by the owning seat.**
   The new section (`PROVINCE.md:651-669`) originally read *"the remaining 86 unread TB2 task
   graders"* while the same paragraph narrowed the count to *"13 of 89 read"*; 89 − 13 = **76**,
   not 86. The "86" figure was carried over from the round-37 paragraph (`PROVINCE.md:277`,
   "remaining 86 … 3 are read"), whose own arithmetic is internally consistent
   (86/85/83/82/81/80 …), so the round-55 paragraph was the odd one out. This seat did not edit
   `PROVINCE.md`; it reported the defect to seat **E9IndexAndReadme** (owner), which corrected the
   line to *"the remaining 76 unread TB2 task graders"* (`PROVINCE.md:667`) and confirmed the fix
   (verified by grep after the correction landed).
2. **`"12 of 89 read"` lives in `corpus/README.md`, not `PROVINCE.md`.** The frozen R55-C3
   after-predicate says *"`PROVINCE.md` gains a round-55 partial-frontier paragraph narrowing
   '12 of 89 read' → '13 of 89'"*. At the base tip `PROVINCE.md` contains **no** "12 of 89" string
   (its TB2 counters are phrased "remaining N TB2 task graders (89 carry `tests/test.sh`; M are
   read)", latest "9 are read" at `PROVINCE.md:611`, and "8 of 89 read" at `:557`); the "12 of 89"
   string is in `corpus/README.md:444` (round-46 paragraph) and the live README now reads "13 of 89
   read" at `:445`. So the narrowing is executed in `corpus/README.md` while `PROVINCE.md` gains a
   differently-phrased paragraph — the substance (13 of 89 read) is carried in both, but a
   literal grep of `PROVINCE.md` for "12 of 89"/"13 of 89" would not match the claim's wording.
   **Owner's ruling (E9IndexAndReadme, no edit made):** the literal "12 of 89 read" is a
   `corpus/README.md` Frontier sub-bullet, while PROVINCE's own convention is the
   "(89 carry `tests/test.sh`; M are read)" phrasing; the frozen claim's narrowing is satisfied
   by the new PROVINCE section's "13 of 89 read", and the substance is present in both files.
3. **Amendment A1's premise verified, and broader than stated.** The chess runner is byte-identical
   to the held S109 regex-log runner — and in fact **30 of 89** upstream tasks share that exact
   runner sha, which is a stronger ground for dropping the third row than the claim states.
4. **No defect found in the frozen artefacts.** The grader sha256, the runner sha256, the
   instruction sha256 and the task.toml sha256 all match what the lane already records
   (S201/S202 rows and `corpus/evidence/round52/graders/SHA256SUMS:18-19`), and the upstream
   bytes are byte-identical to the lane capture for all 89 tasks that the lane holds.

## 8. Commands run (all read-only) and their outcomes

| # | command | outcome |
|---|---|---|
| 1 | `curl api.github.com/repos/harbor-framework/terminal-bench-2/contents/chess-best-move?ref=2fd12b88…` | HTTP 200, 8100 B |
| 2 | `curl …/contents/chess-best-move/{solution,tests,environment}?ref=2fd12b88…` | HTTP 200 ×3 |
| 3 | `curl raw…/chess-best-move/task.toml` | HTTP 200, 849 B, sha `d8f01d3c…` |
| 4 | `curl raw…/chess-best-move/tests/test_outputs.py` | HTTP 200, 971 B, sha `a540714e…`, cmp-identical to lane capture |
| 5 | `curl raw…/chess-best-move/tests/test.sh` | HTTP 200, 608 B, sha `4770437e…`; upstream `regex-log/tests/test.sh` same sha |
| 6 | `curl raw…/chess-best-move/{instruction.md,.gitignore,README.md,environment/Dockerfile,environment/make.py,solution/solve.sh}` | HTTP 200 ×6, shas tabulated in §1 |
| 7 | `curl api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1` | HTTP 200, 453 523 B, `truncated=false`, 1038 blobs |
| 8 | `curl api.github.com/repos/laude-institute/terminal-bench-2` | 301 → `harbor-framework/terminal-bench-2`, id 1063848495 |
| 9 | 89× `curl raw…/<task>/tests/test_outputs.py` + `cmp` vs lane capture | 88 identical, `sanitize-git-repo` intentionally absent (GH013), **0 drift** |
| 10 | 89× `curl raw…/<task>/tests/test.sh` | 30 share sha `4770437e…c334`, 59 distinct |
| 11 | 89× `curl raw…/<task>/instruction.md` | 86 332 B; `move.txt` mentioned by 1 task only |
| 12 | 5× `curl raw…/<task>/environment/tests/test_outputs.py` | no multiset-equality in any |
| 13 | static re-derivation of the 12 frozen case predictions from the upstream assertion | 12/12 match, mismatches = 0 |

Total fetched ≈ **1.02 MB** (fulltree 453 523 + graders 390 556 + instructions 86 332 + runners
57 647 + tree listing 8 100 + task files ≈ 17 000 + 5 env variants ≈ 25 000) — under the 2 MB bound.
No POST, no auth endpoint, no model-serving call, no benchmark run. Scratch:
`/fast/scratch/hyaku/kengaku-r55/SC1UpstreamContext/` (deleted after the receipts were copied into
this seat's output dir).
