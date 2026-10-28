# R50C1CritBlind8 — two blind hostile modules for the fixture fence (R50-C1, novelty)

REV 8acd0f830452198706c21af8bc52d611c0f29177 (lane tip measured, `git clone --shared`)
FREEZE 3b02d573d58cc6d2e0d27ef92ac0815354912252 — `git merge-base --is-ancestor 3b02d57… 8acd0f8…` → **yes**, before any measurement
FENCE UNDER ATTACK `plans/fixture_fence.py` sha256 `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (the S3-repaired fence at the tip; the stage-1 base fence `05d5fe03…` was **not** the fence measured — the two differ by commit `6db0279`)
COUNTER `plans/round50_c1_verify.py` sha256 `850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999`
BUILDER `plans/honest50/build_honest_population.py` `35e3de60…` · POPULATION pin `b5197f94…` (126 rows)
GIT `git version 2.56.0` · Python 3.14

TIP AT REPORT TIME `297e17927ba9342a87ba27a48cc5270a001de7cb` (other seats landed after my measurement). Both
instrument digests are **unchanged** at that tip — `plans/fixture_fence.py` still `57adce4a…`,
`plans/round50_c1_verify.py` still `850ec790…` — and `plans/sealed50/` still holds 20 modules, so every verdict
below applies to the tree the integrator will fold into.

## Axes named

| axis | why this seat touches it |
|---|---|
| **novelty (C1)** — primary | the TWO sealed modules change `<S>` (`SEALED total`) and the sealed-clean count; the mutant witnesses bear on the mutant floor (Q38) |
| quality (Q38) | every kill direction I report is *witnessed* on a mutated fence copy, never assumed |
| coverage | **not claimed, not touched** — read-only seat, no `SCORECARD.md`/`corpus/` writes |
| calibration (C2) | untouched |

## What I delivered

| file | shape | digest (sha256) | verdict on fence `57adce4a` |
|---|---|---|---|
| `C1CritBlind8/sealed/s50_11_packed_peel_outside_store.py` | item (i): `packed-refs` peel row `^<sha>` repointed at a commit whose only bytes sit in a second object store inside the fixture | `1e7b35c0b146ced5982a104c02e8e2ed49401660522739a3e4221de129ddc335` | **ADMIT** |
| `C1CritBlind8/sealed/s50_12_commit_graph_chain_outside.py` | item (ii): honest single-file `objects/info/commit-graph` (magic `CGPH`) + `objects/info/commit-graphs/commit-graph-chain` carrying one row git writes and one row that is an absolute host path outside `d` | `5ba4c6f368a1875fd9e81ea6bdd59e4f5951a023008c25d37430a38cfc283086` | **BREACH** `commit-graph-chain carries a row git does not write` |
| `C1CritBlind8/substitutes/s50_13_packed_peel_shape.py` | **substitute** for item (i), offered because (i) is not a containment shape: peel row of 41 hex digits | `7ddfc16587c01be2fd8bb0a6d257090c2236d6c5b375663df05a1db17a68a9d1` | **BREACH** `repo/.git carries a bad peeled line` |

Receipts (all under this seat's wave dir, `C1CritBlind8/receipts/`): `env-and-delivered.txt`, `variant-matrix.txt`,
`mutant-direction.txt`, `counter-letter.txt`, `counter-substitute.txt`. The driver (`C1CritBlind8/probe/drive.py`),
the eight matrix probes (`C1CritBlind8/probe/mods/`) and the two mutated fence copies used for the Q38 witnesses
(`C1CritBlind8/probe/mutants/`, **never** a fence candidate) are copied into this seat dir for rerun
(`C1CritBlind8/probe/README.md`). Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind8` was removed before
yield; it appears inside the receipts only as the directory the commands were executed in.

## Exact commands run (verbatim in the receipts)

```
git clone --shared <lane> <scratch>/lane && git -C <scratch>/lane checkout 8acd0f830452198706c21af8bc52d611c0f29177
python3 probe/drive.py --lane <scratch>/lane --work <scratch>/probe/w-a --mods C1CritBlind8/sealed
python3 probe/drive.py --lane <scratch>/lane --work <scratch>/probe/w-m --mods <scratch>/probe/mods
python3 probe/drive.py ... --mods C1CritBlind8/sealed     --fence <scratch>/probe/fence_nochain.py
python3 probe/drive.py ... --mods C1CritBlind8/substitutes --fence <scratch>/probe/fence_nopeel.py
cd <scratch>/lane-probe && python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --work <work>
```

