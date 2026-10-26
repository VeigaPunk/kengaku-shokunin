## Errata (round 39)

Appended 2026-10-26 (round 39 wave-2 falsify, seat `F39RevErrata`, scratch clone only — reverted after the run).
This is a deliberate reproduction of the round-39 lesson row "load-bearing fixture bytes edited", not lane content.
Append-only form: the bytes above stand as filed; this section is the correction of record.

Erratum: the `recheck:` line reds as written — `sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS`
resolves bare basenames against the CWD.

Corrected `recheck:` line (replaces :5, one line):

    recheck: 180d — re-fetch the three pinned URLs, `(cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS)`, and re-run `plans/tb2_grader_probe.py`; the recheck: correction is recorded in the round-39 lesson; any digest or receipt change supersedes this entry
