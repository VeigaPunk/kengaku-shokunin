# LessonScribeR79 — round-79 lesson draft: `## Mistakes` + `## Gate`

Seat LessonScribeR79 (scribe, leaf — no subagents dispatched). Deliverable: text-only draft for L1
`KengakuR79` to integrate into `corpus/lessons/round-79.md`. No lane file written besides this
report. Path base: unprefixed paths resolve from the lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(Q47); the one fleet-root path is written in full. Date 2026-11-04 UTC. No tool installs
(pacman untouched, no `uv`/`npx`/binary installs — none needed).

## 0. Verified facts (commands I ran, outputs observed)

All reads are over committed bytes (lane tip = freeze commit `5d6843134017780c045e92eed4e83264188a7d47`;
`git status --porcelain` shows only `corpus/README.md`, `plans/round51-surfaces.json` modified plus
untracked `.ufo/waves/round-79/` wave files, so the round-79 evidence and lesson bytes on disk equal
the freeze tree).

1. Real defect split of round 78's `c2-before.txt`:
   `awk '/^DEFECT /{c[$2]++; n++} END{for (k in c) printf "%s %d\n", k, c[k]; printf "TOTAL %d\n", n}' corpus/evidence/round78/c2-before.txt | sort`
   → `COMMAND-ABSENT 11`, `PASS-UNLOCATED 5`, `TOOL-UNNAMED 11`, `WORKTREE-ABSENT 2`, `TOTAL 29`.
2. `TOOL-UNPINNED` never fired at any committed revision of that receipt:
   `git log --all --format=%H -- corpus/evidence/round78/c2-before.txt` → six revisions
   (`04fdd644 ab4e314f 3cc5cecb a16e1ede bbf4f36c ec2d3d78`); `git show <rev>:… | grep -c 'DEFECT TOOL-UNPINNED'`
   → `0` at every one.
3. The wrong split is still live in three surfaces: fleet report
   `/home/vgpnk/Projects/shokunin/.ufo/reports/round-78/kengaku.md:97`, `SCORECARD.md:3615`
   (superseded-split note at `:3629`, re-derivation correction at `:3695`), and
   `corpus/lessons/round-78.md:53-54`.
