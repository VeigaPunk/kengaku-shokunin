# R50C1ExecRepairB — second independent repair candidate for the fixture fence (R50-C1, novelty)

Seat: executor, leaf, one labrat (self). Lane measured: `kengaku-shokunin`.
Report written read-only against the lane; the only lane writes are this file and `C1ExecRepairB/` under
`.ufo/waves/round-50/w1/`.

REV 3b02d573d58cc6d2e0d27ef92ac0815354912252 (freeze commit; verified an ancestor of the lane tip
`5c56819f7964f4af19c960de08a49cd8f95781ce` with `git merge-base --is-ancestor` printing `ANCESTOR_OK`).
Every measurement below ran on `git clone --shared` of the lane checked out at that revision, tree clean
(`TREE dirty=0` in every counter run).

## Axes named

- **novelty (R50-C1)** — a repair that reaches `HONEST admitted=126` by a *different mechanism* than the base
  fence's single-pass allowlist, so the lane's repair question has more than one witness.
- **safety/size (advisory to the L1)** — which of the two repair candidates is smaller and safer to land, with
  the criterion stated so the L1 can apply it to Repair A's report (which this seat did not read).

## What candidate B is

`fence_candidate_b.py` (sha256 `4e68592ca640a4f384b767db179ad79b8c5e9863086311ac87968810412ef393`,
1059 lines) is the base fence plus a **two-phase resolve-then-classify** decision:

1. **Resolve.** `_tree` now accepts a `.git` *file* only as a single `gitdir: <path>` line, and `_discover`
   follows every pointer git writes — gitfile, `commondir`, `gitdir`, `objects/info/alternates` — to a path
   that must (a) be lexically inside `d` after `normpath`, (b) have every component below `d` exist as a
   non-symlink (`_chain_ok`), so the lexical path *is* the real path. A pointer that leaves `d` is refused
   **where it is read**, and the resolved store graph is closed before any store is classified.
2. **Classify.** Each resolved directory is classified by kind: `store` (`git init` + commits, plus
   `FETCH_HEAD`, `shallow`, `worktrees/`), `wtmeta` (one linked-worktree metadata dir: `HEAD`, `ORIG_HEAD`,
   `index`, `commondir`, `gitdir`, `logs`, `refs`), or `objects` (`info/{alternates,commit-graph,packs}`,
   `pack/`, loose). Ref namespaces, reflog namespaces, `info/refs` and `config` are classified against
   allowlists that name only what git writes for the honest classes in the pinned population.

`realpath` is deliberately **not** used: resolving a symlink can name a path outside `d` before the refusal, so
component-wise `lstat` (`_chain_ok`) does the same job without ever naming an outside path. No `subprocess`,
`socket` or `os.system` import exists in the candidate (grep: no match), i.e. the fence still starts no git
child at all.

Diff against the base: `22` hunks, `+550` / `-66` lines, 575 → 1059 lines (`candidate_b.diff`, bundled).

## Commands run (exact)

    S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecRepairB
    git clone --shared --no-hardlinks -q <lane> $S/lane && git -C $S/lane checkout -q 3b02d573…
    sha256sum plans/fixture_fence.py plans/round50_c1_verify.py plans/honest50/population.txt
    # base, four legs
    cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work-base --skip-mutants
    # candidate B, four legs
    cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work-base \
        --skip-mutants --fence $S/candidate_b.py
    # candidate B, carried mutant battery (to record applicability, not as evidence of Q38 kills)
    cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work-base \
        --fence $S/candidate_b.py
    # supplementary outside-`d` counter (not part of the R50-C1 predicate)
    cd $S/lane && TMPDIR=$S python3 plans/round46_c1_verify.py --lane . --work $S/work46 \
        --fence $S/candidate_b.py
    # mechanism probe: refuse hostile pointers, admit honest pointer classes
    cd $S && TMPDIR=$S python3 probe.py $S/lane $S/probe-out $S/candidate_b.py

Pins confirmed before any measurement:

    05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
    f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  plans/round50_c1_verify.py
    b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt

## Observed outputs (verbatim)

Base fence, four legs (`receipts/fourleg-base.txt`, exit 1):

    REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
    TREE dirty=0
    FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
    POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=113 refused=13 error=0
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 build_errors=0
    PREDICATE R50-C1 fail

Candidate B, four legs (`receipts/fourleg-candidate-b.txt`, exit 0):

    REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
    TREE dirty=0
    FENCE …/candidate_b.py sha256=4e68592ca640a4f384b767db179ad79b8c5e9863086311ac87968810412ef393
    POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=126 refused=0 error=0
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 build_errors=0
    PREDICATE R50-C1 pass

The `PREDICATE … pass` line above is the counter's four-leg verdict with `--skip-mutants` on the stage-1 tree,
where `plans/sealed50/` does not yet exist. It is **not** C1 admission: the claim needs `SEALED total ≥ 18`,
`MUTANTS total ≥ 12` with `caught ≥ 12`, and a clean-clone scored run. This seat claims no admission.

