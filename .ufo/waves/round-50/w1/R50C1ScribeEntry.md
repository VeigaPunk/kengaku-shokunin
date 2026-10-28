# R50C1ScribeEntry — `corpus/knowledge/fixture-honest-geometry.md` draft (R50-C1, novelty)

role: scribe · claim served: R50-C1 (novelty) · lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
date: 2026-10-28 · author seat: R50C1ScribeEntry · write scope: this file only (no production file touched)
item: draft a `corpus/knowledge/` entry for the honest-geometry instrument — provenance trio, construct,
126-population composition + pin, the five refused honest classes and their documented git shapes, the controls
that must fail, and the measured base numbers.

REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 (lane tip at the final read; every digest below re-taken there)
Freeze 3b02d573d58cc6d2e0d27ef92ac0815354912252 is an ancestor of that tip (`git merge-base --is-ancestor` exit 0,
verified twice: at 5c56819… and again at c3372a9…).
Entry blob measured: `corpus/knowledge/fixture-honest-geometry.md` sha256 `231288ff358289c6baba2e73cb8d7ad564f01587d79bb9e72719d197cb8a8ed0`,
landed by commit 822f3b7 and unchanged at c3372a9.

VERDICT: **DRAFTED, NOT MEASURED.** The complete replacement entry is in §4 and is evidence-grounded; the landed
entry's `recheck:` currently asserts an unmeasured state and the entry has no controls section, no measured
refusal/sealed numbers, no anchors in its `source:` line and no `corpus/README.md` index/coverage row (Q7). No
R50-C1 admission is claimed; no counter was executed by this seat (numbers are cited from committed receipts, and
the mutant state is attributed to the wave brief, not re-derived).

## Axes named

- **novelty (primary, R50-C1).** The knowledge entry is the construct record the novelty claim rests on: the lane's
  first frozen honest denominator plus one predicate that scores over-refusal, under-refusal and mutation together.
  The landed entry (42 lines) does not state the construct, the literals, the controls or the refused-class reasons,
  so the artifact a reader would re-derive from is missing exactly the parts that make the instrument novel.
- **quality (secondary, non-harm).** The draft repairs a Q1 provenance defect (a `recheck:` that claims
  `admitted=126` at a revision whose fence still admits 113) and a Q7 landing defect (entry without README index
  or coverage-map row), without editing anything.
- **coverage — not claimed this round** (operator-capped); **C2 calibration — untouched** by this seat.

## 1. Prerequisites checked before any work

The lane moved twice while this seat read it; the revision recorded above is the final one, and every claim below
was re-read or re-hashed at it. Reads only — no clone, no counter, no write outside this report.

```
$ git rev-parse HEAD
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
$ git log -1 --format='%H %ci %s'
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 2026-10-28 14:25:30 -0300 round-50: C1 counter open-window repair (module attribution keyed by path, not basename); predicate unchanged
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD ; echo $?
0
$ git show HEAD:plans/fixture_fence.py | sha256sum
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  -
$ git show HEAD:plans/round50_c1_verify.py | sha256sum
d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  -
$ git show HEAD:plans/honest50/population.txt | sha256sum
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  -
$ git show HEAD:corpus/knowledge/fixture-honest-geometry.md | sha256sum
231288ff358289c6baba2e73cb8d7ad564f01587d79bb9e72719d197cb8a8ed0  -
```

The counter digest moved under the recorded open window: `f9b9873e…` (stage-1 freeze) → `d8787b34…`
(commit c3372a9; `plans/round-50-claims.md:153` records old→new with "predicate unchanged"). Both digests are
named in the draft's `verified-at:` so a reader can bind the entry to the instrument actually measured.

Timeline of the lane while this seat ran (recorded so the moving tip is not a surprise in the receipt):
`5c56819` (wave spec) → `822f3b7` (S173–S177 sources + the entry + C2 corrections; 14:24:13) → `c3372a9`
(counter repair; 14:25:30). The entry blob did not change between 822f3b7 and c3372a9.

## 2. Deliverable — the entry draft

