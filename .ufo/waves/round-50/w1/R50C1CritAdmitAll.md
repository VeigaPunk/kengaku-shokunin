# R50C1CritAdmitAll — four degenerate fences through the R50-C1 counter

Seat: critic, R50-C1 (novelty). Report path as assigned. Lane read-only; all fixtures built in seat scratch, which
was removed before yield (receipts transcribed below).

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252   (freeze commit; counter f9b9873e…, fence 05d5fe03…)
REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1   (lane tip when the seat ran; counter d8787b34…)
```

Ancestry was checked before any measurement: `git merge-base --is-ancestor 3b02d573… <lane HEAD>` → true at seat
start (lane HEAD was `5c56819`, i.e. already past the declared base tip `71f5f5f` because the stage-1 freeze sits on
top of it) and still true after the lane advanced mid-seat to `c3372a9`.

## Axes named

1. **Control validity / kill reach** — does each degenerate fence fail the predicate, on which leg, with which
   numbers? (A control that passed would invalidate the counter and the target per the claims' kill rule.)
2. **Leg separability** — which leg does the discriminating work, and is the HONEST leg with the in-`d` indirection
   fixtures what separates boundary reasoning from shape matching?
3. **Instrument integrity** (adjacent, arising from the measurement) — did the mid-seat counter repair
   (`c3372a9`, module attribution keyed by path instead of basename) change any measured verdict, and is the
   SEALED leg's `<S> ≥ 18` condition enforced by the counter?

## Method

Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C1CritAdmitAll`, `TMPDIR` inside it, one `git clone --shared` of the
lane, detached at `3b02d57…`, then switched (in the same clone, after the lane advanced) to `c3372a9…`. Trees were
clean in every run (`TREE dirty=0`), so `--allow-dirty` was never used. The mutant leg was skipped
(`--skip-mutants`) exactly as the assignment directs for a control: it scores fence mutants, not the fence, and it
cannot change which leg a control fails.

Two of the four fences are committed (`plans/controls50/admit_all.py` `99014708…`,
`plans/controls50/refuse_all.py` `9a8033d2…`); two were authored in scratch because the lane has no such control
(sources inline below, digests recorded). `refuse_all` is measured with the frozen counter; `admit_all` likewise.
No production file was read-write, and no `git` mutating command touched the lane.

Exact commands (one per fence; `$S` = seat scratch):

```
cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work --skip-mutants
cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work --skip-mutants --fence plans/controls50/admit_all.py
cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work --skip-mutants --fence plans/controls50/refuse_all.py
cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work --skip-mutants --fence $S/controls/only_dot_git_exists.py
cd $S/lane && TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work --skip-mutants --fence $S/controls/refuse_if_alternates_or_gitfile_or_symlink.py
# corroboration / ablation
… --fence plans/controls50/keyed_names.py
… --fence $S/controls/gitfile_symlink_only.py
… --fence $S/controls/alternates_only.py
cd $S/lane && TMPDIR=$S python3 $S/isolation.py $S/lane <fences…>
```

Every run exits 1 with `PREDICATE R50-C1 fail`; no control reached `pass`.

## Receipts (verbatim summary lines)

Baseline at the repaired tip, default fence (`05d5fe03…`, unchanged):

