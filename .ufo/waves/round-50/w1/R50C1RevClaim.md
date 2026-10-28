# R50C1RevClaim — adversarial review of R50-C1 falsifiability and causal separability

Seat: R50C1RevClaim (reviewer). Item: under the frozen kill rule, (a) is R50-C1 reachable **without** the
fence repair, (b) does C1 depend on any C2 artifact, (c) is the mutant floor satisfiable by a fence that does
not resolve pointers (shape keys). Plus the strongest non-author rejection case and whether committed evidence
answers it.

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
```
REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1   (lane tip when the review started)
    git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD -> FREEZE_IS_ANCESTOR=yes
    freeze commit 3b02d573d58cc6d2e0d27ef92ac0815354912252 2026-10-28T14:18:09-03:00
CLONE /fast/scratch/hyaku/kengaku-r50/R50C1RevClaim/lane, `git clone --shared`, checked out at the freeze commit.
```
Frozen digests verified against `plans/round-50-claims.md` at the measured revision:
```
d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  plans/round50_c1_verify.py   (tip; = open-window row new digest)
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py       (base fence, unchanged at tip)
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt
2e5cfe6622c5d1497570724939b1346f15d80ed4b978e5fcaee925bb8b5ff865  plans/mutants50/c1-mutants.json  (committed bytes)
```
The live checkout is **labile** (state at review close): ` M corpus/QUALITY.md`,
` M plans/fixture_fence.py` (worktree sha `57adce4a…`, an uncommitted S2 repair candidate),
` M plans/mutants50/c1-mutants.json` (worktree sha `6ce17b22…`, 16 rows, uncommitted),
` M plans/round50_c1_verify.py` (worktree sha `850ec790…`, uncommitted), `?? plans/sealed50/` (uncommitted).
Every finding below is measured on **committed** bytes — the freeze clone or `c3372a9:` objects — never on the
live tree; the uncommitted candidates are assessed only where stated in "State at review close". S2 has not
landed: `plans/sealed50/` exists in no commit.

## Axes named

- **A1 — reachability without the repair.** Can `PREDICATE R50-C1 pass` be printed by a fence that does not
  repair the five honest classes, i.e. that does no boundary reasoning at all?
- **A2 — C1↔C2 dependency.** Does C1's code/artifact closure read anything C2 writes (or the reverse)?
- **A3 — mutant-floor meaning.** Does `MUTANTS caught≥12 / broken=0` require pointer resolution, or only
  sensitivity of the measured fence to frozen text diffs?
- **A4 — predicate/claim conformance.** Do the frozen after-block's five lines and `<S>` floor actually bind
  the counter's exit code?

## Commands run (all read-only against the lane; candidate code only in scratch)

```
# base control, fast leg
cd <clone> && python3 plans/round50_c1_verify.py --lane . --skip-mutants
# base control, full mutant leg (committed 23-row battery)
cd <clone> && python3 plans/round50_c1_verify.py --lane .
# A1/A3 probe: a 3-line fence that inspects no byte of d, plus 12 re-derived mutants (scratch clone + clean archive copy)
git -C <clone> archive 3b02d57 | tar -x -C <scratch>/clean     # non-repo clean tree; TREE dirty=0
cp <scratch>/probe/honest_path_key.py <tree>/plans/fixture_fence.py
cp <scratch>/probe/probe-mutants.json <tree>/plans/mutants50/c1-mutants.json
cd <tree> && python3 plans/round50_c1_verify.py --lane .
cd <tree> && python3 plans/round50_c1_verify.py --lane . --skip-mutants
```

### Base-fence control (reproduces the claim's "before" exactly)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
EXIT=1
```
The instrument's observational core is real and reproducible: the lane previously had no counter that printed
`admitted=113 refused=13` over a pinned 126-fixture population.

Full mutant leg on the same base fence with the committed battery (`2e5cfe66…`):
```
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
PREDICATE R50-C1 fail
EXIT=1
```
Twelve of twenty-three hunks do not apply to the base fence (`patch-rc=1 … hunk FAILED`); only three rows change
the verdict vector. (The task brief's "4 of 23" is not what the committed battery produces here; the applicable
count is 3, the non-applicable count 12. Either way the carried battery is a candidate, not a floor.)

### A1/A3 probe — a fence that resolves nothing passes every leg

Probe fence, verbatim, 3 effective lines (sha256 `f35568159b1a7854b57b0572fd09610ca8693b3e2bf6d74732fc7e2651c0d434`):
```python
"""Shape-keyed candidate probe for R50-C1 (scratch only, never lands)…"""
import os

