# R50FRDistillFindings — wave-close distill of the round-50 w1 seat reports

Seat: `R50FRDistillFindings` (reviewer, leaf) · serves **R50-C1 (novelty)** and **R50-C2 (calibration)**.
Item: read every seat report present under `.ufo/waves/round-50/w1/`, fold them into one findings table
(claim · finding · evidence pointer · severity for admission · duplicates merged), and flag findings that
contradict one another.

```
REV  lane tip at measurement   d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78  ("round-50: scored C1 receipt, measured outcomes, LOG entry, corpus index")
REV  base tip per assignment   71f5f5f77591d8c3d19297ee9785436da45209e4
REV  freeze measured           3b02d573d58cc6d2e0d27ef92ac0815354912252  (ancestor of the lane tip: verified)
REV  freeze vs base tip        `merge-base --is-ancestor 3b02d57 71f5f5f` -> NO; freeze is 2 commits PAST the base tip
REV  fence at tip              57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1  (991 lines)
REV  counter at tip            d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  (committed bytes)
REV  counter, worktree only    850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999  (`M plans/round50_c1_verify.py`, uncommitted, not measured by any receipt)
REV  C2 audit at tip           b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef
REV  population pin            b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  (126 rows)
REV  battery at tip            e885f0a6e69e33af55519279c5efab5f8dd8950df95b1e08a41e39e3043f5ccb  (15 rows)
REV  sealed sets               12 (`plans/sealed46`) + 18 (`plans/sealed50`); refusals 20
REV  report snapshot           47 `*.md` seat reports read; wave still writing at snapshot time
ENV  git 2.56.0 · Python 3.14 · linux 7.2.11-arch1-1
```

Axes named: **novelty** (C1 — is the instrument that certifies the repair able to certify it?) and
**calibration** (C2 — does `unresolved=0` mean every pointer re-runs?). No admission of either claim is
claimed here; nothing in `plans/`, `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`,
`MANIFEST.json` or `.ufo/state` was written.

## 0. Coverage — 47 reports, all read

`R50C1ConnOverlap`, `R50C1CritAdmitAll`, `R50C1CritBlind1..6`, `R50C1CritDoNothing`, `R50C1CritIdent`,
`R50C1CritPopScope`, `R50C1CritPredicate`, `R50C1ExecAlternates`, `R50C1ExecCleanRun`,
`R50C1ExecCounterSelftest`, `R50C1ExecFetchHead`, `R50C1ExecGitfile`, `R50C1ExecMutAttrib`,
`R50C1ExecMutRebase`, `R50C1ExecPopRepro`, `R50C1ExecRefs`, `R50C1ExecRepair`, `R50C1ExecRepairB`,
`R50C1ExecSealedAudit`, `R50C1LabratProbe`, `R50C1MutBypass`, `R50C1MutSealed`, `R50C1RevClaim`,
`R50C1RevRerun`, `R50C1RevengerIntent`, `R50C1ScoutPrior`, `R50C1ScribeEntry`, `R50C1ScribeLimit`,
`R50C1SimplBudget`, `R50C2CritHash`, `R50C2CritNonVacuity`, `R50C2CritScope`, `R50C2ExecAudit`,
`R50C2ExecCorrections`, `R50C2ExecVerifyTargets`, `R50C2RevNoHarm`, `R50C2RevRerun`,
`R50C2ScribeCorrections`, `R50FRExecCensus`, `R50FRScoutAlternates`, `R50FRScoutGitDocs`,
`R50FRScribeMistake`, plus the receipt files `R50C1CritDoNothing-*.txt`, `R50C1ExecMutAttrib-*`,
`R50C1ExecMutRebase-*`, `R50C1ExecMutAttrib-attrib.py`. Reports that land after this snapshot are not in
the table; `ls -1t` at yield time showed the wave still appending.

## 1. What I measured at the scored revision (not re-derived from seats)