```
REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
FENCE …/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

Freeze vs tip, side by side (identical vectors; the freeze run used counter `f9b9873e…`, the tip run `d8787b34…`):

```
== admit_all                                                   3b02d57                        || c3372a9
HONEST fixtures=126 admitted=126 refused=0 error=0                                              identical
REFUSALS total=20 clean=0 leaked=34 build_errors=0                                              identical
SEALED total=12 clean=0 leaked=15 build_errors=0                                                identical
PREDICATE R50-C1 fail                                                                           identical
== refuse_all
HONEST fixtures=126 admitted=0 refused=126 error=0                                              identical
REFUSALS total=20 clean=20 leaked=0 build_errors=0                                              identical
SEALED total=12 clean=12 leaked=0 build_errors=0                                                identical
== only_dot_git_exists
HONEST fixtures=126 admitted=126 refused=0 error=0                                              identical
REFUSALS total=20 clean=2 leaked=32 build_errors=0                                              identical
SEALED total=12 clean=3 leaked=9 build_errors=0                                                 identical
== refuse_if_alternates_or_gitfile_or_symlink
HONEST fixtures=126 admitted=123 refused=3 error=0                                              identical
REFUSALS total=20 clean=5 leaked=29 build_errors=0                                              identical
SEALED total=12 clean=9 leaked=3 build_errors=0                                                 identical
```

Face-specific lines (tip run):

```
# refuse_if_alternates_or_gitfile_or_symlink
HONEST-REFUSED n20-linked-worktree .git is a file (gitdir redirect)
HONEST-REFUSED n21-separate-gitdir .git is a file (gitdir redirect)
HONEST-REFUSED n22-alternates-in-d objects/info/alternates present

# keyed_names (committed claims-table control; corroboration only, other seats own it)
HONEST-REFUSED n20-linked-worktree keyed: commondir
HONEST-REFUSED n21-separate-gitdir keyed: gitfile
HONEST-REFUSED n22-alternates-in-d keyed: alternates

# gitfile_symlink_only (ablation, no alternates key)
HONEST fixtures=126 admitted=124 refused=2 error=0
HONEST-REFUSED n20-linked-worktree .git is a file (gitdir redirect)
HONEST-REFUSED n21-separate-gitdir .git is a file (gitdir redirect)
REFUSALS total=20 clean=3 leaked=31 build_errors=0
SEALED total=12 clean=6 leaked=9 build_errors=0

