# R50C1CritBlind2 — blind hostile modules for the C1 sealed leg (commondir escape, two-hop gitfile→alternates)

Seat: critic (R50C1CritBlind2), wave round-50/w1, claim served: **R50-C1 (novelty)**.
Lane: `kengaku-shokunin`. Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind2` (removed before yield).

## Axes named

| axis | what this seat moves | what it must not harm |
|---|---|---|
| **novelty** (primary) | two held-out hostile shapes no frozen module composes: an escaping `commondir` in an otherwise-valid store; a hostile `objects/info/alternates` hidden behind an **admitted** in-`d` gitfile hop | the honest population (126) — both modules are hostile-only and are built to be refused, so they cannot raise the HONEST leg |
| instrument integrity (supporting) | evidence that the SEALED leg's "clean" means *refused*, not *refused for the named property* | the predicate sentence, the four leg names, the literals `126/20/12/SEALED50_MIN`, the population pin — untouched |

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
```
Measured on a `git clone --shared` of the lane checked out at the stage-1 freeze `3b02d573` (never the live
checkout). Ancestry precondition verified before any measurement:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 3b02d573… HEAD && echo FROZEN_IS_ANCESTOR
FROZEN_IS_ANCESTOR
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
```
Fence under test (base, unmodified): `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.
Counter measured: `plans/round50_c1_verify.py` @ `d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2`
(the stage-1 open-window repair digest recorded in `plans/round-50-claims.md`).

## Deliverable — two blind hostile modules

Written to the wave dir (this is the transcription the item asks for; the scratch copies are byte-identical):

| file | sha256 | fixtures |
|---|---|---|
| `.ufo/waves/round-50/w1/R50C1CritBlind2/sealed/x1_commondir_escape.py` | `e60b2934995272d252f97813acc3e3cac8220382d0aebe9b958a1f2f10049b4a` | `x1-cd-abs`, `x1-cd-rel` |
| `.ufo/waves/round-50/w1/R50C1CritBlind2/sealed/x2_gitfile_alternates_escape.py` | `5b0eadd40b75cb9ef87114424866d9d1a87ace8b54c8f2dc6563f71e0336f302` | `x2-alt-abs`, `x2-alt-rel` |

Both follow the round-44 builder contract (`FIXTURES = [{fid, tool, expect, defects, build}]`,
`build(ctx, d) -> argv tail`), so they drop into `plans/sealed50/` unchanged and the counter's SEALED leg builds
them with `build_honest_population.build_once`. `tool` is `anchor` with `--lane <repo>` for every fixture: the
argv shape is the honest novel-class shape, so the *only* difference from the honest counterpart is the escape.

### X1 — `commondir` whose target escapes `d` (single hop)

`d/lane` is an ordinary repository (`git init` + two commits: HEAD, config, description, hooks/, info/exclude,
logs/, objects/, refs/, index, COMMIT_EDITMSG), plus **one** foreign entry: `.git/commondir` naming a full store
**beside `d`**. Two forms: absolute (`x1-cd-abs`) and relative, `..`-escaping, resolved against the gitdir
(`x1-cd-rel` → line `../../../cd-store-rel/.git`, contains no absolute path).

### X2 — two hops: admitted gitfile, hostile `alternates`

Hop 1 is byte-for-byte the honest class `n21_separate_gitdir` construction (`git init --separate-git-dir`, gitfile
rewritten to `gitdir: ../store`, two commits). Hop 2 is the **single added file** `store/objects/info/alternates`
naming an object store beside `d`. Two forms: absolute (`x2-alt-abs`) and relative (`x2-alt-rel` → line
`../../../alt-store-rel/.git/objects`).

## Expected refusals (the item's statement)

