# R50C1CritBlind1 — blind hostile modules against the repaired fence (R50-C1, novelty)

Seat: critic, wave `round-50/w1`, lane `kengaku-shokunin`. Item: author TWO blind hostile modules, each an
out-of-`d` escape a naive pointer-resolution repair would admit — (i) a `.git` FILE whose target is a symlink
chain ending outside `d`, (ii) an `objects/info/alternates` line whose absolute path resolves through `..` to
outside `d` — and state each expected refusal. Read: `plans/round-50-claims.md` (full), `plans/fixture_fence.py`
at the freeze tree only, plus the frozen (stage-1) counter contract and the frozen honest `n20`/`n21`/`n22`
modules for the loader contract. No other seat's repair was read; the working-tree `plans/round50_c1_verify.py`
(modified by another seat) was never opened.

## Axes named

- **novelty (primary, R50-C1)** — held-out strength of the `SEALED` leg: do the blind modules separate a *correct*
  containment rule from the *naive* one a repair actually writes? These two modules attack the exact two code
  paths the honest repair opens (`n20`/`n21` gitfile parsing, `n22` alternates parsing), not the pre-existing
  blanket refusals.
- **coverage (observed, not claimed)** — the sealed floor counts modules, not escape mechanisms (finding F3).
- Correctness is not claimed for the fence; I author the attackers, not the repair.

## Deliverables (written)

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-50/w1/C1CritBlind1/sealed/`

| file | sha256 | fid(s) | expected refusal |
|---|---|---|---|
| `s50_gitfile_symlink_chain.py` | `70705f02751b5d8b92ccd2001be573a74b5c2f065b007c327cc4bb6c2776c8f1` | `s50-gitfile-symlink-chain` | BREACH — the store the `.git` file names resolves outside `d` (chain `hop1 -> hop2 -> ../gitdir`) |
| `s50_alternates_dotdot_abs.py` | `9fe77895491822abff0c2cf539c9eb8ea303732b3c4828e5363e6167c806d853` | `s50-alternates-dotdot-abs` | BREACH — the alternates entry resolves outside `d` (`<d>/lane/.git/objects/../../../../store/.git/objects`) |

Both are `tool: "order"` fixtures returning the contract argv tail, authored to the frozen round-44 builder
contract `build(ctx, d) -> list[str]`; fids collide with nothing in `plans/battery4*`, `plans/sealed46`,
`plans/refusals46` (scan: 0 hits for `s50`). Filenames are distinct from every frozen sealed module, so the
stage-1 counter's `path.name` attribution defect (the one recorded as repaired in the claims doc) cannot
mis-attribute them.

Receipts (`…/w1/C1CritBlind1/receipts/`) and the scratch probes (`…/w1/C1CritBlind1/probes/`) are the evidence for
every number below. Probes are scratch candidates, not lane code.

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252     # stage-1 freeze, measured tree
LANE_TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1  # lane tip when read; freeze is an ancestor
FENCE plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
COUNTER plans/round50_c1_verify.py sha256=f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76 (stage-1)
git 2.56.0 · Python 3.14.8
```

Ancestry checked before any measurement:
`git -C <lane> merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD` → rc 0 (`FREEZE_ANCESTOR=ok`).
All work ran against `git clone --shared` of the lane checked out at `3b02d57…`, never the live checkout.

## Commands run (scratch root `$S=/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind1`, `TMPDIR=$S`)

```
git clone --shared -q <lane> "$S/lane" && git -C "$S/lane" checkout -q 3b02d57…
python3 "$S/driver.py"  --lane "$S/lane" --work "$S/work"      --modules "$S/candidate"
python3 "$S/compare.py" --lane "$S/lane" --work "$S/cmp" --blind "$S/candidate" \
        --honest plans/honest50/modules/novel49 plans/honest50/modules/novel50 --naive "$S/naive_fence.py"
cp <modules> "$S/lane/plans/sealed50/"
cd "$S/lane" && python3 plans/round50_c1_verify.py --lane . --work "$S/counterwork" --skip-mutants --allow-dirty
```

## Observed — the frozen counter accepts both modules and refuses them (base fence)

