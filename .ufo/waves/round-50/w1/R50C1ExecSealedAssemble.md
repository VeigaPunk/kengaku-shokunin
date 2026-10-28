# R50C1ExecSealedAssemble — `plans/sealed50/` candidate assembled and gated

Seat `R50C1ExecSealedAssemble` (executor, leaf), serving **R50-C1 (novelty)**. Wave `round-50/w1`, lane
`kengaku-shokunin`. Item: assemble the `plans/sealed50/` candidate from the blind critic modules and the hostile
variants — de-duplicate by fixture identity, verify the FIXTURES contract and two-build determinism, reject
modules whose fixture is not refused by the BASE fence, and emit the candidate plus a manifest row per module.

Axes named: **novelty** (primary: the sealed leg's held-out hostile rows), with three engineering axes the item
imposes — fixture-identity reproducibility, base-refusal honesty, and counter consumability. Coverage and
calibration (C2) are untouched. **No admission of R50-C1 or R50-C2 is claimed here** and no production file was
edited, committed, pushed, stashed or checked out.

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252      # stage-1 freeze; every measurement ran against it
LANE_TIP_AT_START d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
ANCESTRY git -C <lane> merge-base --is-ancestor 3b02d57… HEAD  -> exit 0   (freeze IS an ancestor of the tip)
CLONE /fast/scratch/hyaku/kengaku-r50/R50C1ExecSealedAssemble/lane
      git -C …/lane rev-parse --show-toplevel = that clone · rev-parse HEAD = 3b02d57… · status --porcelain = 0 lines
FENCE plans/fixture_fence.py 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
      (the clone's fence digest equals the frozen BASE digest)
ENV   Python 3.14.8 · git 2.56.0 · Linux 7.2.11-arch1-1
```

Every git fixture command ran through the lane's own `Ctx` inside the clone (`Ctx.ENV` per child, no global git
env was exported). Nothing was installed; no pacman/uv/npx transaction was attempted.

## Candidate pool — 30 module files, 40 fixtures

| source | files | what |
|---|---|---|
| `plans/sealed50/` @ lane tip | 18 | the S3-landed set (blind modules copied in by the S3 commit + the hostile `s50_01…s50_10` variants) |
| `C1CritBlind1/sealed/` | 2 | `s50_alternates_dotdot_abs`, `s50_gitfile_symlink_chain` |
| `R50C1CritBlind2/sealed/` | 2 | `x1_commondir_escape`, `x2_gitfile_alternates_escape` |
| `C1CritBlind3/sealed/` | 2 | `b1_replace_ref_target_outside_store`, `b2_fetch_head_hardlink_out` |
| `C1CritBlind4/sealed/` | 2 | `c4_gitfile_delimiter`, `c4_gitfile_store_include` |
| `C1CritBlind5/sealed/` | 2 | `h_alternates_chain`, `h_wt_commondir_out` |
| `C1CritBlind6/sealed/` | 2 | `s6_gitfile_rel_objects_link`, `s6_second_store_mount` |

Eight of the twelve blind files are **byte-identical** to their `plans/sealed50/` copies; four are blind-only
(`h_alternates_chain`, `h_wt_commondir_out`, `x1_commondir_escape`, `x2_gitfile_alternates_escape`); one
diverges (`s6_second_store_mount`, blind `cfb0005d…` vs lane `f2425983…`, see Finding 4).

## Gates (definitions used)

1. **FIXTURES contract** — module imports; `FIXTURES` is a non-empty list; each row is a dict carrying
   `fid`/`tool`/`expect`/`defects`/`build` with the first three non-empty strings, `defects` a list, `build` a
   callable; `build(ctx, d)` returns `list[str]`; the fixture dir survives; fids unique inside the module.
2. **Two-build determinism** — the fixture is built, destroyed, and rebuilt **at the identical absolute fixture
   path**; the population builder's canonical `tree_identity` and the normalised `argv` must be equal. (Rebuild
   at the identical path is the definition the population builder uses; a *different* absolute root is measured
   separately as a portability axis, because several hostile modules embed their build path **by design**.)
3. **BASE refusal** — the frozen BASE fence `05d5fe03…` must return a truthy `breach()` for **every** fixture of
   the module. The verdict travels in a child process exit status exactly as the counter does it
   (10 = BREACH, 11 = ADMIT, 12 = ERROR), so an exception is never an admission.
4. **De-duplication by fixture identity** — one survivor per `fid` across modules, and one survivor per
   byte-identical build identity `(tree_sha256, tool, normalised argv)`. The better contract/portability tuple
   wins; ties prefer the lane variant (the integration target), then name order.

Driver (copied verbatim into this directory): `assemble.py`.

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r50/R50C1ExecSealedAssemble
$ git clone --shared -q <lane> "$S/lane"; git -C "$S/lane" checkout -q 3b02d57…
$ python3 assemble.py --lane "$S/lane" --work "$S/work" --candidates "$S/candidates" --out "$S/out"
CANDIDATES modules=30 fixtures=40
KEPT modules=21 fixtures=26
DROPPED modules=9
```

## Result — 21 modules / 26 fixtures accepted, 9 module files dropped

`assemble.log` is the verbatim gate log. Drops in full:

| dropped file | sha256 | reason |
|---|---|---|
| `c4_gitfile_delimiter.py` (blind copy **and** lane copy, identical) | `95429f87…` | **gate: both fixtures nondeterministic** |
| `b1_replace_ref_target_outside_store.py` (blind copy) | `34354116…` | duplicate fid `b1-replace-target-outside-store` (kept lane copy, same bytes) |
| `b2_fetch_head_hardlink_out.py` (blind copy) | `6a15228b…` | duplicate fid `b2-fetch-head-hardlink-out` (kept lane copy, same bytes) |
| `c4_gitfile_store_include.py` (blind copy) | `3c99e89b…` | duplicate fid `b4b-gitfile-store-include` (kept lane copy, same bytes) |
| `s50_alternates_dotdot_abs.py` (blind copy) | `9fe77895…` | duplicate fid `s50-alternates-dotdot-abs` (kept lane copy, same bytes) |
| `s50_gitfile_symlink_chain.py` (blind copy) | `70705f02…` | duplicate fid `s50-gitfile-symlink-chain` (kept lane copy, same bytes) |
| `s6_gitfile_rel_objects_link.py` (blind copy) | `efe4ad43…` | duplicate fids `seal6-gitfile-up-outside`, `…-up-inside-link`, `…-submodule-store-link` (kept lane copy, same bytes) |
| `s6_second_store_mount.py` (blind copy) | `cfb0005d…` | duplicate fids `seal6-second-store-outside`, `seal6-second-store-twin` (divergent bytes; lane `f2425983…` kept — Finding 4) |

The single unique rejected module is `c4_gitfile_delimiter.py`, and the rejection is measured, not assumed:

```
FIXTURE b4a-gitfile-nul-two-stores
  rep0 CANONICAL-IDENTITY-ERROR ValueError: lstat: embedded null character in path
  rep1 CANONICAL-IDENTITY-ERROR ValueError: lstat: embedded null character in path
  index-file store/index
FIXTURE b4a-gitfile-newline-two-pointers
  rep0 digest=8b7beb981fe611bf masked=[]
  rep1 digest=ba4d6e1f4880168d masked=[]
  index-file store/index
```

(1) The NUL pointer cannot be resolved by the canonical identity at all — `gitfile_index_paths` builds a path
containing the NUL and `lstat` raises. (2) The newline gitfile does not match the builder's single-line
`GITFILE` regex, so the separate store's `index` is never masked and its stat cache makes the two rebuilds
differ. A NUL-skip identity variant was implemented and still left the module nondeterministic, so the gate is
not an instrument artifact. `assemble.log` records both fixtures as `det=False base=BREACH`.

### Determinism and base-refusal receipts

`determinism-receipt.txt` (per fixture: same-path digest, rebuild digest, cross-root digest):

```
NONDETERMINISTIC rows: 0
ROOT-DEPENDENT fixtures: s50-alternates-dotdot-abs,seal6-second-store-outside,x1-cd-abs,x2-alt-abs
```

All 26 accepted fixtures are rebuild-equal; the four root-dependent rows embed their absolute build path in the
fixture bytes on purpose (an unknown-prefix `alternates` line, an absolute `commondir`, an absolute
`--separate-git-dir` store, an absolute `alternates` store). Every accepted fixture is **BASE-BREACH**; the
refusal reasons are in `manifest.tsv`/`manifest.json` and, grouped:

| base reason | fixtures |
|---|---|
| `lane/.git/objects/info/alternates present (object-store redirect)` | `b1-replace-target-outside-store`, `bl5-alternates-chain-out`, `s50-alternates-dotdot-abs` |
| `lane/.git/FETCH_HEAD is not a plain-init entry` | `b2-fetch-head-hardlink-out` |
| `wt/.git is a file (gitdir redirect), not a directory` | `b4b-gitfile-store-include`, `bl5-wt-commondir-out`, `x2-alt-abs`, `x2-alt-rel` |
| `.git is a file (gitdir redirect), not a directory` | `seal6-gitfile-up-outside`; `sub/repo/.git …`, `second/.git …`, `other/.git …` analogous |
| `outside-link is a symlink` / `hop2 is a symlink` | `s50-01-stray-symlink`, `s50-gitfile-symlink-chain` |
| `shared-link has more than one hard link` | `s50-02-hardlink-outside` |
| `repo/.git/refs/weird is not refs/heads or refs/tags` | `s50-03-unknown-ref-namespace` |
| `pre-commit is not a hook sample` | `s50-04-live-hook` |
| `repo/.git/objects/info/packsets present (object-store redirect)` | `s50-05-objinfo-unknown` |
| `--lane value '../outside-lane' resolves outside the fixture` | `s50-07-argv-escape` |
| `heads/master is not a 40-hex ref` | `s50-08-ref-value-junk` |
| `repo/.git has no objects` | `s50-09-store-no-objects` |
| `refs/weird has a name git does not write` | `s50-10-reflog-name` |
| `lane/.git/commondir is not a plain-init entry` | `x1-cd-abs`, `x1-cd-rel` |
| `3a/65620f5… has more than one hard link` | `seal6-second-store-twin` |

No fid collides with `plans/sealed46/`, `plans/refusals46/` or the frozen 126-row `population.txt`; all 26
fixture tree digests are distinct (no shape duplicate).

## Integration proof — the committed counter consumes the assembled set

A second freeze clone carried only the candidate (`plans/sealed50/`, 21 files, hashes equal to the manifest),
then the counter at lane HEAD (`d8787b34…`, sha256 re-verified) ran over it:

```
$ python3 counter_head.py --lane "$S/lane-int" --work "$S/work-int" --skip-mutants --allow-dirty
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE …/lane-int/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=21 clean=21 leaked=0 build_errors=0
PREDICATE R50-C1 fail
EXIT 1
```

(`--allow-dirty` because the candidate is an untracked directory in that clone; the predicate's dirty-tree
failure is not what is being measured. The `HONEST admitted=113` and the `fail` are the frozen BASE-fence
control — correct and expected. The measurable line is `SEALED total=21 clean=21 leaked=0`: every assembled
module builds and is refused by the BASE fence through the counter's own legs, not through this seat's harness.)

Independent second instrument (the wave's existing `R50C1ExecSealedAudit/audit_sealed.py`, run in its read-only
mode over the emitted directory) agrees on the loaded gates — `audit-crosscheck.txt`:

```
nondeterministic none
root-dependent s50_alternates_dotdot_abs.py · s6_second_store_mount.py · x1_commondir_escape.py · x2_gitfile_alternates_escape.py
duplicate-fid none
contract-ok 20/21 · CONTRACT-FAIL s50_01_stray_symlink.py  absolute path literal in source: /etc/hostname
BASE … BREACH   (26/26 fixtures)
```

The one disagreement is a **policy flag, not a gate failure**: that tool also rejects any bare absolute-path
literal, and `s50_01_stray_symlink.py` links `d/outside-link -> /etc/hostname`. The fixture builds
deterministically, is root-independent and is BASE-refused, so this seat's declared gates keep it; the flag is
carried in the manifest notes so the integrator can drop it on policy grounds alone.

## Delivered artifacts

All under `.ufo/waves/round-50/w1/C1ExecSealedAssemble/`:

| path | content |
|---|---|
| `sealed50/` | the 21 accepted modules (26 fixtures); each file's sha256 re-verified against the manifest after copy (21/21 match, 0 missing) |
| `manifest.json` | fences + revision + per-fixture rows (file, sha256, fixture, tool, expected, base verdict + reason, three tree digests, determinism, root-independence, source) + drops + module notes |
| `manifest.tsv` | the same rows, one line per fixture (header: `file, sha256, fixture, tool, expected, base_verdict, deterministic, root_independent, tree_sha256, tree_sha256_rebuild, tree_sha256_crossroot`) |
| `modules.tsv` | **one row per module**: `file, sha256, fixtures, expected, base_verdicts, deterministic, root_independent, source` |
| `assemble.py`, `assemble.log` | the gate driver and its verbatim output |
| `determinism-receipt.txt`, `audit-crosscheck.txt`, `integration-sealed-leg.txt`, `delimiter-defect.txt` | measurement receipts |
| `revisions.txt` | REV/ancestry/digests/environment block |

`expected` in the manifests is the module's own `FIXTURES["expect"]` token (`reject` / `accept` / `error` /
`breach`) — a legacy field of the fixture batteries, not the assembly's expectation. The assembly's expectation
is the separate `base_verdict` column, which must read `BREACH`.

## Findings for the integrator

1. **The landed S3 set contains one module that fails the contract/determinism gate.**
   `plans/sealed50/c4_gitfile_delimiter.py` (`95429f87…`, committed in `6db0279`) cannot be identity-pinned: its
   NUL fixture makes the canonical digest raise and its newline fixture leaves the separate store's `index`
   unmasked and volatile. The landed receipt's `SEALED total=18 clean=18` is not contradicted — the counter only
   builds and refuses, it never digests sealed fixtures — but the S3 set cannot be re-built and compared
   fixture-for-fixture. This candidate excludes it. Its newline fixture is a genuinely sharp hostile case
   (git refuses the gitfile; a line-oriented reader takes a valid in-`d` store); landing it would need the
   identity instrument to mask the store index of a delimiter gitfile, or the fixture to be rewritten so the
   store is found. That is an instrument decision, not this seat's.
2. **Four blind modules that pass every gate are not in the landed set**: `h_alternates_chain`,
   `h_wt_commondir_out`, `x1_commondir_escape`, `x2_gitfile_alternates_escape` (4 modules, 8 fixtures). Highest
   novelty of the four is `h_alternates_chain`: the alternates **chain** whose direct hop is inside `d` and whose
   second hop leaves it — the exact case a repair built on "direct target resolves inside `d`" admits while still
   satisfying the honest `n22` class. The base refuses it only by the blanket alternates rule, so its BASE
   verdict carries no information about the repair; the repaired-fence run is where it earns its keep.
   `x1_commondir_escape` is the hand-forged standalone `commondir`, the shape `round-50-claims.md` records as a
   *decided exclusion* for the honest population; it is a legitimate hostile module but adds less novelty than
   `h_wt_commondir_out`, which reaches the same escape from a git-written linked worktree.
3. **Base refusal is necessary, not sufficient, for a sealed row** (consistent with `R50C1MutSealed` §5.3.4).
   Six accepted fixtures are refused by the generic "`.git` is a file" rule before their pointer is examined, and
   three by the blanket alternates rule. Their rows are real hostile cases and the BASE gate is the item's gate,
   but a reader must not treat `BASE BREACH` as evidence that the fence saw the intended construct.
4. **The lane variant of `s6_second_store_mount` dropped the blind variant's prefix trap.** The blind module
   names its outside store `f"{d.name}-evil"` (a sibling that shares `d`'s prefix, defeating `startswith`);
   the landed copy names it `s6-store-second`. Both fids are unchanged, so de-duplication keeps exactly one and
   this candidate carries the lane copy. The two names are not the same hostile case; if the prefix trap is
   wanted it needs its own fid.
5. `s50_01_stray_symlink` carries a host absolute literal (`/etc/hostname`) — the wave audit tool flags it as
   ineligible; see the policy note above.

## Limits

* Verdicts are the BASE fence's `breach()` only (decided in a separate interpreter, exit-status carried). No
  leak/strace leg (`plans/round46_c1_verify.py`'s property), no honest leg, no mutant leg, and **no repaired-fence
  measurement** — that is the S2/S3 instrument, not this item. `--skip-mutants` in the integration run is
  deliberate; the carried mutant battery is the C1 seat's object.
* Determinism uses the population builder's canonical identity; for delimiter gitfiles a NUL-skip variant was
  defined and recorded (`delimiter-defect.txt`), and it does not change the verdict.
* Cross-root portability was measured but is not a gate; four fixtures are root-dependent by construction.
* One host: Python 3.14.8, git 2.56.0, Linux 7.2.11. Fixture semantics remain "states git itself writes"; a
  hand-forged `commondir` (Finding 2) is the recorded exception class.
* Nothing here touches `plans/*`, `corpus/*`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `.ufo/state`,
  `MANIFEST.json` or any sibling repository. The lane working tree was already dirty at seat start
  (` M plans/round50_c1_verify.py`, working digest `850ec790…`, not the committed `d8787b34…`); that modification
  belongs to another seat, was neither used as an instrument nor altered here, and the integration run used the
  counter read out of the commit (`git show HEAD:plans/round50_c1_verify.py`). Scratch tree `/fast/scratch/hyaku/kengaku-r50/R50C1ExecSealedAssemble`
  was removed before this seat yielded (every receipt above was copied into this directory first).

VERDICT: the assembled candidate is **21 modules / 26 fixtures** (17 of the 18 landed modules + all 4 blind-only
modules), every fixture FIXTURES-contract-clean, rebuild-deterministic at an identical absolute path, and
BASE-refused (`SEALED total=21 clean=21 leaked=0` through the committed counter `d8787b34…` on a freeze clone);
one landed module (`c4_gitfile_delimiter.py`, `95429f87…`) is rejected on a measured determinism defect (NUL
gitfile digest raises; newline gitfile leaves the store index unmasked and volatile); de-duplication removed six
byte-identical blind copies and one divergent `s6_second_store_mount` variant (prefix trap lost — Finding 4);
no fid or shape collisions with the frozen populations.
