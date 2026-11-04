# MutantR77 — independent frozen-counter mutation probe
Axes: coverage and calibration. Freeze: `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb` (`git log -1 --format=%H -- plans/round-77-claims.md`, rc 0). Frozen claims read in full before commands. No commits, pushes, mutating git commands, installs, or production edits.
## Detector and interpretation
Frozen tool bytes were exported with `git archive 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb` (rc 0), with a private copied `.git` and detached HEAD file at that revision. All probe writes stayed under `/fast/scratch/hyaku/kengaku-r77/MutantR77/`. Each independent mutant ran the identical bounded detector three times against the **real lane worktree**, not a fixture: pristine → mutated → exact restoration. Per subprocess timeout: 90 seconds; four independent probes at a time. No timeout occurred.
Command template: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/<counter>-<mutant>.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`; cwd = scratch root. Every literal command and output is recorded below. `--rev` was not passed: these observations measure the lane during this wave, not a promised final landing revision. Frozen implementations, predicates, targets, controls, and kill rules were not redefined.
Expected detector: a semantically wrong result must fail the frozen target/defect predicate (rc 1). A successful pristine and restored run enclosing a mutant rc 0 is a survivor; enclosing mutant rc 1 is killed. Any failed pristine/restored run is inconclusive, never a kill. A healthy real tree need not activate every negative branch: survival here is specifically real-tree detector coverage, not proof that the separately advertised fixture battery misses the mutant. The built-in mutant matrices were not used.
## Results
- C1: mutants=9 survivors=6 killed=3 inconclusive=0.
- C2: mutants=8 survivors=0 killed=0 inconclusive=8.

C2 had no eligible green baseline: every run printed `registered=0 closed=0 discharged=0 legs_passed=6 legs_pending=0 wrong=8`, seven `MISSING-ROW` defects and `LEG-FAIL V7 ... carries no passing predicate line`, rc 1. Therefore **none of its eight mutant failures are claimed as kills**, and zero observed survivors does not establish coverage. These are wave-time observations, not a judgment of later landing bytes.

Duplicate-identity qualification: the frozen C1 has **no duplicate rejection to remove**. Its lines 453/469 collect identities in a set and line 538 computes `unique` from that same set; no branch emits `DUPLICATE-SURFACE`. The pristine real-tree output already prints `SURFACES total=28` and `IDENTITIES n=26 unique=26`. The requested “drop duplicate-identity detection” is thus not representable literally. Probe `drop-identity-accounting` removes the closest existing behavior (collection), explicitly not a fictitious rejection. Eight other semantic C1 probes were executed, so this absent guard does not reduce the minimum eight actual probes.

Source citations were searched with the dedicated grep tool: frozen scratch C1 patterns `identities`, `digest.startswith`, `covers`, `dated_absent`, `UNLISTED-SURFACE`; C2 patterns `state ==`, `ev_lit`, `fromisoformat`, `check_trivial`, `m_sha`; frozen claims patterns `TARGET|Kill rules|Selftest|mutant matrix|DUPLICATE|Stated limits`. These yielded the exact mutation sites below and claims lines 47, 61–64, 105–109. No L1 prose was used as execution evidence.
## Per-mutant evidence

### C1 / invert-path-comparison — killed

Frozen line 293. Consequence: Existing-path verdict reverses.

```diff
-len(live) == len(targets)
+len(live) != len(targets)
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `cf444265ccd799fa8d203be49f44d943272132f9aefa5571d64eeb319aa79b8b`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-invert-path-comparison.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-invert-path-comparison.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 present path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 present path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 present path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 present path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 present path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 present path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 present path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 present path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 absent path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 absent path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 absent path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 absent path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 absent path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 present cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 present path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 absent path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=19 absent=8 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=11 disagree=17
DEFECTS n=17
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
DEFECT STALE-ABSENT 1023 Research notes (SSOT for eval craft) marker=2026-11-04
DEFECT STALE-ABSENT 1024 Research notes (former wikillm path) marker=2026-11-04
DEFECT STALE-ABSENT 1025 Local benchmark battery marker=2026-11-04
DEFECT STALE-ABSENT 1026 Local benchmark battery (former path) marker=2026-11-04
DEFECT STALE-ABSENT 1030 Route telemetry marker=2026-11-04
DEFECT STALE-ABSENT 1031 Bounty-hunter tree marker=2026-11-04
DEFECT STALE-ABSENT 1032 Client CLI telemetry marker=2026-11-04
DEFECT STALE-ABSENT 1033 Client CLI sync state marker=2026-11-04
DEFECT STALE-ABSENT 1034 Model catalogs (local index) marker=2026-11-04
DEFECT STALE-TEXT 1036 Own probe artifacts
DEFECT STALE-TEXT 1039 Attribution frozen tables
DEFECT STALE-TEXT 1040 Corpus gate docs
DEFECT STALE-TEXT 1044 Public literature (cite anchor)
DEFECT STALE-TEXT 1045 Open-model catalog digest
DEFECT STALE-ABSENT 1048 Serving-stack process pin (rounds 10-14) marker=2026-11-04
DEFECT STALE-ABSENT 1049 Ephemeral probe trees (rounds 4-7) marker=2026-11-04
DEFECT STALE-TEXT 1050 Corpus index
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-invert-path-comparison.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / drop-unlisted-loop — survived

