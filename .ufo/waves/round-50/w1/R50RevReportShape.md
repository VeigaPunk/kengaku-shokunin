# R50RevReportShape — round-report structure pre-check (contract tick-list + defects)

Seat role: reviewer (leaf; no dispatch). Serves R50-C1 (novelty) + R50-C2 (calibration) by checking the round
report's **structure and evidence attribution** against the report contract. Read-only against the lane; the only
lane write is this file. No admission is claimed or implied here.

REV measured: lane tip `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78` (`refs/heads/master`), clean clone
`/fast/scratch/hyaku/kengaku-r50/R50RevReportShape/lane` (`git clone --shared`). Freeze
`3b02d573d58cc6d2e0d27ef92ac0815354912252` verified an ancestor of the tip
(`git -C <lane> merge-base --is-ancestor 3b02d573 HEAD` → exit 0) **before** any measurement.
Tip moved during this seat: the first `git rev-parse HEAD` in this session returned
`d6f2fce9889f429162c12f851bae41891bedf5cd`; every finding below was re-measured after the tip reached
`d45c5bb`. Report under test: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kengaku.md` (fleet root,
`kengaku` lane report; 125 lines) — the file the contract's gates run against.

## Axes named

1. **Calibration (R50-C2 support)** — does every number and pointer in the round report resolve at the published
   tip, and does each receipt's `REV` equal the revision the prose attributes it to?
2. **Landed-state truthfulness (R50-C1 support)** — does the report describe bytes that exist in a commit, or
   bytes that exist only in a working tree?

Both are cheap to check and independent of the C1/C2 predicate runs other seats own.

## Contract tick-list (L1 can tick each line)

Contract source: `.ufo/waves/round-34/build/R34CriticReportShape.md:9-21` (items 1–11), plus the round-33
six-section ordering it preserves (`round-33/kengaku.md:8,18,27,85,91,99`) and the SHONEN marker rule
(`SHONEN.md:5-12`). Status is what I observed on the filed report at `REV d45c5bb`.

| # | gate | exact check | pass condition | status at `d45c5bb` |
|---|---|---|---|---|
| G1 | six sections in order | `grep -n '^## ' .ufo/reports/round-50/kengaku.md` | `Work performed`, `Landed changes`, `Before → after measurements`, `Sources & frontier`, `Trend verdicts`, `SHONEN`, in that order, each once | **PASS** (L15, L55, L73, L84, L97, L110) |
| G2 | SHONEN heading count | `grep -c '^## SHONEN' <report>` | exactly `1`, output recorded in the report | heading count **PASS** (`1`), **recorded output FAIL** (see D10) |
| G3 | four boxes, canonical text/order | compare each box with `SHONEN.md:5,7,9,11` | 4 boxes, same order, canonical text | **PASS** (4 boxes; text matches; box 4 paraphrases `(PROVINCE.md still accurate)` → `; PROVINCE.md still accurate`) |
| G4 | one physical line per box | `awk '/^## SHONEN/,0' <report> \| grep -n '\[~\]\|\[x\]\|\[ \]'` | one line per box | **FAIL** — boxes wrap: L112-113, L114-115, L116-117, L118-119 |
| G5 | marker at line start | `grep -c '^- \[~\]' <report>` | equals 4 (or the lane's current `[~]`/`[x]`/`[ ]` mix) | **FAIL** — `0`; markers are backticked (`` - `[~]` … ``); `grep -c '\[~\]'` = 4 |
| G6 | SHONEN section holds nothing else | read after the 4th box | no stale-lane/tool/L0 prose inside `## SHONEN` | **FAIL** — L121-125 (stale-lane, tool installs, L0, inherited state) sit inside `## SHONEN` |
| G7 | stale-lane line | `grep -n '^Stale-lane\|^## Stale-lane' <report>` | explicit: respawn-per-round + whether another mission is open | **PASS (content)** `Stale-lane: respawn-per-round driver; no other mission of this lane is open.` — **placement WARN** (inside SHONEN, see G6) |
| G8 | tool installs | `grep -n 'Tool installs' <report>` | tool/version/channel/reason each, or explicit `none` | **PASS (content)** `Tool installs: none (no pacman transaction attempted; nothing needed).` — placement WARN |
| G9 | misroot sweep | `grep -ci 'misroot' <report>` | enumerated misrooted artifacts + recovery, or `sweep found none` | **FAIL** — `0` |
| G10 | pre-report gates recorded | `git -C kengaku-shokunin ls-remote origin refs/heads/master` vs `git rev-parse HEAD`; `grep -c '^## SHONEN' <report>` | both hashes printed and equal; SHONEN count printed | **PARTIAL** — tip `d45c5bb…` matches `ls-remote` (verified: both `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`); the SHONEN count output is absent |
| G11 | one resolvable pointer per bullet | join each bullet's continuation lines; require `plans/…`, `corpus/…`, `.ufo/…` (full, not ellipsized) or `file:line` | every bullet | **FAIL** — `quality` (L102) and `discernment` (L104) bullets carry no resolvable pointer; `Wave` bullet's spec path is ellipsized (`…/round-50/w1-spec.json`) |
| G12 | before→after per claim | each claim row carries before command+revision+output+exit and after command+revision+output+exit | 2 claims × 2 sides | **FAIL** — C1 before revision wrong (D1); C2 before revision wrong (D2); C2 after has no receipt file (D5) |
| G13 | cited receipt's `REV` equals prose revision | diff the `REV` line of each cited receipt against the revision named in the same row | exact match | **FAIL** — both before rows name `71f5f5f`; both receipts say `f7281bc` (D1, D2) |
| G14 | every number has a producing command | every figure in the report traces to a committed command + output | yes | **FAIL** — C2 after `279` has no receipt anywhere in the tree (D5); axis numbers 9/8/8/8 uncited (D12) |
| G15 | landed-changes table completeness | every row has a commit + LOG/evidence pointer; `git cat-file -e <c>^{commit}` for each | all rows | **PASS** — 8 commits, all resolve: `f7281bc 3b02d57 5c56819 822f3b7 c3372a9 6db0279 d6f2fce d45c5bb`; every row cites `## Round 50` |
| G16 | report's tree claims match `git status --porcelain` | compare the "inherited state"/clean statements with the live tree | truthful | **FAIL** — `Inherited state: none uncommitted at close` vs ` M plans/round50_c1_verify.py` (D4) |
| G17 | cited pointers exist at the *published tip* | `git -C kengaku-shokunin cat-file -e HEAD:<pointer>` | every pointer tracked | **FAIL** — every `w1/` pointer is untracked: `git ls-files .ufo/waves/round-50/w1 \| wc -l` = `0` (D6) |
| G18 | no model alias / route name in the artifact | `grep -icE 'opus\|sonnet\|gpt-[0-9]\|deepseek\|gemini\|cursor/\|claude-\|flash\|haiku' <report>` | `0` | **PASS** (`0`) |
| G19 | sources census before→after with receipt | report carries the census script, both exits, row counts, tier/status histograms, rows added by tier, rows touched, frontier advance, assimilation | all present | **PASS** — `165 → 170` rows, `A=146/B=22/C=2`, `mined=154/queued=8/rejected=8`, 5 added all tier A, none touched, census re-run exit 0; missing only the raw census stdout (r48 pasted it) → **WARN** |

