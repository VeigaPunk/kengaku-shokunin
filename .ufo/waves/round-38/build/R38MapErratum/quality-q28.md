## Round38 criterion — a requirement-map label is derived from every violating case

- **Q28 — a requirement-map label is derived from every executed case that violates the requirement, never
  from one witness; every case the row cites must itself violate the row's line.** A map row that names one
  convenient case can be green and wrong at the same time, because a check that reads only the cited cases
  never sees the violating case cited nowhere. The round-37 instance is `corpus/knowledge/tb2-git-webserver-grader.md:107`,
  `| instruction.md:9 | enforced | capitalised, leading-space |`, beside `CASE token-in-body … observed=pass`
  in the same receipt (`corpus/evidence/round37/git-webserver-probe.txt:35`) — a state whose served body is
  not `hello world`, observed passing. Under the map's own definition (`:97-98`, `enforced` = a violating case
  observed `fail`) the row is false, and the frozen counter printed `V7 ok rows=4 bad=0`, `checks=7
  defects=0`, `PREDICATE C2 pass` over it (falsifier receipt
  `.ufo/waves/round-37/falsify/F37CritC2Map/c2-verify-run.txt`; V7 itself re-run by this criterion's seat →
  `(True, 'rows=4 bad=0')`), because `plans/round37_c2_verify.py:192-201` asks only for the
  direction among the **cited** cases. Two wave-2 seats reached it independently
  (`F37CritC2Map` row 9; `F37CritC2Overclaim` F1) and the round-37 closure routed it as D2
  (`corpus/lessons/round-37-verifier-spotcheck.md` §5). The same rule on the same receipt reddens row 8
  (`:106`): its `catch-all-200` witness answers `/hello.html` with `200 hello world`, which satisfies the line
  as written, so it is not a violating case and may not be cited as one (`F37CritC2Map` row 8).
  Check (executable, round-38 instance): `python3 plans/round38_c2_verify.py --lane .` prints
  `V7 ok rows=7 tags=7 bad=0` (one row per `TAG` line of the frozen dry table, seven of them), then
  `checks=7 defects=0`, then `PREDICATE C2 pass`, exit 0. V7's rule
  (`plans/round38_c2_verify.py:239-248`): for each row, the violating set is every receipt case whose
  `violates=` set carries the row's tag; the label must equal `derive` over that set — `enforced` iff all are
  observed `fail`, `unenforced` iff all are observed `pass`, `partly` otherwise (`:205-210`) — and every id the
  row cites in backticks must be a member of that set. Row layout is
  `| \`instruction.md:<L>\` | \`<tag>\` | <label> | <cases> |` with `<L>` the tag's frozen line (`MAP_ROW`,
  `:66`), so a three-cell map copied from the round-37 entry is rejected as an unparsed row rather than
  silently accepted.
  Shown able to fail: the round-37 row 9. Its tag's violating set contains `capitalised` (observed fail) and
  `token-in-body` (observed pass), so the derived label is `partly` and the filed `enforced` trips the
  `label != want` leg (`:243-245`); the round-37 row 8 trips the citation leg (`:246-248`) with
  `catch-all-200`. Neither row is red under the round-37 counter, which is the defect this criterion names —
  the correction of record is the erratum appended at `corpus/knowledge/tb2-git-webserver-grader.md` §Errata
  (round 38), and the new entry's map (`corpus/knowledge/tb2-build-pmars-grader.md`) carries `violates=` tags
  in its receipt so V7 can derive rather than trust.
  Limits: the derived label is only as good as the frozen `violates=` tags — a violating case nobody tagged is
  invisible, and the dry table is the denominator, frozen before the run, so a case added later does not enter;
  "violates" is a human judgement recorded pre-run, so this criterion moves the decision into a reviewable
  artifact, it does not mechanise the semantics; one label per tag collapses a line that carries two clauses
  (row 7's port half and push half), which still needs prose qualification — the erratum carries it; a set with
  one observed verdict derives `enforced` or `unenforced` outright, so a thin tag set passes cheaply; and the
  rule cannot be applied retroactively to a receipt without tags (round-37's has none, `grep -c violates=` →
  `0`), which is why round 37 gets an erratum and not a re-score.
  Lesson: routed item D2, `corpus/lessons/round-37-verifier-spotcheck.md` §5; the two falsifier reports are
  `.ufo/waves/round-37/falsify/F37CritC2Map.md` and `F37CritC2Overclaim.md`. Supersedes: none.