Supplementary outside-`d` counter, base instrument `plans/round46_c1_verify.py`,
`receipts/round46-supplement.txt`, exit 0:

    HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
    REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
    CALIBRATION advertised=32 contradicted=0
    PREDICATE C1 pass

i.e. candidate B keeps the round-46 ✓property: zero reads/touches outside `d` while deciding, and it admits
all 104 battery honest fixtures that instrument knows.

Mechanism probe (`receipts/mechanism-reasons.txt`) — hostile pointers are refused *by resolution*, honest
pointer classes are admitted:

    f1-gitdir-outside BREACH pointer '…/probe-out/m000/side/gitdir' leaves the fixture
    f5-alternates-outside BREACH ../../../probe-out/m001/f000/lane/.git/objects/info/alternates row: pointer '…/probe-out/m001/store/.git/objects' leaves the fixture
    f7-cd-accept BREACH lane/.git carries worktree metadata at a store root
    f7-cd-reject BREACH lane/.git carries worktree metadata at a store root
    f7-cd-anchor BREACH lane/.git carries worktree metadata at a store root
    g3-wtmeta-out BREACH repo/.git/worktrees/g3-wt/gitdir: pointer '…/probe-out/m003/g3-wt/.git' leaves the fixture
    g4-cd-hidden BREACH repo/.git/modules is not a plain-init entry
    n20-linked-worktree ADMIT
    n21-separate-gitdir ADMIT
    n22-alternates-in-d ADMIT

Carried r49 mutant battery against candidate B (`receipts/mutants-carried.txt`, exit 1):

    MUTANTS total=23 caught=1 broken=15 floor=12 verdict=unmet   (7 rows applied and survived)

15 of 23 rows do not apply at all (`patch-rc=1`, "hunk FAILED") because they are inline diffs against a
different source; the 7 that apply target lines this candidate rewrote. Conclusion for the L1, not a defect of
this candidate: `plans/mutants50/` **must be re-derived against whichever repair is landed** — a row whose kill
direction was witnessed on one candidate is not witnessed on another (QUALITY Q38, and the claims' open window
already allows exactly this repair).

## Which repair is smaller and safer — candidate B's own measurement

Candidate B's size: `+550/-66` over 575 base lines, 22 hunks, 1059 lines, 14 new helpers (`_isreg`,
`_chain_ok`, `_resolve`, `_pointer`, `_gitfile_target`, `_config_url`, `_hex_lines`, `_alternates`,
`_log_dir_ok`, `_info_refs`, `_worktrees`, `_wtrefs`, `_wtmeta`, `_discover`), 4 rewritten (`_config`,
`_ref_tree`, `_objects`, `_store`) and 4 edited in place (`_tree`, `_refs`, `_logs`, `breach`).

Criterion the L1 should apply to Repair A (I did not read its report, so I state the test rather than a
comparison I cannot witness):

1. **Does the repair *resolve* a pointer or *classify around* it?** Candidate B resolves every pointer to a
   path inside `d` and refuses escapes at the pointer. Consequence: an honest class whose pointer target is
   unusual (absolute gitfile rewritten relative, nested `commondir`, alternates chain) is admitted **iff** its
   target is inside `d`, without the fence needing a rule per class. Cost: `_resolve`/`_chain_ok`/`_discover`
   (~120 lines) and the risk that a pointer shape git writes is not followed (mitigated: every pointer the
   four legs exercise is followed, and `alternates` chains are closed over a visited set).
2. **Does the smaller diff keep the round-46 `read=0` property?** Candidate B does (`receipts/round46-supplement.txt`),
   because it never follows a symlink and never starts a child. A repair that keeps `os.path.realpath` would
   pass the four legs but name paths outside `d` during resolution; that is the single most likely way a
   *smaller* diff is also *less safe*, and it is measurable with the same round-46 command.
3. **Config surface.** Candidate B widens `[core]` with `version 0|1`, `[extensions] relativeWorktrees` (only
   with format version 1), `[user] name|email`, `[remote] url|fetch`, `[branch] remote|merge`. A repair that
   only adds `[user]`/`[remote]` keys without the version gate would admit a worktree-config escape shape;
   the gate is two lines and should be present in either repair.
4. **Mutant re-derivation cost.** Because candidate B rewrites 7 of the 23 target sites, all 23 rows need
   re-derivation against it; the L1 should price that into the choice. Candidate B is therefore *not* smaller
   in total landing cost if Repair A's mechanism leaves the carried rows applicable.

My own recommendation, stated as a measurement rather than a preference: if Repair A's four-leg result is the
same (126/126, 20/20, 12/12) and its diff is materially smaller **and** its round-46 run also shows
`read=0`, land Repair A and take candidate B as the independent second witness (its value is the mechanism
difference, not the size). If Repair A's diff is smaller only because it classifies pointers by name
per-class, candidate B is the safer of the two on the criterion in (1)+(2), because refusals then happen at
the pointer rather than by enumerating the shapes a pointer may take.