## SHONEN box list (from `SHONEN.md`, canonical order)

Marker states in `SHONEN.md` today: all four `[~]`. The report must carry exactly one line per box, in this
order, marker at line start, each with a resolvable pointer.

1. `[~]` SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SHONEN.md:5`; pointer `SKILL.md`
2. `[~]` At least one end-to-end domain task executed and logged in LOG.md — `SHONEN.md:7`; pointer `LOG.md:7`
3. `[~]` Instructions executable by an agent without oral context — `SHONEN.md:9`; pointer `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`
4. `[~]` No cross-domain bleed (PROVINCE.md still accurate) — `SHONEN.md:11`; pointer `PROVINCE.md:129`

Canonical one-line form (as filed by r48, `round-48/kengaku.md:94-99`):

    [~] SKILL.md contains real decision tables, error patterns, checklists and cited sources — `SKILL.md:23-46`.
    [~] An end-to-end domain task is executed and logged — `LOG.md:7`; round 50 ...
    [~] Instructions are executable without oral context — `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`.
    [~] No cross-domain bleed; PROVINCE remains accurate — `PROVINCE.md:129`.

The round-50 report keeps all four `[~]` (consistent with the lane file) but breaks the literal form: G4 and G5.

## Defects, by severity

### Blocker — the report's landed-state claim about the C1 instrument is falsified by the committed tree (D3)

Report (L17-21) states the shipped instrument "is decided in a **separate process** per fixture (exit 10/11/12),
and fixture parents are opaque random tokens padded with decoys"; L55-57 note says that repair "landed inside
`6db0279`'s tree; its digest is `d8787b34…`-lineage (final in `d45c5bb`)".

Measured:

```text
$ for c in 6db0279 d6f2fce d45c5bb; do git show $c:plans/round50_c1_verify.py | sha256sum; git show $c:plans/round50_c1_verify.py | grep -c HARNESS; done
d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  0
d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  0
d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  0
$ git show HEAD:plans/round50_c1_verify.py | grep -n 'def verdicts\|fence_mod.breach'
122:def verdicts(fence_mod, fixtures):
127:            r = fence_mod.breach(f["dir"], f["argv"], f["tool"])
$ sha256sum plans/round50_c1_verify.py            # working tree, uncommitted
850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999  plans/round50_c1_verify.py
$ grep -c HARNESS plans/round50_c1_verify.py
3
```

So: no commit contains the subprocess harness or the name-hiding; `d8787b34…` is exactly the digest the claims
ledger records for repair **1** (module attribution — `plans/round-50-claims.md` open-window table), and every
commit from `c3372a9` to `d45c5bb` still calls `fence_mod.breach(...)` **in process**. The harness exists only as
an uncommitted working-tree modification (`850ec790…`), for which the claims' open-window table has no row.

The scored receipt cannot be attributed to the harness either: `corpus/evidence/round50/c1-receipt.txt` pins
`FENCE … sha256=57adce4a…` but prints **no counter digest** (`grep -ci counter` = `0`), and both counter versions
print the identical `POPULATION`/`HONEST`/`REFUSALS`/`SEALED`/`MUTANTS`/`PREDICATE` literals (`grep -c` of each
literal is equal in both files). [INFERENCE] The scored run used the committed in-process counter: the harness
version is in no commit, and the receipt's `TREE dirty=0` excludes running it from a dirty tree.
Consequence: the `R50C1CritPredicate` forgery (`caught=23`) that the report says was "turned into an instrument
repair" is **not** repaired in the artifact the receipt scores — the report's own evidence chain is broken.

Fix (either):
(a) commit the harness + name hiding as a new commit, record old→new digest (`d8787b34… → 850ec790…`) in the
claims' open-window table and the S2/S3 commit, add `COUNTER sha256=<digest>` to the counter's receipt output, and
re-score; or
(b) strike the separate-process/name-hiding sentence and report the shipped instrument as in-process with that
forgery class unrepaired (then the C1 kill-rule reading and the "blind critic re-measured the shipped bytes"
sentence need re-wording to be about the fence only, which is what the blind receipt actually covers).

### Blocker — before-side revisions are wrong for both claims (D1, D2)

```text
$ git cat-file -e 71f5f5f:plans/round50_c1_verify.py      # absent
$ git cat-file -e 71f5f5f:plans/round50_c2_audit.py       # absent
$ git cat-file -e 71f5f5f:plans/honest50/population.txt   # absent
$ git cat-file -e 71f5f5f:plans/fixture_fence.py          # exists
```

The report's C1 before row reads "`python3 plans/round50_c1_verify.py --lane .` at `71f5f5f` with the base
fence … (`.ufo/waves/round-50/claims/c1-control-do-nothing.txt`)". That command and its frozen population did not
exist at `71f5f5f`; the cited receipt says so itself:

```text
# R50-C1 control: do-nothing (base fence unchanged, S1 tree f7281bc)
# command: python3 plans/round50_c1_verify.py --lane . --skip-mutants
REV f7281bc90ca953ff3b84413a21023b9793ef2043
TREE dirty=1
FENCE … sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
HONEST fixtures=126 admitted=113 refused=13 error=0
… REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

