# Round 27 prediction timing and summary resolvability

Axes: calibration hygiene and unambiguous scoring. Scope is Q1–Q8 and the new E0–E8 comparison instrument only; no policy outcomes were calculated or reviewed.

## Findings

- **Medium — Q5 summary precision is unspecified.** `plans/round-27-claims.md:55-56,97` defines the event as a ≥10-point per-file/per-cell shift, while the prescribed `CELLSHIFT <id> max_abs_pp=<v> cell=<file:cell>` format at lines 59-62 gives no precision/rounding rule for `<v>`. The maximum is the right statistic, and the key is explicitly file+cell, but a rounded value at the threshold is not guaranteed to score unambiguously from the stated interface. Specify adequate fixed precision or emit an exact threshold predicate/ratio.
- **Low — “before any instrument output” needs scope.** The 08:35:01 round-start receipt includes prior round-26 `grader_perturb.py` output (`corpus/evidence/round27-calibration/round-start.txt:11-16`), which is part of the stated forecast basis. No evidence shows output from the new round-27 `parser_policy_compare.py` before registration. This is a pass only when “instrument output” means output of the new E0–E8 instrument.

## Timing evidence

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %cI %aI %s' 11a7fc8c64dc` → `11a7fc8c64dc5d634331be24ccf5936f84a11f03`, committer `2026-10-21T08:35:51-03:00`, author `2026-10-21T08:35:50-03:00`; the commit adds `plans/round-27-claims.md` (git show --stat: +153 lines). The prediction rows are at `plans/round-27-claims.md:91-100`; the committed blob and working file compared identical (`cmp` exit 0), with all eight Q rows present.
- At the commit, `git cat-file -e 11a7fc8c64dc:plans/parser_policy_compare.py` failed “path ... does not exist” (exit 128); `git log --all -- plans/parser_policy_compare.py` returned no entries. The 08:35:01 receipt independently records the same absent path at lines 35-37. A later search found no such file under the lane or `/tmp` to depth 5 (find exit 1); earliest visible `/tmp/kengaku-r27-*` birth time was 08:39:50, after the commit. The lane mtime scan also surfaced the daily reflection, but it was already committed in `ec36f37e` at 08:31:40; its proposal contains no measured policy outcome, and its mtime is not used to infer write order. The broad `/tmp` content scan timed out, so deleted/off-tree hand-run outputs cannot be excluded absolutely.

## Q1–Q8 resolvability from prescribed `--summary`

- **Q1: yes.** E1 `agree` and `n=1964` determine whether `n-agree ≥ 1` (`claims.md:50-52,93`).
- **Q2: yes.** E4 `agree < 982` is exactly below 50% of 1964 (`:50-52,94`).
- **Q3: yes.** E2 `n-agree ≤ 19` implements ≤1% (19.64 records, integer count) (`:50-52,95`).
- **Q4: yes.** Compare `n-agree` for E7 and E3 (`:50-52,96`).
- **Q5: not fully, as specified.** Compare maximum `CELLSHIFT` for E1/E2/E3/E6/E7/E8 to 10; the omitted precision rule is the gap above (`:55-56,97`).
- **Q6: yes.** E6 `agree=1964` is equivalent to zero disagreements (`:50-52,98`).
- **Q7: yes.** Compare `pass_rate` for E0/E1/E2/E3/E5/E6/E7/E8; four decimals distinguish the nearest possible gaps around 2 pp for n=1964 (39/1964=1.9857 pp; 40/1964=2.0367 pp) (`:50-52,99`).
- **Q8: yes.** E5 `flip_pf ≥ 1` is printed directly (`:50-52,100`). Its bare-fallback parenthetical follows from E0's bare fallback versus E5's no-fallback semantics (`:37,42-45`), and is not a separate summary field.

The preregistration labels these as code-derived, non-blind forecasts and explicitly takes no calibration credit from their score (`plans/round-27-claims.md:85-89`). Existing grader behavior maps extraction `None` to FAIL (`grader.py:221-225`); it is not a Q1–Q8 summary blocker.

## Residual risk and verification gaps

The timing evidence establishes absence of the named instrument in the commit tree and available workspace search, not universal absence of any manually generated/deleted output. No E0–E8 run or prediction outcome was inspected. No installs.

VERDICT: Q1–Q8 were committed before any evidenced output from the new comparison instrument; Q1–Q4 and Q6–Q8 are unambiguously summary-scoreable, while Q5 needs a stated CELLSHIFT precision rule.