# alternates_only (ablation, alternates key only)
HONEST fixtures=126 admitted=125 refused=1 error=0
HONEST-REFUSED n22-alternates-in-d objects/info/alternates present
REFUSALS total=20 clean=1 leaked=33 build_errors=0
SEALED total=12 clean=0 leaked=15 build_errors=0
```

## Finding 1 — exact failing leg per fence

`error=0` and `POPULATION mismatched=0 build_errors=0` on all four: no fence raised, no fixture failed to build, so
every failure below is a verdict, not an exception.

| fence | HONEST | REFUSALS | SEALED | failing leg(s) |
|---|---|---|---|---|
| `admit_all` | 126/126 admitted | clean 0/20, **34 fixture leaks** | clean 0/12, 15 leaks | **REFUSALS + SEALED** (leaks). HONEST passes, so it gives no signal. |
| `refuse_all` | **0/126 admitted (126 refused)** | clean 20/20, 0 leaks | clean 12/12, 0 leaks | **HONEST only.** Both hostile legs are satisfied perfectly. |
| `only_dot_git_exists` | 126/126 admitted | clean 2/20, 32 leaks | clean 3/12, 9 leaks | **REFUSALS + SEALED.** HONEST is blind to it. |
| `refuse_if_alternates_or_gitfile_or_symlink` | **123/126, 3 refused** | clean 5/20, 29 leaks | clean 9/12, 3 leaks | **HONEST + REFUSALS + SEALED.** First fence whose over-refusal is caught. |

Clean-module sets behind those counts (modules not printed as `*-MISS`):

- `only_dot_git_exists`: REFUSALS clean `{f6_above, f17_argv_nul}`; SEALED clean
  `{a_newline_anchor, a_phantom_anchor, a_phantom_order}`.
- `refuse_if_alternates_or_gitfile_or_symlink`: REFUSALS clean
  `{f1_gitfile, f5_alternates, f14_gitdir_include_symlink, f15_objects_symlink_out, f17_argv_nul}`; SEALED clean
  `{a_newline_anchor, a_phantom_anchor, a_phantom_order, p_info_redirect, p_pack_redirect, p_refs_redirect,
  s_objects_link, s_packed_refs, s_refs_link}`.
- `keyed_names`: REFUSALS clean 7, SEALED clean 6 (of 12); 25 refusal-fixture leaks.

One of the shape fence's five clean refusals (`f17_argv_nul`) and both of `only_dot_git_exists`'s clean modules are
**accidental**: measured reasons are `lane is not a directory` (argv token carries a NUL, so no lane resolves) and
`no .git entry at the lane` (the `f6_above` repository lives above `d`). The counter can only see verdicts, so a
degenerate fence that happens to refuse a hostile module for the wrong reason counts as clean. That inflates
`clean` but cannot change the predicate outcome here.

## Finding 2 — the ablation: HONEST's separating power IS the in-`d` indirection fixtures

Built once, then each fence evaluated over the full 126, over the 123 fixtures with `n20-linked-worktree`,
`n21-separate-gitdir`, `n22-alternates-in-d` removed, and over those three alone (`isolation.py`, verbatim):

```
REV build honest=126 kept=123 indirection_only=3 build_errors=0
  only_dot_git_exists.py                    FULL 126 admitted=126 refused=0
                                            WITHOUT-n20-n21-n22 123 admitted=123 refused=0
                                            ONLY-n20-n21-n22 3 admitted=3 refused=0
  refuse_if_alternates_or_gitfile_or_symlink FULL 126 admitted=123 refused=3 [n20, n21, n22]
                                            WITHOUT-n20-n21-n22 123 admitted=123 refused=0
                                            ONLY-n20-n21-n22 3 admitted=0 refused=3
  gitfile_symlink_only.py                   FULL 126 admitted=124 refused=2 [n20, n21]
                                            WITHOUT-n20-n21-n22 123 admitted=123 refused=0
                                            ONLY-n20-n21-n22 3 admitted=1 refused=2
  alternates_only.py                        FULL 126 admitted=125 refused=1 [n22]
                                            WITHOUT-n20-n21-n22 123 admitted=123 refused=0
                                            ONLY-n20-n21-n22 3 admitted=2 refused=1
  keyed_names.py                            FULL 126 admitted=123 refused=3 [n20, n21, n22]
                                            WITHOUT-n20-n21-n22 123 admitted=123 refused=0
                                            ONLY-n20-n21-n22 3 admitted=0 refused=3
  admit_all.py                              FULL/WITHOUT/ONLY: all admitted (no signal under any subset)
  refuse_all.py                             FULL/WITHOUT/ONLY: all refused (HONEST fails without them)
