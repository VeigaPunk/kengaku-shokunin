# ProbeMutate — R67-C1 receipt checker, mutate-run-revert (round 67, wave 1, seat ProbeMutate)

Mutation probe of the frozen counter `plans/round67_c1_pipeline_probe.py` (sha256
`32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836`, `r67-c1/1`), `--check-receipt`
path only, against the receipt of record and twelve single-change mutants of it. No grader run,
no pytest, no port 12355 listener, no `flock` wrap (the checker path opens no socket — `check_receipt`
reads receipt, sibling junit dir, committed case files and grader bytes only). No installs.
Full table and diffs: `ProbeMutate/mutations.md`, `ProbeMutate/results.tsv`, `ProbeMutate/out/`,
`ProbeMutate/diffs/`.

## 1. Baseline (must be green before any mutant counts)

`PYTHONDONTWRITEBYTECODE=1 python3 plans/round67_c1_pipeline_probe.py --check-receipt <base copy>/receipt.txt`
from the lane → **rc 0**, `CHECK ok cases=6`, `PREDICATE R67-C1 pass`. Base copy is byte-identical
to `corpus/evidence/round67/pipe/receipt.txt` (sha `a9b9735b…f1e7`) and to all six
`receipt.junit/*.xml`. The same base was re-run last: rc 0 again. So a mutant rc 1 is a kill, not a
broken fixture.

## 2. Matrix — 9 killed, 3 survived, 0 tracebacks

Twelve one-change mutants (each asserted by the generator to differ from base on exactly one line
or one removed junit file) plus one compound diagnostic; 14 checker runs.

| mutant | observed rc | verdict |
|---|---|---|
| m01 flip `VECTOR q1-ref exists=P`→`F` | 1 (2 defects: frozen mismatch + junit disagreement) | killed |
| m02 delete `VECTOR q3-stub` line | **0** (`CHECK ok cases=6`, `PREDICATE … pass`) | **survived** |
| m03 delete `CASE q4-hooks-noop` line | 1 (`missing CASE/VECTOR for q4-hooks-noop`) | killed |
| m04 `CASE q1-ref case_sha256` → zeros | 1 (`case_sha mismatch for q1-ref`) | killed |
| m05 `CASE q6 junit_sha256` → zeros | 1 (`junit sha mismatch for q6-unscaled-loss`) | killed |
| m06 `PROBE sha256` → zeros | 1 (`PROBE sha does not match committed probe bytes`) | killed |
| m07 `PROBE version=r67-c1/1`→`r67-c1/9` | 1 (`PROBE version does not match the probe`) | killed |
| m08 `GRADER sha256` → zeros | 1 (`GRADER line missing or not the pinned sha`) | killed |
| m09 `VECTOR q5-full-model ws2=F`→`P` (row `PPPP`) | 1 (2 defects) | killed |
| m10 delete `receipt.junit/q3-stub.xml` | 1 (`junit missing for q3-stub`) | killed |
| m11 `CASE q4 rc=1`→`rc=7` (extra) | **0** | **survived** |
| m12 `VECTOR q4 frozen=match`→`mismatch` (extra) | **0** | **survived** |
| X compound: m02 **plus** `q3-stub.xml` replaced by the `q1-ref` junit bytes while `CASE q3-stub` still claims its committed `junit_sha256` | **0** | **survived** |

Tracebacks: 0 of 14 runs. `SETUP`/exit 2: 0. Two independent full runs produced byte-identical
stdout.

## 3. The one finding that matters — the `VECTOR`/`CASE` pairing is one-directional

`check_receipt` builds `seen` from `CASE` lines (`plans/round67_c1_pipeline_probe.py:263-276`) and
validates the frozen vector, the junit sha, junit parseability and the case sha **inside** the
`VECTOR` branch (`:277-295`). Completeness is `missing = [c for c in CASES if c not in seen]`
(`:296`) — CASE-derived. Consequences observed:

- deleting a `VECTOR` line passes (m02), and the passing line still says `cases=6` because that
  count is `len(seen)` = number of `CASE` lines;
- with that line gone, the case's junit sha is no longer checked at all: the compound run passed
  with `receipt.junit/q3-stub.xml` holding the `q1-ref` bytes (`d3ebcfd9…`) while the receipt line
  still asserted `junit_sha256=5e15cf01…`. One deleted line hides a failing case's whole junit.

The frozen predicate sentence says the receipt "carries six `VECTOR` lines whose outcome vectors
equal the frozen table"; the counter accepts five-or-more. The receipt of record carries all six,
so **the C1 predicate over `corpus/evidence/round67/pipe/receipt.txt` is not contradicted** — rc 0,
`PREDICATE R67-C1 pass`. What is weaker than advertised is the counter's discrimination on any
other receipt, i.e. exactly the direction kill rule (b) exists for. Per the seat role this is a
coverage finding: reported, not fixed; no frozen byte was edited.

m11/m12 are the same class in miniature: `rc=` and `frozen=` are parsed and then discarded
(`:269`, `:271`), so `rc=7` on a failing case and `frozen=mismatch` on a matching vector both
print pass. `frozen=` is presentation; `rc=` is unverifiable without re-running, so it is at best
an acknowledged limit and at worst misleading evidence text.

## 4. Restoration evidence

Mutants were reverted by deleting the scratch directories; the checker writes nothing, and no
committed byte was opened for writing. After the matrix: base copy sha `a9b9735b…f1e7` (unchanged);
committed `corpus/evidence/round67/pipe/receipt.txt` sha `a9b9735b…f1e7` and
`plans/round67_c1_pipeline_probe.py` sha `32bacf1d…b836` (both unchanged);
`git -C <lane> status --porcelain -- plans corpus/evidence/round67/pipe` shows only the two
pre-existing `??` entries (the round's receipt and junit dir, mtime 18:54, predating this seat);
no `__pycache__`/`*.pyc` under `plans/`. Scratch `/fast/scratch/hyaku/kengaku-r67/ProbeMutate`
removed after `ProbeMutate/` received `results.tsv`, `manifest.tsv`, both scripts, 14 stdout
captures and 13 diffs.

## 5. Commands (exact, with exit codes)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /fast/scratch/hyaku/kengaku-r67/ProbeMutate/make_mutants.py   # rc 0
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /fast/scratch/hyaku/kengaku-r67/ProbeMutate/run_all.py        # rc 0
PYTHONDONTWRITEBYTECODE=1 python3 plans/round67_c1_pipeline_probe.py --check-receipt <S>/base/receipt.txt   # rc 0
   … same command per mutant: rc 1 for m01,m03,m04,m05,m06,m07,m08,m09,m10; rc 0 for m02,m11,m12
PYTHONDONTWRITEBYTECODE=1 python3 plans/round67_c1_pipeline_probe.py --check-receipt <S>/compound/receipt.txt  # rc 0
sha256sum corpus/evidence/round67/pipe/receipt.txt plans/round67_c1_pipeline_probe.py                    # rc 0, unchanged
```

Tooling: nothing installed; only `/usr/bin/python3` 3.14.8 and the lane's own `python3`. No
network used. No model passed.

**Verdict: 9/12 mutants killed, 3 survived, 0 tracebacks. R67-C1's predicate over the receipt of
record stands (rc 0, `PREDICATE R67-C1 pass`); the counter does not enforce the receipt's six
`VECTOR` lines, and a dropped `VECTOR` line hides that case's junit entirely (demonstrated).**
