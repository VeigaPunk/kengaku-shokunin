# SC1UpstreamContext — round 55 w1 (scout, coverage axis) — upstream context for `chess-best-move`

**Verdict: upstream context at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` fully gathered; every
frozen R55-C3 byte the lane cites is confirmed against upstream. One arithmetic defect found
(`PROVINCE.md` remainder 86 → 76) — reported to its owning seat and **fixed** there; one file
attribution mismatch in the claim's wording — reported and ruled on by the owner (no edit).**

Full findings: `.ufo/waves/round-55/w1/SC1UpstreamContext/context.md`.
Receipts in the same dir: `api-contents-chess-best-move.json`, `upstream-task-list.txt`,
`upstream-file-sha256.txt`, `byte-identity-sweep-89-graders.txt`, `runner-sha-groups.txt`,
`case-prediction-rederivation.txt`.

## What I ran (read-only GETs only; no git/jj mutation; no lane file edited)

| # | command | outcome |
|---|---|---|
| 1 | `curl api.github.com/repos/harbor-framework/terminal-bench-2/contents/chess-best-move?ref=2fd12b88…` | HTTP 200, 8100 B — 7 entries (4 files + 3 dirs) |
| 2 | `curl …/contents/chess-best-move/{solution,tests,environment}?ref=2fd12b88…` | HTTP 200 ×3 |
| 3 | `curl raw…/chess-best-move/task.toml` | HTTP 200, 849 B, sha `d8f01d3c…2f9e` |
| 4 | `curl raw…/chess-best-move/tests/test_outputs.py` | HTTP 200, 971 B, sha `a540714e…f286` — cmp-identical to the lane capture |
| 5 | `curl raw…/chess-best-move/tests/test.sh` | HTTP 200, 608 B, sha `4770437e…c334` — same sha as upstream `regex-log/tests/test.sh` |
| 6 | `curl raw…/chess-best-move/{instruction.md,.gitignore,README.md,environment/Dockerfile,environment/make.py,solution/solve.sh}` | HTTP 200 ×6 |
| 7 | `curl api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1` | HTTP 200, 453 523 B, `truncated=false`, 1038 blobs |
| 8 | `curl api.github.com/repos/laude-institute/terminal-bench-2` | 301 → `harbor-framework/terminal-bench-2`, id 1063848495 |
| 9 | 89× `curl raw…/<task>/tests/test_outputs.py` + `cmp` vs `corpus/evidence/round52/graders/` | 88 identical, 1 intentionally absent (`sanitize-git-repo`, GH013), **0 byte drift** |
| 10 | 89× `curl raw…/<task>/tests/test.sh` | 30 tasks share sha `4770437e…c334`; 59 distinct |
| 11 | 89× `curl raw…/<task>/instruction.md` | 86 332 B; `move.txt` named by 1 task only |
| 12 | 5× `curl raw…/<task>/environment/tests/test_outputs.py` | no multiset-equality in any |
| 13 | static re-derivation of the 12 frozen R55-C3 case predictions from the upstream assertion | 12/12 match, mismatches = 0 |

Exit codes: all `curl` calls exit 0 with HTTP 200 except #8, which returns HTTP 301 (redirect, by
design — the alias resolves to the same repo and the same bytes). No POST, no auth endpoint, no
model-serving call, no benchmark run. Total fetched ≈ 1.02 MB (< 2 MB bound).

## Findings (acceptance)

1. **Tree listing** — `chess-best-move/` at the pin: `.gitignore` (177 B), `README.md` (1909 B),
   `instruction.md` (260 B), `task.toml` (849 B), `environment/` (`Dockerfile` 512 B,
   `make.py` 3651 B), `solution/` (`solve.sh` 7555 B), `tests/` (`test.sh` 608 B,
   `test_outputs.py` 971 B). Repo-wide: **89 top-level task dirs + 3 root files = 92 top-level
   entries**; 1038 blobs; **no `tasks/` prefix** (a fetch with that prefix 404s).
2. **task.toml summary** — `schema_version "1.1"`, `artifacts []`, name
   `terminal-bench/chess-best-move`, `keywords ["games"]`, author **Nicholas Carlini**
   `<nicholas@carlini.com>` (both `[[task.authors]]` and `[metadata]`), `difficulty "medium"`,
   `category "games"`, `tags []`, expert 45.0 min / junior 180.0 min, **verifier timeout 900 s**,
   **agent timeout 900 s**, build timeout 600 s, image `alexgshaw/chess-best-move:20251031`,
   cpus 1 / 2048 MB / 10240 MB / 0 gpus, `allow_internet = true`, `mcp_servers []`, all three env
   tables empty. Every field the claim names matches.
3. **solution dir** — **exists**, one file: `solution/solve.sh` (7555 B). Names only, as scoped.
4. **Neighbour note** — **no other task at the pin carries a `move.txt`-style token artefact.**
   `/app/move.txt` occurs in exactly one of the 94 upstream graders (89 task + 5
   `environment/tests/` variants), and exactly one of the 89 upstream instructions names it. Only
   `chess-best-move` compares an agent-written token file by **order-insensitive full-multiset
   equality** (`sorted(x) == sorted(y)` — one hit across all 94 upstream graders; no grader uses
   `collections.Counter`). Nearest neighbours by class: `extract-moves-from-video`
   (`/app/solution.txt`, Levenshtein ≥ 90 %, similarity not equality), `password-recovery`
   (`/app/recovered_passwords.txt`, `split("\n")` line membership — r45), `feal-linear-cryptanalysis`
   (`/app/plaintexts.txt`, substring membership — r44), `count-dataset-tokens` (substring),
   `gcode-to-text` / `crack-7z-hash` / `mteb-*` (exact single value), `code-from-image`
   (`startswith` + asserts), `db-wal-recovery` (`ids == sorted(ids)`, ordering), `sparql-university`
   (sorted display join). Chess-adjacent but not move-token: `regex-chess` (grades FEN, artefact is
   `/app/re.json`), `winning-avg-corewars`.

## Files I wrote (only these)

- `.ufo/waves/round-55/w1/SC1UpstreamContext/context.md` — the scoped findings
- `.ufo/waves/round-55/w1/SC1UpstreamContext.md` — this report (the `Report:` trailer path)
- `.ufo/waves/round-55/w1/SC1UpstreamContext/report.md` — the contract's report path
- `.ufo/waves/round-55/w1/SC1UpstreamContext/{api-contents-chess-best-move.json,
  upstream-task-list.txt, upstream-file-sha256.txt, byte-identity-sweep-89-graders.txt,
  runner-sha-groups.txt, case-prediction-rederivation.txt}` — receipts

No tracked lane file was created or modified by this seat; `git status` in the lane shows the same
set of sibling-owned modifications as before this seat ran.

## Defects found (reported; this seat edited none of them)

1. **`PROVINCE.md` round-55 paragraph understated the remainder — FIXED by the owning seat
   (E9IndexAndReadme).** `PROVINCE.md:667` read *"the remaining 86 unread TB2 task graders"*
   while the same paragraph narrowed to *"13 of 89 read"*; 89 − 13 = **76**. The "86" was carried
   over from the round-37 paragraph (`PROVINCE.md:277`, "86 … 3 are read") and the earlier
   paragraphs are internally consistent (86/85/83/82/81/80 …), so the round-55 paragraph was the
   odd one out. This seat did not touch `PROVINCE.md`; it reported the defect to the owner, which
   corrected the line to *"the remaining 76 unread TB2 task graders"* — verified by grep after the
   correction landed.
2. **The claim's file attribution for the "12 of 89 → 13 of 89" narrowing does not match the
   repo — owner's ruling: no edit needed.** The frozen R55-C3 after-predicate names
   `PROVINCE.md`; at the base tip `PROVINCE.md` contains **no** "12 of 89" string (its counters are
   phrased "remaining N TB2 task graders (89 carry `tests/test.sh`; M are read)", latest "9 are
   read" at `:611`, "8 of 89 read" at `:557`). The literal "12 of 89 read" is
   `corpus/README.md:444` (round-46 paragraph), and the live README now reads "13 of 89 read" at
   `:445`. E9IndexAndReadme's ruling: the literal "12 of 89 read" is a `corpus/README.md` Frontier
   sub-bullet, PROVINCE's own convention is the "(89 carry `tests/test.sh`; M are read)" phrasing,
   and the frozen claim's narrowing is satisfied by the new PROVINCE section's "13 of 89 read" —
   substance present in both files, no edit made.
3. **Amendment A1's premise verified and broader than stated** (an observation, not a defect): the
   chess runner is byte-identical to the held S109 regex-log runner, and **30 of 89** upstream tasks
   share that exact runner sha — stronger ground for dropping the third SOURCES row than the claim
   states.
4. **No defect in the frozen artefacts.** Grader sha, runner sha, instruction sha and task.toml sha
   all match what the lane already records (S201/S202 rows; `SHA256SUMS:18-19`), and upstream bytes
   are cmp-identical to the lane capture for all 89 tasks the lane holds (the single gap is the
   documented GH013 exclusion of `sanitize-git-repo`, whose upstream sha matches the sha already
   recorded in `SHA256SUMS:158`).

## Dead ends / limits

- `laude-institute/terminal-bench-2` is an alias (301 → `harbor-framework/terminal-bench-2`, repo
  id 1063848495); both raw paths serve identical bytes, so the SOURCES URL choice is cosmetic.
- `tests/test.sh` under a `tasks/` prefix 404s — task dirs live at the repo root.
- The 12-case re-derivation is **static** (the upstream assertion applied to the case bytes in
  plain Python): it independently reproduces the frozen prediction table and the probe receipt's
  `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, but it does **not** execute the grader,
  so it is not itself a substitute for the probe run.
- Upstream `solution/solve.sh` was fetched (needed for the solution-dir answer) but **not** used as
  an oracle source, keeping R55-C3 kill rule (b) clean.
- The KB entry `corpus/knowledge/tb2-chess-best-move-grader.md` does not exist in the working tree
  yet although S201/S202's used-by cell cites it — presumably in flight under E7KnowledgeEntry;
  noted, not touched.

## Scratch

`/fast/scratch/hyaku/kengaku-r55/SC1UpstreamContext/` — created, used, and **deleted** after the
receipts were copied into the seat's output dir. No tool was installed (nothing needed installing);
no `pacman` transaction was run.