HONEST_KEY = os.sep + "honest" + os.sep


def breach(d, argv, tool):
    p = os.path.normpath(str(d))
    if HONEST_KEY in (p + os.sep):
        return None
    return "shape key: fixture path is not under an honest-component build root"
```
It reads no store byte, starts no child, resolves no pointer, and does not touch the five refused classes. It
passes because the counter itself builds the honest leg under `work / "honest"` (`round50_c1_verify.py:196`) and
every hostile leg under `work / "<refusals46|sealed46>"` (`:228`), so the harness label is in the `d` string the
fence receives. Clean tree (`git archive` copy, `TREE dirty=0`, no `--allow-dirty`):

```
TREE dirty=0
FENCE …/plans/fixture_fence.py sha256=f35568159b1a7854b57b0572fd09610ca8693b3e2bf6d74732fc7e2651c0d434
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=12 caught=12 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
EXIT=0
```
The 12 mutants were re-derived exactly as the S2 open window permits: each row replaces the single admit-test
line with a distinct false predicate (`if False and …`, `if 0 and …`, `if None and …`, `if "" and …`, `…
and False:`, `if (p + os.sep).startswith(HONEST_KEY):`, `if HONEST_KEY not in (p + os.sep):`, `if HONEST_KEY in
p[:0]:`, `… and p == "":`, `… and len(HONEST_KEY) == 0:`, `if "\x00" + HONEST_KEY in (p + os.sep):`, `if
HONEST_KEY in (p + os.sep) is False:`). Every row applies cleanly, imports, and flips the vector; all twelve are
witnessed by the run itself, so Q38 "witnessed, not assumed" is satisfied in letter.

`--skip-mutants` on the same tree:
```
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 pass
EXIT=0
```
No `MUTANTS` line at all, and the predicate still passes and exits 0.

## Findings by severity

### F1 — HIGH. The predicate is reachable without the repair, and cannot tell boundary reasoning from a harness-path key (A1)

`breach(d, argv, tool)` receives the fixture's absolute path; the counter's own build layout encodes the leg in
that path (`round50_c1_verify.py:196` `work / "honest"`, `:228` `work / rel.replace("/","-")`). A fence that
admits on the substring `/honest/` prints `HONEST admitted=126 refused=0`, `REFUSALS 20/20`, `SEALED 12/12`,
`MUTANTS 12/12`, `PREDICATE pass`, exit 0 (A1/A3 receipt above). So:

- **Reachable without the repair: yes.** The kill rule measures *admission outcomes over known corpora* only.
  Nothing in the frozen predicate asserts that the fence classifies a store, that it reads any byte of `d`, or
  that the five refused classes were repaired rather than bypassed. The claim's sentence "the fence repaired so
  it passes" is carried by prose, not by the predicate.
- **The frozen controls do not close it.** `controls50/keyed_names.py` keys on file *shapes* and is expected to
  fail HONEST — its recorded receipt does (`HONEST admitted=123 refused=3`, `REFUSALS clean=7 leaked=25`). Path
  keying is a different failure mode that passes HONEST by construction; no frozen control exercises it.
- **The dirty-tree guard is not a defence.** The pass above is on `TREE dirty=0` in a non-repo archive copy; the
  same bytes committed to the lane print a 40-hex `REV` with identical legs.

### F2 — HIGH. The `<S> ≥ 18` after-condition is not part of the predicate (A1/A4)

The claims file states `<S> ≥ 18 … are literals in the counter (SEALED50_MIN, MUTANT_MIN), not values the counter
can satisfy from the files it reads`. That is false for S. The counter has `SEALED50_MIN = 6` (`:65`), no `18`
literal anywhere, and the blind-set check runs only if the directory exists:
```python
if (lane / "plans/sealed50").is_dir():          # :262
    n = len(sorted((lane / "plans/sealed50").glob("*.py")))
    if n < SEALED50_MIN: … ok = False           # :264-265