All runs in a `git clone --shared` of the lane, checked out at `d45c5bb`, `TREE dirty=0`, `TMPDIR` in
`/fast/scratch/hyaku/kengaku-r50/R50FRDistillFindings`, `--work` always passed. The live checkout was never
the target of a run.

### 1.1 The claim's own command, full predicate

```
$ git -C lane rev-parse HEAD                     -> d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
$ python3 plans/round50_c1_verify.py --lane .
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE <clone>/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
C1_EXIT=0
```

The committed `corpus/evidence/round50/c1-receipt.txt` (at `d45c5bb`) prints the same block at `REV d6f2fce`,
exit 0. The repair half is **real**: `HONEST 126/126` is reproduced independently by this seat,
`R50C1CritPopScope` §7, `R50C1CritBlind5`, `R50C1ExecRepairB` (candidate B) and `R50C1LabratProbe`.

### 1.2 `--skip-mutants` still prints a pass

```
$ python3 plans/round50_c1_verify.py --lane . --skip-mutants --work "$S/w7"
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
PREDICATE R50-C1 pass
EXIT=0
```

No `MUTANTS` line; exit 0. The frozen after-block requires five lines including `MUTANTS`.

### 1.3 A fence that reads no git byte reaches the frozen predicate (decisive)

Scratch fence (`$S/cand/pathkey2.py`, sha256 `89fdf553…`), transcribed because the scratch tree is removed:

```python
import sys

def breach(d, argv, tool):
    s = str(d)
    if "/honest/" in s:
        return None
    return "not the honest leg (harness layout)"

_PAYLOAD = "<scratch>/cand/forge_mod.py"      # a module whose breach() returns a string for everything
try:
    sys.modules["__main__"].apply_mutant = lambda fp, payload, dest: (_PAYLOAD, None)
except Exception:
    pass
```

```
$ python3 plans/round50_c1_verify.py --lane . --work "$S/w6" --fence <pathkey2.py>
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE <pathkey2.py> sha256=89fdf5538f4bfee7c5d75e6bd2317e4dcf8af7bf4669a46daa1a1b50ca4c9139
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
EXIT=0
```

This is `R50C1CritPredicate`'s Receipt D, reproduced on the **scored** revision and the **scored** counter
digest. The fence inspects zero bytes of any fixture; it keys on the counter's own build layout
(`work/honest/…`, `round50_c1_verify.py:240` in the worktree file, `:196`/`:228` in the committed one) and it
rebinds `__main__.apply_mutant` at import time because the counter imports the fence into its own process
(`load(fence_path, "k50_fence")`).

### 1.4 The in-flight counter fixes the forge but not the path key

The worktree counter `850ec790…` (uncommitted) scores each fixture in a separate process and carries the
verdict in the exit status. Copied into the clone and run against the same path-keying fence (no forge):

```
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=0 broken=15 floor=12 verdict=unmet
PREDICATE R50-C1 fail
EXIT=1
```

So: the in-process forgery is closed; the **path key is still open** (honest/refusals/sealed all green for a
fence that reads nothing); the only thing that failed it was the mutant leg's inability to apply the 15
payloads to a foreign fence (`broken=15`), which the gate does not score. A keying fence that leaves the
battery's contexts applicable would pass.

### 1.5 C2 at the scored revision

```
$ python3 plans/round50_c2_audit.py --lane .          # cwd = clone at d45c5bb
TIP d6f2fce9889f429162c12f851bae41891bedf5cd branch=master
POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0
C2_EXIT=0
```

The `TIP` line names `d6f2fce`, one commit **behind** the tree the audit read (`d45c5bb`), because `audit()`
takes the tip from `rev-parse master` (`plans/round50_c2_audit.py:74-77`).

### 1.6 C2's green is reachable with zero real fixes (decisive)

