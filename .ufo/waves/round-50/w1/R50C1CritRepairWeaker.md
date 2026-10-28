# R50C1CritRepairWeaker — which repair candidate is weaker for the security property (critic)

Seat: critic, leaf, no subagent dispatch. Lane `kengaku-shokunin`, round 50, wave `w1`.
Report written read-only against the lane; the only lane write is this file.

**REV** `3b02d573d58cc6d2e0d27ef92ac0815354912252` — the stage-1 freeze. Verified an ancestor of the lane tip
before any measurement (`git merge-base --is-ancestor 3b02d57 <tip>` → `ANCESTOR_OK`; lane tip at seat start
`8acd0f830452198706c21af8bc52d611c0f29177`). Every fence measurement below ran on `git clone --shared` of the lane
detached at that commit, tree clean (`TREE dirty=0` in every counter receipt).

Candidates compared, digests recomputed by me from the wave directory:

    plans/fixture_fence.py @ 3b02d57            05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  (frozen base = control)
    C1ExecRepair/fence_candidate.py             2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc  (repair A, "five-class containment")
    C1ExecRepairB/fence_candidate_b.py          4e68592ca640a4f384b767db179ad79b8c5e9863086311ac87968810412ef393  (repair B, "two-phase resolve-then-classify")

Axes named: **novelty / security property of the fence** (does the repaired fence admit a fixture whose git
store, discovered repos and argv stay inside `d`), and the derived criterion **monotonicity** — a repair may not
admit a fixture the frozen base refused unless the new admission is proved contained. Nothing else was judged;
I claim no R50-C1/C2 admission and edited no production file.

## Answer

**Repair A is the weaker of the two on the security property.** It admits a hostile fixture that the frozen base
fence refuses and that repair B refuses, and the admitted fixture carries a `gitdir:` pointer whose value names
a path **outside `d`**. The hole is one line of A's own code: it computes the worktree back-pointer target and
then throws it away (`fence_candidate.py:783-785`, `_back, why = _file_ref(p / "gitdir", …)`, `if why: return
why`) — the round trip the base fence's gitfile refusal made unnecessary is never checked once the gitfile
surface is opened. B checks exactly that (`fence_candidate_b.py:809-810`, `if _norm(back) != _norm(gd): return
f"{label}/gitdir does not point back at this metadata dir"`).

## 1. Verdicts reproduced through the frozen counter (both candidates, same clone, same pin)

    $ cd <clone> && python3 plans/round50_c1_verify.py --lane . --work <w> --skip-mutants            # base
    REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
    TREE dirty=0
    FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
    POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=113 refused=13 error=0
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 build_errors=0
    PREDICATE R50-C1 fail

    $ … --fence <A>/fence_candidate.py --skip-mutants
    REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
    TREE dirty=0
    FENCE …/fa.py sha256=2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc
    POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=117 refused=9 error=0
    HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
    HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
    HONEST-REFUSED n14-stash-entry … has a name git does not write
    HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph is not git's alternates file
    HONEST-REFUSED n16-notes-ref … has a name git does not write
    HONEST-REFUSED n18-shallow-fetch repo/.git/config section header b'[remote "origin"]' is not plain
    HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
    HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
    HONEST-REFUSED n08-tag-detached repo/.git/HEAD is not a plain branch HEAD
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 build_errors=0
    PREDICATE R50-C1 fail                                                   (exit 1)

    $ … --fence <B>/fence_candidate_b.py --skip-mutants
    REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
    TREE dirty=0
    FENCE …/fb.py sha256=4e68592ca640a4f384b767db179ad79b8c5e9863086311ac87968810412ef393
    POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=126 refused=0 error=0
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 build_errors=0
    PREDICATE R50-C1 pass                                                   (exit 0, `--skip-mutants`: not admission)

Both candidates refuse **every** frozen hostile fixture (20/20 refusal modules, 12/12 sealed46 modules; 34 + 15
built fixtures), so on the frozen hostile sets the two are indistinguishable. The measured difference on the
frozen *honest* set (117/9 vs 126/0) is A **over-refusing** — a novelty defect for A, not a security one.

## 2. The minimal hostile fixture: A admits, B refuses

Base: the frozen honest `n20-linked-worktree` fixture (repo + linked worktree `wt`, metadata
`repo/.git/worktrees/wt/`). Two file writes, nothing else:

    worktrees/wt/gitdir  <-  "index\n"                        # was "../../../../wt/.git"
    worktrees/wt/index   <-  "gitdir: <a path outside d>\n"  # was a real git index (A/B check size only)

