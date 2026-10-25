# R33FN3HashContext — N3 `ae95fe0` contextual binding probe (falsify wave)

Seat: `KengakuR33.R33FN3HashContext` (leaf mutation-tester; no subagents).
Date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen claim: C2 N3 (`plans/round-33-claims.md` §C2) — the round-31 fleet report
"carries an appended erratum … naming the real locator-fix commit `ae95fe0`".

## Attack (mutant)

Inject a report that has a *valid* erratum sentence for the phantom hash but keeps
`ae95fe0` confined to an **unrelated footer** — i.e. the real commit is not attached
to the erratum and not even near it.

Fixture (`/tmp` sandbox, file `r31.md`; N3/N4 fleet constants monkeypatched to the
sandbox in-process so the whole counter runs hermetic):

```
# kengaku round-31 fleet report

The locator fix for the verifier-mode precedence docstring landed at commit a44b5a8.

## Erratum (round 33)
The a44b5a8 citation above is a phantom hash — git cat-file -t fails; it is superseded by the real fix.

<~2600 chars of unrelated filler>

---
Footer (ops log, unrelated to this report): the deployment manifest pinned build tooling at ae95fe0.
```

Measured token distances in the mutant fixture:
- `a44b5a8` → `erratum` = **13** chars, → `superseded` = **108** chars (both inside
  the 300-char `near()` window, so the erratum clause is genuine).
- `ae95fe0` → `superseded` = **4016** chars, → `erratum` = **4111** chars
  (i.e. the commit token is nowhere near the erratum).

## Detector output

| scenario | r31 content | `check_n3` | full counter (in-process `--lane` sandbox) |
|---|---|---|---|
| green (baseline) | `ae95fe0` inside the erratum (59 chars from `superseded`) | `''` (pass) | `checks=6 defects=0` exit 0 |
| **mutant** | `ae95fe0` only in unrelated footer (4016 chars away) | `''` (**pass**) | `checks=6 defects=0` exit 0 |
| red (restore) | `ae95fe0` removed entirely | `'the appended erratum does not name the real locator-fix commit ae95fe0'` | `DEFECT N3 round31-report-phantom-hash: … | checks=6 defects=1` exit 1 |

Commands: `python3 plans/round33_defects.py --lane <sandbox>` (hermetic via
in-process `R31_REPORT`/`R32_REPORT` monkeypatch to the sandbox), plus direct
`check_n3(<sandbox>, r31)` calls. The detector is sensitive to *absence* of
`ae95fe0` (red) but blind to *context*: the mutant passes.

## Verdict: **uncaught** (mutant survived)

`check_n3` (`plans/round33_defects.py:100-111`) binds only the phantom hash to the
erratum label:

```python
if not near(text, "a44b5a8", "superseded") and not near(text, "a44b5a8", "erratum"):
    return "no appended erratum supersedes the a44b5a8 citation"
if "ae95fe0" not in text:
    return "the appended erratum does not name the real locator-fix commit ae95fe0"
```

`ae95fe0` is a bare file-wide substring check — no `near()`/word-boundary binding to
the erratum. A report whose erratum names the wrong fix while `ae95fe0` sits in an
unrelated footer passes N3 and the whole counter. This reproduces the build-wave
finding R33CounterAttack E3 (`"ae95fe0" in text`, not near-bound).

## Restoration evidence

- Sandbox fixture sha256 before/after every run identical (green
  `b1c85ead7458f53f…`, mutant `5c2f2eb0454daea3…`, red `3f02f71ef7fe20a4…`);
  `check_n3` and the counter are read-only — no byte changed.
- No lane/fleet file touched; no tools installed (python3 only); this report is the
  only lane-tree write.

## Secondary observations (calibration)

- **Predicate/code width mismatch (claim 400 vs code 300):** frozen claim says
  "within 400 characters"; `near()` defaults to `width=300` (E3b in R33CounterAttack,
  reproduced here: `near()` signature at `round33_defects.py:60`).
- **`near()` never crosses newlines** (`re` without `DOTALL`): the erratum binding
  is same-line-only (E3c).
- **N3/N4 are not hermetic under `--lane`:** they default to absolute fleet paths
  (`R31_REPORT`/`R32_REPORT`), so a bare `--lane` run's N3/N4 result depends on live
  fleet state (B6); the hermetic in-process runs above are unaffected.
