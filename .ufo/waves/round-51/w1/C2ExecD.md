# C2ExecD — attribution of ledger rows 28–36 (R51-C2)

Seat: `C2ExecD` (executor, leaf). Wave: kengaku round 51, hyaku run 11. Milestone: C1 surface truth +
C2 routed-finding attribution.

**Axes named.** `adjacency` (primary — every routed finding names its owner lane and its disposition,
R51-C2). `freshness` (C1) is **not** touched by this seat: no `PROVINCE.md`, manifest or surface counter
file was read for a verdict here, and nothing in my write scope can move it.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

The lane tip I measured is `4090c3d` (`round-51: v2 wave spec (64 seats) + validated dispatch payload`);
the stage-1 freeze `e07f131` is its parent and `297e179` (the base tip named in
`plans/round-51-claims.md`) is its grandparent. Nothing in rows 28–36 or in the files their checks read
changed between `297e179` and `4090c3d`, so the attribution holds at either revision.

## Scope

Rows 28–36 of `corpus/routed-findings.jsonl` (0-based indices 27..35), ids `R42-R3-09` … `R42-R3-17`.
Written as a 9-line JSONL fragment at
`.ufo/waves/round-51/w1/C2ExecD.jsonl` — one complete row object per line, every original field preserved
verbatim, plus `owner` and `disposition` (no row needed `next`: none is `routed`/`referral`).

## Commands run (all read-only against the lane; writes only in scratch)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r51/C2ExecD && export TMPDIR=$_
cd /fast/scratch/hyaku/kengaku-r51/C2ExecD && git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane rev-parse --show-toplevel   # -> /fast/scratch/hyaku/kengaku-r51/C2ExecD/lane
git -C lane rev-parse HEAD              # -> 4090c3db79d11279ab5e5121ba25e74aa316e6e7
# each of the 9 checks, run exactly as the frozen instrument runs them:
bash -lc "<check>"   cwd=/fast/scratch/hyaku/kengaku-r51/C2ExecD/work   LANE=/fast/scratch/.../lane
# the frozen counter, on the shared clone with my 9 rows overlaid (scratch-only edit):
cd lane && python3 plans/round51_routing.py --lane . --run-checks
```

## Summary table

| idx | id | class | status | owner | disposition | check rc |
|---|---|---|---|---|---|---|
| 27 | R42-R3-09 | entry-vacuous-clause | open | `kengaku` | `accepted-risk` | 0 (authored) |
| 28 | R42-R3-10 | lesson-false-measurement | closed | `kengaku` | `fixed-verified` | 0 |
| 29 | R42-R3-11 | lesson-unsupported-carry-claim | closed | `kengaku` | `fixed-verified` | 0 |
| 30 | R42-R3-12 | lesson-unpersisted-number | closed | `kengaku` | `fixed-verified` | 0 |
| 31 | R42-R3-13 | lesson-wrong-pointer | closed | `kengaku` | `fixed-verified` | 0 |
| 32 | R42-R3-14 | lesson-line-ref-off-by-one | refused | `kengaku` | `refused-out-of-scope` | 0 |
| 33 | R42-R3-15 | lesson-unreproducible-command | closed | `kengaku` | `fixed-verified` | 0 |
| 34 | R42-R3-16 | lesson-line-ref-off-by-one | refused | `kengaku` | `refused-out-of-scope` | 0 |
| 35 | R42-R3-17 | lesson-fix-without-receipt | closed | `kengaku` | `fixed-verified` | 0 |

All 9 checks exit **0** in this run, from a scratch cwd, with `LANE` pointing at the clone.

## Owner: `kengaku`, with the evidence used

Every one of the nine sources is this lane's own wave output and every defect is about this lane's own
record of the fibsqrt grader — not about a sibling's surface. The ownership sentence that decides it is
`PROVINCE.md:561-562`:

> Round-42 routing (from the `R42PkgProse` draft, confirmed by the L1). This lane owns what the captured
> grader checks and what passes it — nothing else.

Applied row by row:

- **R42-R3-09** — source `.ufo/waves/round-42/falsify/F42RevC2Package.md:124` (D9). The defect is the
  clause at `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:328` ("this grader writes nothing outside its
  own `./sim` and pytest's cache"). The entry is this lane's knowledge entry for the captured grader, so
  the prose that credits the clause is `kengaku`'s.
- **R42-R3-10 … R42-R3-13, R42-R3-15, R42-R3-17** — the five closed lesson rows and the two refused
  pointer rows all target `corpus/lessons/round-42.md`, this lane's own lesson; the fix in each case is
  an appended erratum in that file.
- **R42-R3-14** — targets `plans/round42_c2_verify.py:327`, this lane's own C2 counter.
- **R42-R3-16** — targets `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile:9-10`, this lane's own
  frozen evidence capture of the grader's image.

No row is `unowned:integrator`: none of the nine asks about a surface outside the captured grader's
checks and this lane's record of them (the unowned parts of round-42 routing — digital-logic correctness
and C-simulator semantics, `PROVINCE.md:562-567` — are not what any of these nine rows assert).

## Dispositions, and why each one

- **`fixed-verified` (6: R42-R3-10, -11, -12, -13, -15, -17).** Each row's `close` names a round-43 errata
  entry (E1–E6) and its `check` re-derives the fix from the file text; all six exit 0 in this run, which
  is exactly the C2 predicate's condition for this value. I re-read the errata block
  (`corpus/lessons/round-42.md:165-203`) and confirmed the checked strings are the *corrections*, not the
  original wrong sentences:
  - E1 "the diff shows only additions, no in-place edits" (`:166-169`) → `only additions` matches.
  - E2 `are **not** "named carried again in the freeze"` (`:171-176`) → literal match.
  - E3 "the route-mix ratios are quoted stdout, not persisted data" (`:177-183`) → literal match.
  - E4 "`:57` pointer corrected — `fibsqrt-probe.txt:6` → `:11`" plus "the `lookup-28` CASE row is
    **line 11**" (`:205-211`) → both literals match.
  - E5 the `-E` form of the census command (`:192-195`) → literal `grep -cE '^ {0,3}\|` matches.
  - E6 "row 3's fix has no failing receipt" (`:196-199`) → literal `E6 — row 3` matches.