`index` is the only file in A's per-worktree allowlist (`WORKTREE_TOP`) whose content is unconstrained; every
other one is validated (`HEAD` branch-HEAD, `ORIG_HEAD` 40-hex, `commondir`/`gitdir` pointers). One write is
therefore not enough and two writes are: the `gitdir` rewrite alone points at an in-d file whose content carries
no `gitdir:` line (measured as `c10`–`c12` below), and the content rewrite alone is unreachable.

Measured verdicts on that fixture, same argv (`--lane wt`), same crate-free in-process call the counter uses
(`breach(d, argv, tool)`):

    FIXTURE …/work5/hostile/d
    EDITS  worktrees/wt/gitdir = 'index'; worktrees/wt/index = 'gitdir: <outside>'
    A ADMIT
    B BREACH repo/.git/worktrees/wt/gitdir: pointer '/fast/scratch/…/outside' leaves the fixture
    BASE (05d5fe03) BREACH wt/.git is a file (gitdir redirect), not a directory

So the fixture is **refused by the frozen base and by repair B, admitted by repair A**: A's repair opens the
gitfile surface and with it admits a fixture that carries an outside-`d` pointer the fence never resolves. A's
own witness set cannot see this axis — its 48 cases contain `wt-gitdir-out`/`-abs`/`-trailing-spaces` (the
*pointer itself* leaving `d`) and a correct-round-trip control, but no case where the pointer stays inside `d`
and its **target's content** leaves it.

Second A-only shape, same class (contained, reported for completeness): an `objects/info/alternates` row naming
any existing in-d directory that is not an object store (`../../../main`, `../../../main/.git`, `../../../`).
A resolves only that target's own `info/alternates` (`fence_candidate.py:436`) and never classifies the target
as an object store; B queues it and refuses (`main/.git is not a loose-object directory`).

## 3. Mutation matrix that produced the discriminating set

One change per copy of an admitted honest fixture, both candidates, identical argv (`/fast/scratch/…/cases.py`;
`A` = repair A, `B` = repair B; `<<< DIFF` marks a discriminator):

    c00-control-n21          A=ADMIT  B=ADMIT          c00-control-n20   A=ADMIT  B=ADMIT
    c00-control-n22          A=ADMIT  B=ADMIT          c00-control-plain A=ADMIT  B=ADMIT
    c01-n21-gitfile-no-newline         A=ADMIT  B=BREACH  <<< DIFF   (B: "is not a single gitdir: line")
    c02-n21-gitfile-crlf               A=BREACH B=BREACH
    c03-n21-gitfile-trailing-spaces    A=BREACH B=BREACH
    c04-n21-gitfile-trailing-slash     A=ADMIT  B=ADMIT
    c05-n21-gitfile-dotdot-return      A=ADMIT  B=ADMIT
    c06-n21-store-commondir            A=BREACH B=BREACH
    c07-n21-store-gitdir-commondir     A=BREACH B=BREACH
    c10-n20-meta-gitdir-to-HEAD        A=ADMIT  B=BREACH  <<< DIFF   (B: "repo/.git/HEAD is not a single gitdir: line")
    c11-n20-meta-gitdir-to-config      A=ADMIT  B=BREACH  <<< DIFF
    c12-n20-meta-gitdir-to-lane-file   A=ADMIT  B=BREACH  <<< DIFF
    c13-n20-meta-HEAD-detached         A=BREACH B=ADMIT   <<< DIFF   (A: "is not a plain branch HEAD")
    c14-n20-wtfile-no-newline          A=ADMIT  B=BREACH  <<< DIFF
    c15-n20-commondir-to-metadir       A=BREACH B=ADMIT   <<< DIFF   (B admits `commondir` -> its own metadata dir)
    c20-n22-alt-to-repo-root           A=ADMIT  B=BREACH  <<< DIFF   (B: "main/.git is not a loose-object directory")
    c21-n22-alt-to-gitdir              A=ADMIT  B=BREACH  <<< DIFF
    c22-n22-alt-to-fixture-root        A=ADMIT  B=BREACH  <<< DIFF
    c23-n22-alt-to-plain-file          A=BREACH B=BREACH
    c24-n22-alt-comment                A=BREACH B=BREACH
    c25-n22-alt-blank-then-out         A=ADMIT  B=ADMIT
    c30-plain-info-packs               A=BREACH B=ADMIT   <<< DIFF   (B: size check only)
    c31-plain-commit-graph-abs         A=BREACH B=ADMIT   <<< DIFF   (B: size check only)
    c32-plain-commit-graph-rel         A=BREACH B=ADMIT   <<< DIFF
    c33-plain-shallow-nonhex           A=BREACH B=BREACH
    c34-plain-refs-remotes             A=BREACH B=ADMIT   <<< DIFF   (honest: git writes refs/remotes)
    c35-plain-config-user              A=BREACH B=ADMIT   <<< DIFF   (honest: n12 class)
    c36-plain-info-refs                A=BREACH B=ADMIT   <<< DIFF   (honest: n07 class)

    SUMMARY: 4 controls admit on both; 26 mutations; 8 A-only admissions in 3 shapes
             (gitfile-no-newline x2, wtmeta-gitdir-no-round-trip x3, alternates-non-object x3);
             8 B-only admissions in 6 shapes (detached wtmeta HEAD, commondir self-cycle,
             info/packs bytes, commit-graph bytes x2, refs/remotes, [user], info/refs).