Three further misstatements in that one row: the receipt ran `--skip-mutants` (the mutant leg was not exercised by
the do-nothing control), it carries **no exit-code line**, and `TREE dirty=1` (fine for a control run under
`--allow-dirty`, but it is not a clean-clone before).

The C2 before row reads "`python3 plans/round50_c2_audit.py --lane .` at `71f5f5f`: `POINTERS total=275 paths=216
hashes=59 resolved=263 … unresolved=12`, exit 1 (`.ufo/waves/round-50/claims/c2-before.txt`)". I recomputed the
audit's own token sets at three revisions from the lane clone (same regex, `git show REV:<file>`, `cat-file -e
REV:<path>`, `merge-base --is-ancestor`):

```text
REV 71f5f5f… total=271 paths=213 hashes=58 resolved=259 exists=201 superseded=0 never-landed=0 unresolved=12
REV f7281bc… total=275 paths=216 hashes=59 resolved=263 exists=204 superseded=0 never-landed=0 unresolved=12
REV d45c5bb… total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0
```

`275/216/59/263` is the **S1 tree `f7281bc`**, exactly what the receipt's header
(`# R50-C2 before (S1 tree f7281bc)`) and `TIP` line say. `271/213/58/259` is `71f5f5f` — the claims file's number.
The report (and the matching `SCORECARD.md` measured-outcomes row, `:2185`) welded the first set to the second
revision. Fix: either cite `271 … unresolved=12` at `71f5f5f` (claims number) **and** `275 …` at `f7281bc`
(receipt), or restate the row to `f7281bc` and note that the counter is what the S1 freeze added, so no
counter-produced number can exist at the base tip.