- **`refused-out-of-scope` (2: R42-R3-14, R42-R3-16).** Both rows are `status: refused` with a `blocker`
  that says **REFUTED at the tip**, and both refutations hold when re-measured:
  - `sed -n 325,329p plans/round42_c2_verify.py` → `:327` is
    `("V7", lambda: v7(lane)), ("V8", lambda: v8(lane)), ("V9", lambda: v9(lane))]` and `:328` is
    `defects = 0`, so the lesson's `:327` cite is exact and the review's D5 was one line early.
  - `sed -n '1,12p' corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile` → `:8` comment, `:9`
    `COPY tests/sim.c /app`, `:10` `COPY gates.txt /app`, so `Dockerfile:9-10` is exact and the review's
    D7 moved both pins one line late.
  Both are corroborated by `corpus/lessons/round-42.md:198-201` ("Re-checked and **not** defects").
  The finding as filed is not a defect in this lane's surface; the lane declined the change, so the
  refusal value is the honest one. (`fixed-verified` would be a lie — nothing was fixed; the check passing
  proves the *cite*, not a repair.)
- **`accepted-risk` (1: R42-R3-09).** The row is `status: open` and its own note says "recorded, not
  claimed closed"; nothing has landed. I verified the clause is still there:
  `grep -n "pytest's cache" corpus/knowledge/tb2-circuit-fibsqrt-grader.md` → the single line `328:`, and
  `grep -rn "R42-R3-09" corpus/` → one hit, the ledger row itself (`corpus/routed-findings.jsonl:28`), so
  no erratum anywhere in the corpus names it — the round-44 seat's recommendation to "drop the clause in
  an appended erratum" (`.ufo/waves/round-44/wave/R44DistillRouted.md:120`) was never executed. The
  lane knowingly keeps a vacuous clause, so `accepted-risk` records that state truthfully; the check
  below re-derives *why* it is vacuous rather than pretending a fix exists.

## Authored check for the one row that had none (R42-R3-09)

```sh
grep -qF "and pytest's cache" "${LANE:-.}/corpus/knowledge/tb2-circuit-fibsqrt-grader.md" && ! grep -qE '^[[:space:]]*(import pytest|from pytest)' "${LANE:-.}/plans/fibsqrt_probe.py" && ! grep -qF -- '-m pytest' "${LANE:-.}/plans/fibsqrt_probe.py" && ! grep -qF 'pytest.main' "${LANE:-.}/plans/fibsqrt_probe.py"
```

It re-derives the row's claim in both halves: the entry still credits "pytest's cache", and the probe
carries no pytest import, no `-m pytest`, and no `pytest.main` — so no pytest cache can exist in the
sandbox the Regrade section describes. `plans/fibsqrt_probe.py`'s only `pytest` tokens are prose
(`:18-19`, `:44`), which the import/entrypoint patterns correctly ignore. Exit 0, no output.

## Measurement: the frozen counter over my rows

Overlaid the 9 attributed rows into the scratch clone's ledger (no lane write) and ran the frozen
command:

```sh
cd /fast/scratch/hyaku/kengaku-r51/C2ExecD/lane && python3 plans/round51_routing.py --lane . --run-checks
```

