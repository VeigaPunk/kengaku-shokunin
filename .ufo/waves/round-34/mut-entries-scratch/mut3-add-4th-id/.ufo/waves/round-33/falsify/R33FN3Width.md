# R33FN3Width — C2/N3 "within 400 characters" vs `check_n3` width=300

- Seat: `KengakuR33.R33FN3Width`
- Round 33 falsify wave, build wave 36; hyaku run 7.
- Sandbox: `/tmp/r33n3width/` (fresh; all git commands scoped there). **No lane bytes
  mutated**; the lane repo, index, and fleet repos were untouched. Only this file is
  written under the lane.

## 1. Frozen claim (verbatim, `plans/round-33-claims.md:90–92`)

> N3 the fleet report `.ufo/reports/round-31/kengaku.md` carries an appended erratum
> with `a44b5a8` within **400 characters** of `superseded` or `erratum` and naming the real
> locator-fix commit `ae95fe0` (append-only; the original token stays);

## 2. Instrument (`plans/round33_defects.py`)

- `near(text, a, b, width: int = 300, ...)` — default width **300** (line 59-60).
- `check_n3` (lines 100–110) calls `near(text, "a44b5a8", "superseded")` and
  `near(text, "a44b5a8", "erratum")` with **no width argument**, so the 300 default binds.
- `check_n3` also requires only `"ae95fe0" in text` (file-wide), not near the erratum.

## 3. Fixture (hermetic, `/tmp/r33n3width/`)

`fixture.py` builds append-only erratum reports: `a44b5a8` + filler (single physical line,
no newline — `near` regex has no `re.DOTALL`) + `superseded` + sentence naming `ae95fe0`.
Distances measured two ways (end-of-token → start-of-label, and start-to-start); the
frozen 400 rule is satisfied by **both** counts at gap 350 (353/360 with earlier
construction artifact; final exact-distance build gives 350 end-to-start, 357 start-to-start).

Fixture set (end-to-start distance): 250 control, 300, 301, 350 target, 400 frozen-edge.

## 4. Observed results

| distance (end→start) | near(default=300) | near(width=400) | check_n3 verdict |
|---|---|---|---|
| 250 | True | True | PASS |
| 300 | True | True | PASS |
| 301 | False | True | **DEFECT** |
| 350 (target) | False | True | **DEFECT** |
| 400 | False | True | **DEFECT** |

All fixtures carry the token, the label, and `ae95fe0`; all satisfy the frozen 400-char
predicate by both counting conventions.

Full CLI contrast (`main(argv)` loop, real `CHECKS` registry) on a minimal git-tracked
lane (`git init` in `/tmp/r33n3width/empty-lane` only, committed fixtures for
N1/N2/N5/N6):

```
$ python3 round33_defects.py --lane /tmp/r33n3width/empty-lane   # R31_REPORT -> report-350.md (fixture)
DEFECT N3 round31-report-phantom-hash: no appended erratum supersedes the a44b5a8 citation
checks=6 defects=1
# exit=1

$ python3 round33_defects.py --lane /tmp/r33n3width/empty-lane   # R31_REPORT -> report-250.md (control)
checks=6 defects=0
# exit=0
```

The two arms differ only in the R31 report; same lane, same code, same git state.

Selftest is green (`SELFTEST checks=14 failed=0`, exit 0) and cannot see the gap: its
N3-green fixture uses `"`a44b5a8` is a phantom hash, superseded: …"` (~19 chars
between token and label), and no selftest case exercises the 301–400 window.

## 5. Live calibration (current repaired tree)

`.ufo/reports/round-31/kengaku.md` (read-only scan):

- last `a44b5a8` @21063, last `superseded` @21355 → end-to-start distance **284**,
  start-to-start 292.
- `ae95fe0` @21189 present.

So the divergence is currently **latent**: the live tree is green (284 ≤ 300) with a
margin of only **16 characters**; any erratum rewrite/re-append that lands 301–400 chars
apart satisfies the frozen predicate yet reddens N3 (CLI exits 1, prints `checks=6
defects=1`).

## 6. Verdict

- **Caught (confirmed false-negative of the frozen rule):** the frozen N3 predicate says
  "within 400 characters", the instrument enforces 300. A valid erratum 350 chars apart
  is misreported as `no appended erratum supersedes the a44b5a8 citation`. Independently
  reproduced with an exact-distance fixture; consistent with build-wave finds
  (R33ClaimsReview.md:10, R33CounterAttack.md E3b/B3, R33FleetErrata.md F2).
- **Current tree:** latent — live report sits at 284/300 (16-char margin).
- Adjacent (same `near()` function, out of my seat scope, already tracked at
  R33CounterAttack.md E3c/R33FN3Newline): the `.` regex without `re.DOTALL` also bars
  any newline-crossing pair, even below 300.

## 7. Suggested smallest safe correction (report-only; not applied per contract)

Either widen `check_n3`'s `near` calls to `width=400` (alignment with the frozen text),
or amend the frozen claim to "within 300 characters" in a future repair round — a single
line change at `plans/round33_defects.py:103,104` (add `width=400`), plus a selftest
case at 350 to pin the boundary.