Apply at `corpus/knowledge/fixture-honest-geometry.md` (L1 integration; this seat may not write `corpus/`). The
draft is a full replacement: the landed entry is 42 lines and lacks the construct, controls and base numbers the
item requires. Q6: it extends the round-46 outside-read instrument (still the instrument for that property) and the
round-48/49 honest-population work; it supersedes no entry.

````markdown
source: S173 — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc — the gitfile mechanism (:26-28), `objects/info/alternates` (:80-89), `refs/replace/<obj-sha1>` (:116), `shallow` (:261-266), `commondir` (:268-273), `worktrees/<id>/gitdir` (:285-292), tag v2.56.0, capture `corpus/evidence/round50/gitrepository-layout.adoc` sha256 `39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439`; S174 — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-init.adoc — `--separate-git-dir` (:69-74), capture sha256 `123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95`; S175 — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc — the `gitdir` back-pointer a moved linked worktree must update (:390-401), capture sha256 `ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc`; S176 — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc — the `refs/replace/` namespace and the replaced object's SHA as the ref name (:20-24), capture sha256 `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631`; S177 — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc — `FETCH_HEAD` records the fetched refs and the objects they point at (:42-43), capture sha256 `fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e`; all five rows opened 2026-10-28.
verified-at: 2026-10-28 (lane REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1; counter `plans/round50_c1_verify.py` sha256 `d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2`, stage-1 digest `f9b9873e…`; base fence `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`)
recheck: 180d — pinned at git tag `v2.56.0`: re-fetch the five URLs at that tag and compare each capture's sha256, then run `python3 plans/round50_c1_verify.py --lane . --skip-mutants` on a **clean clone** of the tip and compare the `HONEST` line. At the stage-1 tree (base fence `05d5fe03…`, REV `f7281bc…`) the command prints `HONEST fixtures=126 admitted=113 refused=13` and `PREDICATE R50-C1 fail` (receipt `.ufo/waves/round-50/claims/c1-control-do-nothing.txt`); the R50-C1 target is the same `HONEST` line at `admitted=126 refused=0` with `PREDICATE R50-C1 pass` and exit 0 after the stage-2 fence repair.

# Fixture honest-geometry: what a git store may honestly look like inside a fixture

## Construct

A fixture fence answers one question about a fixture directory `d`: is the fixture's git store — and every store,
file and argv entry the graded tool can reach — inside `d`? `plans/fixture_fence.py` answers it in
`breach(d, argv, tool) -> str | None` (a reason refuses, `None` admits) with a plain-init **allowlist**: `.git`
must be a real directory; refs live only under `refs/heads|tags`; `info/` holds only `exclude`; `config` is parsed
line by line against a `[core]` key allowlist; one walk rejects any symlink, special file or hard-linked file; and
no git child is started (the store classification is the proof). Allowlisting the shape a plain `git init` writes
over-refuses every ordinary repository state git itself writes beyond that shape. The honest distinction is
**containment after resolution**, not the entry name: a gitfile whose target resolves inside `d` names a store
that may be classified; one that resolves outside is a redirect.

`plans/round50_c1_verify.py` scores both directions at once. One command prints five legs and one predicate:

| leg | what must hold |
|---|---|
| `POPULATION` | each of the 126 frozen honest fixtures is rebuilt and its canonical `tree_sha256` equals the pinned row; frozen literal `HONEST_TOTAL = 126` |
| `HONEST` | every honest fixture is **admitted** (`breach() is None`); a refusal is over-refusal, an exception is `error=`, never an admission |
| `REFUSALS` | all 20 frozen hostile modules of `plans/refusals46/` are refused (34 module-fixture cases); frozen literal `REFUSALS_TOTAL = 20` |
| `SEALED` | the 12 frozen modules of `plans/sealed46/` (15 cases) plus the blind `plans/sealed50/` modules are refused; `SEALED50_MIN = 6`, so at least 18 modules once `plans/sealed50/` exists |
| `MUTANTS` | each row of `plans/mutants50/c1-mutants.json` is applied to the fence under test and must change the verdict vector; frozen floor `MUTANT_MIN = 12` rows with at least 12 caught |

`PREDICATE R50-C1 pass` and exit 0 only when all five hold, and the predicate is bound to a clean tree (a dirty
tree prints `TREE dirty=<n>` and fails unless `--allow-dirty`, which is a controls-only testing flag). The repair
window may change the counter only before the first scored run; it must record old→new digests and may not change
the predicate sentence, the four leg names or the literals (`plans/round-50-claims.md`).