**All four fixtures must be refused (`BREACH`) by any fence that claims R50-C1.** The property each fixture
pins: after resolving the indirection, the common dir / object dir it names is **outside `d`**, so an admitting
fence makes the tool read config, refs or objects outside `d` — the property the fence advertises it never does.
`expect: "error"` is set on every fixture (the counter's SEALED leg only requires `BREACH`; it ignores `expect`).

Measured on the base fence — every fixture refused, with the reason the *base* uses (which is **not** the escape,
see Finding 2):

```
$ python3 probe.py <clone> <work> <sealed dir>          # scratch harness, builds via build_once, calls fence.breach
x1-cd-abs BREACH | lane/.git/commondir is not a plain-init entry
x1-cd-rel BREACH | lane/.git/commondir is not a plain-init entry
x2-alt-abs BREACH | wt/.git is a file (gitdir redirect), not a directory
x2-alt-rel BREACH | wt/.git is a file (gitdir redirect), not a directory
fixtures= 4
```
Full receipt: `receipts/probe-base-fence.json`.

## Materiality — the escapes are real git reads outside `d` (verbatim)

```
== x1-cd-rel commondir line:
../../../cd-store-rel/.git
== git resolves it:
<scratch>/m-x1_commondir_escape/cd-store-rel/.git
fcaa5c965ba0d77c2e9f9b0e1eb6456b0e0b0948 refs/heads/master        <- show-ref: refs read from the OUTSIDE store
fcaa5c9 case                                                       <- log: commit read from the OUTSIDE store
== x2-alt-rel alternates line:
../../../alt-store-rel/.git/objects
== git borrows outside:
tree bd139c98e3546984a25d4f48adf816cc83c2dca6
author fixture <fixture@kengaku.invalid> 1767225600 +0000          <- cat-file -p of the OUTSIDE commit, rc=0
```
`git -C wt count-objects -v` on both x2 fixtures prints `alternate: <scratch>/alt-store-*/…/.git/objects`
(outside `d`). Commands ran under `env -i … GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null` per call, never
exported.

## Counter run with the modules installed in the sealed leg

Modules copied into the clone's `plans/sealed50/` (clone only, never the live lane) and the frozen counter run:

```
$ python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --work <scratch>/work/counter
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE …/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=2 leaked=0 build_errors=0
SEALED50-TOTAL 2 expected_min=6
PREDICATE R50-C1 fail
```
(`TREE dirty=1` is the untracked `plans/sealed50/` I added inside the clone; `--allow-dirty` is the testing-only
flag. `PREDICATE fail` is the base fence's `HONEST admitted=113`, as frozen — not a defect of these modules.)
Receipt: `receipts/counter-sealed.txt`.

**Routed fact for the L1:** these two modules supply **2 of the ≥6** blind modules `SEALED50_MIN` requires; the
leg is not satisfiable by this seat alone.

## Novelty evidence (measured structure, not prose)

Every fixture of the frozen hostile sets was built and walked (`receipts/structure.txt`), reporting only
indirection kinds actually present in the built tree (`in`/`OUT` = target inside/outside `d`):

```
refusals46  f18_wtmeta_out.py          g3-wtmeta-out    commondir=1(in) wtgitdir=1(OUT)
refusals46  f19_commondir_hidden.py    g4-cd-hidden     commondir=1(OUT)
refusals46  f1_gitfile.py              f1-gitdir-outside gitfile=1(OUT)
refusals46  f5_alternates.py           f5-alternates-outside alternates=1(OUT)
refusals46  f7_commondir.py            f7-cd-{accept,reject,anchor} commondir=1(OUT)
blind       x1_commondir_escape.py     x1-cd-abs / x1-cd-rel      commondir=1(OUT)
blind       x2_gitfile_alternates_escape.py x2-alt-abs / x2-alt-rel gitfile=1(in) alternates=1(OUT)
```
No other module in `plans/refusals46` or `plans/sealed46` carries any of the four indirection kinds. Consequences,
each measured:

1. **No frozen hostile module has a gitfile whose target is inside `d`.** `f1_gitfile` is the only gitfile and its
   target is outside. X2 is therefore the corpus's **first composition**: an *admitted* hop (the honest `n21`
   shape, which the repaired fence must admit) followed by a hostile hop.
2. **No frozen module composes hops at all** — one indirection kind per fixture, except `f18` (in-`d` commondir
   with an outside worktree back-pointer, a different family).
3. **`f7`'s refusal is over-determined.** Measured tree of `f7-cd-accept`: `lane/.git` contains exactly
   `['HEAD', 'commondir']` — no config, objects, refs or index, so a fence would refuse that store even if it
   resolved the commondir correctly. X1's store is complete and otherwise allowlisted; the escaping `commondir`
   is its only anomaly, so X1 separates "refused because incomplete" from "refused because escaping".
4. `n21`'s honest store is a plain store (`store/` with hooks/, info/, logs/, objects/, refs/, HEAD, config,
   description, index). X2 differs from it by exactly one added file. A fence that admits `n21` must run its
   store classification on `store` — X2 pins whether that classification also inspects `objects/info`.