4. S256 capture verified from the committed working-tree file
   `corpus/evidence/round79/sources/tb2-readme.md`: `wc -c` → `4574`; `sha256sum` →
   `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364` (equals the S256 row's claim);
   `grep -n 'popular benchmark'` → line **24**. The file is tracked
   (`git ls-files --error-unmatch` ok) but absent from freeze tree `5d684313`
   (`git show 5d684313:…` → "exists on disk, but not in '5d684313'") — it must land in a round commit
   before close or the registry row cites an uncommitted capture.
5. Word count of the S256 quote: `printf '%s' '<quote>' | wc -w` → **21** (the freeze's lesson draft
   says "22 words" — off by one, the exact R78-D4 class).
6. Criteria readings: `corpus/QUALITY.md` **Q8** = "rejections are kept" (nothing about counts);
   **Q28** = "a requirement-map label is derived from every executed case that violates the
   requirement" (round 38, nothing about ordering); **Q50** (`corpus/QUALITY.md:1211`, round 69) =
   "a round report cites a digest, a count or a revision-bound claim only after re-deriving it from
   the committed bytes at citation time; the citation carries the command that re-derives it, and a
   mismatch is a dated erratum, never an in-place edit." Q24's ordering leg ("a counter of record …
   proved, before it scores any data"; restated in Q30/Q31's supersede notes as "a control lands with
   the freeze, not after the first score") and Q30 (order-of-operations class) are the nearest
   ordering criteria.
7. Control receipts are unstamped: `grep -l 'LANE_TIP' corpus/evidence/round79/*.txt` → no file.
   Each control receipt is a two-line body (`CONTROL <mode> … target_reached=False`) with no
   `LANE_TIP`/`COMMAND`/`--rev`. The freeze commit `5d684313` lands claims, counters, ledger, the 16
   SKILL cells, before-receipts and the three controls in one commit (its own message says so), so no
   committed byte can order them. Base-revision absence of the ledger:
   `git cat-file -e 660ec0b9:plans/grader-population-ledger.json` fails (c1-before.txt ran at
   `--rev 660ec0b9` and prints `LEDGER rows=0`).

## 1. Draft `## Mistakes` rows (round-79 shape; replace the freeze's M79-1 and M79-2)

- **M79-1 · class `invented-evidence-split` · evidence `corpus/evidence/round78/c2-before.txt`
  against the three surfaces that printed the split — fleet report
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-78/kengaku.md:97`, `SCORECARD.md:3615`,
  `corpus/lessons/round-78.md:53-54` · captured-by `QUALITY.md` **Q50** (`corpus/QUALITY.md:1211`;
  re-derive every cited count from committed bytes at citation time, command included) · fix:
  R79-C2's D1 row — per the frozen claims its `check` exits 0 exactly when the repair holds, so the
  correction it validates must re-derive the receipt's per-class split by command; red at
  `660ec0b9`.** Round 78 printed `11 TOOL-UNNAMED, 10 COMMAND-ABSENT, 4 PASS-UNLOCATED,
  2 WORKTREE-ABSENT, 2 TOOL-UNPINNED` (sum 29); the receipt's bytes re-derive `11 COMMAND-ABSENT,
  5 PASS-UNLOCATED, 11 TOOL-UNNAMED, 2 WORKTREE-ABSENT` (sum 29) by the awk command in §0.1, and
  `TOOL-UNPINNED` never fired at any of the six committed revisions of the receipt (§0.2). The
  10/4 split was the superseded 27-defect first reading (SCORECARD.md:3629 names it); the 2
  `TOOL-UNPINNED` rows were invented to keep the sum at 29. The criterion that should have caught it
  existed since round 69 (Q50) — the closure never ran it over its own summary; the outside
  spot-check had to. The fix can fail: a correction whose stated split does not re-derive from
  `c2-before.txt` by the §0.1 command cannot pass a check that re-derives it, and R1 forbids
  repairing the old lines in place.
- **M79-2 · class `control-ordering` · evidence: freeze commit `5d684313` (claims + counters +
  `plans/grader-population-ledger.json` + the 16 `SKILL.md` cells + the three control receipts in
  one commit) and unstamped control receipts (`grep -l 'LANE_TIP' corpus/evidence/round79/*.txt`
  → no file) · captured-by `none` enforceable on these bytes — Q24's ordering leg and Q30's
  order-of-operations gate read committed history, and the freeze bundled artifact and controls into
  one commit, so no byte can order them · fix for round 80: land the control code and its skip rule
  in a commit that precedes the ledger's authoring, and score each control against the base
  revision's absent state (`--rev 660ec0b9`), the receipt carrying `COMMAND` (control mode +
  `--rev`) and `LANE_TIP`.** The three C1 controls (`namegrep`, `default-reason`, `all-blocked`)
  were first scored after the 88-row ledger and the 16 `SKILL.md` cells were authored, so the
  control receipts are not strictly pre-data — and their two-line bodies name no revision, no
  command and no stamp block, unlike every round-78 receipt R78-C2 taught the lane to make
  self-locating; a reader cannot tell from committed bytes that the controls lost against the base's
  absent state rather than against the finished ledger. The fix can fail: a control receipt whose
  `COMMAND` names a revision whose tree already contains
  `plans/grader-population-ledger.json` (`git cat-file -e <rev>:plans/grader-population-ledger.json`
  succeeds) fails the criterion; at `660ec0b9` the file is absent, which is the green state.

(M79-3 of the freeze draft stands as written — no conflict found by this read.)

## 2. Draft `## Gate` block (round-78 prose shape)

- **S256 admitted, scope narrowed by a superseding row.** The harness's own execution model: a
  Terminal-Bench 2.0 run is a *containerized* run. URL opened live by L1 `KengakuR79` this round
  (re-fetched byte-identical by wave seat `SourcesScribeR79`; capture bytes, sha and line re-read
  from the committed file by this seat):
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md`.
  Access date 2026-11-04 UTC. Capture `corpus/evidence/round79/sources/tb2-readme.md`, HTTP 200,
  4 574 bytes, sha256 `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364`. Located
  quote, capture line 24, **21 words**: **"Terminal-Bench is a popular benchmark for measuring the
  capabilities of agents and language models to perform valuable work in containerized
  environments."** Kind `docs`, tier A for the containerized execution model **only**. Registry
  change: S256 (`mined`, freeze commit `5d684313`) claims more than its capture grounds — the scope
  cell asserts the grader's `test.sh` "installs and starts services inside a container" and that "an
  in-process offline replay is a different execution surface", neither of which the README says — so
  the row is superseded by a new row (next free id) that names S256 and carries the narrowed scope;
  rows are corrected by a new superseding row, never in place (round-42 criterion; `anchor` and
  what-it-grounds are outside SOURCES v1's mutable set, the mechanism R78-D4 already priced).
  Used-by: `corpus/lessons/round-79.md`, `plans/round-79-claims.md`.
- **S257 admitted** as `own-work` for the priced population (round-62 census receipt +
  `plans/grader-population-ledger.json`): keep the freeze's wording; no defect found by this read.
- **Reject candidate:** "the harness README grounds the full blocker-taxonomy premise — that a
  grader's `test.sh` installs **and starts services** inside a container, and that an in-process
  offline replay is therefore a different execution surface." Reason: the pinned README contains no
  service-startup sentence and says nothing about the lane's offline probe; this round's live opens
  at the same tree found a task `test.sh` that stages packages (curl, a uv installer, pytest) and a
  Dockerfile that selects a base image — neither starts a service (`SourcesScribeR79`: three live
  fetches at `2fd12b88` — README 4 574 B, `nginx-request-logging/tests/test.sh` 634 B,
  `environment/Dockerfile` 246 B; none starts a service). The taxonomy's actual ground is the lane's
  own detector sweep over the 88 graders' stored bytes (own-work), not this README. Flip: pin
  upstream bytes in which a grader's `test.sh` starts a service, plus a lane receipt locating the
  offline probe's staging boundary against that same mechanism; then re-admit the wide scope as a
  new superseding row naming the narrow one.

## 3. Corrections the L1 must apply to the freeze's existing draft

1. **M79-1 captured-by is wrong twice.** The freeze says captured-by `none` and asserts "QUALITY Q8
   (numbers match the receipt they cite) did not exist as a gate". Q8 is "rejections are kept"; a
   fitting criterion has existed since round 69 — **Q50** (`corpus/QUALITY.md:1211`) — with R1 for
   the append-only correction mechanics. Replace per §1. (A Mistakes row about invented evidence
   that mis-cites the criteria file would re-commit the R78-D4 citation-metadata class one round
   after mining it.)
2. **M79-2 captured-by is a mis-cite.** `QUALITY Q28` is the round-38 requirement-map criterion. The
   nearest legs are Q24's ordering leg and Q30's order-of-operations class, neither enforceable on
   this round's single-commit freeze; state it per §1 (honest `none`, with the would-be criterion
   named in the fix).
3. **Gate S256 bullet: "22 words" → 21** (mechanical count, §0.5) — the same slip class this round's
   own Corrections section just repaired for S254 (15, not 17).
4. **Land the S256 capture.** `corpus/evidence/round79/sources/tb2-readme.md` is tracked in the
   index but absent from commit `5d684313` (§0.4); the registry row and this Gate cite committed
   capture bytes, so it must be in the round's landing commit before close (Q7's spirit: no support
   rests on an unlanded working copy).

## 4. Provenance, limits, out of scope

- Commands used: `awk`, `grep`, `sed`, `tail`, `wc`, `sha256sum`, `sort`, and read-only `git`
  (`rev-parse`, `log --all`, `show`, `ls-tree`, `ls-files`, `status`, `cat-file`). No counter was
  executed (no `--selftest/--mutants/--control-*` runs; the drafting item needs none). No writes
  outside this report and a removed 4.5 KB `/tmp` scratch (`/tmp/tb2r.md`, deleted; not cited).
- The freeze's claimed counter readings (e.g. `DEFECTS n=0`, `COVERAGE replayed=24 …`) were observed
  only as committed receipt bytes (`corpus/evidence/round79/c1-after.txt` tail), never re-run; the
  C2 discharge rows and their checks are other seats' surface and are not verified here.
- The claim "the three losing controls were first scored after the ledger and the 16 SKILL cells
  were authored" is taken from this seat's assignment (the wave's process knowledge); what the
  committed bytes independently establish is §0.7: single-commit bundling plus unstamped receipts
  make the ordering unauditable, which is the defect class the fix closes.