## 4. Materiality — what the fixture set cannot distinguish

I tried to turn each candidate's extra admission into a witnessed outside-`d` read with git 2.56.0 under
`strace -f -e trace=openat,newfstatat,stat,access`:

    A's fixture (the two-edit n20 above), from wt/ and repo/:
      status --porcelain        outside=0   rev-parse --show-toplevel  outside=0
      log --oneline -1          outside=0   worktree list [--porcelain] outside=0 (from both roots)
      worktree prune -n -v      outside=0   count-objects -v           outside=0
      carrier (worktrees/wt/index) opened 3x, outside path opened 0x
    B's commit-graph carrier (objects/info/commit-graph = "<abs path outside d>"):
      log --oneline -1 / commit-graph verify / count-objects -v / rev-list --count HEAD -> outside=0
      git itself: "error: commit-graph file is too small" — it parses the bytes as a graph header, does not
      follow a path (gitformat-commit-graph(5) puts the chain under objects/info/commit-graphs/, which B refuses)
    B's info/packs carrier (first token naming an outside pack):
      count-objects -v / gc --auto / fsck --connectivity-only / log --oneline -1 -> outside=0
      (objects/info/packs is consumed by the dumb-http walker, not by local object access)

So on this host's git **neither candidate's extra admission yields a witnessed outside-`d` read** for the
commands measured, and the frozen fixture set (126 honest + 20 refusal + 12 sealed modules) produces *identical*
verdicts for both: it cannot distinguish the two on the containment property at all. What separates them is
**pointer closure**, and that is what I decided on:

- A's admitted set contains a fixture whose pointer graph reaches outside `d`: the bytes `gitdir: <outside>`
  sit in a file A classifies by size only, reached through a back-pointer A resolved and discarded. The same
  bytes in a `.git` file are refused by *both* candidates; B refuses them at `worktrees/<id>/gitdir` too.
- B's admitted set closes every pointer it can parse; its unvalidated files (`objects/info/packs`,
  `objects/info/commit-graph`) are opaque object-info blobs, not pointer files, and are measured inert for
  local git.
- Both candidates admit a state git never writes in the metadata dir (`A`: non-round-trip `gitdir`, gitfile with
  no trailing newline; `B`: `commondir` pointing at its own metadata dir). That is a shared provenance limit.

Bounded caveat, stated as a limit not a hedge: if the L1's criterion is instead "no unvalidated bytes anywhere in
an admitted fixture may name a path outside `d`", then B fails that criterion too (c30–c32) and the two are tied
on it; A still fails the strict pointer-closure criterion *and* over-refuses nine honest classes, so A is weaker
under either criterion after that one is excluded.

## 5. Smallest safe correction

For **A** (if it is kept as the landing candidate — three local edits, no new mechanism):

1. `_worktree`: require the back pointer to close. `_back` is already computed at line 783; add
   `if _norm(_back) != _norm(p): return f"{label}/gitdir does not point back at this metadata dir"`. This alone
   refuses the counterexample above.
2. `_worktree`, wtmeta `index`: A admits any bytes (size only, lines 778-779). At minimum require the git index
   signature `b"DIRC"` at offset 0, so the metadata `index` cannot be a pointer carrier; B has the same gap (it
   also checks size only), so this is a shared hardening, not an A-only one.