Why this is an instrument and not a recount: the standing counters `plans/round45_c1_verify.py` and
`plans/round46_c1_verify.py` measure a fence's *under*-refusal and its outside-`d` reads; round 48 first measured
over-refusal (`HONEST fixtures=120 admitted=112 refused=8`); round 49 built the population to 124 and never landed
or scored a repair. Round 50 freezes the honest denominator and scores admission, refusal and mutation in one
predicate. `plans/round46_c1_verify.py` remains the instrument for the outside-`d` read property; this entry
extends it, it does not replace it.

## Population (frozen, pinned)

| family | fixtures | source |
|---|---|---|
| `battery42` | 29 | `plans/battery42/*.py` |
| `battery43` | 42 | `plans/battery43/*.py` |
| `battery44` | 33 | `plans/battery44/*.py` |
| `r46novel` | 9 | `plans/honest50/modules/r46novel/` |
| `novel48` | 7 | `plans/honest50/modules/novel48/` |
| `novel49` | 4 | `plans/honest50/modules/novel49/` (`n17`–`n20`) |
| `novel50` | 2 | `plans/honest50/modules/novel50/` (`n21`, `n22`) |
| **total** | **126** | 104 battery + 22 novel documented classes |

Pin: `plans/honest50/population.txt` sha256 `b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69`
(126 `HONEST` rows plus a four-line provenance header); builder `plans/honest50/build_honest_population.py`
sha256 `b2560ebc9c9d1451c47c89039868f4f60d440cd1fa52b92f00baf6d0324a8002`. The builder receipt
(`plans/honest50/builder-receipt.txt`, REV `71f5f5f…`) prints
`COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 novel49=4 novel50=2`, `fixtures=126`,
`modules=44`, and `MASK .git/index .git/worktrees/*/index`.

Identity is the builder's canonical digest: `D <rel> <mode>` per directory and `F <rel> <mode> <content-sha256>`
per file, sorted; only the two git stat caches are masked (`.git/index` at any depth,
`.git/worktrees/<name>/index`), each measured rather than assumed. A `POPULATION … mismatched=0 build_errors=0`
line says every fixture rebuilt byte-identically to its pin on this host.

## The five honest classes the base fence refuses

The base fence refuses 13 of 126 honest fixtures. Five are the documented shapes this entry rests on — every one
is inside `d`, written by a documented git mechanism, and refused by name/shape:

| class | fixture builds | documented shape and source | base-fence reason (verbatim) |
|---|---|---|---|
| `n17` replace refs | `git replace <first> HEAD` | `refs/replace/<obj-sha1>` is a ref whose **name** is the SHA of the replaced object — S176 (:20-24), S173 (:116) | `repo/.git/refs/replace is not refs/heads or refs/tags` |
| `n18` shallow boundary | `git fetch --depth 1 ../src` then `reset --hard FETCH_HEAD` | `.git/shallow` is written and maintained by the shallow-clone mechanism; `FETCH_HEAD` records the fetched refs and their objects — S173 (:261-266), S177 (:42-43) | `repo/.git/FETCH_HEAD is not a plain-init entry` |
| `n20` linked worktree | `git worktree add --relative-paths ../wt feature` | the work tree carries a `.git` **file** naming `repo/.git/worktrees/wt`, whose `gitdir` file points back — S173 (:285-292), S175 (:390-401) | `wt/.git is a file (gitdir redirect), not a directory` |
| `n21` separate gitdir | `git init --separate-git-dir ../store wt`, gitfile rewritten to `gitdir: ../store` | `--separate-git-dir` writes "a text file there containing the path to the actual repository" — S174 (:69-74), S173 (:26-28) | `wt/.git is a file (gitdir redirect), not a directory` |
| `n22` alternates inside `d` | `lane/.git/objects/info/alternates` = `../../../main/.git/objects` | `objects/info/alternates` records paths to alternate object stores the repository borrows from, one pathname per line, resolved relative to the object database — S173 (:80-89) | `lane/.git/objects/info/alternates present (object-store redirect)` |