`drive.py` is a thin driver in my scratch: it builds each candidate with the lane's own
`plans/honest50/build_honest_population.py:build_once` into an opaque, `PAD=8` decoy-padded parent (the counter's Q39
rule) and decides each fixture with the counter's own `HARNESS` string, verdict in the exit status (10 BREACH ·
11 ADMIT). `lane-probe` is a second `git clone --shared` of the tip used only to add the candidate modules to
`plans/sealed50/` and read the instrument's own `SEALED` line. The live checkout was never written.

## Observed outputs (verbatim)

Delivered modules, fence `57adce4a`:

```
s50-11-packed-peel-outside-store expect=error rc=11 verdict=ADMIT why=ADMIT
s50-12-commit-graph-chain-outside expect=error rc=10 verdict=BREACH why=BREACH commit-graph-chain carries a row git does not write
```

Instrument level, both modules copied into `plans/sealed50/` of the tip clone (`--allow-dirty --skip-mutants`, testing mode):

```
REV 8acd0f830452198706c21af8bc52d611c0f29177
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=22 clean=21 leaked=1 build_errors=0
SEALED-MISS s50_11_packed_peel_outside_store.py s50-11-packed-peel-outside-store ADMIT ADMIT
PREDICATE R50-C1 fail
```

Same clone with item (i) replaced by `s50_13`:

```
SEALED total=22 clean=22 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

Variant matrix (eight shapes, same harness, fence `57adce4a`):

```
p02-peel-dangling          ADMIT    peel names an oid present in no store
p04-ref-target-outside     ADMIT    packed ref ROW (not peel) names an object only in an in-fixture store
p05-chain-hex-outside-only ADMIT    chain row 40-hex, graph file only in an in-fixture store
p06-chain-hex-nowhere      ADMIT    chain row 40-hex, graph file nowhere
p07-honest-control         ADMIT    annotated tag + pack-refs + commit-graph, untouched (baseline)
p08-peel-before-ref        ADMIT    `^` peel row before every ref row (order violation)
p09-peel-41hex             BREACH   repo/.git carries a bad peeled line
p10-info-chain-direct      BREACH   commit-graph-chain is not a plain object-info entry (object-store redirect)
```

Mutant witnesses (Q38 — direction witnessed, not assumed):

```
mutant A (fence 7ccee77baaef3856e9f1816c73fb045f0b58c138d0b9b562322fc7c63af2434c, `_graph_dir` chain loop deleted)
  s50-12 BREACH -> ADMIT ; s50-11 ADMIT -> ADMIT (non-discriminating)
mutant B (fence 1597dfee935063e11df03d35ffdf265062fc074e14d81faf1171cf3b0a1eab49, `_packed` peel HEX40 check deleted)
  s50-13 BREACH -> ADMIT