```

So: **with those three fixtures removed from the population, every name-keyed fence reads `123/123 admitted` —
zero HONEST signal.** The HONEST leg's ability to catch over-refusal of legitimate in-`d` indirection is carried
entirely by `n20`, `n21`, `n22`, and by nothing else in the 126.

## Finding 3 — is HONEST "what separates boundary reasoning from shape matching"?

Measured answer: **yes on the over-refusal side, no on its own, and the two r50 classes are not both load-bearing.**

- The decisive case for HONEST-only discrimination is `refuse_all`: it satisfies REFUSALS 20/20 and SEALED 12/12
  with zero leaks and is still rejected — HONEST `admitted=0`. No other leg can reject a completely conservative
  fence, so the HONEST leg is *necessary* for the predicate to mean anything.
- For the shape matchers, HONEST catches them only because the population contains the in-`d` counterparts of the
  names they key on: `gitfile` → `n20` **and** `n21` (both carry a `.git` file, so either alone suffices — measured:
  `gitfile_symlink_only` refuses both, `alternates_only` refuses neither), `alternates` → `n22` **only** (measured:
  with the gitfile key dropped, `n22` is the sole HONEST refusal), `commondir` → `n20` (`keyed_names`).
  The two r50 classes carry: `n22` uniquely carries the alternates half; `n21` is redundant with `n20` for the
  gitfile half. A population holding only `n22` would still catch both committed shape controls; one holding only
  `n21` would miss the alternates key entirely.
- HONEST is **not sufficient alone**: all four measured shape matchers also leak 25–33 of 34 refusal fixtures and
  3–9 of 15 sealed fixtures, so the rejection is a conjunction of legs. Shape matching is caught from *both* sides —
  over-refusal by HONEST (only via the three in-`d` fixtures) and under-refusal by REFUSALS/SEALED — and the
  claims' control table sentence ("expected fail on the in-`d` honest classes it refuses") names only the first
  half of what the counter actually measures for `keyed_names` (HONEST 3 refused *and* 25 fixture leaks).

## Incidental findings (adjacent, not this item's verdict)

1. **Counter repair is verdict-preserving.** Mid-seat the lane advanced `5c56819 → 822f3b7 → c3372a9`; `c3372a9`
   repairs `plans/round50_c1_verify.py` (`module` attribution from `path.name` to `str(path)`, both sites),
   digest `f9b9873e… → d8787b34…`. All four control vectors are byte-identical before and after, and the baseline
   fence still reads `HONEST admitted=113 refused=13`. The repair makes the `clean` computation path-keyed instead
   of basename-keyed; no verdict changed on any measured fence.
2. **`SEALED50_MIN` is only enforced when `plans/sealed50/` exists.** Measured at both revisions:
   `SEALED total=12` with no `plans/sealed50/` and no counter objection (code path:
   `if (lane / "plans/sealed50").is_dir(): … if n < SEALED50_MIN`). The claims' predicate sentence requires
   `<S> ≥ 18` (12 frozen + ≥6 blind); today the counter would print `SEALED total=12 clean=12 leaked=0` and let a
   fence otherwise pass. `[INFERENCE]` consequence: the S3 scored run could satisfy the counter while violating the
   claim's literal `<S> ≥ 18`, unless the sealed50 authoring lands in S2. Open-window repair candidate for the L1
   (literal `SEALED46_TOTAL + SEALED50_MIN` floor, not a conditional).
3. The base fence's HONEST refusals include the three in-`d` indirection fixtures
   (`n20` "…is a file (gitdir redirect)", `n21` same, `n22` "objects/info/alternates present") among the 13; that is
   the repair surface C1 claims, unchanged at the tip.

## Scratch artifacts transcribed (removed before yield)

`only_dot_git_exists.py` `634d1e83ec1105a80ea56b2b4a45d569d30dd6ce149574cadd307e098570a350`:

```python
import os, pathlib
def _lane(d, argv):
    lane = None
    for i, tok in enumerate(argv):
        if tok == "--lane" and i + 1 < len(argv):
            lane = argv[i + 1]; break
    p = pathlib.Path(d) if lane is None else pathlib.Path(lane)
    return p if p.is_absolute() else pathlib.Path(d) / p
def breach(d, argv, tool):
    lane = _lane(d, argv)
    if os.path.lexists(os.path.join(str(lane), ".git")):
        return None
    return "no .git entry at the lane"
```

`refuse_if_alternates_or_gitfile_or_symlink.py` `e68a597ee1165f8b70fa047ba459c707f1347ecde89090bf31fc7eafce535848`:

```python
import os, pathlib, stat
def _lane(d, argv):
    lane = None
    for i, tok in enumerate(argv):
        if tok == "--lane" and i + 1 < len(argv):
            lane = argv[i + 1]; break
    p = pathlib.Path(d) if lane is None else pathlib.Path(lane)
    return p if p.is_absolute() else pathlib.Path(d) / p
def _scan(d):
    st = os.lstat(d)
    if stat.S_ISLNK(st.st_mode):
        return "fixture dir is a symlink"
    for root, dirs, files in os.walk(d, followlinks=False):
        rp = pathlib.Path(root)
        for name in list(dirs) + list(files):
            m = os.lstat(rp / name)
            if stat.S_ISLNK(m.st_mode):
                return f"{name} is a symlink"
            if name == ".git" and stat.S_ISREG(m.st_mode):
                return ".git is a file (gitdir redirect)"
            if (name == "alternates" and rp.name == "info" and rp.parent.name == "objects"
                    and stat.S_ISREG(m.st_mode)):
                return "objects/info/alternates present"
    return None