## Post-measurement coordination facts (added after the four-leg run; neither changes the receipt above)

**The lane's `plans/fixture_fence.py` moved after this seat measured.** Read-only check at 14:40:
`sha256 57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`, 991 lines, uncommitted
(`git status --porcelain plans/fixture_fence.py` → ` M`). This seat's clone was taken at `3b02d573` and still
holds the frozen base `05d5fe03…`; **every number in this report describes the frozen base and candidate B, not
the current lane file.** Candidate B is a scratch candidate and must not be stacked on, merged with, or
concatenated to the lane's working-tree repair; the L1 chooses one repair and re-derives the mutant battery and
the control receipts against it.

**Peer-reported, not witnessed by this seat:** `C1ExecRepair`'s candidate
(`.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py`) is reported at `HONEST 126 admitted=117 refused=9`,
i.e. incomplete by its own measure. This seat did not open that report or that file (assignment).

**Regression class probed on candidate B** (`refs_probe.py`, `receipts/refs-probe.txt`): the peer reported that
a dropped `_refs` call once let `n17` pass *by absence*, a defect the frozen 32 hostile modules miss. Candidate
B's hand-built, ref-only-broken stores were probed against the transcribed deliverable:

    p1-replace-content-not-hex BREACH …/refs/replace/aaaa… is not a 40-hex ref
    p2-replace-name-not-hex BREACH …/refs/replace/notasha is not a 40-hex replace ref
    p3-notes-content-not-hex BREACH …/refs/notes/commits is not a 40-hex ref
    p4-head-ref-content-not-hex BREACH …/refs/heads/master is not a 40-hex ref
    p5-unknown-ref-namespace BREACH repo/.git/refs/foo is not a ref namespace git writes
    p6-stash-content-not-hex BREACH …/refs/stash is not a 40-hex ref
    p7-refs-entry-is-symlink BREACH …/refs/heads/link is a symlink
    p0-clean-control ADMIT

Every reason names a ref path, so `_refs`/`_ref_tree` executed: the "passed by absence" class is absent from
candidate B, and the cost is only that `_store` calls `_refs` unconditionally as its last leg. The probe is not
`n17`-specific and needs no git child; the L1 can run the same script against whichever repair lands before S2.

**Cosmetic, inherited from the base:** some refusal reasons render as `../../../tmp_…/repo/.git/…` because the
walk labels paths relative to a relative label (`_rel(q, label)` with `label` already relative to `d`). The
frozen base prints the same shape for `n14`/`n16` (`receipts/fourleg-base.txt`), so this is parity, not a
regression, and no counter compares reason strings.

## Limits

- Four legs only (`--skip-mutants`). The mutant leg is the L1's re-derivation job; the carried battery is not
  evidence for candidate B (1/23 caught, 15/23 inapplicable).
- Candidate B was measured on the stage-1 freeze, where `plans/sealed50/` is empty, so `SEALED total=12`; the
  claim's `SEALED total ≥ 18` needs the blind modules authored this wave. The candidate was **not** authored
  blind against the sealed-50 modules (they do not exist yet at measurement time), but it also was not tuned
  to `plans/sealed46/`: the mechanism is a general pointer-resolution rule, and the sealed-46 shapes are
  refused by the symlink/`read=0` rules that predate this seat.
- Honest-population sensitivity is the population's own limit, unchanged: identity pins make it visible, the
  population was not modified by this seat (`mismatched=0`).
- The candidate classifies bytes; it does not run git. The outside-`d` read property is measured by the
  round-46 counter, run here as supplementary evidence only (the claims say it is not part of the predicate).
- `alternates` chains are closed over a visited set, so a cycle is classified once and admitted; git does not
  write cycles and the population has none — recorded, not tested.
- Tool installs this seat: none (no pacman, `uv`, `npx` or binary installs; nothing recorded because nothing
  was installed).
- The live lane's `plans/mutants50/c1-mutants.json` is being rewritten by another seat while this seat ran
  (`git status` in the lane shows it modified). This seat measured the **frozen** copy from its clone at
  `3b02d573`; the `1/23 caught, 15/23 inapplicable` reading describes that frozen battery, not whatever the
  lane holds now.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C1ExecRepairB` removed before yield; everything citable was
copied into this wave dir first (`fence_candidate_b.py`, `candidate_b.diff`, `receipts/`).

VERDICT candidate B PASSES the four legs at REV 3b02d573 (HONEST 126/126, REFUSALS 20/20, SEALED 12/12,
POPULATION 126 mismatched=0) with a different mechanism from the base fence's single-pass allowlist, keeps
`read=0` on the supplementary round-46 counter, and is bigger than the base by +550/-66 lines; R50-C1
admission is not claimed and the carried mutant battery does not apply (must be re-derived).
