## Errata (round 44, closure R1; nothing above edited)

Round-44 seat `R44FlipLines` re-read the round-43 Gate row that refused `task.toml`, `setup.py`, `solve.sh`, `feal.h` and
`SHA256SUMS` as one candidate set — verdict "**REJECT — captured, not rows**", flip "an entry sentence that rests on one
of them alone" (`corpus/lessons/round-43.md:41`) — against the round-43 non-author spot-check that disagreed with the
recorded flip verdict (`corpus/lessons/round-43-verifier-spotcheck.md` §5 R1) and the two round-44 `Flip check` lines
appended to that lesson. **The flip fired, twice, before round 43 closed.** This entry rests on `task.toml:22` alone for
the verifier ceiling (`:40-41`, `:122`, `:299-302`) and on `solve.sh:90` alone for the oracle's decisive line (`:230`,
`:251-252`, `:306`). Both files are therefore admitted as **rows of the round-43 package, tier B, outside the frozen
spec**: `plans/pkg-spec-r43.json` is digest-pinned by `plans/round43_c2_verify.py` V2 (`SPEC_SHA256`) and may not gain
rows — exactly how S136/S137 were added ("tier B mechanism rows added by executed flips, not by the spec", `:421-422`).
The rows are **S147** (`task.toml`) and **S148** (`solution/solve.sh`), both `mined`, opened 2026-10-26, recheck `180d`,
used-by this entry; their full 11-cell text is drafted with this errata in
`.ufo/waves/round-44/wave/R44FlipLines/sources-rows.draft.md`, to be inserted in `corpus/SOURCES.md` directly after `S137`
(the registry's last row at this seat's read: 130 rows, maximum id `S137`; round 44's own package takes S138–S146, so
these two are the next free ids and the landing census line is the count of record). Neither row changes a capture, the
manifest, or the spec: both files are already two of the twelve entries in
`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/SHA256SUMS`.

Provenance re-measured this round, not carried: both pinned URLs re-fetched 2026-10-26 20:38 -03, `200`, `cmp` identical
to the captures — `task.toml` 928 bytes, `dcb9f2f15047…e2383eecb`; `solution/solve.sh` 2644 bytes, `6846dd2877aa…4071a9620`.
The tier choice is argued, not assumed: C is unavailable because `corpus/SOURCES.md:15` makes a tier-C row "lead only,
never sole support" and `corpus/QUALITY.md` Q2 (`:25-27`) says "a tier-C row never stands alone", while each of these two
rows stands alone as the support of one claim; A is unavailable because neither file states the graded rule (that is
`test_outputs.py:30`, S129) — they fix the harness the predicate runs inside and the end state one receipt case executes,
the same role S136/S137 play (`:424-425`).

- **E3 — finding 11's "only time bound" sentence, and `:40-41`/`:122`, are re-sourced to S147, not withdrawn.** The
  claims — "the only bound is the verifier timeout of 1800 s (`task.toml:22`)" (`:40-41`), "the only ceiling is
  `task.toml:22`'s 1800 s verifier timeout" (`:122`), "The only ceiling in the captured material is `task.toml:22`'s
  `timeout_sec = 1800.0` for the verifier" and "it is the only time bound the grader's environment actually carries"
  (`:299-302`) — are claims about the graded environment, which is what a tier-B row is for here (`:424-425`). They are
  true of the twelve captures: `test.sh` runs `uvx … pytest …` with no `timeout` wrapper or deadline (`test.sh:17-22`),
  `README.md:35` only asserts that the test "Confirms the attack completes within the time limit", and no other captured
  file carries an enforced process bound — the README's time sentences are prose no harness reads. Scope narrows to
  S147: `:66`'s "read only, never exercised" stands, and `:326-332`'s statement that the 1800 s verifier timeout is
  untested stands — this entry still never runs the image or a timeout.
- **E4 — the `slow-oracle-45s` Mechanism row (`:240`) is re-sourced to S147.** The row's decisive line and quote are
  unchanged (`task.toml:22`, "timeout_sec = 1800.0", 3 words, verified verbatim on that captured line). What changes is
  only that the decisive line now belongs to a registry row instead of to an unregistered capture; the row's reading is
  E3's claim, and the case's verdict (`slow-oracle-45s` `P`) still rests on `:29` being an untimed plain call.