`receipts/counter-base-fence.out` (verbatim, unabridged elsewhere in that file):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1CritBlind1/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=2 leaked=0 build_errors=0
SEALED50-TOTAL 2 expected_min=6
PREDICATE R50-C1 fail
```

Read this the right way: our two modules load, build and are **each attributed clean (BREACH)** by the counter's
own sealed leg — the second `SEALED` line is the `plans/sealed50` leg over exactly these two files. `PREDICATE
fail` is the base fence (13 honest over-refusals) plus `SEALED50-TOTAL 2 expected_min=6`, i.e. this seat supplied
2 of the ≥6 blind modules the wave must land; it is not a fault in the modules. `TREE dirty=1` is my
`plans/sealed50/` copy inside the clone; the lane checkout was never written.

## Observed — each fixture is a live out-of-`d` escape, not a cosmetic one

`receipts/escape-facts.json` (git run exactly as a tool behind the fence would run it):

- `s50-gitfile-symlink-chain` — fence: `BREACH` / `hop2 is a symlink`;
  `git -C <lane> rev-parse --absolute-git-dir` → `…/f000/../gitdir`, **`git_dir_inside_d=false`**; `git log`
  rc 0 (the repo works through the chain). The `.git` text is the bare name `hop1`: no `..`, no absolute
  component, nothing a lexical test can object to.
- `s50-alternates-dotdot-abs` — fence: `BREACH` / `lane/.git/objects/info/alternates present (object-store
  redirect)`; the outside store's `HEAD` (`8e4c79a979197857ef833f1d814d9315f6bc076a`) is readable from the lane
  (`git cat-file -p` rc 0) while **`borrowed_object_in_lane_odb=false`** — git genuinely read an object that
  exists nowhere inside `d`.

## Observed — the discrimination the claim needs (naive admits, correct refuses)

`receipts/discriminator.out`. Two repairs differing **only** in containment policy, over the same pointer
handling (gitfile + worktree `commondir` + alternates):

- `naive` = the pathlib idiom a hasty repair writes: `pathlib.Path(target).is_relative_to(d)`. `PurePath` never
  collapses `..` and never resolves symlinks.
- `correct` = `os.path.realpath(target)` then a prefix test.

```
blind  s50-gitfile-symlink-chain    base=BREACH naive=ADMIT  correct=BREACH
blind  s50-alternates-dotdot-abs    base=BREACH naive=ADMIT  correct=BREACH
honest n20-linked-worktree          base=BREACH naive=ADMIT  correct=ADMIT
honest n21-separate-gitdir          base=BREACH naive=ADMIT  correct=ADMIT
honest n22-alternates-in-d          base=BREACH naive=ADMIT  correct=ADMIT
DISCRIMINATING blinds=2/2
```

That is the whole point of the pair: the repair that fixes the honest leg (`n20`/`n21`/`n22` all ADMIT under
both policies) still leaks both blind fixtures under the naive policy, and only the realpath policy refuses them
while keeping the honest classes admitted. Raw-probe detail from `escape-facts.json`: for (ii)
`pathlib.Path(line).is_relative_to(d)` → **ADMIT**, `line.startswith(str(d))` → **ADMIT**, `normpath`+prefix →
REFUSE, `realpath` → REFUSE; for (i) `normpath`+prefix → **ADMIT**, `is_relative_to` → **ADMIT**, `realpath` →
REFUSE.

Read the scope of that word "naive" precisely, because it is narrower than it sounds: the pair discriminates the
**unnormalized containment idioms** — a raw prefix test, and `pathlib.Path(...).is_relative_to(d)`, which does
not collapse `..`. It does **not** discriminate a repair that normalizes first: `normpath`+prefix refuses (ii)
after collapse and, together with a per-pointer `lstat` symlink refusal, refuses (i) at the hop. Measured below
against a repair seat's candidate, independently of my probes.

## Third-party crosscheck (post-hoc, cited — not my measurement)

Seat `R50C1ExecRepair` ran both of my sealed files against its own unlanded candidate
(`9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1`) in a scratch clone and recorded the
reasons in `.ufo/waves/round-50/w1/C1ExecRepair/receipt-blind50-crosscheck.txt` (digests of my files match the
ones above):

```
counter: SEALED total=2 clean=2 leaked=0 build_errors=0
s50_gitfile_symlink_chain.py       s50-gitfile-symlink-chain    BREACH hop2 is a symlink
s50_alternates_dotdot_abs.py       s50-alternates-dotdot-abs    BREACH …names '…/objects/../../../../store/.git/objects', which resolves outside the fixture
```

So on that implementation (i) is refused by the symlink rule and (ii) **by the rule under test, after
normalization** — i.e. the pair is correct-but-non-discriminating there, which is exactly what the `normpath`
row of my own probes predicted. This does not weaken the modules as held-outs (they are still refused, so they
cannot leak), it bounds what their refusal proves: only a repair that decides containment on unnormalized text
can be caught by them. A blind set that relies on my two files alone would therefore not cover the normalization
axis; that axis needs a fixture where lexical normalization and kernel resolution disagree (the chained-observer
shape named in F4, which I did not author).

## Counterexample / findings against the claim's measurement

**F1 — `SEALED` discrimination is a property of the blind set, not of the predicate.** The predicate only counts
`clean == len(files)` (each module's every fixture BREACH). It cannot tell a module that separates naive from
correct containment from one that is refused by a rule the base fence already had, nor from one refused by a rule
the *repair* added without touching the property under test. Both of my modules are "clean" on the base fence for
reasons that are *not* the property under test: (i) `hop2 is a symlink`, (ii) `alternates present` — and the
crosscheck above shows the same for a normalizing repair, where (i) again dies on the symlink rule. Their refusal
is correct in every state measured, so they cannot leak; what the predicate cannot see is how much of that
refusal is the branch under test. A blind set made only of such modules would satisfy `SEALED50_MIN` while
proving nothing about the repaired branch. The predicate still cannot check this for any module, and it does not.

**F2 — the escape shapes sit exactly on the honest repair's new branches (why these two and not others).** The
honest classes the base fence refuses are `n17..n22`; only `n20`/`n21` (gitfile) and `n22` (alternates) force new
parsing code. Any repair that admits them must parse a pointer and decide containment, which is precisely the
decision both modules attack — measured: base refuses all three, both repair policies admit all three.

**F3 — the floor counts files, not mechanisms.** `SEALED50_MIN` is `len(glob("*.py"))`; six near-duplicate
modules satisfy it. My two files add two mechanisms (gitfile-chain, alternates-`..`), not two variations of one.
The smallest safe correction is bookkeeping, not code: the S2/S3 receipt should name the *mechanisms* the ≥6
blind modules cover, so a later reader can see the floor was met by six shapes rather than six spellings.

**F4 — a gap I did not author (now built by peers; still not my measurement).** Chained alternates: an alternates
entry pointing at an object directory *inside* `d` that is not a repository, whose own
`objects/info/alternates` leaves `d`, is followed by git but is not a store any walk of `d` collects. A repair
that checks only the entries of collected stores would admit it. I did not build it (outside this item) and claim
nothing about it. Status since: peer `R50C1ExecAlternates` measured it as a genuine escape (the outside object is
read), and `R50C1ExecRepair` reproduced it and made its `_alternates` traversal recursive with a visited set and
`ALTERNATES_DEPTH = 4`; per its report the repo/bare-repo/plain-dir hop variants now refuse while an honest in-`d`
2-hop chain and an in-`d` cycle still ADMIT. Both are third-party reports I neither ran nor audited.

**F5 — a depth cap is a leak unless it refuses; this is the cheapest unmeasured attack on the recursive repair.**
If `ALTERNATES_DEPTH = 4` means "stop descending after four hops and decide on what was seen", a chain of five
in-`d` hops plus one outside hop is admitted with every link looking honest. The shape, ~20 lines, no symlinks and
no `..`: `d/lane/.git/objects/info/alternates` → `d/h1/objects` (a plain directory, no `.git`) → its own
`objects/info/alternates` → `d/h2/objects` → … → `d/h5/objects` → `/outside/store/.git/objects`, with each `hN`
holding a *complete copied store* so no refusal can be explained by a missing `HEAD`/`objects`/`refs`. Two
fixtures pin it: depth = cap must REFUSE (the chain still escapes), and an honest in-`d` chain of the same length
that ends inside `d` must ADMIT — otherwise the cap is being enforced by blanket refusal and the honest leg is
being paid for it. Same test the peer's own dropped-`_refs` find demands: never accept "refused" as evidence that
the *branch under test* refused. The visited set has the parallel defect if it is keyed on the spelled path
rather than `realpath` (two spellings of one directory dodge the dedupe, and a revisit that is skipped must be a
refusal, not an admission).

Resolution (third-party; I verified the receipt text and the candidate digest
`2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc`, I did not run it). `receipt-adversarial-48.txt`
lines 38-39 and 51 show what the item asks: `alt-chain-cap5` (five in-`d` hops) BREACH "chains deeper than 4
object stores" — reaching the cap refuses, it does not decide on what was seen; `alt-chain-cap-escape` (four
in-`d` hops, then an outside hop) BREACH naming the outside store in the chain; `honest-alt-chain-4` ADMIT at
exactly the cap, so the honest leg is not paying for the bound. The dedupe argument holds under mark-before-process
plus a refusing cap (a skip can only mean "already fully proved"), which is what those two lines measure.

One residual dependency, stated as a dependency and not a defect: `normpath` is equivalent to `realpath` for the
visited key **only because every symlink under `d` is refused** by the tree rule. It is not equivalent in
general — an intermediate symlink component in an alternates path leaves the final component a real directory, so
a pointer-level `lstat` does not see it and only `realpath` distinguishes it from the normalized spelling. Today
that path is unreachable because the walk refuses the symlink first, so the equivalence is sound; but it makes the
symlink refusal load-bearing for *two* rules (the walk and the alternates containment), and it means the
normpath-vs-realpath axis stays unmeasured for as long as the walk stays strict. Whoever narrows that rule later
must re-run the alternates leg with a symlinked intermediate component, because neither of my modules nor any
fixture in this set would catch it: mine are `..`-based, and `normpath` collapses those.

## Smallest safe correction

No production file needs to change for this item. The integrator should (a) copy the two files from
`…/w1/C1CritBlind1/sealed/` into `plans/sealed50/` unchanged (digests above), and (b) in the S3 receipt, state per
blind module which *mechanism* it covers and whether its refusal was witnessed on the branch under test (not only
on a pre-existing blanket rule) — otherwise F1/F3 leave `SEALED` satisfiable without evidence. Scope of the pair,
stated so no one over-reads it: a repair that keeps the base fence's blanket `.git`-file refusal always refuses
(i) (correct, non-discriminating); a repair that normalizes containment before deciding (`normpath`+prefix, or
`realpath`) refuses (ii) too, as the `R50C1ExecRepair` crosscheck measured, and a `lstat` symlink refusal at each
pointer kills (i) at the hop. What the pair catches is containment decided on **unnormalized** text — a raw
prefix test, or `pathlib.Path(...).is_relative_to(d)`, where `..` is invisible. Since (ii) is the one aimed at a
decision function a repair might actually write, a blind set relying on these two alone leaves the normalization
axis uncovered; F4/F5 name the shapes that would cover it (the chain, and its depth-cap boundary).

## Limits

- Blindness: I read the fence at the freeze tree, the claims doc, the stage-1 counter contract (`f9b9873…`) and
  the frozen honest `n20`/`n21`/`n22` modules (needed for the loader contract and to prove the honest classes
  stay admitted). I did **not** read the working-tree `plans/round50_c1_verify.py` (another seat's repair) nor any
  seat's fence repair. The counter I ran is the stage-1 instrument, not the repaired one, so the `MUTANTS` leg
  was skipped (`--skip-mutants`) and no mutant claim is made.
- The two "repair" policies in `probes/naive_fence.py` are my own scratch constructions, not the lane's repair;
  they exist only to witness the admit/refuse separation. `correct` is a 60-line probe, not a candidate fence,
  and its admission of `n20`/`n21`/`n22` is not evidence that the frozen 126-fixture honest leg passes.
- Sealed modules carry no identity pin: (ii) embeds the build path in the alternates line (as frozen refusal
  `f5` does), so it is not identity-comparable and does not need to be. A blind module that fails to build is
  counted in `build_errors` and fails the leg, so build fragility is visible, not silent.
- `SEALED50-TOTAL 2 expected_min=6` in my counter run is this seat's share of the wave, not a defect.
- I did **not** test the landed fence (`plans/fixture_fence.py` sha256
  `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`, read at tip `d45c5bb`) nor the unlanded
  candidate `9baedf13…`. The only post-hoc evidence I cite is `R50C1ExecRepair`'s written receipt for the
  candidate, quoted as third-party measurement with matching digests; the landed-fence run belongs to the
  integrator or the verifier, not to the blind author, and my modules' provenance stays "authored against the
  base fence description, digests fixed before any repair was measured".
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind1` was removed before yield; every number above is
  reproducible from the copied receipts and probes in the wave dir with `--work "$S"` pointed at any new
  scratch. Receipts contain the scratch prefix as build provenance.

## VERDICT

Both blind modules are **delivered and discriminating against unnormalized containment**: authored blind to the
repair, refused by the base fence through the counter's own sealed leg (`SEALED total=2 clean=2`), each a *live*
out-of-`d` escape witnessed by git itself, and each **admitted by the naive pathlib containment repair while
refused by realpath containment**, with the three honest indirection classes admitted by both. Against a
normalizing repair (`normpath`+prefix with a per-pointer symlink `lstat`) both are refused — (ii) by the rule
under test, (i) by the symlink rule — as `R50C1ExecRepair`'s crosscheck receipt independently measured, so there
they are correct-but-non-discriminating, not leaks. Impacted axis: novelty (R50-C1 `SEALED`). Findings F1/F3: the
predicate counts files and verdicts, so the S3 receipt must record per-module mechanism and whether the refusal
was witnessed on the branch under test, or the sealed floor proves less than it appears to.