On a copy of the clone checked out at the **frozen** tree `3b02d57` (before the corrections block existed),
I appended 12 `SUPERSEDED` rows whose targets are unrelated files or bare directories
(`plans/round45_c1_verify.py`, `plans/round46_c1_verify.py`, `SCORECARD.md`, `.`, `plans`, `.ufo`,
`corpus/knowledge`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, the two real `.jsonl` ledgers):

```
$ python3 plans/round50_c2_audit.py --lane .     # frozen tree + bogus rows
POINTERS total=275 paths=216 hashes=59 resolved=275 exists=204 superseded=12 never-landed=0 unresolved=0
EXIT=0
```

`audit()`'s only target test is `(lane / target).exists()`. This reproduces `R50C2CritNonVacuity`'s variant B on
the scored instrument digest `b911d03a…`.

## 2. Findings table

Severity is **for admission of the named claim**: `BLOCKING` = the claim as written cannot be admitted on this
evidence; `HIGH` = the evidence is materially weaker than the claim states; `MEDIUM` = audit-trail or
interpretation defect; `LOW` = bookkeeping; `INFO` = supporting evidence, no defect.

| id | claim | finding | evidence pointer | sev | duplicates merged |
|---|---|---|---|---|---|
| F1 | C1 | **The committed counter scores a fence that reads no git byte.** In-process import + fixture-path layout key + `__main__.apply_mutant` rebinding prints the full claimed block, `PREDICATE pass`, exit 0 at the scored revision. The counter cannot distinguish boundary reasoning from harness-path keying. | §1.3 above; `R50C1CritPredicate.md` F1/F2 + Receipts A/C/D; `R50C1RevClaim.md` F1; `R50C1MutBypass.md` D1/D2/D3 | **BLOCKING** | CritPredicate F1, CritPredicate F2, RevClaim F1, MutBypass D1-D3, SimplBudget §3, CritDoNothing "smallest safe correction" 1-3, ExecCounterSelftest (d)(e) |
| F2 | C2 | **`unresolved=0` means "some path exists".** 12 rows to unrelated files/directories green the audit on the frozen tree; a `never-landed` lie is accepted behind a duplicate row; a 0-byte sibling can resolve a dangling `.jsonl` pointer. | §1.6 above; `R50C2CritNonVacuity.md` variants A/B/C; `R50C2RevRerun.md` F1(b) | **BLOCKING** | NonVacuity D1 + variants, CritScope F1, RevRerun F1, ExecAudit §4, ExecVerifyTargets 1 |
| F3 | C1 | **The SEALED leg is not held out.** Blind module names appear in wave reports before the sealed set froze (`name-leaks` 6 rows), the fence repair seat ran two of them through its own candidate (`receipt-blind50-crosscheck.txt`), and the sealed set sat in the worktree from 14:36 while the fence was finalised. `c4_gitfile_delimiter` is `contract-ok NO` + `nondeterministic`; 4 of 12 modules are root-dependent. | `R50C1ExecSealedAudit.md` (name-leaks, contract, root-dependent); `R50C1ExecRepair.md` "Blind hostile modules … external check"; `R50C1CritBlind5.md` (runs the landed fence) | **HIGH** | ExecSealedAudit, ExecRepair crosscheck, Blind1 F1/F3, Blind5 gap note |
| F4 | C1 | **Receipt shape ≠ frozen after-block.** Two `SEALED` lines are printed (12, then 18); the frozen single line `SEALED total=<S> clean=<S> leaked=0 build_errors=0` is never printed; `<S> ≥ 18` is not an enforced invariant (`SEALED50_MIN=6` and only when the dir exists); `sealed46` has no total check at all. | §1.1 above; `R50C1RevRerun.md` F3/F4; `R50C1SimplBudget.md` 3.2/3.3; `R50C1CritDoNothing.md` | **HIGH** | RevRerun F3/F4, RevClaim F2, CritPredicate F4, SimplBudget 3.2/3.3, MutBypass D6, ScribeLimit 7, ExecCounterSelftest D1 |
| F5 | C1 | **Pass mode accepts the testing flags.** `--skip-mutants` prints `PREDICATE pass`, exit 0 with no mutant leg (measured); `--allow-dirty` and `--fence` are equally unscored. A scored receipt can therefore omit a leg or name a foreign fence. | §1.2 above; `R50C1CritPredicate.md` F3; `R50C1RevClaim.md` F3 | **HIGH** | CritPredicate F3, RevClaim F3, MutBypass M1/M1b, CritDoNothing, ScribeLimit 11 |
| F6 | C1 | **The mutant gate ignores `broken`** (`caught < MIN or len < MIN` only), and `patch` without `--forward` credits a *reversed* payload as a kill; `ERROR`-vs-reference also counts as caught. Q38 witnessing lives in the battery's provenance, not the arithmetic. | `R50C1SimplBudget.md` 3.1/3.4; `R50C1ExecMutAttrib.md` D1/D2 (`patch` "Assuming -R", `st` NameError, 164 ADMIT→ERROR) | **HIGH** | SimplBudget 3.1/3.4, ExecMutAttrib D1/D2, ExecCounterSelftest (e), CritPredicate F4 |
| F7 | C2 | **Three of the twelve correction rows manufacture provenance.** `.jsonl`→`.json` and `.sha256.repo`→`.sh` are tokenizer truncations; the rows "correct" pointers no author wrote. One row targets the wrong artifact (`predictions-r9.sh -> predictions-r9.md` while its own reason names and the citing lines verify `predictions-r9.sha256.repo`); `analyze.py -> never-landed` contradicts the SCORECARD line that names `round9-fleet/analyze.py`. | `SCORECARD.md:2145-2156` at tip; `R50C2CritScope.md` F1/F2; `R50C2ExecAudit.md` §5; `R50C2ExecVerifyTargets.md` rows 1/2/3; `R50C2RevNoHarm.md` §2 | **HIGH** | CritScope F1/F2, ExecAudit §5, VerifyTargets 1-3, RevNoHarm §2, RevRerun F1 |
| F8 | C1 | **The honest denominator is a sample and the claim reads as coverage.** The landed fence still refuses 10 documented git-written classes / 22 entries (multi-pack-index, mid-merge state, split commit-graph, sparse-checkout, submodules, split-index, sha256, reftable, core.worktree, rerere); `## Named limits` in the claims file has **no** coverage-bound sentence (checked at `d45c5bb`). | `R50C1CritPopScope.md` §5 + landed VERDICT; `plans/round-50-claims.md` §C1 Named limits | **HIGH** | CritPopScope §4/§5/§7, ScribeEntry limit defects, ScoutPrior "instrument-not-found (not a proof of absence)" |
| F9 | C2 | **The surface is narrower than the sentence "every artifact pointer".** `.ufo/` pointers (70 with 7 broken — the same defect class), brace groups (5 members missing), globs, bare directories, `considerthese/`, `scripts/`, `merge/`, and non-`EXTS` extensions are outside the audit. | `R50C2CritScope.md` F3 table | **HIGH** | CritScope F3, RevRerun F1(c), ScribeCorrections limit |
| F10 | C1 | **No digest binds the fence, the builder or the battery.** `FENCE sha256=` is printed and compared to nothing; the landed battery has `"candidate_fence_sha256": null`; the claims file still says the fence under test is "still the base fence" `05d5fe03…` and its open-window table has one row (the counter only); `population.txt` line 2 cites `builder_sha256=b2560ebc…`, a blob absent from the object database. | §3 measurements; `plans/mutants50/c1-mutants.json` at tip; `plans/round-50-claims.md:9,149-157`; `plans/honest50/population.txt:2`; `R50C1RevClaim.md` F4; `R50C1ExecPopRepro.md` A2/A5 | **HIGH** | RevClaim F4, ExecPopRepro, ScribeEntry 3, MutBypass D3, SimplBudget R8 |
| F11 | C2 | **The receipt names the wrong revision.** At `d45c5bb` the audit prints `TIP d6f2fce … branch=master` and checks hash ancestry against the local branch, not the measured tree. Latent today (all hashes are ancestors of both), fatal the moment a hash is tip-only. | §1.5 above; `R50C2RevRerun.md` F5; `R50C2CritScope.md` §1; `R50C2CritHash.md` F4 | **MEDIUM** | RevRerun F5, CritScope §1, CritHash F3/F4 |
| F12 | C1 | **Identity pins are blind in five shapes** (masked `.git/index` bytes/size/mode/presence/type = 125/126 fixtures, `__pycache__` subtrees, inode/hardlink, mtime, xattr). No adjudicated verdict flips today; the "visible rather than silent" sentence is falsified for git's stat cache. | `R50C1CritIdent.md` probe matrix + VERDICT | **MEDIUM** | CritIdent, ScribeLimit 10 |
| F13 | C1 | **The SEALED leg cannot witness the property its modules name.** A module refused for a blanket reason counts `clean`; `SEALED50_MIN` counts files, not mechanisms; single-site symlink deletions are invisible on both fences. | `R50C1CritBlind1.md` F1/F3; `R50C1CritBlind2.md` F1; `R50C1CritBlind3.md` counterexample; `R50C1MutSealed.md` §5 | **MEDIUM** | Blind1 F1/F3, Blind2 F1, Blind3, Blind5 gap, MutSealed §5, CritAdmitAll F2/F3 |
| F14 | C1 | **Battery lineage is not the one the seats witnessed.** `R50C1ExecMutRebase` delivered a 19-row battery (sha `53873ed0…`, pinned to `9baedf13…`) with 19/19 witnessed kills; the landed battery is a different 15-row file with null fence pin; two of the 19 rows are whole-population (n=116) and carry no discrimination. | `R50C1ExecMutRebase.md` Result 3; `R50C1ExecMutAttrib.md` §3; `plans/mutants50/c1-mutants.json` at tip | **MEDIUM** | MutRebase, MutAttrib §3, CritPopScope 5 |
| F15 | C2 | **The lane's own record contradicts itself numerically.** `SCORECARD.md:2134` says `total=271` at `71f5f5f`; `:2179` says `total=275` at `71f5f5f`; measured at `71f5f5f` is 271, and 275 is the `f7281bc` receipt. The claims prose says "six pointers … and four corpus paths" for a measured 7 + 5. | `SCORECARD.md:2134,2179`; `R50C2ExecAudit.md` §6; `R50C2CritScope.md` F0; `R50C2RevNoHarm.md` VERDICT | **MEDIUM** | ExecAudit §6, CritScope F0, RevNoHarm, RevRerun F2 |
| F16 | C1 | **The population pin cannot be regenerated and is mis-attributed**: header names a builder blob that exists nowhere and a lane revision at which the builder does not exist. Content is fully reproduced (126/126 identities, three runs byte-identical), so this is provenance, not identity. | `R50C1ExecPopRepro.md` A2/A5 + defect report | **MEDIUM** | ExecPopRepro, ScribeEntry |
| F17 | C1 | **Docs drift around the claim**: `plans/honest50/README.md` is the round-49 124-fixture doc; SOURCES anchors S173/S174/S175/S177 need repair; the landed knowledge entry asserted a `126/126` recheck at a revision where the counter printed `113/13` (it became true one commit later). | `R50C1ScribeEntry.md` §3; `R50FRScoutGitDocs.md` VERDICT; `R50FRScoutAlternates.md` VERDICT | **MEDIUM** | ScribeEntry 1 + "Additional findings", ScoutGitDocs, ScoutAlternates |
| F18 | C1 | **Receipt enumeration and census.** `refused[:12]` hides the 13th refusal (`n08-tag-detached`); the dispatch/claims prose "five honest classes" understates the measured 13 classes. | `R50C1MutBypass.md` D7; `R50C1CritDoNothing.md` coordination note; `R50C1ExecRefs.md` F1; `R50C1ExecCleanRun.md` finding 3 | **LOW** | MutBypass D7, CritDoNothing, ExecRefs F1, ExecCleanRun 3, PopScope |
| F19 | C1 | **A missing `--work` directory is a traceback with exit 1**, indistinguishable from `fail` (I hit it twice: `FileNotFoundError … k50-c1-*.`), although exit 2 is reserved for setup errors. | `R50C1RevRerun.md` F5; §1.3 first attempt | **LOW** | RevRerun F5, CleanRun 2, PopScope 5 |
| F20 | C1 | **Guard hardening**: `REV unknown` / `TREE dirty=0` on a non-repo lane; broken-mutant reason truncation makes receipts non-byte-comparable. | `R50C1MutBypass.md` D4/D8; `R50C1CritDoNothing.md` false-clean section | **LOW** | MutBypass D4/D8, CritDoNothing |
| F21 | C2 | **Selftest coverage**: the hash leg is never exercised for failure; the last `SUPERSEDED` row silently wins; a green selftest coexisted with a red surface at the freeze (`pristine_rc=1`) — resolved at the tip (`pristine_rc=0`). | `R50C2RevRerun.md` F3/F4/F6; `R50C2ScribeCorrections.md` finding 3 | **LOW** | RevRerun F3/F4/F6, ScribeCorrections 3, NonVacuity duplicate-row variant |
| F22 | both | **Supporting measurements, no defect**: git reads an out-of-`d` store unconditionally with `GIT_CEILING_DIRECTORIES` set (so the containment leg is necessary); the five refused classes were shape heuristics, not named security boundaries; no sibling lane owns "git fixture geometry" or prints an admitted/refused honest denominator; the phenomenon is documented in git 2.56.0, the instrument is not in the opened sources; census `sources-census.sh validate` → 15 `W04` warnings, `ok`, exit 0; the four committed controls all fail on their own leg and HONEST's separating power is exactly `n20`/`n21`/`n22`. | `R50C1LabratProbe.md` §4; `R50C1RevengerIntent.md` §1/§2; `R50C1ConnOverlap.md` F1-F5; `R50C1ScoutPrior.md`; `R50FRExecCensus.md` §2; `R50C1CritAdmitAll.md` F2/F3; `R50C1CritDoNothing.md` control table | **INFO** | LabratProbe, RevengerIntent, ConnOverlap, ScoutPrior, ExecCensus, CritAdmitAll, CritDoNothing |

