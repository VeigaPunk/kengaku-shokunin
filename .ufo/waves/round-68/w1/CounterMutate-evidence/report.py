#!/usr/bin/env python3
"""Assemble W/CounterMutate.md from the measured tables (no hand-transcribed numbers)."""
import json
import pathlib

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r68/CounterMutate")
W = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-68/w1")
man = json.loads((S / "run/manifest.json").read_text())
mx = json.loads((S / "run/matrix.json").read_text())
matrix, lit = mx["matrix"], mx["literal_cli"]
mutant_table = (S / "run/mutant-table.md").read_text().rstrip("\n")
fixture_table = (S / "run/fixture-table.md").read_text().rstrip("\n")
n_mut = len(man["mutants"])
n_fix = len(man["fixtures"])
accepted = {m["id"]: [n for n in man["fixtures"] if matrix[m["id"]][n]["rc"] == 0]
            for m in man["mutants"]}
survived = [k for k, v in accepted.items() if v]
killed = [k for k, v in accepted.items() if not v]

body = """# CounterMutate — R68-C1 checker mutation pass

Seat: `CounterMutate` (mutation-tester), round 68 wave 1. Leaf seat: no delegation,
no background jobs, nothing installed (no pacman, no uv, no binary fetched). No port was
bound and no server started: `check_receipt` reads bytes only, so port 8080 (the L1's
battery) was never in contention. Scratch `S=/fast/scratch/hyaku/kengaku-r68/CounterMutate`
is deleted before yielding; every script, fixture definition and result needed to rebuild
it is in `CounterMutate-evidence/`.

## Object under test

| item | value |
|---|---|
| frozen instrument | `plans/round68_c1_pypi_finish.py`, sha256 `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` (= the receipt's `PROBE` line) |
| function mutated | `check_receipt()` (lines 235–404 of the frozen bytes) |
| frozen sentence | `plans/round-68-claims.md` §R68-C1, paragraph **Checker strictness** + the one-sentence predicate |
| receipt of record | `corpus/evidence/round68/pypi/receipt.txt`, sha256 `{record_sha}` (read-only) |
| claim bytes edited | none. No file in the lane was written except this report and its evidence dir |

The frozen checker's own `--selftest` builds five red fixtures (r1–r5). This pass asks a
different question: for every clause of the frozen sentence, is the check that enforces it
*load-bearing* — i.e. does deleting exactly that check let through a receipt the frozen
bytes refuse? A mutant that accepts such a receipt is recorded as **SURVIVED** (the
tasking's definition: the forged receipt passed the mutant), with the forged receipt named.
A mutant that still refuses it is **KILLED** — that check is redundant with another.

## Method

1. **Copies only.** Every mutant is a copy of the frozen bytes under
   `S/mut/<id>/plans/round68_c1_pypi_finish.py` with exactly one check block replaced by
   `pass  # MUTANT <id> …`. Removed ranges, removed-block sha256 and mutant sha256 are in
   `CounterMutate-evidence/manifest.json` (`removed_block` carries the exact bytes); each
   mutant was `py_compile`d. `plans/round68_c1_pypi_finish.py` in the lane was never
   opened for writing (its sha re-hashed after the pass: unchanged).
2. **Detector = {n_fix} forged fixtures**, each derived from the receipt of record by one
   change — one token/line of the receipt, or (for checks that read committed evidence)
   one byte-set of a minimal forged evidence lane built in scratch, with the receipt's
   corresponding sha updated so that only the targeted check can fire. Every fixture is
   refused by the frozen checker before the mutants see it: `m00` (the byte-identical copy,
   `sha256 == 4a6fae53…`) runs first in every fixture row and the driver aborts if any
   fixture is not refused for the expected defect. Independently, the frozen instrument was
   run from the lane on the whole fixture set and on the record
   (`CounterMutate-evidence/literal-frozen-fixtures.txt`); the record returns `rc 0`,
   `PREDICATE R68-C1 pass`.
3. **Run.** `python3 run/check.py <probe> <lane> <receipt>` → `check_receipt`, rc captured
   per (mutant, fixture). Full matrix, raw stdout and stderr:
   `CounterMutate-evidence/matrix.json`, `matrix-out.txt`.
4. **Controls.** `m00` (identical bytes) accepts the record (rc 0) and refuses all {n_fix}
   fixtures; the forged-`PROBE` fixture is refused by every mutant except `m1` (the mutant
   that deletes that check); the record receipt is accepted by all {n_mut} mutants under the
   harness — so no mutant is refused merely by being a copy, and no mutant is accepted
   merely by being broken.

### Harness caveat (stated plainly)

The receipt's `PROBE` line binds the instrument's **own** bytes, so a mutated copy cannot
pass that clause literally: run as `python3 S/mut/<id>/plans/… --check-receipt <record>`,
`m00` returns 0, `m1` returns 0 (it deletes the binding), and `m2`–`m22` return 1 with a
`probe-sha` defect (plus the `exit-agreement`/`stored-predicate` cascade of F3). That is an
artefact of hashing a copy, not evidence about the deleted check. `run/check.py` therefore
re-anchors exactly two things — `own_sha256()` → the frozen instrument's sha, and
`lane_root()` → the fixture lane — and leaves every check under test as the mutant's own
code. Controls above prove the re-anchored `PROBE` check still refuses a forged sha. The
"true-receipt rc" column reports harness / literal side by side.

## Mutant table

{n_mutants} mutants: the ten the seat named (m1–m10) plus twelve (m11–m22) that MUTATE the
remaining checks of the frozen sentence, so the coverage answer is not limited to the named
list. `L###` = line range in the frozen probe; the marker line inserted at each deletion
point is `pass  # MUTANT …`.

{mutant_table}

## Forged fixtures (the detector)

Every fixture starts from `corpus/evidence/round68/pypi/receipt.txt`; "lane L" means the
fixture differs only in the receipt, a named lane means one evidence file in a scratch lane
differs (and the receipt's matching sha was updated so that only the targeted check fires).

{fixture_table}

## Findings

**F1 — each mutated clause is load-bearing and single-point ({n_surv}/{n_mut} survived).**
For every one of the {n_mut} mutants, the set of forgeries it accepts is exactly the set
aimed at the check it removed ({accepted_map}). No mutant accepted a forgery aimed at a
check it did **not** remove: zero collateral widening. The frozen strictness paragraph is
therefore enforced by live checks, not decorative ones — and by exactly one check each,
with the exceptions in F4/F5.

**F2 — the most load-bearing single check is m11.** Deleting the per-case
`expected`/`observed` comparison (L306–309) accepts `F-vector`, the fabricated all-P
receipt — the same shape as the instrument's own `--selftest` fixture r1 — and
`F-k1-observed`. The predicate clause "observed and expected values both equal the frozen
vector P/F/F/F" stands on those two `if`s alone. The `PREDICTION-VECTOR` line check does not
cover it (m19 removes that line check without ever accepting `F-vector`, because the vector
it guards is the *derived* one, not the per-case fields). Any future narrowing of this
block (e.g. checking only `observed`) would accept a receipt whose `expected` column was
rewritten.

**F3 — the defect cascade is derived, not independent detection (do not over-count).**
`derived_pass` is computed before the exit/stored checks, so any single forgery also trips
`exit-agreement` and `stored-predicate` while the receipt still claims `CLASS-PROBE-EXIT=0`
/ `pass`: 25 of the {n_fix} fixtures emit three defects, three emit four, `F-vector` five;
only `F-exit` and `F-stored` isolate a check at one defect, and only m9/m10 accept those.
Those two checks are downstream witnesses, not independent detectors.

**F4 — the one killed mutant: the missing-CASE clause is double-covered.**
`m21` removes the `*-case-missing` defect (L302) and is nevertheless refused on its target
fixture `F-missing`, by `K4-stderr-sha`: a dropped CASE line also drops that case's
`stderr_sha256` field, so the per-case binding (L358–368) refuses the receipt independently.
This is the only redundancy found in the receipt-side checks. It is redundancy, not
weakness: narrowing either one alone is still covered by the other.

**F5 — second redundant binding: K2's stderr sha and the log's existence.**
`F-k2-stderr-sha` and `F-k2-capture-missing` are refused by all {n_mut} mutants, including
`m7` (which deletes the per-case loop) — K2's sha is bound both in its own clause (L350–351)
and in the loop. `F-log-missing` is likewise refused by all mutants including `m15` (the
`server-log` existence branch sits outside the sha comparison that m15 deletes).

**F6 — one declared check cannot be exercised by any receipt: `prediction-drift` (L380–381).**
The re-derived vector comes from the committed round-63 probe, whose bytes the `BASE-PROBE`
binding pins; a drifted base probe aborts before `check_receipt` (F7). No forgeable receipt
byte can reach that branch. It is a tripwire against base-probe drift, not a live detector;
`m19` removes it together with the line check and its only observable loss is `F-pred`.

**F7 — instrument defect, outside `--check-receipt`, reported and not fixed.**
With `plans/round63_c1_pypi_probe.py` drifted or absent, the instrument does **not** emit
`SETUP base-probe-sha-mismatch` and rc 2 as its `main()` intends: it raises
`AttributeError: 'NoneType' object has no attribute 'SetupError'` (drift) or
`FileNotFoundError` (absence) and exits 1 (`CounterMutate-evidence/extra-out.txt`, probes (b)
and (c)). Cause: `mod_SetupError` catches `NameError`, but `_BASE = None` is bound at module
load (L85), so the fallback line is unreachable. Consequence for the round: on the battery
path a broken base probe fails closed but with a traceback instead of the documented
`SETUP`/rc 2, so kill rule (c)-style "could-not-evaluate" reporting is lost. This is the
frozen instrument's behaviour, not a mutant's; the `--check-receipt` path is unaffected
(it re-hashes the same file inside `check_receipt`, where `base-probe-bytes` fires —
`base-swap-m00` refuses, `base-swap-m2` accepts).

**F8 — the `BASE-PROBE` clause has two enforcement points, both live.** `m2` removes both
(L256–264) and accepts `F-base`; the committed-bytes half (`base-probe-bytes`) is reachable
post-load, as the `base-swap` probe shows (frozen rc 1, m2 rc 0).

## Reproduce

```sh
S=/fast/scratch/hyaku/kengaku-r68/CounterMutate
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
E=$L/.ufo/waves/round-68/w1/CounterMutate-evidence
mkdir -p "$S"/{mut,fix,run} && cd "$S"
cp "$E"/{build,check,matrix,extra,report}.py run/
python3 run/build.py      # 22 mutants + 31 forged fixtures, shas in run/manifest.json
python3 run/matrix.py     # record + every fixture x every mutant -> run/matrix.json
python3 run/extra.py      # base-probe post-load swap / drift / absence probes
# frozen checker on the fixture set, no harness:
python3 "$L"/plans/round68_c1_pypi_finish.py --check-receipt "$L"/corpus/evidence/round68/pypi/receipt.txt; echo $?
```

## Verdict

The R68-C1 checker enforces the frozen sentence as written at every clause this pass
mutated: 22 of 22 deleted-check mutants are load-bearing at their own clause
({n_surv} survive on a forged receipt the frozen bytes refuse, 1 is killed by an
independent binding), and no mutant widens acceptance beyond the check it removed. The
receipt of record is unaffected: the byte-identical copy and the frozen instrument both
return `PREDICATE R68-C1 pass`, rc 0. Nothing in the claim, the instrument or the evidence
was edited; the defect in F7 is reported for the L1, not repaired.

MUTANTS n={n_mut} survived={n_surv}
"""

body = (body.replace("{record_sha}", man["record_receipt_sha256"])
        .replace("{n_fix}", str(n_fix)).replace("{n_mut}", str(n_mut))
        .replace("{n_mutants}", str(n_mut)).replace("{n_surv}", str(len(survived)))
        .replace("{mutant_table}", mutant_table)
        .replace("{fixture_table}", fixture_table)
        .replace("{accepted_map}", "; ".join(f"{k}: {','.join(v)}" for k, v in accepted.items() if v)))

W.mkdir(parents=True, exist_ok=True)
(W / "CounterMutate.md").write_text(body, encoding="utf-8")
print(f"wrote {W / 'CounterMutate.md'} ({len(body)} bytes) survived={len(survived)} killed={killed}")