## Counterexample: a repair that satisfies every frozen leg still leaks 3 of these 4 fixtures

Scratch-only candidate fence `receipts/naive_repair2.py` (NOT a deliverable, never landed): it lifts the base
fence's blanket refusals with the containment checks the **frozen** sets force — gitfile target inside `d`,
`.git/worktrees/*/gitdir` back-pointer inside `d` (this is what `f18` demands) — and the **relative shortcut** they
do not force: a relative `commondir` line and relative `alternates` lines are admitted without resolving them
(`f7`/`f5` are absolute; `f19` is refused earlier as "lane is not a repository").

```
$ python3 measure.py <clone> <work> <sealed dir> receipts/naive_repair2.py
honest-indirection  n21_separate_gitdir.py   n21-separate-gitdir  base=BREACH naive=ADMIT
honest-indirection  n22_alternates_in_d.py   n22-alternates-in-d  base=BREACH naive=ADMIT
honest-indirection  n20_linked_worktree.py   n20-linked-worktree  base=BREACH naive=ADMIT
blind  x1_commondir_escape.py                x1-cd-abs            base=BREACH naive=BREACH
blind  x1_commondir_escape.py                x1-cd-rel            base=BREACH naive=ADMIT   <- LEAK
blind  x2_gitfile_alternates_escape.py       x2-alt-abs           base=BREACH naive=ADMIT   <- LEAK
blind  x2_gitfile_alternates_escape.py       x2-alt-rel           base=BREACH naive=ADMIT   <- LEAK
refusals46  f18_wtmeta_out.py                g3-wtmeta-out        base=BREACH naive=BREACH

LEG honest-indirection  fence=naive modules=3   clean=0   leaked=3 n20_linked_worktree.py,n21_separate_gitdir.py,n22_alternates_in_d.py
LEG blind               fence=naive modules=2   clean=0   leaked=2 x1_commondir_escape.py,x2_gitfile_alternates_escape.py
LEG refusals46          fence=naive modules=20  clean=20  leaked=0
LEG sealed46            fence=naive modules=12  clean=12  leaked=0
```
Receipt: `receipts/measure2.txt`. Reading: a fence that admits the three honest indirection classes and keeps
**REFUSALS 20/20 and SEALED46 12/12 clean** still hands the tool a config/refs store and an object store outside
`d`. The frozen 32 modules and the 126-fixture honest population do not pin the two decisions these modules pin:

- **D1** a relative `commondir` line must be resolved and containment-tested (the honest `n20` line `../..` is
  relative *and* inside; the hostile relative line climbs out);
- **D2** the store reached through a gitfile must be classified **as the resolved store** — its
  `objects/info/alternates` included — not just used to satisfy the `--lane`/toplevel question.

An earlier, cruder candidate (`relative shortcut` applied to gitfiles too) leaked both X1 and X2 as well as the
frozen `f18`, i.e. it was already invalid against the frozen set; `naive_repair2` is the sharpened version that
survives every frozen leg and still leaks, which is why these modules are the ones that carry the novelty.

## Findings for the L1 (counterexample · evidence · axes · correction)