## 3. Measured state of the two claims at `d45c5bb`

**C1.** The literal predicate passes and the S3 receipt is byte-faithful to an independent rerun. The fence
repair is real (`HONEST 126/126`, `REFUSALS 20/20`, `SEALED 12/12 + 18/18`, `MUTANTS 15/15`, no git child —
`grep -nE "subprocess|Popen|os.system|execv|fork"` over `57adce4a…` → none). What fails is the
**certification**: the instrument that produced the receipt is defeated by a fence that reads nothing (§1.3),
the frozen after-block's single `SEALED` line is never printed (§1.1), and the sealed set stopped being
held out (§F3). `SCORECARD.md:2176` states the counter "decides … in separate processes with Q39 name hiding"
— that is true only of the **uncommitted** `850ec790…` file, and even that file leaves the path key open
(§1.4). The frozen claims file still describes the fence as "still the base fence" `05d5fe03…` and records no
fence digest row (`grep -c '^| 2026' plans/round-50-claims.md` → 1, the counter).

**C2.** The literal predicate passes (`unresolved=0`, exit 0) and the block is append-only (12 insertions, 0
deletions; `R50C2RevNoHarm` confirms byte-for-byte). What fails is the **meaning**: 12 rows to unrelated
existing paths green the audit (§1.6), 3 of the 12 landed rows correct tokenizer phantoms, one row targets a
different artifact than its own reason names, the receipt's `TIP` names a revision one commit behind the tree
it read (§1.5), and the surface excludes the `.ufo/` pointers where the same defect class is live.

