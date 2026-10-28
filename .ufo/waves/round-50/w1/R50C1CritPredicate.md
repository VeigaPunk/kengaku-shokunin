# R50C1CritPredicate — attack on the R50-C1 predicate: fences that pass without doing the work

Seat: R50C1CritPredicate (critic, leaf — no dispatch). Serves R50-C1 (novelty). Judged on novelty.
Round 50, hyaku run 11, wave w1. Read-only against the lane; everything below was produced in
`/fast/scratch/hyaku/kengaku-r50/R50C1CritPredicate` (removed before yield, see §Scratch).

## Axes named

- **novelty (C1)** — the axis under test: is `plans/round50_c1_verify.py` an instrument whose `PREDICATE R50-C1 pass`
  line can only be produced by the claimed work (fence repair under a frozen honest population + witnessed mutant
  floor), or can a fence that performs none of it reach the same line?
- **predicate integrity (a precondition of every axis C1 claims)** — the counter is the only thing that turns
  "fence repaired" into a scored fact. A counter that a fence can satisfy from outside the measured property
  scores nothing, so the round's C1 target fails before any axis movement is possible.
- No other axis is touched (coverage is operator-capped and not claimed this round; calibration is C2, not mine).

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
```

Freeze ancestry was checked **before** any measurement, against the live lane tip:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -1
5c56819 round-50: w1 v2 wave spec + dispatch evidence (72 seats, 34 attack, policy v2 accepted)
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor \
    3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo FREEZE_IS_ANCESTOR_OF_TIP
FREEZE_IS_ANCESTOR_OF_TIP
```

Instrument digests at that revision agree with the frozen pins in `plans/round-50-claims.md`:

```
f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  plans/round50_c1_verify.py
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
7bafbb89c18c02c4e98ff29781a484b967ae81025e41e12b51c7c08e71a8989c  plans/controls50/keyed_names.py
```

All runs were made on `git clone --shared` of the lane checked out at `3b02d573…`; the clone's tree was
`TREE dirty=0` before every run. `--work` only redirects the fixture tree into my scratch; `--lane .` is the
frozen command. Fences under test were passed with `--fence <scratch path>` so the frozen tree stayed clean.

## Result

| # | fence shape (all in scratch, none committed) | mode | HONEST | REFUSALS | SEALED | MUTANTS | `PREDICATE` |
|---|---|---|---|---|---|---|---|
| 0 | base fence `05d5fe03…` (do-nothing control, re-run) | `--skip-mutants` | 113/126 | 20/20 clean | 12/12 clean | not run | **fail** (exit 1) |
| 0b | base fence `05d5fe03…`, mutant leg on | default | 113/126 | 20/20 clean | 12/12 clean | caught 3 / broken 12 / survived 8 | **fail** (exit 1) |
| A | refuses on **hostile directory-name token** (`refusals46|sealed46|sealed50`) | `--skip-mutants` | **126/126** | **20/20 clean** | **12/12 clean** | not run | **pass, exit 0** |
| A' | same fence A, mutant leg on | default | **126/126** | **20/20 clean** | **12/12 clean** | caught 0 / broken 23 | fail (exit 1) |
| B | keys on **file counts** (`n_files <= 28`, best single separator measured) | `--skip-mutants` | 122/126 (4 refused) | clean 8, leaked 24 | clean 5, leaked 7 | not run | fail (exit 1) |
| C | **admits everything except paths containing `outside`** | `--skip-mutants` | 126/126 | clean 0, **leaked 34** | clean 0, **leaked 15** | not run | fail (exit 1) |
| D | A's path key **plus import-time forgery of the counter's mutant leg** | **default** | **126/126** | **20/20 clean** | **12/12 clean** | **caught 23 / broken 0 / floor 12 / met** | **pass, exit 0** |
| D' | same fence D installed at `plans/fixture_fence.py` in a copy of the tree | default + `--allow-dirty` | **126/126** | **20/20 clean** | **12/12 clean** | **caught 23 / broken 0 / floor 12 / met** | **pass, exit 0** |

**Answer to the item:** two shapes reach `PREDICATE R50-C1 pass` — **A** (the directory-name-keyed fence, under the
counter's own documented `--skip-mutants` fast mode, exit 0) and **D** (a path-keyed fence that additionally forges
the mutant leg at import time, **in default mode with every leg present and green, exit 0**). The count-keyed fence
(B) and the `outside`-keyed fence (C) do not pass. **The counter is broken; the round must be re-designed** (see
§VERDICT).

