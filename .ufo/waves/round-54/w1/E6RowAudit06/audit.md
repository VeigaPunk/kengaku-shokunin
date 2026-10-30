# Independent R54-C2 row audit

Shared clone HEAD: `62e9bba5e4a0bed376890299aa6a09039db7e68e`.
Every row was run with the counter's `hermetic_env()` and TMPDIR under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit06/`; timeout 600 seconds. All three script paths exist and all argv are entry mode (no forbidden selftest/help/dry/version option).

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| gate-flip-check | 1 | 1 | true | CONFIRMED |
| gate-timing | 0 | 0 | n/a (no declared fragment) | CONFIRMED |
| git-leak-probe | 0 | 0 | n/a (no declared fragment) | CONFIRMED |

## Commands and observed output tails

### gate-flip-check
`python3 plans/gate_flip_check.py --lesson corpus/lessons/round-52.md`
```text
FLIP line=36 flip_line=36 item=S191 shapes=flip: resolution=unresolved:no-line
FLIP line=37 flip_line=37 item=S192 shapes=flip: resolution=unresolved:no-line
FLIP line=38 flip_line=38 item=S193 shapes=flip: resolution=unresolved:no-line
FLIP-DETAIL lesson=corpus/lessons/round-52.md lesson_round=52 refused_rows=3 malformed_resolutions=0
FLIPS total=3 unresolved=3
FLIP-CITE entries=- missing=README.md,LEARNING.md not_fired=0 red=0
exit=1
```
Declared evidence fragment appears verbatim.

### gate-timing
`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit 536925b5320fa64298030b4ee76a58fc4b82723f`
```text
PASS line 77 Gate admit: candidate='knowledge/grader-perturbation-audit.md'
  cited seat-report paths: '.ufo/waves/round-26/falsify/FxEntryAll.md', '.ufo/waves/round-26/falsify/FxEntryNumbers.md', '.ufo/waves/round-26/falsify/FxSourceCheckList.md'
  existing returned second-seat report(s): .ufo/waves/round-26/falsify/FxEntryAll.md, .ufo/waves/round-26/falsify/FxEntryNumbers.md, .ufo/waves/round-26/falsify/FxSourceCheckList.md
gate_timing_check: commit=536925b5320fa64298030b4ee76a58fc4b82723f lesson=corpus/lessons/round-26.md admissions=1 passed=1 failed=0 second-seat-reports=53
exit=0
```
No evidence fragment declared for this row.

### git-leak-probe
`python3 plans/git_leak_probe.py --lane .`
Output tail (last five lines):
```text
CASE clean-echo predicted=pass observed=pass tests=PPPPP predicted_tests=PPPPP match=yes violates= -- reflog expired, gc --prune=now, literal written: the cleanup the instruction asks for
CASE dangling-secret-blob predicted=fail observed=fail tests=PPPFP predicted_tests=PPPFP match=yes violates=secret-gone -- after the cleanup a loose blob holding the secret is written: fsck lists it dangling
CASE dangling-secret-commit predicted=fail observed=fail tests=PPPFP predicted_tests=PPPFP match=yes violates=secret-gone -- after the cleanup an unreferenced commit whose message is the secret
CASE branch-keeps-leak predicted=fail observed=fail tests=PFPPP predicted_tests=PFPPP match=yes violates=secret-gone -- the reset-away secret commit re-
[full tail line clipped in captured tool output]
exit=0
```
No evidence fragment declared for this row. The probe completed with its declared exit; terminal output was clipped by the tool capture for the final line, so the last CASE line is preserved only as captured above.