## 4. Contradictions between reports (each flagged, none silently resolved)

1. **`SCORECARD.md:2176` vs the committed counter.** The record says the counter runs the fence "in separate
   processes with Q39 name hiding"; the committed bytes (`d8787b34…`) import it in-process and build fixtures
   under `work/honest/`. Measured, not inferred (§1.3). The out-of-process version exists only as
   `M plans/round50_c1_verify.py` (`850ec790…`) and is cited by no receipt.
2. **`SCORECARD.md:2134` vs `:2179`** — `total=271` and `total=275` both attributed to `71f5f5f`; measured is
   271 (the 275 belongs to `f7281bc`).
3. **`R50C1CritBlind4` self-report ("deterministic", modules delivered) vs `R50C1ExecSealedAudit`**
   (`contract-ok … NO`, `nondeterministic c4_gitfile_delimiter.py`, build raises on the NUL fixture). Same
   file, opposite verdicts; the audit's negative controls make its measurement the stronger one.
4. **Wave brief "4 of 23 change the verdict vector" vs three independent measurements of 3**
   (`MutBypass caught=3 broken=12`, `SimplBudget caught=3 broken=12`, `CritPredicate caught=3 broken=12`) on
   the base fence, and `ExecMutRebase`'s 1 caught on the *candidate* fence (different object, reconciles).
   The brief's number has no measurement behind it.