```
With `plans/sealed50/` absent (true at every commit through the tip), the leg is silently skipped, `SEALED
total=12` is printed, and `PREDICATE pass`/exit 0 is reachable — as both probe receipts show. The kill rule's
list also omits "S < 18": "any refusal or sealed module not refused" is satisfied by 12/12. Consequence: the one
leg with held-out evidence is optional; and because a path-keyed (or table-keyed) fence refuses every unknown
module *correctly by accident*, even a compliant ≥18 blind set would not catch F1.

### F3 — MEDIUM. `--skip-mutants` yields a passing receipt with an entire leg missing (A3/A4)

`--skip-mutants` is "testing only" (`:156`) but is not rejected in scored mode: the run prints
`PREDICATE R50-C1 pass`, exit 0, with no `MUTANTS` line (receipt above). The frozen after-block requires five
lines in this order; the frozen kill rule covers only "PREDICATE line absent or fail; exit code ≠ 0". A scored
`c1-receipt.txt` can therefore omit the mutant floor and still exit 0. The receipt check is human-only.

### F4 — MEDIUM. No frozen digest binds the fence or the builder; only the population file is pinned (A1/A3)

The counter's only literal pin is `POPULATION_SHA` (`:66`). `FENCE sha256=` is printed (`:184`) and compared to
nothing; `plans/honest50/build_honest_population.py` (frozen in the claims file as `35e3de60…`) is loaded
unchecked. Because the population identity leg verifies `hb.tree_identity(...)` — a function of the same mutable
builder module — a builder "open-window repair" that changes what is built *and* how identity is computed is
invisible to the counter. The fence half is recoverable by a human comparing the receipt's `FENCE sha256=` to the
claims file's open-window table (the recorded counter repair `f9b9873e… → d8787b34…` does match the tip bytes and
is the only table row); the builder half has no such check.

### F5 — MEDIUM. Mutant-row identity fields are unenforced, and the floor is a sensitivity test, not a reasoning test (A3)

The mutant loader uses only `m["id"]` and `m["payload"]` (`:274-280`); `payload_sha256`, `digest` and the battery's
`candidate_fence_sha256` are never checked. Under the frozen schema the mutant floor only requires that each
frozen text diff applies, imports, and changes the `(fid, verdict)` vector of *the fence under test*. Any fence
has at least 12 such one-line sensitivities — proven by the probe (12/12, broken=0). The floor therefore provides
no evidence of pointer resolution, and it cannot: it is measured against whatever fence the author lands, after
the fence exists. Q38's "witnessed" requirement is satisfied trivially by the live run, so it cannot distinguish
a reasoned mutation battery from twelve dead-code flips.

### F6 — LOW (question answered: no coupling). C1 depends on no C2 artifact, and C2 on no C1 artifact (A2)

C1's closure is the counter, the builder, `plans/round44_c1_verify.py`, the population, the battery modules, the
refusal/sealed module dirs and the mutant battery. It reads no self-assessment file (the only occurrence of
`SCORECARD` is a docstring mention at `:4`). C2 corrects `SCORECARD.md` text only, and the round-50 SCORECARD row
(`SCORECARD.md:2133`) names only `plans/round50_c1_verify.py`, which exists — so C2's pointer surface does not
include C1's unlanded S2/S3 artifacts (`plans/mutants50/`, `plans/sealed50/`, `corpus/evidence/round50/c1-receipt.txt`).
Separability therefore holds in module terms, both directions. Out-of-scope observation for the C2 seat: the claims
row and `SCORECARD.md:2134` give the C2 before-total as 271 while the corrections block header says 275.

## The strongest non-author rejection case, and whether committed evidence answers it

> C1 is admitted by an instrument that only counts admissions over corpora the author itself built and can read.
> The honest leg, the refusal leg and the sealed leg are all in-tree before the fence is written; the fence is
> free to key on any of it — the module tag in the build path (demonstrated), an embedded table of the 126
> `tree_sha256` values, or the argv/fid shapes. Any such fence prints the claim's entire after-block. The one
> held-out defence, blind sealed modules, (i) is optional in the counter (F2) and (ii) cannot help, because a
> lookup fence refuses unknown fixtures correctly. The mutant floor is satisfied by twelve one-line flips of the
> lookup itself (F5). So the predicate proves only "a fence exists that admits the pinned 126 and refuses the
> pinned 32" — a lookup table satisfies it — and not "the fence was repaired with boundary reasoning", which is
> the sentence the novelty increment rests on.

Committed evidence does **not** answer it. No leg in `plans/round50_c1_verify.py` observes *why* a fixture is
admitted; no frozen control keys on the harness path or on embedded fixture identities; the round-46 outside-`d`
counter (supplementary, not in this predicate) passes trivially for a fence that reads nothing; and `plans/sealed50/`
does not exist in any commit. The positive evidence is limited to the reproducible over-refusal measurement
(`113/13`), which is the instrument half of the claim and is sound.

## State at review close (uncommitted S2 candidates; assessed from bytes, not scored)

An uncommitted counter candidate (`plans/round50_c1_verify.py`, worktree sha `850ec790…`) changes the harness in
two ways relevant to these findings:

- It builds every module under a **random per-module parent** with decoy siblings (`secrets.token_hex(8)`,
  `PAD = 8`), removing the `/honest/` leg label from `d`. That closes the *specific mechanism* demonstrated in
  F1; it does not touch F1's residual (a fence carrying an embedded table of the 126 pinned identities needs no
  path signal and passes unchanged), and it adds nothing for F2–F5.
- It decides each verdict in a separate `-I` process with the verdict carried in the exit code. This closes a
  different hole — an in-process fence that mutates the counter's own globals — which is outside this item.

F2, F3, F4 and F5 are **unchanged** in that candidate (verified by reading the worktree file): `sealed50` still
guarded by `is_dir()` with `SEALED50_MIN = 6` and no `18` literal (`:307-310`); `if not a.skip_mutants:` still
returns 0 without a MUTANTS line (`:313`); still no fence/builder digest literal; the mutant loader still reads
only `id`/`payload`. A second uncommitted repair candidate (`plans/fixture_fence.py` `57adce4a…`, 533+/117− against
the frozen `05d5fe03…`) is textually a different repair from the scratch candidate reported by seat
`R50C1ExecRepair` (`9baedf13…`); both are unmeasured here and must not be stacked.

## Residual risk and verification gaps

- Fixing F1 requires a **path-neutral, unpredictable build root** (random component names that encode neither leg
  nor module, e.g. `mkdtemp` per fixture) *and* a fifth frozen control (`path_keyed.py`, expected fail) — without
  both, the control would pass today and invalidate the target rather than the fence.
- Fixing F2/F3 requires `SEALED50_MIN`-style enforcement of the `≥18` total with the directory required to exist,
  and a hard fail (not a skip) when a leg is omitted.
- Fixing the residual (embedded-table) risk requires a **held-out honest population** authored blind and
  pre-registered by digest before the fence is written — symmetric to sealed50 on the hostile side. Nothing
  committed today can distinguish a table-keyed fence that performs no outside-`d` read.
- Not measured: the uncommitted S2 candidate (`plans/mutants50` 16-row worktree battery, `plans/sealed50/` worktree
  modules); the live checkout is mid-S2 and its bytes are not evidence.
- Not run: the round-46 outside-`d` counter on the probe fence (unnecessary — the probe opens no path at all), and
  any scored mutation of the lane's own files (forbidden by seat bounds).
- Host git 2.56.0, linux 7.2.11-arch1-1; findings are predicate-design findings and do not depend on git output.

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1RevClaim` was removed after this report was written (probe fence and
mutant generator are transcribed above so the result is reproducible without it).

VERDICT: **REJECT (recommendation) the repair half of R50-C1 under the frozen predicate as currently written.**
A1: reachable without the repair — demonstrated with a 3-line, reasoning-free fence that passes all four legs,
exit 0, on a clean tree. A2: no C1↔C2 artifact dependency either way. A3: the mutant floor is satisfiable by a
fence that resolves nothing — demonstrated 12/12 caught, 0 broken. The instrument half (pinned 126-fixture
over-refusal measurement) is reproducible and stands; the predicate does not bind "repaired" and cannot, until
`≥18` is enforced, the build root is path-neutral with a path-key control, fence/builder digests are pinned in the
counter, `--skip-mutants` fails in scored mode, and a blind held-out honest population exists.
