# R31FxQuoteS100 — falsification of the S100 claims in `benchmark-verifier-execution-model.md`

Seat: `L1Kengaku31.R31FxQuoteS100` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Target: the S100 registry row (`corpus/SOURCES.md:113`) and the entry's Terminal-Bench 2.0 claims
(`corpus/knowledge/benchmark-verifier-execution-model.md:81-83`) at pinned commit
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
Scratch: `/tmp/r31fx-quotes100/` (360 KB test.sh capture + JSON evidence, under the 60 MB cap).
No tool installed or upgraded (used pre-existing `gh` CLI, authenticated, and `curl`).

## Re-fetch 1 — root listing split 92/89/3 (claim: `SOURCES.md:113`, "repository root listing… one contents API call")

Command (one contents API call for that ref):

    gh api "repos/laude-institute/terminal-bench-2/contents?ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6" --jq '.[] | [.type,.name] | @tsv'

Result: 92 total entries — **89 directories** and **3 files**: `.gitignore`, `LICENSE`, `README.md`.
The split claim survived exactly.

Cross-check (independent enumeration, second API call): recursive git tree at the same ref:

    gh api "repos/laude-institute/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"

→ 1 446 entries, `truncated: false`; 92 top-level paths (89 task dirs + the same 3 files).
Consistent.

## Re-fetch 2 — 301 redirect to harbor-framework (claim: `SOURCES.md:113`)

    curl -sI https://github.com/laude-institute/terminal-bench-2
    → HTTP/2 301
    → location: https://github.com/harbor-framework/terminal-bench-2

    curl -s -o /dev/null -w "final=%{url_effective} code=%{http_code} redirects=%{num_redirects}\n" -L https://github.com/laude-institute/terminal-bench-2
    → final=https://github.com/harbor-framework/terminal-bench-2 code=200 redirects=1

Claim survived.

## Re-fetch 3 — tree-sha equality (claim: `SOURCES.md:113`, "whose root tree sha equals the pinned commit's tree")

    gh api "repos/laude-institute/terminal-bench-2/git/commits/2fd12b88aafdd04a52c298e3940bcb189f9766d6" --jq '{sha,tree:.tree.sha}'
    → {"sha":"2fd12b88aafdd04a52c298e3940bcb189f9766d6","tree":"ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa"}
    gh api "repos/laude-institute/terminal-bench-2/commits?per_page=1" --jq '.[0] | {sha,tree:.commit.tree.sha}'
    → {"sha":"2fd12b88aafdd04a52c298e3940bcb189f9766d6","tree":"ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa"}

The default branch HEAD is currently exactly the pinned commit, same tree sha `ec7c02c…`.
Claim survived (in fact trivially: the pin *is* the branch tip; the row's "no git tags" framing
is consistent with identifying the tree by commit).

## Re-fetch 4 — README.md line 46 (claim: `SOURCES.md:113`)

    curl -s https://raw.githubusercontent.com/laude-institute/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md | sed -n '46p'
    → uv run harbor run --dataset terminal-bench@2.0 \

The span `uv run harbor run --dataset terminal-bench@2.0` is present at line 46. Claim survived.
Observation (anchor nit, not a falsification): the span is 6 whitespace-tokens, not the 8 the row
labels; the quote itself is present verbatim at :46.

## Re-fetch 5 — entry's "88 of 89 test.sh files contain no reset block" (entry: `…execution-model.md:81-83`; wave-seat definition in `.ufo/waves/round-31/build/R31DraftEntry.md:185-191`)

The wave seat's reset-block definition is "no `git checkout`, `git reset` or `git stash`"
(R31DraftEntry.md:187-188). I re-fetched **all 89** `tests/test.sh` raw at the pin (superset of the
six-sample requirement; each raw.githubusercontent.com GET returned 200; capture 360 KB at
`/tmp/r31fx-quotes100/testsh/<dir>.sh`):

    for d in <89 dirs from the contents fetch>; do
      curl -s https://raw.githubusercontent.com/laude-institute/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/$d/tests/test.sh -o testsh/$d.sh
    done

Then scanned every file for `git checkout`, `git reset`, `git stash` (case-sensitive) and the bare
word `reset` (case-insensitive), plus a broader restore-ish token set (`restore`, `re-clone`,
`git clone`, `cp -r`, `rm -rf /tests`, …).

Results (per-file table at `/tmp/r31fx-quotes100/scan_results.json`):
- Exactly **1** of the 89 files contains any of `git checkout`/`git reset`/`git stash`:
  `fix-ocaml-gc/tests/test.sh` (`git checkout tag_purposefully_broken_sweeping_changes` at line 19,
  after `git clone` of upstream at line 19 and `cp -r ocaml-original/testsuite ocaml/` at line 20 —
  an intentional restore; its own comment "to stop the model cheating" at lines 17-18).
- The other **88** contain no `git checkout`, `git reset` or `git stash`, and **0 of 89** contain the
  literal word `reset` anywhere.
- Consistent with the seat report: all 89 invoke `pytest`; 87 call `/tests/test_outputs.py`
  absolutely; `mcmc-sampling-stan` and `rstan-to-pystan` `cd /tests` first.
- Six named samples (all clean): `adaptive-rejection-sampler`, `bn-fit-modify`,
  `break-filter-js-from-html`, `build-cython-ext`, `build-pmars`, `build-pov-ray`; plus the entry's
  two table manifests `protein-assembly` and `headless-terminal`.

What the sweep supports: the numeric 88/89 split at this pin, under the wave-seat's token definition
(no `git checkout`/`git reset`/`git stash`), and that `fix-ocaml-gc` is the sole git-restore driver.
What it cannot support: absence of any reset/anti-tamper mechanism expressed through other verbs
(`cp`/`tar`/`rsync`/Dockerfile entrypoints — the seat report itself bounds this,
R31DraftEntry.md:236-238), and nothing about tasks added after the pin. The entry's sentence is
therefore accurate as written but inherits the seat's token-level definition.

## VERDICT

S100's four assigned claims **survived**: the 92/89/3 root split (`gh api …/contents?ref=2fd12b88…`,
92 entries, 89 dirs, 3 files), the 301 redirect (`curl -sI` → `location: …/harbor-framework/terminal-bench-2`),
tree-sha equality (pin tree `ec7c02c7…` == default-branch HEAD tree; the pin is the current tip), and
the entry's "88 of 89 test.sh files contain no reset block" (full 89-file raw re-fetch; 88 clean,
only `fix-ocaml-gc` carries git-restore tokens). Nothing fell; the only discrepancy observed is a
label nit in the S100 row (the README :46 span is 6 words, not 8) — not part of the claimed facts.
Residual gaps: the 88/89 match is token-defined and does not prove the absence of non-git restore
mechanisms, and the pin's identity as "the release" is asserted by the row, not by a git tag.