5. **`R50C1ExecRefs`/`ExecCleanRun`/`CritDoNothing`/`MutBypass` "13 classes" vs the dispatch's "five honest
   classes".** The claims file's own `Before` line (`refused=13`) is right; only the class list in the
   dispatch is wrong (`R50C1ExecRefs` F1 states this).
6. **`R50C1RevClaim` "REJECT the repair half" vs `CritPopScope` §7 / `ExecRepair` / `ExecRepairB` "the repair
   is real and passes".** Both are true of different objects — the fence is repaired; the counter that certifies
   it is bypassable. The admission record must state which object each sentence is about.
7. **`R50C1ScribeEntry` defect 1 (the landed knowledge entry asserted `126/126` before any run printed it) vs
   the S3 receipt now printing `126/126`.** The assertion became true one commit later; the provenance order
   violation at `822f3b7` remains.
8. **`R50C1CritPopScope` self-update**: its base-fence VERDICT (11 classes / 23 entries) and its landed VERDICT
   (10 classes / 22 entries at `57adce4a`) differ; use the landed §7 numbers.
9. **"SEALED 30/30" (CritPopScope §7) vs the counter's two lines `12` + `18`.** Both true; the frozen claim's
   one-line form with `<S> ≥ 18` is the one the receipt never prints.