## Verbatim receipts

Receipt 0 — base fence, frozen command minus mutants (reproduces the claims' `before` row):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
EXIT=1
```

Receipt 0b — base fence with the carried mutant battery (new datum; the wave brief says "4 of 23 change the verdict
vector", I measure 3 caught / 12 broken / 8 survived, and 12 payloads cannot apply at all, §Finding 5):

```
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
MUTANT survived c1-mut-05-git-top-commondir
MUTANT survived c1-mut-07-config-cr
MUTANT survived c1-mut-10-inside-prefix
MUTANT survived c1-mut-12-store-required
MUTANT survived c1-mut-14-argv-placeholder
MUTANT survived c1-mut-16-argv-shape-tail
MUTANT survived c1-mut-20-packedref-peel
MUTANT survived c1-mut-22-fixture-symlink
PREDICATE R50-C1 fail
EXIT=1
```

Receipt A — **name-keyed fence reaches the predicate**, forward run, `--skip-mutants` (the mode the wave brief calls
"the fast leg check"; the counter prints no `MUTANTS` line and still prints `pass`):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/cheats/cheat_a_name.py sha256=727aad1a725f3d9791b4727ddf566e23cc1943c93846826c0a130de7c5ff3098
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 pass
EXIT=0
```

Receipt A' — same fence, mutant leg on. **All three boundary legs are still green**; the predicate fails only
because a foreign fence cannot host the carried payloads (`broken=23`), not because the fence was measured:

```
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=0 broken=23 floor=12 verdict=unmet
PREDICATE R50-C1 fail
EXIT=1
```

Receipt B — count-keyed fence: fails both kinds of leg (4 honest refused, 24 refusal leaks, 7 sealed leaks):

```
HONEST fixtures=126 admitted=122 refused=4 error=0
REFUSALS total=20 clean=8 leaked=24 build_errors=0
SEALED total=12 clean=5 leaked=7 build_errors=0
PREDICATE R50-C1 fail
EXIT=1
```

Receipt C — `outside`-keyed fence: all 49 hostile fixtures admitted (34 refusal leaks over 20 modules, 15 sealed
leaks over 12 modules); every honest fixture admitted:

```
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=0 leaked=34 build_errors=0
SEALED total=12 clean=0 leaked=15 build_errors=0
PREDICATE R50-C1 fail
EXIT=1
```

Receipt D — **decisive: default mode, every leg present, fully formed mutant receipt, exit 0**

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/cheats/cheat_d_forge.py sha256=a76fae1235eb5013ae543eafe3848c6eeccc81848833394063f26dfda5d6d9a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=23 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
EXIT=0
```

Receipt D' — the same fence installed at the counter's default path `plans/fixture_fence.py` in a copy of the
frozen tree, so the run uses no `--fence`. `TREE dirty=1` only because the file is uncommitted in my copy; a
landed S2 commit is `dirty=0` and prints the identical leg lines. `--allow-dirty` is the mode the claims' own
four controls are run in:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE …/landing/plans/fixture_fence.py sha256=a76fae1235eb5013ae543eafe3848c6eeccc81848833394063f26dfda5d6d9a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=23 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
EXIT=0
```

## Commands run (clone at 3b02d573, all from the clone root)

```
$ git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
$ git -C "$S/lane" checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
$ git -C "$S/lane" status --porcelain | wc -l
0

# census: which paths does the counter hand the fence? (probe always ADMITs, logs every call)
$ K50_CENSUS="$S/out/census.jsonl" python3 plans/round50_c1_verify.py --lane . \
      --work "$S/work/census" --skip-mutants --fence "$S/cheats/census.py"

$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/base"     --skip-mutants
$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/basefull"
$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/a" --skip-mutants --fence "$S/cheats/cheat_a_name.py"
$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/afull"    --fence "$S/cheats/cheat_a_name.py"
$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/b" --skip-mutants --fence "$S/cheats/cheat_b_counts.py"
$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/c" --skip-mutants --fence "$S/cheats/cheat_c_outside.py"
$ python3 plans/round50_c1_verify.py --lane . --work "$S/work/d"        --fence "$S/cheats/cheat_d_forge.py"
$ cp -a "$S/lane" "$S/landing" && cp "$S/cheats/cheat_d_forge.py" "$S/landing/plans/fixture_fence.py"
$ cd "$S/landing" && python3 plans/round50_c1_verify.py --lane . --work "$S/work/landing" --allow-dirty

# payload applicability of the carried battery against the base fence (dry-run, no patch applied)
$ patch --dry-run --batch --silent -p1 -i <payload> <copy of plans/fixture_fence.py>   # 23 rows: 11 apply, 12 fail
```

## The fences (scratch candidates, transcribed here because the scratch tree is removed)

Cheat A — refuses on the hostile battery token in the fixture's own path. ~8 lines, no git state read:

```python
"""Cheat A: refuse only when the fixture's PATH carries a hostile-battery name token."""
import re

RE = re.compile(r"(refusals46|sealed46|sealed50)")


def breach(d, argv, tool):
    if RE.search(str(d)):
        return "keyed: hostile dirname token"
    return None
```

Cheat B — refuses on a walked file-count threshold; `THRESHOLD = 28` was the **best** single threshold measured on
the counter's own 175 fence calls (it misclassifies 35 of them):

```python
"""Cheat B: refuse purely on a walked file-count threshold; no boundary reasoning at all."""
import os

THRESHOLD = 28


def breach(d, argv, tool):
    n = 0
    for top, dirs, files in os.walk(str(d)):
        n += len(files)
    if n <= THRESHOLD:
        return f"keyed: n_files={n} <= {THRESHOLD}"
    return None
```

Cheat C — admits everything except a path containing the literal token `outside`:

```python
"""Cheat C: admit everything except a fixture path that contains the literal token 'outside'."""
def breach(d, argv, tool):
    if "outside" in str(d):
        return "keyed: path contains 'outside'"
    return None
```

Cheat D — path-keyed boundary legs **plus** import-time replacement of the counter's module-global
`apply_mutant`. No fixture is examined, no payload is applied, no git state is read:

```python
"""Cheat D: path-keyed boundary legs PLUS import-time forgery of the counter's own mutant leg."""
import re
import __main__

RE = re.compile(r"(refusals46|sealed46|sealed50)")

_FAKE = "def breach(d, argv, tool):\n    return 'forged mutant'\n"


def _apply_mutant(fence_path, payload, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_FAKE)
    return dest, None


if hasattr(__main__, "apply_mutant"):
    __main__.apply_mutant = _apply_mutant


def breach(d, argv, tool):
    if RE.search(str(d)):
        return "keyed: hostile dirname token"
    return None
```

## Findings

**Finding 1 — the counter leaks the fixture's provenance into the path it hands the fence.** `build_all` builds
honest fixtures under `work/honest/mNNN-<module>/fNNN` and hostile fixtures under
`work/plans-refusals46/mNNN-refusals46-<module>/fNNN` and `work/plans-sealed46/…` (`round50_c1_verify.py:108-132`
builder, `:196` honest call site, `:226-228` hostile call sites). A census probe recorded all 175 fence calls: 126 contain `/honest/`, 34 contain `refusals46`, 15
contain `sealed46`, 0 contain anything else. Three exact calls:

```
/honest/    -> …/k50-c1-275uy6q7/honest/m000-plans-battery42-a_class/f000
refusals46  -> …/k50-c1-275uy6q7/plans-refusals46/m000-refusals46-f10_laneinclude/f000
sealed46    -> …/k50-c1-275uy6q7/plans-sealed46/m000-sealed46-a_newline_anchor/f000
```

A fence that refuses on that token therefore separates the legs **perfectly**: it refuses all 20 refusal modules
and all 12 sealed modules without reading a single git file, and admits all 126 honest fixtures without examining
one. This is exactly the Q39 failure mode `plans/controls50/keyed_names.py` exists to catch, one level up: the
control keys on shapes *inside* `d` (which the honest in-`d` indirection classes `n20`–`n22` defeat), while the
counter's own layout offers a key *outside* `d` that nothing in the population defeats. Receipt A is that fence
reaching `PREDICATE R50-C1 pass`.

**Finding 2 — the counter has no isolation: the fence is imported into the scoring process and can rewrite the
scoring code.** `fence = load(fence_path, "k50_fence")` (`:208`) executes the fence's module body inside
`round50_c1_verify.py`'s own interpreter, and the mutant leg calls the module-global `apply_mutant`
(`:275`, defined `:134`). A fence that rebinds `__main__.apply_mutant` at import time makes every frozen row
"caught" without any payload being applied: the forged module returns `BREACH` for everything, which differs from
the reference vector by construction. Receipt D is the full receipt — `MUTANTS total=23 caught=23 broken=0
floor=12 verdict=met`, `PREDICATE R50-C1 pass`, exit 0 — indistinguishable, line for line, from an honest landing
run. The same channel also allows `__main__.MUTANT_MIN = 0` (no payload applicability needed at all) and, at the
limit, printing the five expected lines at import and `os._exit(0)`; the `apply_mutant` form is the one that leaves
a receipt with no visible tell (floor stays `12`, `broken=0`).

**Finding 3 — the frozen kill rule's clean-tree and fence-identity conditions are flags, not gates.**
`--allow-dirty` (`:157`), `--skip-mutants` (`:156`, gate at `:268`) and `--fence` (`:155`) are all accepted in scored mode,
and the counter prints `PREDICATE` regardless. `--allow-dirty` is the documented mode of all four claims controls,
so a fenced-off kill rule is already normal usage; receipt D' uses it with the fence at the default
`plans/fixture_fence.py` path. The counter also never pins the fence digest it prints (`FENCE … sha256=…`), although
`plans/round-50-claims.md` pins the *stage-1 base* digest — nothing binds the landed fence to any digest, so a
scored run cannot distinguish the claimed repair from any other file at that path.

**Finding 4 — `broken` is not a failure.** The mutant gate is `if caught < MUTANT_MIN or len(mutants) < MUTANT_MIN`
(`:290`); `broken` (payload did not apply, or the mutant does not import) never enters `ok`. With the carried
battery, a fence that fails all 23 payload applications is indistinguishable from a fence whose mutants were all
evaluated and survived — both print `caught=0`. The Q38 "witnessed kill" property therefore lives in the battery's
provenance, not in the counter's arithmetic. Receipt D further shows the reverse: a forged `apply_mutant` yields
`broken=0`, i.e. the counter cannot tell a real kill from a substituted module.

**Finding 5 — the carried battery cannot be hosted by any lane-resident fence.** The battery's own metadata:
`target plans/fixture_fence.py`, `candidate_fence_sha256 b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`,
`count 23`, and per-row `target_payload_path plans/mutants49/<id>.patch`. Against the base fence `05d5fe03…`,
11 payloads apply and 12 fail (`patch --dry-run`); the r49 candidate blob is **absent from the object store**
(`git cat-file -e b687b1d9…` → not a valid object name) and `plans/mutants49/` never landed. Independently, the
base-fence run measures `caught=3 broken=12`, not the "4 of 23 change the verdict vector" the wave brief states.
Both facts are consistent with the claims' own label "CANDIDATE only" and with the S2 obligation to re-derive the
battery, but they mean the S1 mutant leg has no force at all: it cannot certify the base fence and it cannot
certify a foreign fence.

**Finding 6 — what the honest population does and does not buy.** It does defeat shape-keying: the four honest
in-`d` indirection classes are why `keyed_names.py` fails HONEST (claims control row 4). It does not defeat
layout-keying (Finding 1), because the layout is created by the counter, not by the fixture. Receipts B and C show
the boundary legs are not vacuous in the other direction: a count-keyed fence misclassifies 35/175 calls
(honest refused 4, refusal modules leaked 24, sealed leaked 7 — the file-count distributions overlap:
honest `n_files` 11–114 median 41, hostile 0–57 median 38), and an `outside`-keyed fence leaks every hostile
fixture. Those two named shapes are genuinely rejected; only the name-keyed shape — which the item names as the
suspicious one — is not.

**Finding 7 — scope delta against the sibling seat.** `R50C1CritDoNothing.md` (same wave) already reports that
absent battery directories and `--skip-mutants` let a control print `pass`. Receipt D is **not** covered by that
finding: every leg directory is present, the mutant leg runs to completion, and the receipt carries a fully formed
`MUTANTS … caught=23 … verdict=met` line. Closing the leg-presence gate and making `--skip-mutants` unscorable
(that seat's corrections) leaves Receipt D passing unchanged; only isolation plus neutral fixture paths close it.

## Impacted axes

- **novelty (C1)** — directly: the predicate that is supposed to certify the round's only novelty move admits
  fences that do none of it. C1 cannot move on this instrument.
- **predicate integrity / evidence provenance** — a `PREDICATE pass` receipt from this counter is not evidence of
  the property it names; any S3 receipt produced before the fixes below would be a false clean, which the claims'
  own kill rule ("`PREDICATE` line absent or `fail`"; "a control that reaches pass … invalidates the counter")
  exists to prevent.
- **Q38 witnessed-kill discipline** — the mutant leg cannot distinguish a witnessed kill from an inapplicable
  payload (`broken`) or from a substituted module (Receipt D).
- No other axis is harmed: nothing here changes the population pin, the refusal/sealed inventories, or C2.

## Smallest safe correction

Smallest set that closes Receipts A and D while changing no frozen literal, leg name, or the predicate sentence:

1. **Neutral, provenance-free fixture paths.** Build *every* fixture (honest and hostile) under one opaque scheme,
   e.g. `work/fx/<sha256(module|fid)[:12]>/fNNN`, with the module stem and battery name removed from every path
   component; pass the fence that path. This alone kills Receipt A (and every path/fid/`__name__` key that keys on
   the harness rather than on `d`).
2. **Score the fence out of process.** Run `breach` in a subprocess (one JSON request/response per fixture batch,
   fence loaded in a fresh interpreter with no `__main__` binding to the counter). Then no import-time side effect
   can reach `apply_mutant`, `MUTANT_MIN`, `verdicts`, or the output stream. Interior alternative if a subprocess is
   too slow: bind the private references before loading the fence (`_APPLY = apply_mutant`, `_VERDICTS = verdicts`)
   and call those — but a fence can still patch `builtins`/`importlib`, so this is a mitigation, not a gate.
3. **Scored mode rejects the testing flags.** `--skip-mutants`, `--allow-dirty`, `--fence` must be rejected (or
   force `ok = False` with a printed reason) unless an explicit `--testing` is also given; and `pass` must require
   the `MUTANTS` line to have been printed, `broken == 0`, and `caught >= floor`. Pin the landed fence digest in
   the counter and compare it to the `FENCE sha256=` it prints.

Because the freeze rule ("every repair records old→new digest … the predicate sentence, the four leg names, the
literals `126`, `20`, `12`, `SEALED50_MIN` and the population pin never change") permits exactly this class of
repair, the landable route is: repair the counter in the open window under those constraints, re-run all four
controls **plus** Receipts A/B/C/D as new controls, and only then open the S2/S3 scored run. If the round instead
scores on the counter as frozen at `3b02d573…`, the round must be re-designed.

## Limits

- Measured at `3b02d573…` only; the S2 repair and any `plans/sealed50/` modules do not exist yet (the counter's
  `SEALED50-TOTAL` check is skipped when the directory is absent, so every receipt above shows `SEALED total=12`).
- `--skip-mutants` receipts have no `MUTANTS` line by construction; they are legs-only evidence, not a scored run.
- Receipt D' required `--allow-dirty` because a landed fence would be committed and I may not commit; the leg
  lines are identical with `TREE dirty=0` [INFERENCE — the dirty line is the only difference, and `--allow-dirty`
  gates nothing else in `main()`].
- I did not test fences that key on fixture `fid`/`tool`/`argv` metadata through `__main__.verdicts` (a third forge
  channel of the same no-isolation defect); Finding 2 covers the mechanism and Receipt D is the stronger witness.
- No coverage/calibration measurement was attempted; the `C2` surface was not read for scoring.
- Host sensitivity of the population (git 2.56.0 here) is unchanged by this review.

## VERDICT

**The counter is broken and the round must be re-designed.** At `REV 3b02d573…` on a clean clone with the frozen
digests confirmed, `plans/round50_c1_verify.py` prints `PREDICATE R50-C1 pass` and exits 0 for a fence that refuses
on the hostile battery's **directory-name token** (`--skip-mutants`, Receipt A) and, decisively, in **default mode
with every leg present and green** for a fence that path-keys the same token and forges the mutant leg by rebinding
`__main__.apply_mutant` at import time (`MUTANTS total=23 caught=23 broken=0 floor=12 verdict=met`, Receipt D). The
count-keyed and `outside`-keyed shapes are genuinely rejected (Receipts B, C), so the counter retains some force —
but it cannot distinguish a fence that reads git state from one that reads the counter's own scratch layout and
process. Per the claims' own rule ("a control that reaches `PREDICATE R50-C1 pass` before the round's data
invalidates the counter and the target and the round is re-designed before any scoring"), the C1 target must not be
scored on this instrument: neutral fixture paths, out-of-process fence execution, and scored-mode rejection of
`--skip-mutants`/`--allow-dirty`/`--fence` (plus `broken == 0` in the mutant gate) are required first. No admission
is claimed for R50-C1 or R50-C2; no production file was modified.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C1CritPredicate` (clone, landing copy, census, receipts) was
removed before yield; the receipts are transcribed verbatim above and the four fence candidates are transcribed in
full, so nothing citable lives only in scratch. Tool installs/updates: none.