### Major — no committed receipt for the C2 after run (D5)

`grep -ci counter` aside, `git grep -l "POINTERS total=279" HEAD` returns nothing and
`git ls-tree -r --name-only HEAD corpus/evidence/round50/` lists only `c1-receipt.txt` + 5 `.adoc` captures. The
number is reproducible — I reproduced it at the tip in a `--shared` clone:

```text
TIP d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78 branch=master
POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0
exit=0
```

but the report gives command + exit with no output file, so no external verifier can re-check it without
re-deriving the run. Fix: commit `.ufo/waves/round-50/claims/c2-after.txt` (or
`corpus/evidence/round50/c2-after.txt`) and cite it; C2's contract is exactly "the pointer re-runs", so its own
after-run must be a pointer.

### Major — every `w1/` evidence pointer is untracked (D6)

`git ls-files .ufo/waves/round-50/w1 | wc -l` = `0`. The report relies on
`.ufo/waves/round-50/w1/R50C1CritPredicate.md`,
`.ufo/waves/round-50/w1/C1CritBlind3/receipts/verdicts-against-lane-repair-57adce4a.json`,
`.ufo/waves/round-50/w1/R50C1ExecMutRebase-witness.tsv` — all on disk, none at the published tip. (The six
`claims/` receipts **are** tracked, from `3b02d57`.) Fix: commit the wave reports/receipts the report leans on (r48
committed its wave artifacts in `d4eacdf…`) or label them "untracked, retained on host" so no reader mistakes them
for tip-resolvable evidence.

### Major — "inherited state: none uncommitted at close" is false (D4)

```text
$ git -C kengaku-shokunin status --porcelain
 M plans/round50_c1_verify.py
?? .ufo/waves/round-50/w1.ready
?? .ufo/waves/round-50/w1.ready.partial
?? .ufo/waves/round-50/w1/
$ git diff --stat
 plans/round50_c1_verify.py | 74 ++++++++++++++++++++++++++++++++++++----------
 1 file changed, 59 insertions(+), 15 deletions(-)
$ stat -c '%y' plans/round50_c1_verify.py   → 2026-10-28 14:35:39 -0300   (tip commit d45c5bb at 14:39:56)
```