10. **`R50FRExecCensus` "the freeze is not an ancestor of `71f5f5f`" vs the item's "base tip `71f5f5f`, freeze
    `3b02d57`".** Not a contradiction: the freeze is a descendant of the base tip and an ancestor of the lane
    tip (verified here; rc=0 against both tips in the correct direction).

## 5. Limits of this distill

- Report snapshot is 47 files; the wave was still appending (`ls -1t` showed new reports between my first and
  last listing: `ExecSealedAudit`, `LabratProbe`, `RevengerIntent`, `C2CritNonVacuity`, `C2CritScope`,
  `ExecCensus`, `ScoutAlternates`, `ScoutGitDocs`, `C2CritHash`, `C2RevNoHarm`, `ScribeMistake`). Findings
  from a report landed after the snapshot are not folded in.
- I re-read findings sections, verdicts and the evidence blocks they cite; I did not re-execute every seat's
  experiment. Findings marked with a path citation are the seat's measurement; findings in §1 are mine, run at
  `d45c5bb` on a `--shared` clone.
- One counter (`850ec790…`) was copied from the live worktree into my clone for a single read-only run
  (§1.4); the live checkout was never the target of a run and never written. The copy lives only in scratch.
- The forgery in §1.3 is a second, independent reproduction of `R50C1CritPredicate` Receipt D; it did not
  discover a new channel. Its value is that it binds the channel to the **scored** revision and digest.