3. `_alternates`: classify the target with `_objects(target, …)` (or refuse a target whose name/contents are not
   an object store), so an alternates row cannot name an arbitrary in-d directory.
   Strictly optional but cheap: match git's pointer grammar exactly — `_one_line` (line 148) strips an optional
   trailing newline, where git never writes that shape and B's `GITFILE_LINE` requires `\n`.

For **B** (if it is the landing candidate): validate the two unvalidated object-info contents —
`objects/info/commit-graph` must start with `CGPH`, `objects/info/packs` must be `P <packname>.pack` lines — and
refuse a `commondir` that resolves to its own metadata directory (c15).

Neither correction touches the predicate sentence, the four leg names, the literals `126`, `20`, `12`,
`SEALED50_MIN`, or the population pin, so either is open-window eligible on its face.

## Limits

- Measured at REV `3b02d57` on git 2.56.0, one host. The counter's `--skip-mutants` leg only: the mutant battery
  is the L1's re-derivation job and both candidates are `unmet` on the carried r49 battery (A `1/23 caught,
  15 broken`; B `1/23, 15 broken`) — not evidence about either candidate.
- The materiality sweep is bounded to 10 git commands and 3 carriers; it shows *no* witnessed escape, not
  *no* escape. A git code path I did not run (e.g. a future `worktree repair` variant) may parse the carrier.
- B was never measured against `plans/sealed50/` blind modules (they did not exist when B ran); A was (2/2
  refused). That is an evidence gap for B, not a measured weakness.
- The mutation matrix is mine (26 shapes), not a frozen set; it is reproducible from the report but it is not a
  scored instrument, and the shapes are chosen against each candidate's rule text, so it under-samples both.
- Both candidates admit arbitrary `.git/index` bytes in a store — a shared, unmeasured content surface.
- I did not read the candidates' *code* beyond the cited rules, and I judged neither claim's admission.

## Reproduction

    S=/fast/scratch/hyaku/kengaku-r50/R50C1CritRepairWeaker; mkdir -p "$S"; export TMPDIR=$S
    git clone --shared -q <lane> "$S/lane" && git -C "$S/lane" checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
    cp .ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py   "$S/fa.py"
    cp .ufo/waves/round-50/w1/C1ExecRepairB/fence_candidate_b.py "$S/fb.py"
    # counter receipts: base / A / B
    (cd "$S/lane" && python3 plans/round50_c1_verify.py --lane . --work "$S/w4a" --skip-mutants)
    (cd "$S/lane" && python3 plans/round50_c1_verify.py --lane . --work "$S/w4b" --fence "$S/fa.py" --skip-mutants)
    (cd "$S/lane" && python3 plans/round50_c1_verify.py --lane . --work "$S/w4c" --fence "$S/fb.py" --skip-mutants)
    # the hostile fixture (build the honest n20 fixture through the counter's own builder, then two writes):
    worktrees/wt/gitdir = "index\n"; worktrees/wt/index = "gitdir: /a/path/outside/d\n"
    # then: fa.breach(d, ["--lane","wt"], "anchor") -> None (ADMIT); fb.breach(...) -> "pointer … leaves the fixture"

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1CritRepairWeaker` removed before yield (clone, built fixtures,
traces and probe drivers included); no scratch tree left on disk. Nothing was installed this seat (no pacman,
`uv`, `npx` or binary install). No lane write except this report; no commit, no mutating git outside the
scratch clone's own detached checkout.

**VERDICT** Repair **A** (`2b142a85…`) is the weaker candidate for the security property: it admits a
two-write mutation of the frozen `n20` fixture (`worktrees/wt/gitdir` → `index`, `worktrees/wt/index` →
`gitdir: <outside d>`) that the frozen base fence `05d5fe03…` and repair **B** (`4e68592c…`) both refuse — B at
the pointer, base at the gitfile — because A discards the worktree back-pointer target it computes
(`fence_candidate.py:783`) and validates only that file's size. On the frozen 126/20/12 fixture set the two are
indistinguishable (both refuse every hostile module); the discriminator is pointer closure, where A admits an
outside-`d` pointer the fence never resolves while B's admitted set closes it. No outside-`d` read was witnessed
for either candidate on git 2.56.0 over the 10 commands measured, and B shares the weaker "unvalidated content"
class (`objects/info/packs`, `objects/info/commit-graph`) plus a `commondir` self-cycle — so the fixture set
distinguishes the two on *pointer closure and honesty*, not yet on a material containment break.