Fix: state the dirty counter by digest with its disposition (this is the same artifact as D3).

### Minor — SHONEN literal form (D7), section placement (D8), misroot sweep (D9), pre-report gates (D10)

- D7: `grep -c '^- \[~\]'` = `0`, `grep -c '\[~\]'` = `4`; boxes wrap onto 2 lines each. Rewrite as four single
  lines with a bare `[~]` marker, per `SHONEN.md` and `round-48/kengaku.md:94-99`.
- D8: stale-lane, tool installs, L0 and inherited-state prose (L121-125) sit inside `## SHONEN`; promote to their
  own headings so G2/G4 and the reading of "one line per box" stay clean (r48: `## Stale-lane`, `## Tool installs`,
  `## L0 questions`).
- D9: `grep -ci misroot` = `0`. Add the sweep line (r49's equivalent: `git -C /home/vgpnk/Projects/shokunin status
  --porcelain` result and what it contained) or `sweep found none`.
- D10: record `grep -c '^## SHONEN'` output and the `ls-remote` hash literally. Both are cheap and both are the
  r34 item-10 gate; the tip/remote claim itself is true (`d45c5bb…` on both).

### Minor — pointers and numbers that are not resolvable or now stale (D11, D12, D13)

- D11: `quality` bullet (L102) names "Q41" and "three Mistakes rows" with no path — cite `corpus/QUALITY.md:1112`
  and `corpus/lessons/round-50.md:9-15`. `discernment` bullet (L104) cites `C1CritBlind3/receipts/…json` and
  `R50C1CritPredicate` as bare names — prefix with `.ufo/waves/round-50/w1/` and `.md`.
- D12: "coverage held at 7 (cap), depth 9, operability 8, freshness 8, adjacency 8 unchanged" has no pointer; those
  values are the carried axis-state line at `SCORECARD.md:1976-1977` (also `:2038`, `:2077`, `:2111`). Cite it.
- D13: the `Wave` bullet's spec path is ellipsized (`…/round-50/w1-spec.json`) and its counts need a timestamp —
  measured now: `w1-spec.json` has `72` items, role histogram `executor 21, critic 20, reviewer 9, scribe 8,
  scout 6, mutation-tester 5, connector 1, simplifier 1, revenger 1` → **35** attack roles by the
  critic+reviewer+mutation-tester+revenger definition, **34** without the revenger (the report's 34; say which
  definition). `w1.ready.partial` holds **55** entries now (mtime 14:40:09, i.e. after the tip commit) though the
  report says 40; `w1/*.md` at depth 1 = **47** files (report: "50+ seat outputs"). `w1-results.json` and any
  `WAVE-DONE` marker are still absent — the report's "partially dispatched, not settled" statement is correct.
- D14 (low): the Landed table labels `f7281bc` "stage-1 freeze" while `corpus/lessons/round-50.md:3` and the wave
  brief call `3b02d573` the stage-1 freeze. Measured: `f7281bc` adds the claims, counter, population, controls and
  C2 command; `3b02d57` adds only the six receipts on top. Name both and state the freeze tip explicitly, or a
  checker pinning `3b02d573` will read the table as pointing at the wrong commit.

## Verified as passing (evidence)

- Sections and order: `grep -n '^## '` → `15 Work performed, 55 Landed changes, 73 Before → after measurements,
  84 Sources & frontier, 97 Trend verdicts, 110 SHONEN`.
- `grep -c '^## SHONEN'` → `1`.
- Four SHONEN boxes, all `[~]`, text/order equal to `SHONEN.md:5,7,9,11`; each carries a pointer that exists
  (`SKILL.md`, `LOG.md ## Round 50` at `LOG.md:1542`, `plans/round50_c1_verify.py`,
  `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`, `PROVINCE.md:129`).
- `Stale-lane:` and `Tool installs:` lines present (content correct; placement defect D8).
- Landed-changes table: 8 rows / 8 commits, all resolve (`git cat-file -e <c>^{commit}`); each row cites `## Round 50`.
- C1 after receipt exists, is tracked, and the report quotes it verbatim: `HONEST fixtures=126 admitted=126
  refused=0 error=0` / `REFUSALS total=20 clean=20 leaked=0` / `SEALED total=12 clean=12` + `SEALED total=18
  clean=18` / `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met` / `PREDICATE R50-C1 pass` / `# exit=0`,
  `REV d6f2fce…`, `TREE dirty=0`. The receipt's fence digest equals the tip blob:
  `git show HEAD:plans/fixture_fence.py | sha256sum` = `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`.
- Attribution across the gap between the scored revision and the tip is sound but unstated: `git diff --stat
  d6f2fce d45c5bb` touches only `LOG.md`, `SCORECARD.md`, `corpus/README.md`, `corpus/evidence/round50/c1-receipt.txt`
  — no `plans/` bytes. Add that one line to the C1 row.
- Sources & frontier: census re-run exit `0`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
  = `170`; tier `A=146 B=22 C=2`; status `mined=154 queued=8 rejected=8`; `S173`–`S177` present at
  `corpus/SOURCES.md:188-192`; `corpus/knowledge/fixture-honest-geometry.md` tracked; `corpus/QUALITY.md:1112` Q41
  present; lesson Gate has 5 `ADMIT` + 1 `REJECT` and 3 `Mistakes` rows (`corpus/lessons/round-50.md:9-30`).
- C1 structural counts the report states are correct: `plans/mutants50/c1-mutants.json` `count=15` /
  `dropped_unwitnessed=7`; `plans/sealed50/**.py` = `18`; `plans/refusals46/**.py` = `20`;
  `plans/honest50/population.txt` = `126` rows.
- Tip/push: `git rev-parse HEAD` = `git ls-remote origin refs/heads/master` = `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`.
- No model alias or route name in the report (G18 = `0`).

## Limits

- I did not re-score C1 (mutant leg is slow and belongs to the clean-run seats) and did not run the C1 counter at
  all; findings D1/D3 are read from receipts and committed blobs, not from a re-run. [INFERENCE] marks the one
  place I reason about which counter produced the receipt.
- The 71f5f5f/f7281bc/d45c5bb counts are produced by a re-implementation of `round50_c2_audit.py`'s token regex and
  resolution rules over `git show`/`cat-file` (no checkout, no worktree mutation), validated by matching the
  committed tool's own output at the tip (`279/219/60/279/…/0`, exit 0) and the receipt at `f7281bc`
  (`275/216/59/263/…/12`). A byte-identical re-run of the tool at `71f5f5f` is impossible without a checkout, which
  this seat is forbidden.
- Wave counts (`w1.ready.partial` 55, `w1/*.md` 47) are a snapshot while the wave still writes; the report's 40 and
  "50+" may have been true at filing. The defect is the missing pointer and timestamp, not necessarily the number.
- The report is a fleet-root file; I did not and must not edit it. All fixes are for the L1.
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50RevReportShape` was created under this seat's name and removed
  before yield; the clone, the counter blobs and the C2 re-implementation were all inside it.

VERDICT: 19-gate contract list delivered. Structure passes 8 gates outright (sections/order, SHONEN count, four
boxes with canonical text and `[~]` markers, stale-lane + tool-install content, landed-changes table, sources
census, tip/push match, no alias). Report must not be filed as-is: 2 blockers (D3 uncommitted C1 harness attributed
to a commit + scored receipt that cannot attribute its counter; D1/D2 before-side revision misattribution), 3
majors (D5 missing C2 after receipt, D6 untracked `w1/` pointers, D4 false clean-tree statement), and 8 minors
(SHONEN literal form/placement, misroot sweep, gate outputs, two pointerless trend bullets, uncited axis numbers,
stale wave counts, stage-label). No R50-C1 or R50-C2 admission is asserted or implied by this seat.