- No LSP server was engaged: the evidence is Markdown/Python/git, and `lsp` would add no semantic proof about
  a regex over prose or about a subprocess exit code. Recorded as the reviewer contract asks.
- Host: git 2.56.0, one filesystem (`/fast`), Python 3.14. The population is host-sensitive by design and
  `mismatched=0` is the only statement this seat makes about identity.
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50FRDistillFindings` was removed before yield (single `--shared`
  clone, two `--reflink=auto` copies for the C2 probes, work dirs, candidate fences), **except** the two
  scratch candidate fences and the C2 probe rows, which are transcribed verbatim above so nothing citable
  lived only there. Tool installs: none (nothing needed; pacman untouched).

## 6. Residual risk / verification gaps

1. If the L1 lands the worktree counter `850ec790…` and re-scores, the in-process forgery closes but the
   **path key does not** (§1.4). Neutral fixture paths (`work/fx/<hash>/…`) are required before any receipt can
   claim "the fence reads git state".
2. The sealed set's evidentiary value is spent: its modules were read by the fence author and named in wave
   reports. A held-out set for the repaired fence would have to be authored after `57adce4a` and never run
   through a competing candidate.
3. C2's `.ufo/` blindness means the correction block fixes the surface it can see while 7 broken `.ufo/`
   pointers of the same class remain. Whether that is in scope is an L1/claim-text decision; the sentence
   "every artifact pointer the self-assessment files carry" is not satisfied by the current surface.
4. `plans/round-50-claims.md` no longer describes the object it froze (fence digest, battery, sealed set).
   Any re-score must either append the missing open-window rows or state that the claims file is superseded by
   the SCORECARD outcomes block.
5. The population header cannot be regenerated (`builder_sha256=b2560ebc…` is not an object). Any future
   mechanical "does the pin reproduce?" gate will red on a correct population.

## VERDICT

**Both claims' literal predicates pass at `REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`, and neither is
supported by the instrument that passed it.** C1: the fence repair is real and independently reproduced
(`HONEST 126/126`, `REFUSALS 20/20`, `SEALED 12/12 + 18/18`, `MUTANTS 15/15`, `PREDICATE pass`, exit 0, no git
child in `57adce4a…`), but the committed counter (`d8787b34…`) scores a fence that inspects no fixture — a
path-keyed fence that rebinds `__main__.apply_mutant` prints the identical block at the scored revision (§1.3);
`--skip-mutants` passes; the frozen single-line `SEALED total=<S>` is never printed; `broken` is not gated; no
digest binds the fence or the battery; and the sealed set is no longer held out. The `SCORECARD.md:2176`
sentence describing out-of-process, name-hiding execution describes an **uncommitted** file. C2: the pointer
audit is green (`unresolved=0`, exit 0), but its only target test is "some path exists" — 12 rows to unrelated
files/directories green it on the frozen tree (§1.6) — 3 of the 12 landed rows correct tokenizer phantoms, one
targets the wrong artifact, and the receipt's `TIP` names a revision one commit behind the tree it read.
**Recommendation to the L1 (not an admission): do not record novelty 7→8 / calibration 8→9 on these
receipts as they stand.** Repair both counters inside the open window under the claims' own listed reasons
(out-of-process scoring *plus* neutral fixture paths *plus* scored-mode rejection of `--skip-mutants`/
`--allow-dirty`/`--fence` *plus* `broken == 0` and one aggregated `SEALED` line for C1; target-identity and a
tokenizer right-boundary for C2), regenerate a genuinely held-out sealed set against the landed fence, append
the fence/battery digest rows and the coverage bound to the claims file, then re-score on a clean clone. If
the window is closed, record both claims as honest stops with these findings attached — the fence work and the
population are real assets regardless of how the increment is recorded.
