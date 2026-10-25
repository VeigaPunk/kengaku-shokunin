# R31FxTB2Reset — attack on the C1 claim "TB2.0 ships no equivalent reset in 88 of 89 test scripts" (2026-10-25)

Seat: `L1Kengaku31.R31FxTB2Reset` (leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Attacked claim: `corpus/knowledge/benchmark-verifier-execution-model.md:81-83` — "Terminal-Bench 2.0
ships no equivalent script: of its 89 `tests/test.sh` files at the pinned commit, 88 contain no reset
block (wave seat `R31DraftEntry`, report `.ufo/waves/round-31/build/R31DraftEntry.md`), so for that
benchmark the harness upload is the only protection of the test surface."
Target (assignment): fetch a bounded but named sample (>= 8 `tests/test.sh` at the pin), search each for
git checkout/restore/reset, `rm -rf` of test paths, and patch application; report sample, hits, and
whether 88/89 is reproducible or a single seat's count needing narrower attribution.

## Method (all evidence is this seat's own fetch)

Pin: `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (terminal-bench-2). The citation URL
`https://github.com/laude-institute/terminal-bench-2` 301-redirects to
`harbor-framework/terminal-bench-2` (S100 row; re-verified: `curl -sS -o /dev/null -w "%{http_code} %{redirect_url}"` on the API URL -> 403 rate limit, raw fetches below both returned 200). GitHub API was rate-limited
(403, `"API rate limit exceeded for 179.218.13.209"`), so enumeration used the GitHub HTML tree page
instead of the trees API; raw file fetches are SHA-pinned, so content is independent of the API.

- Enumeration: `curl -sSL "https://github.com/laude-institute/terminal-bench-2/tree/2fd12b88aafdd04a52c298e3940bcb189f9766d6"` (tree_page.html, 482 886 bytes) -> 92 root entries: 89 task dirs + `.gitignore`, `LICENSE`, `README.md` (matches S079/S100). Task list saved to `/tmp/r31fx-TB2Reset/tasks.txt` (89 names).
- Fetch: all 89 `tests/test.sh` via `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/tests/test.sh` (this supersedes the >= 8 required sample: the full population was swept). Scratch `/tmp/r31fx-TB2Reset/tests/` — 89 files, 57 647 bytes, 356 KB on disk, under the 60 MB cap. One retry needed (`write-compressor`, first pass returned 88 files; second fetch HTTP 200, 608 bytes).
- Representative checksums (sha256): protein-assembly `9ede4664…`, headless-terminal `bfaa3213…`, mcmc-sampling-stan `349d2c34…`, rstan-to-pystan `6c3d54c3…`, fix-ocaml-gc `9a211472…`, train-fasttext `f7895d4d…`, cancel-async-tasks `79600a6b…`, write-compressor `4770437e…`. Every fetched file invokes `pytest` (`grep -L 'pytest' tests/*.sh` -> empty).

## Search results (full population, not a sample)

Patterns run with `grep -nE` over all 89 files (`tests/*.sh`), each hit file+line quoted below.

1. **git checkout / restore / reset / stash / clean** — `git +checkout|git +restore|git +reset|git +stash|git +clean`
   - **1 hit, 1 file**: `tests/fix-ocaml-gc.sh:20` — `git clone https://github.com/sadiqj/ocaml/ ocaml-original && cd ocaml-original && git checkout tag_purposefully_broken_sweeping_changes && cd ..`
   - All other `git` tokens in the tree are installs: `merge-diff-arc-agi-task.sh:3,5` (`apt-get install -y curl git`), `sam-cell-seg.sh:5,41` (install; `git+https://…MobileSAM.git` as a pip `-w` dep).
   - Zero `git restore`, `git reset`, `git stash`, `git clean` anywhere.
2. **`rm -rf` / `rm -r` / `rm -f` / `rm -fr` / `rm -R`** (incl. `find … -delete`, `rmdir`) — `rm +-[a-zA-Z]*r[a-zA-Z]*|rm +-[a-zA-Z]*f|find .* -delete|rmdir|rm +-fr|rm +-R`
   - **2 hits, same 1 file**: `tests/fix-ocaml-gc.sh:21` — `rm -rf ocaml/testsuite && cp -r ocaml-original/testsuite ocaml/`; `tests/fix-ocaml-gc.sh:27` — `rm tests.txt` (deletes a workdir file before rebuilding).
3. **Patch application** — `git +apply|patch +-p|apply_patch|patch <|applypatch|patch ` — **0 hits across all 89 files**.
4. Adjacent restore-ish mechanisms (extra, beyond the assignment's three): `cp -r|rsync|cp -a` -> only `fix-ocaml-gc.sh:21` (same exception file). Literal words `reset` / `restore` -> 0 hits in the whole tree's `tests/test.sh`.

### What the one exception actually does (not a /tests reset)

`fix-ocaml-gc.sh` (1 160 bytes) lines 18-28: re-clones upstream ocaml at a broken tag, `rm -rf ocaml/testsuite && cp -r ocaml-original/testsuite ocaml/`, `rm tests.txt`, then builds and runs the project's own testsuite, and finally `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`. Its comment ("… copy the testsuite from the original, to stop the model cheating" at lines 18-19, the "to stop the model cheating" clause on line 19) is exactly the seat's quote. **None of its actions touch `/tests`** — the graded test surface. It restores the *project-under-test's* suite, not the verifier's test files.

### /tests-mutating lines found (context, not resets)

- `tests/cancel-async-tasks.sh:17` — `cp /tests/test.py /app/test.py` (copies a test file into the app dir, not a reset).
- `tests/sam-cell-seg.sh:24-26` — `cp /tests/test_metadata.csv .` etc. (copies test inputs out of /tests).
- `tests/train-fasttext.sh:18` — `tar -xzf /tests/private_test.tar.gz -C /tests` (**extracts additional test files into /tests after the harness upload**, before pytest). This contradicts any reading of "the harness upload is the only protection" as "what sits in /tests at grading time is exactly the host upload"; it does not add a *restore/reset* mechanism — 0 of 89 scripts restore anything under `/tests`.

## Verdict on the number

- **88/89 is reproducible, not merely a single seat's count.** Re-derived here by a complete independent sweep of all 89 `tests/test.sh` at the pin: exactly 1 file (`fix-ocaml-gc.sh`) contains any git checkout/restore/reset/stash/clean, any `rm -rf`/`rm -f` of a path, or any cp/rsync restore; 88 files contain none of these under any of the scanned definitions; patch application is absent from all 89. `git apply`/`patch` (the SWE-bench Pro reset's own mechanism) appears in **0** of 89.
- The entry's attribution ("wave seat R31DraftEntry, report .ufo/waves/round-31/build/R31DraftEntry.md") is valid provenance but is **not** the only support: the figure stands independently.
- One nuance the entry understates, not overstates: the single exception does **not** implement an equivalent of SWE-bench Pro's *test-space* reset (its `git checkout HEAD -- "$path"` / `rm -f` walk of tracked+untracked test-code paths). `fix-ocaml-gc` restores the project-under-test's testsuite from an upstream clone; `/tests` is reset by no script at all. So "harness upload is the only protection of the test surface" survives every attempted counterexample (and is in one sense stronger than the 88/89 phrasing implies: 89/89 scripts leave `/tests` unrestored — 88 trivially, the exception by only touching the project tree).
- Scope limits (unchanged from the seat's own disclosure): this is a static-file sweep at one pin; the 89 task Dockerfiles/entrypoints and runtime behavior were not read, so a task could still restore state outside the `tests/test.sh` surface without appearing in this count. The `train-fasttext` tar-into-`/tests` line shows the scripts are not passive pytest wrappers and can mutate `/tests` post-upload, but that mutation is additive, not a reset.

## Evidence index (all under /tmp/r31fx-TB2Reset/)

- `tasks.txt` — 89 task dir names (from tree_page.html, pin SHA).
- `tests/<task>.sh` — 89 pinned `tests/test.sh`, sha256 per manifest (repr. hashes above; full manifest in `manifest.json`).
- `tree_page.html` — pinned GitHub HTML tree (92 root entries).
- Scan commands as recorded above; each hit is a `tests/<task>.sh:<line>` pointer.

VERDICT: The 88/89 figure **survived** — reproduced exactly by a full 89-file sweep at the pin under the narrow (git checkout/reset/stash) and broad (git restore/clean, rm -rf/-f of paths, cp/rsync restore, patch application) definitions; the one exception (`fix-ocaml-gc.sh`) is confirmed verbatim and is the *only* nonzero hit in every category. What **fell** is not the count but any reading that the exception is an equivalent of SWE-bench Pro's test-space reset: it never touches `/tests`, so the entry's "harness upload is the only protection of the test surface" conclusion survives and is if anything understated (0 of 89 scripts restore `/tests`; 88 restore nothing at all). No misattribution found: the number is independently reproducible, not solely the seat's count.