Frozen line 518. Consequence: Uncarried older declarations disappear.

```diff
-for heading, lineno, cells in superseded_rows(reader):
+for heading, lineno, cells in []:
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `c288881d8105a6173db2fddd1259efd893104704a0b855e77fb3f8622da719b8`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-drop-unlisted-loop.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-drop-unlisted-loop.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-drop-unlisted-loop.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / present-as-absent — killed

Frozen line 476. Consequence: Present rows take absence-marker branch.

```diff
-if verdict == "present":
+if verdict == "absent":
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `230f324e84e82f7980a8ec541920f6a46c43d20389f1d6cdde7682f190c5ac86`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-present-as-absent.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-present-as-absent.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=15 disagree=13
DEFECTS n=13
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
DEFECT STALE-ABSENT 1023 Research notes (SSOT for eval craft) marker=2026-11-04
DEFECT STALE-ABSENT 1024 Research notes (former wikillm path) marker=2026-11-04
DEFECT STALE-ABSENT 1025 Local benchmark battery marker=2026-11-04
DEFECT STALE-ABSENT 1026 Local benchmark battery (former path) marker=2026-11-04
DEFECT STALE-ABSENT 1027 Served local model (:34113) marker=2026-11-04
DEFECT STALE-ABSENT 1028 Served local model (:45669) marker=2026-11-04
DEFECT STALE-ABSENT 1030 Route telemetry marker=2026-11-04
DEFECT STALE-ABSENT 1031 Bounty-hunter tree marker=2026-11-04
DEFECT STALE-ABSENT 1032 Client CLI telemetry marker=2026-11-04
DEFECT STALE-ABSENT 1033 Client CLI sync state marker=2026-11-04
DEFECT STALE-ABSENT 1034 Model catalogs (local index) marker=2026-11-04
DEFECT STALE-ABSENT 1048 Serving-stack process pin (rounds 10-14) marker=2026-11-04
DEFECT STALE-ABSENT 1049 Ephemeral probe trees (rounds 4-7) marker=2026-11-04
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-present-as-absent.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / skip-dated-marker — survived

Frozen line 483. Consequence: Missing ABSENT marker is accepted.

```diff
-elif verdict == "absent":
-            if not dated_absent:
+elif verdict == "absent":
+            if False:
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `698bee241eb06b66f0f65455e93e38d77f7fdff66a972b6267180177dace9131`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-skip-dated-marker.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-skip-dated-marker.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-skip-dated-marker.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / covers-always-true — survived

Frozen line 226. Consequence: Every older anchor is claimed covered.

```diff
-a, b = normalize_anchor(canon), normalize_anchor(declared)
+return True
+    a, b = normalize_anchor(canon), normalize_anchor(declared)
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `1d1417244e8128167ddf66d046029061eb3d330feb01f0369c93dcd620e33234`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-covers-always-true.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-covers-always-true.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-covers-always-true.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / hash-prefix-only — survived

