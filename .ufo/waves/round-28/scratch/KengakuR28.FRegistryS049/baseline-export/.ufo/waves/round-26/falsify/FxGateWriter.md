# FxGateWriter — Q13 identity falsification

Axes: calibration (Q13); novelty/coverage unchanged.

## Finding — HIGH: Q13 checks the report seat label, not a conflicting/missing report author

Target: `plans/gate_timing_check.py` at integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; candidate `corpus/knowledge/grader-perturbation-audit.md` (draft only at this revision; its draft has `writer: KengakuR26-2`). QUALITY Q13 is `corpus/QUALITY.md:97-107`.

In `plans/gate_timing_check.py:310-337`, the checker reads the candidate's writer, derives report identity from the cited path's stem and registry role, and compares those two. It never reads or checks a report `writer:` field. The CLI accepts a different registered reviewer seat even when that report explicitly identifies its writer as `KengakuR26-2`, or has no report writer identity. Thus the assigned author-identity criterion is not fail-closed. (Q13 currently phrases this as report-seat identity; if seat label alone is the intended authority, this is a narrower contract than the assigned report-author test.)

## Scratch reproduction

All fixture commits and executions were isolated to `/tmp/kengaku-r26-FxGateWriter.oYzoUn/repo`; no live lane files or Git/jj state were changed. Clone: `git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r26-FxGateWriter.oYzoUn/repo && git -C /tmp/kengaku-r26-FxGateWriter.oYzoUn/repo checkout --quiet --detach 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` (exit 0).

Fixture candidate has `writer: KengakuR26-2`; `.ufo/waves/round-26/wave-2/swarm-registry.json` registers `FxIdentity` as `reviewer`; the Gate cites `wave-2/FxIdentity.md`; all reports are nonempty, name the intended knowledge path, and have `VERDICT:` except where the writer line alone is varied.

- `python3 plans/gate_timing_check.py --selftest` — exit **0**; `[selftest] ALL PASS`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/identity.md --commit 7281f832ac14c5a9759e979cc494e4e248a2a05e` — exit **0**. Report says `writer: KengakuR26-2`; checker prints `PASS`, `passed=1 failed=0`.
- Same command at `--commit 6879752d658f78f7f5a011e375cc3cd7d5896c0f` — exit **0**. Report has no `writer:` line; checker prints `PASS`, `passed=1 failed=0`.
- Same command at `--commit b4f2f5018c30263f8b822a6a708260f432406680` — exit **0**. Report says `writer: FxIdentity`; checker prints `PASS`, `passed=1 failed=0` (expected distinct-reviewer control).
- Same command at `--commit 65cbe88b101feedfe505bb5140b9b6f137ed6348` — exit **1**. Report seat itself is `KengakuR26-2`; checker correctly reports `seat is the candidate writer 'KengakuR26-2'`.
- Same command at `--commit 9dcff8e235a38a251203373bdd6d3914100adea6` — exit **1**. Candidate lacks `writer:`; checker correctly reports `candidate has no committed writer: field`.
- Timing control: same fixture without its report at `dee6dfe6c757ad772d83f94db0e527df4f3076ec` — exit **1** (`absent from commit tree`, `passed=0 failed=1`).
- `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9` — exit **1**, generic `wave-2 seats` not accepted; `second-seat-reports=0`.

## Residual risk and verification gaps

The checks prove the supplied commit tree and registered seat label, not authorship of report contents. Resolve whether Q13's identity authority is deliberately the registry/path seat or the report's declared writer; under the assigned report-author test, same-author and missing-author cases above are false green. Actual round-26 admission remains untested here: the integration receipt records the candidate as draft-only. LSP is unavailable (`read xd://lsp`: no such mounted tool); no LSP references/definition/diagnostics were claimed. No installs; no build/lint/formatter runs.

VERDICT: The checker fails closed on a same-named report seat and missing candidate writer, but not on a cited report that names the candidate writer—or omits its own writer—when filed under a different registered reviewer seat.