The remaining eight refused fixtures include seven earlier-class over-refusals — `n03` detached HEAD, `n07`
reflog/gc, and `n12`–`n16` (local `[user]` config, `[remote "origin"]`, stash reflog, commit-graph, notes reflog).
The eighth is the one refusal no committed receipt names: the counter prints `HONEST-REFUSED` for `refused[:12]`
(`plans/round50_c1_verify.py:216`), so 12 of the 13 refusals are enumerated and the thirteenth is not. All five
classes above are in the enumerated set.

## Controls that must fail

Four committed control fences are run through the same counter (`--allow-dirty` on the stage-1 tree); each must
reach `PREDICATE R50-C1 fail`, or the counter and the round are invalid:

| control | what it skips | observed (committed receipt, REV `f7281bc…`) |
|---|---|---|
| `plans/fixture_fence.py` @ stage 1 (do-nothing) | all claimed work | `HONEST fixtures=126 admitted=113 refused=13` → `PREDICATE R50-C1 fail`, exit 1 |
| `plans/controls50/admit_all.py` | refusal reasoning | `HONEST fixtures=126 admitted=126 refused=0` but `REFUSALS total=20 clean=0 leaked=34`, `SEALED total=12 clean=0 leaked=15` → fail |
| `plans/controls50/refuse_all.py` | admission reasoning | `HONEST fixtures=126 admitted=0 refused=126` while `REFUSALS 20/20` and `SEALED 12/12` → fail |
| `plans/controls50/keyed_names.py` (Q39 shape keys) | boundary reasoning (name/shape-keyed, no target resolution) | `HONEST fixtures=126 admitted=123 refused=3` (`n20` commondir, `n21` gitfile, `n22` alternates), `REFUSALS clean=7 leaked=25`, `SEALED clean=6 leaked=9` → fail |

Receipts: `.ufo/waves/round-50/claims/c1-control-{do-nothing,admit_all,refuse_all,keyed_names}.txt` (committed at
3b02d57). The same four controls were re-run on a clean `git clone --shared` of the freeze with the repaired
counter and reproduced these numbers (`TREE dirty=0`, REV `3b02d573…`,
`.ufo/waves/round-50/w1/R50C1CritDoNothing-*.txt`), and the base-fence before-receipt
(`.ufo/waves/round-50/w1/C1ExecCleanRun/receipt-base-fence.txt`, REV `3b02d573…`) reproduced
`HONEST … 113/13`, `REFUSALS 20/20`, `SEALED 12/12`, `PREDICATE fail`, exit 1, byte-identically across two runs
modulo the mkdtemp suffix.

## Measured base numbers (before the repair)

`.ufo/waves/round-50/claims/c1-control-do-nothing.txt`, verbatim:

```
REV f7281bc90ca953ff3b84413a21023b9793ef2043
TREE dirty=1
FENCE /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

On the clean clone at the freeze the same lines print with `TREE dirty=0` and exit 1. The target (not yet
measured at any revision, and not claimed here) is `HONEST admitted=126 refused=0`, `SEALED` ≥ 18 with
`leaked=0`, `MUTANTS caught≥12 floor=12 verdict=met`, `PREDICATE R50-C1 pass`, exit 0.

The mutant leg is candidate-only at this revision: `plans/mutants50/c1-mutants.json` holds 23 inline diffs whose
declared `candidate_fence_sha256` is `b687b1d9…`, an object that does not exist in the lane clone
(`git cat-file -t` → `fatal: Not a valid object name`); the wave brief records that 4 of 23 rows change the base
fence's verdict vector. The frozen floor is 12, and QUALITY Q38 requires the kill direction of every frozen row to
be witnessed on the repaired fence before scoring — stage-2 work, not this entry's number.

## Scope limits (negative space)

- The counter measures **admission decisions only**. Outside-`d` reads while deciding are not observed (the
  round-46 counter's strace legs remain the instrument); io_uring is not observed; host paths outside the scratch
  root are not counted; post-admission fence behaviour is unexercised.
- The population is "states git itself writes", not "every state a third-party tool (libgit2, jj, an IDE) may
  write". A standalone `commondir` file is a decided exclusion, not an unknown: git writes `commondir` only for a
  linked worktree, which `n20` already holds.
- Identity pins are host-git-sensitive (`hooks/*.sample`, `info/exclude`, `worktree --relative-paths` ≥ 2.48; git
  2.56.0 here); a pin mismatch is reported as `POPULATION … mismatched=`, never silently re-pinned.
- The refusal leg is fixed at 20 modules / 12 sealed modules; a hostile shape absent from those batteries is
  unmeasured. The `SEALED ≥ 18` literal is enforced only once `plans/sealed50/` exists; at this revision it does
  not, so the leg scores 12.
- The mutant floor is a floor, not correctness: up to 11 survivors still print `verdict=met`.
- Receipts cap the honest-refusal listing at 12 of 13, so the full refused set is not recoverable from the receipt
  alone.

Falsifiers: a frozen honest fixture that rebuilds to its pinned identity and is refused by the repaired fence
falsifies the over-refusal claim; a frozen hostile module admitted by the repaired fence falsifies the
under-refusal claim; a mutant row that leaves the verdict vector unchanged is a survivor, not a kill; a
`POPULATION mismatched>0` run invalidates the run before any fence result is read.

## Extends

`corpus/knowledge/benchmark-task-validity-checklist.md`'s "an artefact and a locus per axis" discipline applied to
the lane's own fence; it extends `plans/round46_c1_verify.py`'s outside-read instrument and the round-48/49
honest-population work. It supersedes no entry.
````

### 2a. Q7 companions the entry needs in the same commit

QUALITY Q7: "Entry file, its `corpus/README.md` index row and its coverage-map row land together." At REV
c3372a9, `grep -c 'fixture-honest-geometry' corpus/README.md` → `0`, so the 822f3b7 landing is short of Q7. Two
rows to add (integration owner):

Knowledge index table (after the last `| knowledge/... |` row):

```markdown
| `knowledge/fixture-honest-geometry.md` | Fixture-fence honest geometry: a frozen 126-fixture honest population and one predicate (admit every honest fixture, refuse every frozen hostile module, kill ≥12 mutants), the five documented in-`d` store shapes the base fence over-refuses (replace refs, shallow/FETCH_HEAD, linked worktree, separate gitdir, in-`d` alternates), and the four controls that must fail | S173–S177 — `corpus/SOURCES.md` rows (git v2.56.0), opened 2026-10-28 |
```

Coverage map (after the last coverage bullet):

```markdown
- **Fixture honest geometry**: covered at measured depth (round 50, 2026-10-28) — knowledge/fixture-honest-geometry.md; S173–S177. The 126 identity-pinned honest fixtures (104 battery + 22 novel classes) are the denominator for the lane's first predicate that scores over-refusal and under-refusal together; base fence `05d5fe03…` admits 113/126 and all four controls fail. Not an outside-`d` read proof (round-46 counter), not io_uring, not third-party-tool store shapes.
```

## 3. Defects found in the landed entry (822f3b7, blob `231288ff…`) — what the draft repairs

| # | landed line(s) | defect | drafted repair |
|---|---|---|---|
| 1 | 3 (`recheck:`) | asserts `python3 plans/round50_c1_verify.py --lane .` "prints `HONEST fixtures=126 admitted=126 refused=0`". At every revision that exists (base fence `05d5fe03…`, REV `f7281bc…`/`3b02d573…`/`c3372a9…`) it prints `admitted=113 refused=13` + `PREDICATE fail`. The line reports the claim's target as a measured recheck — a Q1 provenance defect. | recheck names the command, the measured stage-1 output (113/13, receipt path) and the post-repair target (126/0) separately |
| 2 | 1 (`source:`) | names the five ids and a capture directory but gives no URL, no line anchor and no capture digest; Q1 requires id + URL + exact anchor | one `source:` line with each URL, its anchor ranges, the capture path and sha256 |
| 3 | 2 (`verified-at:`) | names neither the lane revision nor the counter digest (which changed under the open window `f9b9873e…` → `d8787b34…`, claims line 153) | names REV `c3372a9…`, both counter digests, and the base fence digest |
| 4 | 5–33 | no construct section: no `breach()` contract, no leg table, no literals (`126`, `20`, `12`, `SEALED50_MIN=6`), no clean-tree rule, no "what was not observable before" | §Construct |
| 5 | 12–18 | class table has no base-fence refusal reason and no fixture-build shape, so the reader cannot reconcile `refused=13` with five classes | adds build + documented anchor + verbatim refusal reason; states the remaining eight and the receipt's 12-of-13 print cap |
| 6 | 27–33 | "Measured" has only the HONEST line; `REFUSALS 20/20` and `SEALED 12/12` are absent; line 32 implies `plans/sealed50/` exists (it does not at REV; `SEALED50_MIN=6` gates it) | full verbatim base receipt + explicit absence of `sealed50` + the frozen literals |
| 7 | — | no controls section, although the claim's controls are part of what the entry documents (a control reaching `pass` invalidates the counter) | §Controls with the four observed receipts |
| 8 | — | no mutant-leg statement (23 candidate rows, declared target digest not an object at REV, 4/23 base-fence changes attributed to the wave brief, floor 12, Q38 witness is S2) | §Measured base numbers, mutant paragraph |
| 9 | 37–42 | limits omit the 12-of-13 print cap, the host-revision binding, and that the `SEALED ≥ 18` literal is not enforced while `sealed50/` is absent | §Scope limits |
| 10 | — | Q7: no `corpus/README.md` index row and no coverage-map bullet in the landing commit | §2a rows |

Additional findings, recorded for the L1 (not repaired here because they are outside this item's file):

- **Anchor drift in S175.** `corpus/SOURCES.md:190` cites `git-worktree.adoc:285-292` for the `gitdir` back-pointer;
  in the captured v2.56.0 file, `:285-292` is the `--reason`/`_<worktree>_` block and the back-pointer text is at
  `:390-401` ("If you manually move a linked worktree, you need to update the `gitdir` file ... run `git worktree
  repair`"). The `worktrees/<id>/gitdir` definition itself is `gitrepository-layout.adoc:285-292` (S173). The draft
  cites both correctly; the S175 anchor could be narrowed in a later SOURCES repair (append-only).
- **Stale population README.** `plans/honest50/README.md` (committed, unchanged at c3372a9) is the round-49
  document: title `plans/honest49/`, "124 fixtures", "42 modules (22 battery + 20 novel)", no `novel50` row. The
  builder receipt in the same directory says `fixtures=126`, `modules=44`. The entry must cite
  `population.txt` + `builder-receipt.txt` (as the draft does), and the README should be corrected in a later
  stage; a reader following the README alone would derive the wrong denominator.
- **Mutant battery target.** `plans/mutants50/c1-mutants.json` declares
  `candidate_fence_sha256=b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`; `git cat-file -t` on it
  in the lane clone fails (`fatal: Not a valid object name`). The rows remain candidate-only as the claims say;
  the S2 re-derivation owns the witness.
- **Receipt internal inconsistency.** `C1ExecCleanRun/receipt-base-fence.txt` says "eight further honest fixtures
  are refused ... (n03, n07, n12, n13, n14, n15, n16)" — that is seven names for eight fixtures; consistent with
  the counter's `refused[:12]` print cap, the thirteenth fid is unnamed. The draft states exactly this rather than
  inventing the eighth name.

## 4. Evidence map (what each drafted claim rests on)

| drafted claim | evidence read at REV c3372a9 |
|---|---|
| fence construct (allowlist, `.git` file refused, refs heads/tags only, no git child) | `plans/fixture_fence.py:1-49` (module docstring + allowlist constants) |
| counter legs/literals/clean-tree rule | `plans/round50_c1_verify.py:1-73` (docstring, `HONEST_TOTAL`, `MUTANT_MIN`, `REFUSALS_TOTAL`, `SEALED46_TOTAL`, `SEALED50_MIN`, `POPULATION_SHA`), `:157-178` (`--allow-dirty`, `TREE dirty`), `:211-217` (HONEST print and `refused[:12]`), `:260-290` (leg totals, predicates) |
| 126 composition: 29/42/33/9/7/4/2 | `awk 'NR>2 && $1=="HONEST"{c[$3]++} …' plans/honest50/population.txt`; `plans/honest50/builder-receipt.txt` `COUNTS` line |
| population pin | `plans/honest50/population.sha256` and `git show HEAD:plans/honest50/population.txt \| sha256sum` |
| identity masking | `plans/honest50/builder-receipt.txt` `MASK .git/index .git/worktrees/*/index`; `plans/honest50/README.md` §Identity (mechanism only; its counts are stale) |
| five classes' builds | `plans/honest50/modules/novel49/{n17_replace_ref,n18_shallow_fetch,n20_linked_worktree}.py`, `novel50/{n21_separate_gitdir,n22_alternates_in_d}.py` (docstrings + `build()`) |
| documented shapes + anchors | `corpus/evidence/round50/gitrepository-layout.adoc:24-30,80-89,116,261-273,278-292`; `git-init.adoc:69-74`; `git-worktree.adoc:390-401`; `git-replace.adoc:20-24`; `git-fetch.adoc:42-43` (all read; capture sha256s recomputed and match the S173–S177 rows) |
| base numbers (113/13, 20/20, 12/12) | `.ufo/waves/round-50/claims/c1-control-do-nothing.txt:1-22`; clean-clone reproduction `.ufo/waves/round-50/w1/C1ExecCleanRun/receipt-base-fence.txt` and `run4.stdout.raw:1-20` |
| four controls' observed numbers | `.ufo/waves/round-50/claims/c1-control-{admit_all,refuse_all,keyed_names}.txt`; re-runs `.ufo/waves/round-50/w1/R50C1CritDoNothing-*.txt` (REV 3b02d57, TREE dirty=0) |
| control fence shapes | `plans/controls50/{admit_all,refuse_all,keyed_names}.py` docstrings |
| refusal/sealed counts 20 / 12 / 15 cases / 34 cases | `ls plans/refusals46/*.py \| wc -l` = 20, `ls plans/sealed46/*.py \| wc -l` = 12; `admit_all` receipt `leaked=34` / `leaked=15` |
| open-window repair old→new digest, predicate unchanged | `plans/round-50-claims.md:149-157`; `git log -1 c3372a9`; `git show HEAD:plans/round50_c1_verify.py \| sha256sum` = `d8787b34…` |
| mutant battery candidate-only, 23 rows | `plans/mutants50/c1-mutants.json` (`count: 23`, `candidate_fence_sha256: b687b1d9…`); `git cat-file -t b687b1d9…` fails |
| Q7 missing rows | `grep -c 'fixture-honest-geometry' corpus/README.md` → 0; `corpus/README.md:24-33` (index table), `:270+` (coverage map) |

## 5. Exact commands run (read-only)

Principal commands, all from `/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless shown otherwise; no command
wrote to the lane, no clone was made, no counter was executed.

```
git rev-parse HEAD
git log -4 --format='%H %ci %s'
git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD ; echo $?
git merge-base --is-ancestor f7281bc90ca953ff3b84413a21023b9793ef2043 5c56819f7964f4af19c960de08a49cd8f95781ce ; echo $?
git show HEAD:plans/fixture_fence.py | sha256sum
git show HEAD:plans/round50_c1_verify.py | sha256sum
git show HEAD:plans/honest50/population.txt | sha256sum
git show HEAD:corpus/knowledge/fixture-honest-geometry.md | sha256sum
git show 3b02d573d58cc6d2e0d27ef92ac0815354912252:<path> | sha256sum      (fence, counter, population, mutants)
git show 822f3b7 --stat --oneline ; git show c3372a9 --stat --oneline
git show 822f3b7 -- plans/round-50-claims.md
git diff corpus/QUALITY.md ; git diff plans/round50_c1_verify.py
git status --porcelain
sha256sum plans/fixture_fence.py plans/round50_c1_verify.py plans/honest50/population.txt
awk 'NR>2 && $1=="HONEST"{c[$3]++} END{for(k in c) print k, c[k]}' plans/honest50/population.txt | sort
grep -c '^HONEST-REFUSED' .ufo/waves/round-50/claims/c1-control-do-nothing.txt
grep -n 'refused\[:12\]' plans/round50_c1_verify.py
grep -n 'SEALED50_MIN\|MUTANT_MIN\|REFUSALS_TOTAL\|HONEST_TOTAL\|POPULATION_SHA' plans/round50_c1_verify.py
grep -n '^HONEST fixtures\|^REFUSALS total\|^SEALED total\|^PREDICATE\|^REV\|^TREE' .ufo/waves/round-50/claims/c1-control-*.txt
cat .ufo/waves/round-50/claims/c1-control-do-nothing.txt
cat .ufo/waves/round-50/claims/c1-control-{admit_all,refuse_all,keyed_names}.txt
sed -n '1,60p' .ufo/waves/round-50/w1/C1ExecCleanRun/receipt-base-fence.txt
for f in .ufo/waves/round-50/w1/R50C1CritDoNothing-*.txt; do sed -n '1,9p' "$f"; grep -E '^(REFUSALS|SEALED|PREDICATE|HONEST)' "$f"; done
git cat-file -t b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52
grep -c 'fixture-honest-geometry' corpus/README.md
grep -n 'S17[3-7] |' corpus/SOURCES.md
git show 3b02d573d58cc6d2e0d27ef92ac0815354912252:corpus/SOURCES.md | grep -c S173     -> 0 (rows land at 822f3b7)
ls plans/refusals46/*.py | wc -l ; ls plans/sealed46/*.py | wc -l ; ls plans/sealed50            -> 20, 12, No such file
python3 -c 'import json; s=json.load(open("plans/mutants50/c1-mutants.json")); print(len(s["mutants"]), s["candidate_fence_sha256"])'
sed -n '1,60p' plans/honest50/modules/novel49/{n17_replace_ref,n18_shallow_fetch,n20_linked_worktree}.py
sed -n '1,60p' plans/honest50/modules/novel50/{n21_separate_gitdir,n22_alternates_in_d}.py
sed -n '24-30p;78-90p;258-275p' corpus/evidence/round50/gitrepository-layout.adoc    (anchors verified by grep -n)
grep -n 'gitfile\|separate-git-dir\|alternates\|commondir\|shallow\|worktrees\|FETCH_HEAD\|refs/replace' corpus/evidence/round50/*.adoc
sed -n '10-60p' corpus/QUALITY.md
```

Verbatim outputs that are evidence are quoted in §1, §2 and §4; the full digests and the base receipt lines are
transcribed above rather than paraphrased.

## 6. Limits of this report

- **No execution.** This seat did not run `plans/round50_c1_verify.py` (role instruction: do not rerun work merely
  to decorate the report; the freeze, the four controls and the clean-clone before-receipt already exist as
  committed/wave receipts). Everything numeric is cited from those receipts; every digest, count and composition
  number was recomputed read-only at REV c3372a9.
- **Mutant state is attributed, not re-derived.** "4 of 23 rows change the base fence's verdict vector" comes from
  the wave brief (`build_spec.py`, `w1-spec.json`); no mutant leg was run.
- **Receipt print cap.** The refused-fid list is `refused[:12]` by construction; the thirteenth fid is unknown from
  any committed receipt, and the draft says so instead of naming it.
- **Timing.** The lane advanced twice during the seat (`5c56819` → `822f3b7` → `c3372a9`); the report records the
  final revision and notes that the entry blob did not change. A later tip that changes the entry or the counter
  is not covered here.
- **No admission.** Nothing in this report admits R50-C1 or R50-C2; no SCORECARD/LOG/corpus byte was touched.

## 7. Scratch

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ScribeEntry` was created, used only as `TMPDIR` for the final
read-only digest/pin pass, removed in the same command, and confirmed absent:

```
$ rm -rf -- "$S"; test ! -e "$S" && echo SCRATCH_REMOVED
SCRATCH_REMOVED
```

No scratch tree remains on disk; no `/tmp` path is cited as evidence.

VERDICT: **DRAFTED, NOT MEASURED.** The replacement entry (§2) supplies the provenance trio with URLs, anchors,
capture digests and the real measured base output; the construct with its five legs, four literals and clean-tree
binding; the 126-row composition with its pin and builder receipt; the five refused honest classes with their
documented shapes and verbatim base-fence reasons; the four controls that must fail; the measured base numbers;
and the mutant-floor caveats. The landed entry's `recheck:` (unmeasured `admitted=126`), missing controls/base
numbers, and missing Q7 README/coverage rows are the defects the draft repairs. No R50-C1 admission is claimed.