def breach(d, argv, tool):
    why = _scan(str(d))
    if why:
        return why
    return None if os.path.isdir(str(_lane(d, argv))) else "lane is not a directory"
```

(The measured source wraps `os.lstat` in `OSError` guards returning `… cannot be lstat'ed`; the condensed form above
keeps the same three triggers, the same precedence and the same strings.)

Ablations `gitfile_symlink_only.py` `2a031702…` and `alternates_only.py` `4bbad570…` are the same walk with one and
two triggers removed respectively. `probe.py` `c1964cee…` (per-fixture verdict dump) and `isolation.py`
`13a76ed6…` (subset ablation) are scratch-only; their logic is stated in the Method and Finding 2 above, and the
counter plus the two ablated fences reproduce every number cited.

## Limits

- Mutant leg not run (`--skip-mutants`), by assignment: it scores fence mutants, not the fence under test.
- Outside-`d` reads are not measured here (round-46 counter's property, deliberately not re-scored).
- Fixture identity is the population builder's digest; host-sensitive git outputs are pinned, not observed live.
- `plans/sealed50/` did not exist at either measured revision, so `SEALED` is the 12 frozen r46 modules only.
- The two scratch fences are candidate controls, not production artifacts; if the L1 wants them committed they need
  the usual control-fence review (`plans/controls50/`), which I did not do.
- Verdicts are per fixture; the counter's `clean` is per module and prints at most two misses per module, so the
  clean-module sets above are derived from the absence of `*-MISS` lines for that module (all 34 refusal and 15
  sealed fixture verdicts are accounted for by `leaked=` plus the printed misses).

## VERDICT

All four degenerate fences are rejected, each on the correct leg and with no exception or population defect:
`admit_all` fails REFUSALS+SEALED (34/15 fixture leaks, HONEST 126/126); `refuse_all` fails HONEST alone (0/126)
while satisfying both hostile legs perfectly; `only_dot_git_exists` fails REFUSALS (`clean=2/20`) + SEALED
(`clean=3/12`) with HONEST blind (126/126); `refuse_if_alternates_or_gitfile_or_symlink` fails HONEST on exactly
`n20`, `n21`, `n22` plus REFUSALS `clean=5/20` and SEALED `clean=9/12`. The HONEST leg's separating power is exactly
the in-`d` indirection fixtures — with them ablated every shape fence reads `123/123 admitted` — but HONEST separates
only the over-refusal half of shape matching; the under-refusal half is carried by REFUSALS/SEALED, and only
`refuse_all` is rejected by HONEST alone. No defect in the counter or the population blocks R50-C1 on this item; the
adjacent `SEALED50_MIN` conditional guard is an open-window repair candidate for the L1. Scratch removed before
yield; no lane file was written.

---

# Addendum — post-landing re-measurement of the same four controls (S3 tree)

The lane advanced while this seat ran: `3b02d57 → c3372a9 → 6db0279` (S3 fence repair `57adce4a…`, `plans/sealed50/`,
re-derived battery, Q41) `→ d6f2fce` (battery frozen at 15 rows) `→ d45c5bb` (scored C1 receipt, measured outcomes,
LOG, corpus index). Because the claim's kill rule binds the controls to the landing tip, the four controls were
re-run on a fresh clean `git clone --shared` detached at the last observed tip.

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78     TREE dirty=0
FENCE 57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
COUNTER d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2
MUTANTS e885f0a6e69e33af55519279c5efab5f8dd8950df95b1e08a41e39e3043f5ccb
POPULATION pin b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 (unchanged)
plans/sealed50/*.py = 18
```

Full predicate (mutant leg included), verbatim:

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE …/lane/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
```

exit 0. This is line-for-line identical to the committed `corpus/evidence/round50/c1-receipt.txt` (whose `REV` is
`d6f2fce`), reproduced independently at a later tip.

## Controls on the landing tree (`--skip-mutants`, every run exit 1)

| fence | HONEST | REFUSALS | SEALED 46 | SEALED 50 | failing leg(s) |
|---|---|---|---|---|---|
| `admit_all` | 126/126 admitted | clean 0, **34 leaks** | clean 0, 15 leaks | clean 0, 22 leaks | REFUSALS + SEALED |
| `refuse_all` | **0/126** | clean 20/20 | 12/12 | 18/18 | **HONEST only** |
| `only_dot_git_exists` | 126/126 admitted | clean 2, 32 leaks | clean 3, 9 leaks | clean 0, 22 leaks | REFUSALS + SEALED |
| `refuse_if_alternates_or_gitfile_or_symlink` | **123/126, refused n20, n21, n22** | clean 5, 29 leaks | clean 9, 3 leaks | clean 8, 10 leaks | HONEST + REFUSALS + SEALED |
| `keyed_names` (corroboration) | 123/126, n20/n21/n22 | clean 7, 25 leaks | clean 6, 9 leaks | clean 8, 10 leaks | HONEST + REFUSALS + SEALED |

```
HONEST-REFUSED n20-linked-worktree .git is a file (gitdir redirect)
HONEST-REFUSED n21-separate-gitdir .git is a file (gitdir redirect)
HONEST-REFUSED n22-alternates-in-d objects/info/alternates present
HONEST-REFUSED n20-linked-worktree keyed: commondir
HONEST-REFUSED n21-separate-gitdir keyed: gitfile
HONEST-REFUSED n22-alternates-in-d keyed: alternates
```

So on the landing tree the kill rule holds: no control reaches `PREDICATE pass`; the HONEST leg is still rejected
for exactly the three in-`d` indirection fixtures; `refuse_all` still satisfies both hostile legs perfectly and is
still rejected by HONEST alone; and the under-refusal of the shape matchers is caught on both sealed sets. The
answer to the item's question is unchanged by the landing.

## Observations for the integrator (outside the four-fence item, no admission judgement)

1. **My earlier incidental finding 2 is resolved by the landing.** `plans/sealed50/` now holds 18 modules, so the
   counter's conditional `SEALED50_MIN` guard is active and `SEALED` totals 30 (12 + 18) ≥ 18.
2. **The claim's After block no longer matches what the command prints.** `plans/round-50-claims.md` still promises
   one line `SEALED total=<S> clean=<S> leaked=0 build_errors=0` with `<S> ≥ 18`; the counter emits **two** `SEALED`
   lines (`total=12` and `total=18`) and the committed receipt contains both, while `SCORECARD.md` writes
   `SEALED 12/12 + 18/18 clean`. Not a kill-rule trigger (the `PREDICATE` line is present, exit 0, tree clean), but
   a judge reading the claim literally finds no single `<S>` line. A counter change now would be post-scored-run, so
   the safe repair is a note in the claims file.
3. **The mutant battery's re-derivation is not recorded in the open-window table.** The table has exactly one row
   (the counter `f9b9873e → d8787b34`). The battery digest moved `2e5cfe66…` (at `c3372a9`) → `e885f0a6…` (at
   `d45c5bb`) with no row, though the claims say every repair of the mutant battery records old→new digest in that
   file; the fence's own `05d5fe03 → 57adce4a` likewise appears nowhere in `plans/round-50-claims.md`
   (`git show d45c5bb:plans/round-50-claims.md | grep -n 57adce4a` → no hit) and no commit message carries it.
4. The two scratch controls were re-created for the re-run as behaviour-equivalent condensations (digests
   `84ef0d4d…` and `96f8517d…`, same three triggers and precedence, `OSError` guards dropped). They reproduce the
   freeze-era `HONEST`, `REFUSALS` and `sealed46` numbers exactly, which is the equivalence check for the sources
   transcribed above. Both scratch trees were removed after the run; the only lane write of this seat remains this
   report.

Landing-tree scratch (`/fast/scratch/hyaku/kengaku-r50/R50C1CritAdmitAll`) was removed before this addendum was
finalised; no production file was opened for writing and no git command was run against the live checkout.