Verbatim summary (exit 1 — the 62 rows other seats own are still unattributed; that is their scope):

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=9 incomplete=62
OWNERS attributed=9 unattributed=62
DISPOSITIONS set=9 bad=62
SOURCES resolved=71 missing=0
CHECKS present=62 absent=9
VERIFIED ran=6 passed=6 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```

`grep -E 'R42-R3-(09|1[0-7])\b'` over the full output (including every `DETAIL` line) → **no match**:
not one of my nine rows is reported. `VERIFIED ran=6 passed=6` is exactly my six `fixed-verified` rows.
`CHECKS absent=9` counts other seats' rows (mine contribute 0).

## Two instrument facts the L1 needs (defects, not fixes — I did not edit production)

**1. `load_owners()` never reads `shokunin.conf`.** Its regex is `\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`,
but the file's lanes are a pipe block (`LANES="$LANES` / `kengaku|kengaku-shokunin|novelty + …`), so the
parse matches nothing and the counter silently falls back to its hardcoded `FALLBACK_OWNERS`. Measured
with the instrument's own function:

```
loaded: ['aggregator', 'chousa', 'kagi', 'kaidoku', 'kake', 'kama', 'kasegi', 'kengaku', 'kotoba',
         'kotodama', 'kumitate', 'mori', 'protocol', 'souji', 'tabi', 'tameshi', 'unowned:integrator']
real-but-rejected: ['audio', 'game-dev-2d', 'game-dev-3d', 'lore', 'mado', 'revenger', 'tsukuroi']
parsed-from-conf count: 0
```

Consequence against the claim's own wording ("every `owner` names a fleet lane from `../shokunin.conf`"):
seven real lanes are unreachable as owners (`lore`, `mado`, `revenger`, `tsukuroi` among them), so a
truthful attribution to any of them would be reported as `OWNER … not a fleet lane`. My nine rows are
unaffected (`kengaku` is in the fallback set), but the C2 after-target cannot be called sound until this
is fixed or the claim is reworded.

**2. Checks are executed with `cwd=<scratch>`, so every lane-relative check fails there.** The runner does
`subprocess.run(["bash","-lc",cmd], cwd=str(tmp))` and exports only `LANE`. The eight pre-existing checks
in my nine rows were lane-relative. Negative control, run from the scratch cwd:

```
rc=2 :: grep -qE 'only additions|four added lines' corpus/lessons/round-42.md
rc=1 :: sed -n 327p plans/round42_c2_verify.py | grep -qF '("V9"'
rc=2 :: grep -qF 'E6 — row 3' corpus/lessons/round-42.md
```

A `fixed-verified` row with such a check would land as `CHECK_FAILED` at the landing tip and sink the
predicate. I therefore normalised the eight paths to `${LANE:-.}/<path>` — the same grep/sed, same
assertion, only cwd-independent (it still works when the cwd *is* the lane). This is the one field I
changed beyond `owner`/`disposition`; the diff is one path prefix per file operand and nothing else, and
the fragment's `check` strings are the runnable form. **The same hazard applies to the 61 checks other
seats are attributing** — the L1 should require the `${LANE:-.}` form in every `fixed-verified` row, or
pass `cwd=lane` in the counter.

## Limits

- Point-in-time at `4090c3d`; `fixed-verified` here means "the check exits 0 in this run", not "no later
  edit can regress it".
- The disposition for the two refuted rows is a judgement the frozen enum does not name: there is no
  `refuted` value, so `refused-out-of-scope` carries it and the row's own `blocker` keeps the refutation
  text intact. If the L1 prefers `accepted-risk` for refuted rows, that is a one-token change; nothing
  else in my rows depends on it.
- I did not attribute any row outside 27..35, did not re-attribute rows other seats hold, and did not run
  C1's counter (no `PROVINCE.md` claim is mine).
- Scratch (`/fast/scratch/hyaku/kengaku-r51/C2ExecD`, incl. the `--shared` clone) is removed before
  yield; nothing citable lives there — every measurement above is quoted in this file.

VERDICT: 9/9 rows in 27..35 attributed to `kengaku` (6 `fixed-verified`, 2 `refused-out-of-scope`, 1
`accepted-risk`) with all nine checks exiting 0 from a scratch cwd and the frozen counter reporting zero
details for them (`VERIFIED ran=6 passed=6 failed=0`); fragment written at
`.ufo/waves/round-51/w1/C2ExecD.jsonl`. Two counter defects handed to the L1: `load_owners()` parses
nothing from `shokunin.conf` (7 real lanes unreachable) and `--run-checks` executes with `cwd=<scratch>`,
so lane-relative checks fail and must use `${LANE:-.}`.