**F1 — the sealed leg cannot witness the property a module names.** The SEALED leg counts `BREACH` per fixture and
ignores `expect`; a fixture refused for an unrelated shape counts clean. Measured: on the base fence all four of my
fixtures are refused for the *blanket* reasons (`commondir is not a plain-init entry`, `wt/.git is a file`), never
because a resolved target escaped `d`. So "SEALED clean=18" would not mean "the escape is contained".
*Axes:* instrument integrity (novelty evidence quality); no claim predicate is touched.
*Smallest safe correction:* none to the counter (the predicate sentence and leg names are frozen and the claim's
named limit is "admission decisions only"). The S2 module docstrings must state the pinned property (mine do), and
the stage-3 receipt must not be read as an escape-witness. If the L1 wants a witnessed refusal reason, that is a
**round-51** instrument, not an open-window repair.

**F2 — the repair must be measured against a composition fixture, not only single-hop ones.** Evidence: the
`naive_repair2` table above (REFUSALS 20/20, SEALED46 12/12, honest n20/n21/n22 admitted → 3 leaks).
*Axes:* novelty (C1's sealed leg is the only place this can be caught), and the fence's own containment claim.
*Smallest safe correction:* the S2 `plans/fixture_fence.py` must (D1) resolve and contain-check `commondir` lines
relative to the gitdir, and (D2) run the store allowlist on the **resolved** gitfile target, including
`objects/info/alternates`, with containment resolved against that store's `objects/` directory. Both modules then
must go `BREACH` while `n20`/`n21`/`n22` stay `ADMIT`. No change to the predicate, the literals or the pin.

**F3 — routed:** `SEALED50_MIN = 6`; this seat supplies 2 (`SEALED50-TOTAL 2 expected_min=6` on the counter run).

## Post-scoring verification against the landed fence (added after the S3 commit landed)

The lane landed the S3 repair while this seat was open: `plans/fixture_fence.py` sha256
`57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (commit `6db0279`), tip
`d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`. The landed `plans/sealed50/` holds **18** modules — my two are **not**
among them, so the scored receipt `corpus/evidence/round50/c1-receipt.txt` never saw them. I measured the landed
fence on a fresh `git clone --shared` at `d45c5bb` (frozen counter `d8787b34`, population pin unchanged):

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=2
FENCE …/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=20 clean=20 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```
(`SEALED total=20` = the landed 18 + my 2, with `--allow-dirty` because I added them inside the clone.) Receipt
`receipts/counter-landed.txt`. **So the two modules are adoptable additively: adding them keeps the predicate green
and raises the held-out count, and they were simply not present at the scored run.**

### F2 is MET on the landed fence — containment is real, measured both ways

```
$ python3 verdicts.py <clone> <work> .ufo/waves/round-50/w1/R50C1CritBlind2/sealed
x1_commondir_escape.py          x1-cd-abs   BREACH  lane/.git/COMMIT_EDITMSG is not a worktree-store entry
x1_commondir_escape.py          x1-cd-rel   BREACH  lane/.git/COMMIT_EDITMSG is not a worktree-store entry
x2_gitfile_alternates_escape.py x2-alt-abs  BREACH  store/objects/info/alternates names a store outside the fixture
x2_gitfile_alternates_escape.py x2-alt-rel  BREACH  store/objects/info/alternates names a store outside the fixture
```
`receipts/verdicts-landed.txt`. **D2 is satisfied** (x2's reason is exactly the resolved-store containment), and
**D1 is satisfied** — proven by a discrimination pair that reaches the rule the x1 refusal never reaches
(`receipts/x1b_wt_commondir.py`, run against the landed fence):

```
x1b-wt-abs  BREACH  lane/.git/commondir names a common dir outside the fixture
x1b-wt-rel  BREACH  lane/.git/commondir names a common dir outside the fixture
x1b-wt-in   ADMIT                      <- same shape, commondir inside d
```
The landed fence also composes containment through the commondir hop (3-hop probe `receipts/x3_three_hop.py`):

```
x3-h3-abs  BREACH  inner/.git/objects/info/alternates names a store outside the fixture
x3-h3-rel  BREACH  inner/.git/objects/info/alternates names a store outside the fixture
x3-h3-in   ADMIT                      <- same 3 hops, alternates target inside d
```

### F1 confirmed at scale on the landed fence (reason-level audit)

The counter cannot see this: it counts `BREACH`, not the reason. Audit over every fixture of the three hostile
sets, classifying whether the refusal reason names the containment/escape property or an allowlist/shape rule
(`receipts/reasons-landed.txt`):

```
AUDIT refusals46  fixtures=34  modules=20  clean=20  all_reasons_name_the_property=6   shape_only=14
AUDIT sealed46    fixtures=15  modules=12  clean=12  all_reasons_name_the_property=7   shape_only=5
AUDIT sealed50    fixtures=26  modules=20  clean=20  all_reasons_name_the_property=10  shape_only=10
```
For the shape modules (`s50_03` refs namespace, `s50_10` reflog name, `c4_gitfile_delimiter` pointer grammar) a
shape refusal **is** the right reason. The finding is narrower and specific: **`x1-cd-abs`/`x1-cd-rel` are the two
fixtures whose named property (escaping `commondir`) is never reached** — they are refused because the landed
fence classifies a `.git` carrying `commondir` as *worktree metadata* and then rejects `COMMIT_EDITMSG` as "not a
worktree-store entry". They count clean without witnessing containment (the `x1b` pair witnesses it instead). This
is exactly the reading limit F1 records, now measured on the landed text rather than predicted.

### Revised finding status

| finding | status after measuring the landed fence |
|---|---|
| F1 (sealed leg cannot witness the named property) | **confirmed, measured**; harmless for the predicate (admission-only, a named limit) but the stage-3 receipt must not be read as an escape witness for `x1` |
| F2 (repair must implement D1 + D2) | **met** by `57adce4a`; discrimination pairs recorded above |
| F3 (`SEALED50_MIN=6`) | satisfied at the tip (18 landed); my 2 are additive, not required |
| adopt the two modules into `plans/sealed50/` | safe: measured `SEALED total=20 clean=20 leaked=0`, `PREDICATE R50-C1 pass` — integrator's call, and a re-run is needed because the scored receipt predates them |

## Limits

- The absolute variants (`x1-cd-abs`, `x2-alt-abs`) embed the build path in the fixture by construction, so they are
  not byte-reproducible across build roots; the relative variants are (`x1-cd-rel` line
  `../../../cd-store-rel/.git`, `x2-alt-rel` line `../../../alt-store-rel/.git/objects`). The counter does not
  identity-pin sealed modules, so this costs nothing in the predicate; it is stated so nobody pins these later.
- The escaped stores live in the module build parent (`d.parent`), exactly like the frozen `f5`/`f7`; the modules
  prove the fence's `d`-containment property, not host paths outside the scratch root.
- At `3b02d573` no landed repair existed; the S3 repair `57adce4a` landed mid-seat and is measured in the
  post-scoring section above (clone at `d45c5bb`, frozen counter `d8787b34`). No claim is made about any fence
  text other than `05d5fe03` (base) and `57adce4a` (landed), and nothing here is a verdict on the scored receipt.
- `naive_repair2.py` is a critic's counterexample, not a proposal; it is not a candidate for `plans/`.
- I did not re-derive the 126-fixture population, the refusal set or the mutant battery (other seats own those).

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind2` (first pass) and `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind2b`
(post-scoring clone at `d45c5bb`, probes, counter work) both removed after the deliverables and receipts were copied
here; verified absent. Nothing outside this wave dir was written; no git mutation was run against the lane (both
clones were `--shared` and were removed with their scratch).

VERDICT: **modules delivered; both refused by the base fence and by the landed fence; both materially escaping `d`;
both leak under a repair that passes every frozen leg.** X2's pair is the corpus's only composition probe (admitted
gitfile hop + hostile alternates hop); X1's pair is the corpus's only escaping `commondir` in an otherwise complete,
allowlisted store. On the landed `57adce4a` the F2 condition is met (D1 and D2 measured with in-`d`/out-of-`d`
discrimination pairs) and the modules are adoptable additively (`SEALED total=20 clean=20`, `PREDICATE R50-C1 pass`);
the scored receipt predates them, and `x1`'s clean status there is over-determined (F1), so it must not be read as
an escape witness. R50-C1 admission is not mine to claim.