- **E5 — the `oracle-solve-sh` Mechanism row (`:230`), finding 2 (`:251-252`) and finding 12 (`:306`) are re-sourced to
  S148.** "`solve.sh` recovers exactly that round key by the characteristic at `solve.sh:90`" (`:306`) is a reading of the
  oracle's own code in S148's bytes: `:59` enumerates seed candidates, `:90` keeps the candidates whose one-round partial
  decryption reproduces the differential, `:96` returns `(candidates[0]*1234567)&0xFFFFFFFF`. Two limits travel with the
  re-sourced claim, both read statically from the same row and neither observed by this seat. (i) The candidate walk is
  `range(0xFFFF)` (`:59`), i.e. seeds 0–65534, so a draw whose sixth key seed is `65535` is outside the recovered set and
  `:95-96` would index the empty survivor list — a 1-in-65536 blind spot of the shipped oracle, not of the grader.
  (ii) The entry's existing oracle-correctness limit (`:399`) is untouched: two passing draws say nothing about other
  draws or inputs.
- **E6 — the provenance paragraph's `solve.sh` statements (`:72-74`) and `task.toml`'s parenthetical (`:66`) are
  superseded.** Three statements are now false and are corrected here, since the append rule forbids editing them above:
  `:72`'s "**own reading, tier C**" (the row is B — E5's support would violate Q2 as C), `:72-73`'s "not a registry row"
  (it is S148), and `:73-74`'s "no finding rests on its internal logic beyond the fact that the recipe returns a value the
  assert accepts" (findings 2 and 12 and the `oracle-solve-sh` Mechanism row do rest on `:59`/`:90`/`:96` — E5). `:66`'s
  "`task.toml` (captured, not a registry row)" is superseded by S147; its "read only, never exercised" clause stands.
  Unchanged and still correct: `:73`'s "it runs as the `oracle-solve-sh` case's recipe inside the sandbox", the paragraph's
  receipt claim (tier A for its own scope), and the status of `setup.py`, `feal.h` and `SHA256SUMS` — captured, not rows;
  no finding rests on them alone, so their half of the round-43 refusal verdict stands.

Two limits of this correction, named.

- **The round-43 Gate carried no quote for `solve.sh`.** It quoted `task.toml:22` in the refused row but described
  `solve.sh` only as "the oracle end state (an input to the probe)" (`corpus/lessons/round-43.md:41`). S148's anchor quote
  is supplied here from the capture at its cited line — `solve.sh:90`, "if (c1l ^ c2l) == 0x02000000:", 6 words,
  verified verbatim on the captured line and on the re-fetched bytes. That is a thin Gate record, not a wrong one.
- **The corrected verdict is not machine-visible yet.** `plans/gate_flip_check.py` resolves an obligation with the
  *first* matching `Flip check` line after the row (`resolve()` returns on the first hit), so the round-43
  `not fired` line stays the recorded resolution while the checker stays green: `FLIP line=41 flip_line=41
  item=task.toml shapes=flip: resolution=line:46:not fired:round=43`, `FLIPS total=2 unresolved=0`, exit 0 — measured
  with the two round-44 lines appended in place (line 48 of the modified lesson). The same appended line *does* resolve
  the row the moment the stale one is absent: with line 46 deleted, the run prints
  `resolution=line:47:fired:round=44`. The instrument scans every line, not only the `## Gate` section, so placement
  decides readability, not the verdict. The Q35 extension (a `not fired` verdict naming a file is red when the cited
  entry carries a `<file>:<line>` citation of it) is therefore still required; it is a separate wave item, not this
  erratum, and this entry does not claim the instrument was fixed.

`## Located quotes` above is untouched: its 18 quote rows (`plans/pkg_gate.py` P4 `checked=18 bad=0` against a floor of 10)
keep their line numbers, and the two quotes this erratum relies on are located in the S147/S148 anchor cells and here.
This append, plus the two `corpus/SOURCES.md` rows it names, touches no frozen surface: no tool, counter, probe, spec,
gate, dry table, capture, receipt or `claims/` file changes.