Frozen line 320. Consequence: Wrong digest suffix is accepted.

```diff
-ok = digest.startswith(head[:8]) and (not tail or digest.endswith(tail))
+ok = digest.startswith(head[:8])
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `609080385f51ed6809d0f53eb131cf90bb4502b3b2b0c2f3b953796edc9c82d5`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-hash-prefix-only.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-hash-prefix-only.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-hash-prefix-only.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / remote-is-live — killed

Frozen line 470. Consequence: No-egress remote row inflates live count.

```diff
-if kind != "remote":
+if True:
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `1c1390da5278dba3efe49f10c2b5f52662eb656165b774a7cc4f0f5013878e55`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-remote-is-live.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-remote-is-live.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=28
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-remote-is-live.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / drop-identity-accounting — survived

Frozen line 469. Consequence: Repeated identities cannot even appear in identity accounting; frozen code has no duplicate rejection.

```diff
-identities.add(f"{kind}:{key}")
+pass # identity collection removed
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `8bcf7b03eea4093491ce595a9a375103e510d80b8a4e34dc86ba254c473f54e6`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-drop-identity-accounting.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-drop-identity-accounting.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=0 unique=0 sha256=e3b0c44298fc1c14…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-drop-identity-accounting.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C1 / skip-date-validation — survived

Frozen line 504. Consequence: Impossible ABSENT dates accepted.

```diff
-datetime.date.fromisoformat(m.group(1))
+None # skip calendar validation
```

SHA256 pristine: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`

SHA256 mutated: `2fec224e3a99e204d53b479cf5324975c77d642895c23501c170fdd363f69da7`

SHA256 restored: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-skip-date-validation.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-skip-date-validation.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c1-skip-date-validation.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 0.

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

### C2 / skip-ancestry — inconclusive

Frozen line 346. Consequence: Nonancestor or unresolved close treated ancestor.

```diff
-state = ancestry(lane, close, reader.tip) if close else "missing"
+state = "ancestor"
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `0df9398443e9217d8b8223252b643fdd393c8772473c269443cb272abfcd53c1`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-skip-ancestry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-skip-ancestry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 0df9398443e9217d8b8223252b643fdd393c8772473c269443cb272abfcd53c1
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-skip-ancestry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / skip-evidence-at-close — inconclusive

Frozen line 365. Consequence: Evidence accepted without reading its commit.

```diff
-tree = reader.at(close, ev_path)
+tree = ev_lit
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `f8991215eafca5462aed6fba942abe4bb8b6d274f9e44ca339133ef4f84d6286`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-skip-evidence-at-close.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-skip-evidence-at-close.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA f8991215eafca5462aed6fba942abe4bb8b6d274f9e44ca339133ef4f84d6286
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-skip-evidence-at-close.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / accept-negated-close — inconclusive

Frozen line 373. Consequence: Explicitly undischarged row accepted.

```diff
-problems.append("NEGATED-DISCHARGE")
+pass # accept negated close
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `7aa5889294e8f93fc4ae462ff5337819547afeddb4323205705d63114d8e48f4`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-accept-negated-close.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-accept-negated-close.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7aa5889294e8f93fc4ae462ff5337819547afeddb4323205705d63114d8e48f4
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-accept-negated-close.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / pending-as-ok — inconclusive

Frozen line 316. Consequence: Pending leg counts passed.

```diff
-if state == "ok":
+if state in ("ok", "pending"):
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `bccb972d8922e10ff02410f91d1064c1f7f92441cf66521431d30d3e1f2ad89d`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-pending-as-ok.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-pending-as-ok.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA bccb972d8922e10ff02410f91d1064c1f7f92441cf66521431d30d3e1f2ad89d
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-pending-as-ok.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / drop-empty-scope — inconclusive

Frozen line 395. Consequence: Empty scope loses its explicit defect; target remains seven.