```

## Findings

**F1 — item (ii) is a valid sealed atom and carries a witnessed mutant kill.** `s50_12` BREACHes on the
`CHAIN_ROW` row rule and flips to ADMIT when that loop is deleted. It is the only fixture I found that
distinguishes a fence that validates every chain row from one that validates only the first (the fixture carries a
valid `graph-<hex>.graph` + a valid row before the hostile row). It also costs nothing on the honest leg: the whole
`--skip-mutants` predicate still prints `PREDICATE R50-C1 pass` with it in place.

**F2 — item (i) as issued is not realizable as a containment attack, and on this fence it is ADMITTED.**
Three independent measurements, each of which would have to be false for the shape to be a legitimate sealed atom:

1. *The fixture builder forbids the outside store.* `plans/round44_c1_verify.py:280-284` (`Ctx._inside`) raises
   `ValueError("path outside the fixture root")` for every path outside `d`, and `ctx.sh`/`ctx.write`/`ctx.init`
   all route through it. A module therefore cannot place an object store outside `d`; the only "outside store" I can
   build is `d/outside-store`, i.e. **inside** `d`.
2. *An in-`d` foreign store is a declared HONEST shape.* Population row 121 is `n22-alternates-in-d`
   (`plans/honest50/modules/novel50/n22_alternates_in_d.py`): `lane/.git/objects/info/alternates` →
   `../../../main/.git/objects`, admitted at `HONEST admitted=126`. So "an object visible only through a store that
   is not the repository's own" is exactly what the frozen population already blesses when it stays inside `d`.
3. *The fence reads no object bytes.* It is a name/type/shape walk (`plans/fixture_fence.py:40`: "admitted by name
   and size without content validation"); `_packed` checks the peel row's 40-hex shape only. A dangling peel cannot
   make the fence open anything, so the shape leaks nothing.

With the outside store necessarily inside `d`, the shape collapses to a dangling reference: `p02-peel-dangling`
(oid in **no** store) is admitted by the same code path with the same verdict, which proves the admission is about
resolvability, not about where the bytes live. Folding `s50_11` into `plans/sealed50/` therefore plants a **false
atom**: measured, it takes the leg to `SEALED total=22 clean=21 leaked=1` and `PREDICATE R50-C1 fail`, for a
property the fence never claimed.

**F3 — there is no resolvability leg at all, on either shape family (5/6 probes ADMIT).** `p02`, `p04` (ref row,
not peel), `p05`, `p06` (chain row naming a graph file that exists nowhere) and `p08` (peel row with no preceding
ref row) are all admitted. This is a decided exclusion of the fence's design, not a regression — but it must be
*stated* in the round, or a future reader will mistake `s50_11` for a defect the fence failed to catch.

**F4 — the obvious repair is unsafe and must not be attempted inside this claim's window.** The natural
"resolvability" leg (require each ref/peel oid to exist as `objects/<xx>/<38>`) over-refuses the frozen population:
honest row 128 `n07-reflog-gc` (`git gc --prune=now`) keeps **zero loose objects** — measured layout
`objects/pack/pack-39d4f40e….{pack,idx,rev}` only, `LOOSE-OBJECTS 0`, `git cat-file -e HEAD` rc=0. A correct leg
would have to parse binary pack indexes, which the fence refuses by doctrine. Under the frozen predicate
(`HONEST admitted=126`) that repair cannot pass.

**F5 — the letter of item (ii) also has a literal alternative that is already refused.** Read as
`objects/info/commit-graph-chain` (the chain placed directly in `objects/info/`), it BREACHes via the
object-info-redirect rule (`p10`). I delivered the `commit-graphs/` reading because it is the layout git writes and
because it additionally forces per-row validation; both readings are receipts here.

## Impacted axes and the smallest safe correction

- **novelty (C1)**: adopt `s50_12` (raises `<S>` by 1 with `leaked=0`) and adopt `s50_13` in place of `s50_11`;
  do **not** fold `s50_11` into `plans/sealed50/`. Predicate sentence, leg names, `126`/`20`/`12`/`SEALED50_MIN`
  literals and the population pin are untouched by this change — no open-window repair is needed for it.
- **Q38 / mutant floor**: `s50_12` and `s50_13` are witnessed discriminators for two concrete mutant payloads
  (the two deletions in `receipts/mutant-direction.txt`); `s50_11` cannot be a mutant row at all, since its
  reference verdict is already ADMIT (a mutant can only move it in the "add a leg" direction).
- **coverage / C2**: untouched.

Two candidate restatements of item (i) for the L1 to choose, ranked by what the fence actually enforces:
1. *(adoptable now)* "a peel row whose oid is not git's 40-hex" → `s50_13`, BREACH, witnessed direction.
2. *(a new claim, not this one)* "no ref or peel row names an object the store cannot resolve without leaving the
   store" — needs pack-index parsing and re-opens `HONEST admitted=126` (F4); it cannot be scored by R50-C1.

## Limits

- Verdicts are the counter's own harness contract; a fence that calls `os._exit(11)` while shrinking is
  indistinguishable from an admission inside it (the counter's named limit, inherited).
- Measurements are on git 2.56.0 / Python 3.14 / x86-64 only; `packed-refs` and commit-graph byte shapes are
  version-sensitive.
- The tip clone ran the counter with `--allow-dirty --skip-mutants` because the candidate modules are untracked in
  it; the mutant leg was not re-scored by the counter (the two witnessed payloads above are the substitute
  evidence), and the population/HONEST/REFUSALS/SEALED lines are unaffected by `--skip-mutants`.
- I did not test any fence in the live checkout, and wrote no production file, no `SCORECARD.md`/`LOG.md`/`corpus/`
  entry, and no commit.

## Defect of my own, reported

A first receipt command ran `mkdir -p probe/work5 probe/work6` with the shell cwd at the fleet root and created
`/home/vgpnk/Projects/shokunin/probe/{work5,work6}`. Both were removed immediately (`rmdir` of the three dirs, then
`ls -d` confirmed `No such file or directory`); the fleet root has no residue. The corrected run `cd`s to the
scratch root first. Scratch tree `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind8` was removed before yield; every
receipt above was copied into this wave dir first.

VERDICT: item (ii) delivered as a valid blind sealed atom with a witnessed mutant kill (`s50_12`, BREACH). Item (i)
delivered and measured **ADMIT** — it cannot be a sealed atom under the frozen predicate without planting a false
atom (F2), so the safe adoption is the substitute `s50_13` (BREACH, witnessed direction) and a recorded statement
that the fence has no ref/graph resolvability leg (F3), with the loose-object repair explicitly refused (F4).
R50-C1 admission is not claimed by this seat.