```diff
-defects.append("DEFECT EMPTY-SCOPE 0 closer names no routed id")
+pass # skip EMPTY-SCOPE
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `537939749026324fec8d613597a06cda74ac01eb5643aab913d65036ea8f3ecf`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-drop-empty-scope.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-drop-empty-scope.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 537939749026324fec8d613597a06cda74ac01eb5643aab913d65036ea8f3ecf
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-drop-empty-scope.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / trivial-always-false — inconclusive

Frozen line 170. Consequence: Trivial discharge check accepted.

```diff
-def check_trivial(cmd: str) -> bool:
+def check_trivial(cmd: str) -> bool:
+    return False
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `95b7d07209b21bccb7279aed47cd5a97c04857fcfbec57f7d5ea36090b87fefc`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-trivial-always-false.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-trivial-always-false.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 95b7d07209b21bccb7279aed47cd5a97c04857fcfbec57f7d5ea36090b87fefc
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-trivial-always-false.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / drop-tool-sha-leg — inconclusive

Frozen line 192. Consequence: V1 mismatched receipt tool SHA accepted.

```diff
-if at_tip != m_sha.group(1):
+if False:
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `1e8f25bc73410b6127085df75fc4601fe486072227d82332a54a8dafaddf1093`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-drop-tool-sha-leg.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-drop-tool-sha-leg.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 1e8f25bc73410b6127085df75fc4601fe486072227d82332a54a8dafaddf1093
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-drop-tool-sha-leg.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

### C2 / accept-noniso-date — inconclusive

Frozen line 355. Consequence: Non-ISO verified_at accepted.

```diff
-datetime.date.fromisoformat(verified)
+None # accept any verified_at
```

SHA256 pristine: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`

SHA256 mutated: `1309ebf4aeaed79bce3be0b824426e2d1bb0713f411c6c00c16c858badc845e9`

SHA256 restored: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c` (exact match: True).

pristine: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-accept-noniso-date.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

mutated: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-accept-noniso-date.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 1309ebf4aeaed79bce3be0b824426e2d1bb0713f411c6c00c16c858badc845e9
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

restored: `python3 /fast/scratch/hyaku/kengaku-r77/MutantR77/c2-accept-noniso-date.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → rc 1.

```text
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
REV worktree
WORKTREE dirty
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V2 ok final tallies + 9 defect classes
LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1
LEG V4 ok block present
LEG V5 ok proposal 2 recorded open
LEG V6 ok one name in both files
LEG V7 fail corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
LEDGER R76-V1 ok close=8da90eb7 evidence=corpus/evidence/round76/c1-selftest.txt
LEDGER R76-V2 ok close=8da90eb7 evidence=SKILL.md
LEDGER R76-V3 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V4 ok close=8da90eb7 evidence=LOG.md
LEDGER R76-V5 ok close=8da90eb7 evidence=corpus/lessons/round-77.md
LEDGER R76-V6 ok close=8da90eb7 evidence=PROVINCE.md
LEDGER R76-V7 ok close=8da90eb7 evidence=corpus/evidence/round77/rerun-r51-c1.txt
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
DEFECTS n=1
DEFECT LEG-FAIL V7 corpus/evidence/round77/rerun-routed-open.txt carries no passing predicate line
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 fail
```

## Restoration and cleanup

Every probe file was restored in a finally block. All 17 restored SHA256 values equal their pristine values. Frozen original counter files were never mutated; final original-file hashes:
- c1: `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2`; equals initial=True.
- c2: `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`; equals initial=True.

`shutil.rmtree('/fast/scratch/hyaku/kengaku-r77/MutantR77')` completed; `Path('/fast/scratch/hyaku/kengaku-r77/MutantR77').exists()` → `False`. No scratch tree remains. Only this report is retained.

## Self-evaluation

Accuracy 4/5 (all 51 detector outputs and hashes retained; worktree was live, not an immutable landing snapshot); completeness 4/5 (17 probes completed; literal duplicate rejection absent, C2 baseline red); clarity 4/5 (full evidence is lengthy); actionability 4/5 (surviving guard lines identified, C2 requires a green baseline); conciseness 4/5 (raw receipts intentionally retained). Mean 4.0/5. Improvements: evaluate C2 only when its actual lane baseline is green; retain an immutable measured-tree snapshot if future probes require cross-run equivalence. No unrun fixture checks are claimed.
